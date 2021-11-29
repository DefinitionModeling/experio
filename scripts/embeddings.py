"""Generate all embeddings using decluter."""

from pathlib import Path

import numpy as np
import pandas as pd
import torch
from beartype import beartype
from rich.console import Console
from tqdm import tqdm
from transformers import AutoModel, AutoTokenizer

from experio.dataset import EtymDefDataset

base_path = Path.cwd() / 'data'
word_path = base_path / 'words_embed.np'
def_path = base_path / 'def_embed.np'
if not word_path.parent.exists():
    word_path.parent.mkdir(parents=True)

console = Console()

tokenizer = AutoTokenizer.from_pretrained('johngiorgi/declutr-small')
model = AutoModel.from_pretrained('johngiorgi/declutr-small')


@beartype
def generate_embeddings(text: list[str], min_val: int = 1e-9) -> np.ndarray:
    """Generate all embeddings using decluter.

    Args:
        text (list[str]): List of sentences to embed.
        min_val (int): Minimum value to use for normalization.

    Returns:
        np.ndarray: Array of embeddings.
    """
    inputs = tokenizer(
        text,
        padding=True,
        truncation=True,
        return_tensors='pt',
    )

    # embed the text
    with torch.no_grad():
        sequence_output = model(**inputs)[0]

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


def batch_embeddings(df: pd.Series, batch_size=256) -> np.ndarray:
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
        embeddings.append(generate_embeddings(list(batch.values)))
    return np.concatenate(embeddings)


if __name__ == '__main__':
    # prepare text
    df = EtymDefDataset().dataset()
    df['word_etym'] = df['word'] + ' ' + df['etym']

    # generate embeddings in batches
    console.log('Generating word/etym embeddings...')
    word_embeddings = batch_embeddings(df['word_etym'])
    np.save(word_path, word_embeddings)

    console.log('Generating def embeddings...')
    def_embeddings = batch_embeddings(df['def'])
    np.save(def_path, def_embeddings)
