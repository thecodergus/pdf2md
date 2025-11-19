from pathlib import Path
from diskcache import Cache
from .types import ChunkInfo, ChunkList


class CacheManager:
    def __init__(self, cache_dir: Path):
        self.cache = Cache(str(cache_dir))

    def is_chunk_processed(self, chunk: ChunkInfo) -> bool:
        return chunk.md_path.exists() and self.cache.get(str(chunk.md_path), False)

    def mark_chunk_processed(self, chunk: ChunkInfo) -> None:
        self.cache[str(chunk.md_path)] = True

    def close(self):
        self.cache.close()
