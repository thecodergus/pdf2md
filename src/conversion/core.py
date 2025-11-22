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

    (Ollama)
    -

    (LM Studio)
    - )

    (LocalAI)
    -

    # Modelos Medios
    (Ollama)
    - minicpm-v:8b (talvez melhorar o prompt ou aumentando o chunk de paginas melhore o resultado)

    (LM Studio)
    - allenai/olmocr-2-7b (Faz o que se deve mas não identa em markdown

    (LocalAI)
    -
    """

    # pipeline_options: VlmPipelineOptions = __options_openrouter(
    #     "qwen/qwen2.5-vl-72b-instruct"
    #      "qwen/qwen3-vl-30b-a3b-instruct"
    #      "nvidia/nemotron-nano-12b-v2-vl"
    #      "opengvlab/internvl3-78b"
    #      "deepcogito/cogito-v2-preview-llama-109b-moe"
    #      "baidu/ernie-4.5-vl-28b-a3b"
    #      "openai/gpt-5-nano"
    # )
    # pipeline_options: VlmPipelineOptions = __options_ollama("llava-phi3:3.8b")

    pipeline_options: VlmPipelineOptions = __options_lmstudio(
        "DevQuasar/falcon2-11B-GGUF"
        #     "lmstudio-community/pixtral-12b-GGUF"
    )

    # pipeline_options: VlmPipelineOptions = __options_localai(
    #   "pocketdoc_dans-personalityengine-v1.2.0-24b"
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
