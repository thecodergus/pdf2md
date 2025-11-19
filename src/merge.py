# Codemagus: Merge funcional de arquivos Markdown ordenados
from pathlib import Path
from .types import ChunkList, ChunkInfo


def merge_markdown_chunks(chunks: ChunkList, output_path: Path) -> None:
    """
    Une todos os arquivos Markdown ordenados em um único arquivo final.
    """
    with output_path.open("w", encoding="utf-8") as outfile:
        for chunk in sorted(chunks, key=lambda c: c.index_):
            if chunk.md_path.exists():
                outfile.write(chunk.md_path.read_text(encoding="utf-8"))
                outfile.write("\n\n")
