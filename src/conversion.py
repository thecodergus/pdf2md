# Codemagus: Conversão PDF→Markdown com docling VLM Qwen3-VL-8B-Instruct (local)
from pathlib import Path
from .types import ChunkInfo, ChunkList
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options_vlm_model import (
    InlineVlmOptions,
    ResponseFormat,
    InferenceFramework,
    TransformersModelType,
    ApiVlmOptions,
)
from docling.datamodel.pipeline_options import (
    VlmPipelineOptions,
    RapidOcrOptions,
)
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.pipeline.vlm_pipeline import VlmPipeline
from docling.datamodel.accelerator_options import AcceleratorDevice, AcceleratorOptions


def configure_docling_converter() -> DocumentConverter:
    """
    Configura o conversor docling para pipeline VLM com modelo Qwen/Qwen3-VL-8B-Instruct (local).
    Outras opções para testar:
    - openbmb/MiniCPM-o-2_6
    - Qwen/Qwen3-VL-32B-Instruct
    - Qwen/Qwen2.5-VL-32B-Instruct
    """

    pipeline_options: VlmPipelineOptions = VlmPipelineOptions(
        vlm_options=ApiVlmOptions(
            url="http://localhost:11434/v1/chat/completions",  # Endpoint padrão Ollama local
            params={
                "model": "qwen3-vl:8b",  # Nome do modelo conforme registrado no Ollama
                "temperature": 0.3,
                "top_p": 0.8,
                "top_k": 40,
                "repeat_penalty": 1.1,  # Substitui presence_penalty
                "max_tokens": 16384,  # Limite de tokens de saída
            },
            prompt="""
                Converta esta página ou documento para Markdown, preservando rigorosamente toda a estrutura, hierarquia e conteúdo original. Siga as especificações técnicas abaixo:
                ## ESTRUTURA E HIERARQUIA
                - **Cabeçalhos:** Detecte e converta TODOS os títulos e subtítulos para o nível correto de cabeçalho Markdown (#, ##, ###, ####, #####, ######), mantendo a hierarquia original sem pular níveis.
                - **Ordem de leitura:** Mantenha exatamente a mesma sequência e posicionamento de todos os elementos do documento.

                ## CÓDIGO E BLOCOS TÉCNICOS
                - **Blocos de código:** Extraia TODOS os blocos de código, comandos de terminal, trechos de configuração, scripts e exemplos de qualquer linguagem.
                - **Identificação de linguagem:** Use fenced code blocks (três backticks) especificando corretamente a linguagem:
                - ```python (para Python)
                - ```javascript (para JavaScript)
                - ```bash (para terminal/shell)
                - ```mermaid (para diagramas Mermaid)
                - ```sql, ```yaml, ```json, ```html, ```css, etc.
                - **Indentação:** Preserve a indentação e o espaçamento exatos do código, inclusive em exemplos Mermaid e listas aninhadas.
                """,
            response_format=ResponseFormat.MARKDOWN,
            timeout=300,  # Timeout ampliado para documentos extensos
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
