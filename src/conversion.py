# Codemagus: Conversão PDF→Markdown com docling VLM granite_docling
from .types import ChunkInfo
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions, RapidOcrOptions
from docling.document_converter import DocumentConverter, PdfFormatOption


ARTIFACTS_PATH: str = "/home/gustavo/.cache/docling/models"


def configure_docling_converter() -> DocumentConverter:
    """
    Configura o conversor docling para pipeline VLM com modelo granite_docling.
    """

    pipeline_options = PdfPipelineOptions(artifacts_path=ARTIFACTS_PATH)
    pipeline_options.ocr_options = RapidOcrOptions(
        backend="torch",
    )

    return DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
        }
    )


def convert_chunk_to_markdown(chunk: ChunkInfo, converter: DocumentConverter) -> None:
    """
    Converte um chunk PDF em Markdown usando docling e salva na pasta cache.
    """
    result = converter.convert(str(chunk.pdf_path))
    markdown = result.document.export_to_markdown()
    chunk.md_path.write_text(markdown, encoding="utf-8")
