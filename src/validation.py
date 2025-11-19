# Codemagus: Validação funcional de PDF com PyMuPDF
from pathlib import Path
import fitz  # PyMuPDF


def is_valid_pdf(pdf_path: Path) -> bool:
    """
    Verifica se o PDF é íntegro e não corrompido.
    """
    try:
        fitz.TOOLS.reset_mupdf_warnings()
        with fitz.open(pdf_path) as doc:
            for i in range(doc.page_count):
                doc.load_page(i)
        return True
    except Exception:
        return False
