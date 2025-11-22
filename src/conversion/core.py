from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import (
    VlmPipelineOptions,
)
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.pipeline.vlm_pipeline import VlmPipeline

from .backends import (
    __options_ollama,
    __options_openrouter,
    __get_openrouter_api_key,
    __options_lmstudio,
    __options_localai,
)


def configure_docling_converter() -> DocumentConverter:
    """
    Configura o conversor docling para pipeline VLM com modelo Qwen/Qwen3-VL-8B-Instruct (local).

    # Modelos bons:
    (OpenRouter)
    - qwen/qwen2.5-vl-72b-instruct
    - qwen/qwen3-vl-235b-a22b-instruct
    - deepcogito/cogito-v2-preview-llama-109b-moe
    - qwen/qwen3-vl-30b-a3b-instruct

    (Ollama)
    -

    (LM Studio)
    -


    (LocalAI)
    -

    # Modelos Medios
    (Ollama)
    - minicpm-v:8b (talvez melhorar o prompt ou aumentando o chunk de paginas melhore o resultado)

    (LM Studio)
    - allenai/olmocr-2-7b (Faz o que se deve mas não identa em markdown)
    - openbmb/MiniCPM-V-4_5-gguf

    (LocalAI)
    -
    """

    pipeline_options: VlmPipelineOptions = __options_openrouter(
        "qwen/qwen2.5-vl-72b-instruct"
    )

    # pipeline_options: VlmPipelineOptions = __options_ollama()

    # pipeline_options: VlmPipelineOptions = __options_lmstudio(

    # )

    # pipeline_options: VlmPipelineOptions = __options_localai(
    #
    # )

    # A tentar conseguir Hospedar:
    # DeepSeek‑VL -> Não compatível com LM Studio, LocalAI e nem Ollama
    # GLM‑4.1V‑9B‑Thinking -> Não compatível com LM Studio, LocalAI e nem Ollama

    return DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_cls=VlmPipeline, pipeline_options=pipeline_options
            )
        }
    )
