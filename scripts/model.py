"""Model for predicting definition embedding given word embedding."""

import math
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from beartype import beartype
from scipy.spatial.distance import cosine
from tqdm import tqdm

from experio.console import console
from experio.dataset import EtymDefDataset
from experio.models import Embeddings

DROP_PERCENT = 0.9
SPLIT_PERCENT = 0.8
LEARNING_RATE = 0.001
RANDOM_SEED = 5
HIDDEN_LAYERS = 3
epochs = 3
base_path = Path.cwd() / 'model'
if not base_path.exists():
    base_path.mkdir(parents=True)
file_path = base_path / 'model.pt'


def train_test_split(
    df: pd.DataFrame,
    embeddings: Embeddings,
    split_percent: float = SPLIT_PERCENT,
    random_seed: int = RANDOM_SEED,
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
    """Split dataset into train and test.

    Args:
        df (pd.DataFrame): Dataframe to split.
        embeddings (Embeddings): Embeddings to use.
        split_percent (float): Percentage of data to use for training.
        random_seed (int): Random seed for sampling.

    Returns:
        tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
            Tuple of train, train_labels, test, test_labels.
    """
    words = set(df['word'])
    split = int(len(words) * split_percent)

    # randomly choose words for training
    train_words = set(df['word'].sample(
        n=split,
        random_state=random_seed,
    ))
    test_words = words - train_words
    train_idxs = df[df['word'].isin(train_words)].index
    test_idxs = df[df['word'].isin(test_words)].index

    # get embeddings
    train_x = embeddings.word_embeddings[train_idxs]
    train_y = embeddings.def_embeddings[train_idxs]
    test_x = embeddings.word_embeddings[test_idxs]
    test_y = embeddings.def_embeddings[test_idxs]

    return (
        torch.tensor(train_x),
        torch.tensor(train_y),
        torch.tensor(test_x),
        torch.tensor(test_y),
    )


def build_model(
    train_x: torch.Tensor,
    train_y: torch.Tensor,
) -> torch.nn.Module:
    """Build model.

    Args:
        train_x (torch.Tensor): Training data.
        train_y (torch.Tensor): Training labels.

    Returns:
        torch.nn.Module: Model.
    """
    input_neurons = train_x.shape[1]
    output_neurons = train_y.shape[1]

    hidden_neurons = int(
        math.sqrt(input_neurons * output_neurons) / HIDDEN_LAYERS,
    )

    console.log('input_neurons: {0}'.format(input_neurons))
    console.log('output_neurons: {0}'.format(output_neurons))
    console.log('hidden layers: {0}'.format(HIDDEN_LAYERS))
    console.log('hidden_neurons per layer: {0}'.format(hidden_neurons))

    return torch.nn.Sequential(
        torch.nn.Linear(
            input_neurons,
            hidden_neurons,
        ),
        torch.nn.ReLU(),
        torch.nn.Linear(
            hidden_neurons,
            hidden_neurons,
        ),
        torch.nn.ReLU(),
        torch.nn.Linear(
            hidden_neurons,
            hidden_neurons,
        ),
        torch.nn.ReLU(),
        torch.nn.Linear(
            hidden_neurons,
            hidden_neurons,
        ),
        torch.nn.ReLU(),
        torch.nn.Linear(
            hidden_neurons,
            output_neurons,
        ),
    )


def train_model(
    model: torch.nn.Module,
    train_x: torch.Tensor,
    train_y: torch.Tensor,
    test_x: torch.Tensor,
    test_y: torch.Tensor,
) -> None:
    """Train model.

    Args:
        model (torch.nn.Module): Model.
        train_x (torch.Tensor): Training data.
        train_y (torch.Tensor): Training labels.
        test_x (torch.Tensor): Test data.
        test_y (torch.Tensor): Test labels.
    """
    # loss function
    criterion = torch.nn.MSELoss()

    # optimizer
    optimizer = torch.optim.Adam(
        model.parameters(),
        lr=LEARNING_RATE,
    )

    # train
    for epoch in range(epochs):
        # train
        model.train()
        for it, (x_data, y_label) in enumerate(zip(train_x, train_y)):
            # forward pass
            y_pred = model(x_data)
            sim = 1 - embedding_similarity(
                y_pred.detach().numpy(),
                y_label.detach().numpy(),
            )

            # calculate loss with simlarity
            loss = criterion(y_pred, y_label)
            loss += sim

            # backward pass
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            if it % 100 == 0:
                console.log(
                    'Epoch {0}/{1}'.format(epoch + 1, epochs),
                    'Batch {0}/{1}'.format(it + 1, len(train_x)),
                    'Loss: {0:.4f}'.format(loss.item()),
                )

    # test
    model.eval()
    with torch.no_grad():
        y_pred = model(test_x)
        loss = criterion(y_pred, test_y)
        console.log('Test loss: {0:.4f}'.format(loss.item()))

    # save model
    torch.save(model.state_dict(), file_path)


def load_model(
    df: pd.DataFrame,
    embeddings: Embeddings,
):
    """Load model.

    Args:
        df (pd.DataFrame): Dataframe to use.
        embeddings (Embeddings): Embeddings to use.

    Returns:
        torch.nn.Module: Model.
    """
    # split into train and test
    train_x, train_y, test_x, test_y = train_test_split(df, embeddings)

    # build model
    model = build_model(train_x, train_y)
    if not file_path.exists():
        console.log('Model not found, training new model.')
        train_model(model, train_x, train_y, test_x, test_y)

    # load model
    model.load_state_dict(torch.load(file_path))
    console.log('Model loaded.')

    return model


@beartype
def embedding_similarity(em1: np.ndarray, em2: np.ndarray) -> float:
    """Calculate embedding distance.

    Args:
        em1 (np.ndarray): Embedding 1.
        em2 (np.ndarray): Embedding 2.

    Returns:
        float: Distance.
    """
    return 1 - cosine(em1, em2)


def nearest_neighbors(
    k_neighbors: int,
    arr: np.ndarray,
    sample: np.ndarray,
) -> list:
    """Find nearest neighbors.

    Args:
        k_neighbors (int): Number of neighbors.
        arr (np.ndarray): Array to search.
        sample (np.ndarray): Sample to search for.

    Returns:
        list: Nearest neighbors.
    """
    highest_sim = []
    console.log('Finding nearest neighbors...', style='cyan')
    for idx in tqdm(range(len((arr)))):
        embedding = arr[idx]
        sim = embedding_similarity(embedding, sample)
        if len(highest_sim) < k_neighbors:
            highest_sim.append((idx, sim))
        else:
            for sim_idx in range(len(highest_sim)):
                if highest_sim[sim_idx][1] < sim:
                    highest_sim[sim_idx] = (idx, sim)
                    break
    return [x[0] for x in highest_sim]


if __name__ == '__main__':
    dataset = EtymDefDataset()
    embeddings = Embeddings()

    df = dataset.dataset()

    # drop 90% of the data
    ddf = df.sample(
        frac=1 - DROP_PERCENT,
        random_state=RANDOM_SEED,
    )

    # load model
    model = load_model(ddf, embeddings)

    # find unseen words with highest similarity to expected
    unseen = df[~df['word'].isin(ddf['word'])]
    unseen_words = set(unseen['word'].sample(
        frac=0.005,
        random_state=RANDOM_SEED,
    ))
    test_df = df[df['word'].isin(unseen_words)]
    test_df['word_etym'] = test_df['word'] + ' ' + test_df['etym']

    console.log('Finding best words by definition distance...')
    word_dists = []
    for word in tqdm(unseen_words):
        word_idx = df[df['word'] == word].index[0]

        # get prediction
        input_sample = embeddings.word_embeddings[word_idx]
        expected = embeddings.def_embeddings[word_idx]
        with torch.no_grad():
            pred = model(torch.tensor(expected)).detach().numpy()

        # find similarity
        word_dist = embedding_similarity(expected, pred)
        word_dists.append((word, word_dist, pred))

    # sort by similarity
    word_dists.sort(key=lambda x: x[1])

    # last 10 elements of sorted list
    best_words = word_dists[-10:]
    console.log('Best words:')
    for res in best_words:
        console.log('Word {0} Dist {1}'.format(res[0], res[1]))

    # test prediction on unseen words
    for res in best_words:
        word = res[0]
        pred = res[2]

        console.log('Word and root etymology:', style='green')
        word_etym = test_df[test_df['word'] == word]['word_etym'].values[0]
        console.log(word_etym)

        definition = test_df[test_df['word'] == word]['def'].values[0]
        console.log('Definition:', style='red')
        console.log(definition)

        # find three most similar embeddings by distance
        def_neighbors = nearest_neighbors(
            k_neighbors=3,
            arr=embeddings.def_embeddings,
            sample=pred,
        )

        # get definitions of neighbors
        def_neighbors_df = df.iloc[def_neighbors]

        # print neighbors definitions
        console.log('Closest definitions:', style='red')
        for _, def_neighbor in def_neighbors_df.iterrows():
            console.log(def_neighbor['def'])

        console.log('\n')
        console.log('-' * len(word))
