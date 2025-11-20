from pathlib import Path
from diskcache import Cache
from .types import ChunkInfo, ChunkList
from concurrent.futures import ThreadPoolExecutor, as_completed


class CacheManager:
    """
    Gerenciador de cache com operações paralelas e tipagem moderna.
    """

    def __init__(self, cache_dir: Path) -> None:
        """
        Inicializa o gerenciador de cache.

        :param cache_dir: Diretório do cache.
        """
        self.cache: Cache = Cache(str(cache_dir))

    def is_chunk_processed(self, chunk: ChunkInfo) -> bool:
        """
        Verifica se um chunk foi processado.

        :param chunk: ChunkInfo a ser verificado.
        :return: True se processado, False caso contrário.
        """
        return chunk.md_path.exists() and self.cache.get(str(chunk.md_path), False)

    def mark_chunk_processed(self, chunk: ChunkInfo) -> None:
        """
        Marca um chunk como processado.

        :param chunk: ChunkInfo a ser marcado.
        """
        self.cache[str(chunk.md_path)] = True

    def clear_cache_parallel(self) -> None:
        """
        Exclui todos os itens do cache de forma paralela utilizando multithreading.

        Utiliza ThreadPoolExecutor para deletar cada chave do cache em threads separadas,
        garantindo performance otimizada para operações I/O-bound.

        :raises Exception: Propaga exceções ocorridas durante a exclusão.
        """
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self.cache.delete, key) for key in self.cache.iterkeys()
            ]
            for future in as_completed(futures):
                exception = future.exception()
                if exception is not None:
                    raise exception

    def close(self) -> None:
        """
        Fecha o cache de forma segura.
        """
        self.cache.close()
