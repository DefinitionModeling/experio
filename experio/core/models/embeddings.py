"""Generate embeddings from input text with universal encoder decluter."""

from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd
import torch
from beartype import beartype
from tqdm import tqdm
from transformers import AutoModel, AutoTokenizer

from experio import const
from experio.console import console
from experio.core.dataset.experio import EtymDefDataset


class Embeddings(object):
    """Generate embeddings from input text with universal encoder decluter."""

    def __init__(self, base_path: Optional[str] = const.BASE_PATH):
        """Initialize the dataset.

        Args:
            base_path (Optional[str]): Base path of the dataset. Defaults to
                const.BASE_PATH.
        """
        self.word_path = '{0}/words_embed.npy'.format(base_path)
        self.def_path = '{0}/def_embed.npy'.format(base_path)
        self.word_embeddings = None
        self.def_embeddings = None

        # make paths if they don't exist
        Path(base_path).mkdir(parents=True, exist_ok=True)
        self.load_models()

        # create embeddings
        if not Path(self.word_path).is_file():
            console.log('Embeddings not found.')
            self.dataset_embeddings()

        self.load_embeddings()

    def dataset_embeddings(self):
        """Generate embeddings from the dataset."""
        df = EtymDefDataset().dataset()
        df['word_etym'] = df['word'] + ' ' + df['etym']
        if not Path(self.word_path).is_file():
            console.log('Generating word/etym embeddings...')
            self.word_embeddings = self.batch_embeddings(df['word_etym'])
            np.save(self.word_path, self.word_embeddings)

        if not Path(self.def_path).is_file():
            console.log('Generating def embeddings...')
            self.def_embeddings = self.batch_embeddings(df['def'])
            np.save(self.def_path, self.def_embeddings)

    def load_models(self) -> None:
        """Load the models."""
        model = 'johngiorgi/declutr-small'
        self.tokenizer = AutoTokenizer.from_pretrained(model)
        self.model = AutoModel.from_pretrained(model)

    @beartype
    def generate_embeddings(
        self,
        text: list[str],
        min_val: int = 1e-9,
    ) -> np.ndarray:
        """Generate all embeddings using decluter.

        Args:
            text (list[str]): List of sentences to embed.
            min_val (int): Minimum value to use for normalization.

        Returns:
            np.ndarray: Array of embeddings.
        """
        inputs = self.tokenizer(
            text,
            padding=True,
            truncation=True,
            return_tensors='pt',
        )

        # embed the text
        with torch.no_grad():
            sequence_output = self.model(**inputs)[0]

        # mean pool the token-level embeddings to get sentence-level embeddings
        embeddings = torch.sum(
            sequence_output * inputs['attention_mask'].unsqueeze(-1),
            dim=1,
        )
        embeddings = embeddings / torch.clamp(
            torch.sum(inputs['attention_mask'], dim=1, keepdims=True),
            min=min_val,
        )

        return embeddings.cpu().numpy()

    def load_embeddings(self) -> None:
        """Load the embeddings."""
        self.word_embeddings = np.load(self.word_path)
        self.def_embeddings = np.load(self.def_path)

    @beartype
    def batch_embeddings(
        self,
        df: pd.Series,
        batch_size=256,
    ) -> np.ndarray:
        """Generate embeddings in batches.

        Args:
            df (pd.Series): Series of sentences to embed.
            batch_size (int): Batch size.

        Returns:
            np.ndarray: Array of embeddings.
        """
        embeddings = []

        for it in tqdm(range(0, len(df), batch_size)):
            if it + batch_size > len(df):
                batch = df.iloc[it:]
            else:
                batch = df.iloc[it:it + batch_size]
            embeddings.append(self.generate_embeddings(list(batch.values)))

        return np.concatenate(embeddings)
