# Codemagus: Conversão PDF→Markdown com docling VLM Qwen3-VL-8B-Instruct (local)
from pathlib import Path
from .types import ChunkInfo, ChunkList
from docling.datamodel.base_models import InputFormat, AcceleratorDevice
from docling.datamodel.pipeline_options_vlm_model import (
    InlineVlmOptions,
    ResponseFormat,
    InferenceFramework,
    TransformersModelType,
)
from docling.datamodel.pipeline_options import VlmPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.pipeline.vlm_pipeline import VlmPipeline


def configure_docling_converter() -> DocumentConverter:
    """
    Configura o conversor docling para pipeline VLM com modelo Qwen/Qwen3-VL-8B-Instruct (local).
    Outras opções para testar:
    - openbmb/MiniCPM-o-2_6
    - Qwen/Qwen3-VL-32B-Instruct
    - Qwen/Qwen2.5-VL-32B-Instruct
    """
    pipeline_options: VlmPipelineOptions = VlmPipelineOptions(
        vlm_options=InlineVlmOptions(
            repo_id="Qwen/Qwen3-VL-8B-Instruct",
            prompt=(
                "Converta esta página para Markdown seguindo a risca a estrutura. "
                "Não perca nenhum texto, código de linguagens de programação/marcação/terminal/estilo ou imagem!"
            ),
            response_format=ResponseFormat.MARKDOWN,
            inference_framework=InferenceFramework.TRANSFORMERS,
            transformers_model_type=TransformersModelType.AUTOMODEL_IMAGETEXTTOTEXT,
            supported_devices=[AcceleratorDevice.CUDA, AcceleratorDevice.CPU],
            scale=2.0,
            temperature=0.3,
            top_p=0.8,
            top_k=20,
            presence_penalty=1.5,
            out_seq_length=16384,
        )
    )
    return DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_cls=VlmPipeline, pipeline_options=pipeline_options
            )
        }
    )


def convert_chunk_to_markdown(chunk: ChunkInfo, converter: DocumentConverter) -> None:
    """
    Converte um chunk PDF em Markdown usando docling e salva na pasta cache.
    """
    result = converter.convert(str(chunk.pdf_path))
    markdown = result.document.export_to_markdown()
    chunk.md_path.write_text(markdown, encoding="utf-8")
