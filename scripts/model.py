"""Model for predicting definition embedding given word embedding."""

from pathlib import Path

import torch

from experio.console import console
from experio.dataset import EtymDefDataset
from experio.models import Embeddings

drop_percent = 0.9
split_percent = 0.8
learning_rate = 0.001
epochs = 5
base_path = Path.cwd() / 'model'
random_seed = 5
if not base_path.exists():
    base_path.mkdir(parents=True)

if __name__ == '__main__':
    dataset = EtymDefDataset()
    embeddings = Embeddings()

    df = dataset.dataset()

    # drop 90% of the data
    df = df.sample(
        frac=drop_percent,
        random_state=random_seed,
    )

    words = set(df['word'])
    split = int(len(words) * split_percent)

    # randomly choose words for training
    train_words = set(df['word'].sample(
        n=split,
        random_state=random_seed,
    ))
    test_words = words - train_words

    # get embeddings
    train_idxs = df[df['word'].isin(train_words)].index
    test_idxs = df[df['word'].isin(test_words)].index
    train_x = torch.tensor(embeddings.word_embeddings[train_idxs])
    train_y = torch.tensor(embeddings.def_embeddings[train_idxs])
    test_x = torch.tensor(embeddings.word_embeddings[test_idxs])
    test_y = torch.tensor(embeddings.def_embeddings[test_idxs])

    # train cnn for neural regression
    model = torch.nn.Sequential(
        torch.nn.Linear(train_x.shape[1], train_y.shape[1]),
        torch.nn.ReLU(),
        torch.nn.Linear(train_y.shape[1], train_y.shape[1]),
        torch.nn.ReLU(),
        torch.nn.Linear(train_y.shape[1], train_y.shape[1]),
        torch.nn.ReLU(),
        torch.nn.Linear(train_y.shape[1], 1),
    )
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    loss_fn = torch.nn.MSELoss()

    for epoch in range(1, epochs):
        console.log('Epoch: {0}'.format(epoch))
        it = 0
        for x_i, y_i in zip(train_x, train_y):
            y_pred = model(x_i)
            loss = loss_fn(y_pred, y_i)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            it += 1
            if it % 100 == 0:
                console.log('Minibatch: {0}, Loss: {1}'.format(
                    it,
                    loss.item(),
                ))

    # test model
    test_preds = model(test_x)
    test_loss = loss_fn(test_preds, test_y)
    console.log('Loss: ', test_loss.item())

    # save model
    torch.save(model.state_dict(), base_path / 'model.pt')
