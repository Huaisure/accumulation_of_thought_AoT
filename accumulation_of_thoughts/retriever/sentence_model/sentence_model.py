from sentence_transformers import SentenceTransformer


class SentenceModel:
    def __init__(self, model_name) -> None:
        try:
            self.model = SentenceTransformer(model_name, device="auto")
        except Exception as e:
            raise ValueError(f"Error loading model: {e}")

    def encode(self, text: str):
        return self.model.encode(text)

    def similarity(self, text1, emb2):
        """
        Calculate the similarity between current text and stored text
        """
        if type(text1) is str:
            emb1 = self.encode(text1)
        if type(emb2) is str:
            emb2 = self.encode(emb2)

        return self.model.cosine_similarity(emb1, emb2)
