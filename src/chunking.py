from pathlib import Path
import fitz
from .types import ChunkInfo, ChunkList


def split_pdf_chunks(pdf_path: Path, chunk_size: int, cache_dir: Path) -> ChunkList:
    """
    Divide o PDF em chunks de N páginas, salva na pasta cache e retorna metadados ordenados.
    """
    with fitz.open(pdf_path) as doc:
        total_pages = doc.page_count
        chunk_infos: list[ChunkInfo] = []
        for start in range(0, total_pages, chunk_size):
            end = min(start + chunk_size, total_pages)
            chunk_idx = (start // chunk_size) + 1
            chunk_pdf = cache_dir / f"{pdf_path.stem}_chunk_{chunk_idx:04d}.pdf"
            chunk_md = cache_dir / f"{pdf_path.stem}_chunk_{chunk_idx:04d}.md"
            if not chunk_pdf.exists():
                chunk_doc = fitz.open()
                chunk_doc.insert_pdf(doc, from_page=start, to_page=end - 1)
                chunk_doc.save(chunk_pdf)
                chunk_doc.close()
            chunk_infos.append(
                ChunkInfo(pdf_path=chunk_pdf, md_path=chunk_md, index_=chunk_idx)
            )
        return tuple(chunk_infos)
