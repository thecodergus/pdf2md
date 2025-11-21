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

    def clear_cache_parallel(self, chunks: ChunkList) -> None:
        """
        Exclui todos os arquivos .md e .pdf dos chunks e limpa o cache associado, de forma paralela.
        """
        file_paths = extract_file_paths_from_chunks(chunks)
        with ThreadPoolExecutor() as executor:
            # Exclusão paralela dos arquivos físicos
            futures = {
                executor.submit(delete_file_safe, path): path for path in file_paths
            }
            for future in as_completed(futures):
                path = futures[future]
                result = future.result()
            cache_keys = [str(chunk.md_path) for chunk in chunks]
            cache_futures = [
                executor.submit(self.cache.delete, key) for key in cache_keys
            ]
            for future in as_completed(cache_futures):
                exception = future.exception()
                if exception is not None:
                    raise exception

    def close(self) -> None:
        """
        Fecha o cache de forma segura.
        """
        self.cache.close()


def extract_file_paths_from_chunks(chunks: ChunkList) -> list[Path]:
    """
    Função pura para extrair todos os caminhos .md e .pdf dos chunks.
    """
    return [chunk.md_path for chunk in chunks] + [chunk.pdf_path for chunk in chunks]


def delete_file_safe(path: Path) -> bool:
    """
    Exclui um arquivo de forma segura, retornando True se sucesso, False se falha.
    """
    try:
        if path.exists():
            path.unlink()
        return True
    except (PermissionError, OSError, FileNotFoundError):
        return False
