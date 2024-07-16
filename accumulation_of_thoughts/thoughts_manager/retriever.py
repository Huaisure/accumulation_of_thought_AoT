"""
Thoughts Retriever
"""

import torch
from .sentence_model import SentenceModel


class Retriever:
    """
    Retriever class
    Search for the most relevant thoughts template
    """

    def __init__(self, model, template_embedding_path, threshold=0.5):
        self.emb = torch.load(template_embedding_path)
        self.model = model
        self.threshold = threshold

    def search(self, text: str, create: bool = False) -> int:
        """
        Search for the most relevant thoughts template

        if the similarity is greater than the threshold:
            return the index of the template
        else return -1
        """
        sim = self.model.similarity(text, self.emb)
        max_sim = max(sim)
        max_index = sim.index(max_sim)
        if create:
            # if create is True, return the index of the most similar template,
            # no matter the similarity is greater than the threshold or not.
            # This is used to create a new template.
            # Because no template in the file > threshold
            return max_index
        if max_sim > self.threshold:
            return max_index
        else:
            return -1

    def search_all(self, text: str) -> list:
        """
        Search for all relevant thoughts templates
        """
        sim = self.model.similarity(text, self.emb)
        index = []
        for i, s in enumerate(sim):
            if s > self.threshold:
                index.append(i)
        return index
