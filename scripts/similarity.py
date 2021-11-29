"""Script to see similarity between two sentence embeddings."""
import torch
from scipy.spatial.distance import cosine

from transformers import AutoModel, AutoTokenizer

if __name__ == '__main__':
    # Load the model
    model = 'johngiorgi/declutr-small'
    tokenizer = AutoTokenizer.from_pretrained(model)
    model = AutoModel.from_pretrained(model)

    # Prepare some text to embed
    texts = [
        'Not mesogenic.',
        'Not biological.',
    ]
    inputs = tokenizer(
        texts,
        padding=True,
        truncation=True,
        return_tensors='pt',
    )

    # Embed the text
    with torch.no_grad():
        sequence_output = model(**inputs)[0]

    # Mean pool the token-level embeddings to get sentence-level embeddings
    embeddings = torch.sum(
        sequence_output * inputs['attention_mask'].unsqueeze(-1), dim=1
    ) / torch.clamp(torch.sum(inputs['attention_mask'], dim=1, keepdims=True), min=1e-9)

    # Compute a semantic similarity via the cosine distance
    semantic_sim = 1 - cosine(embeddings[0], embeddings[1])
    print(semantic_sim)
