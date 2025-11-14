from __future__ import annotations

from typing import Iterable

import numpy as np

Vector = list[float]


class EmbeddingService:
    """Simple wrapper for embedding generation (stubbed for now)."""

    def __init__(self, model: str = "stub") -> None:
        self.model = model

    async def embed(self, texts: Iterable[str]) -> list[Vector]:
        if self.model == "stub":
            return [self._hash_embed(text) for text in texts]
        raise NotImplementedError("Only stub embeddings implemented")

    def _hash_embed(self, text: str, dim: int = 1536) -> Vector:
        rng = np.random.default_rng(abs(hash(text)) % (2**32))
        vector = rng.standard_normal(dim)
        norm = np.linalg.norm(vector)
        return (vector / norm).astype(float).tolist()
