# Codemagus: Conversão PDF→Markdown com docling VLM Qwen3-VL-8B-Instruct (local)
from pathlib import Path
import os
from typing import Final
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
    TableStructureOptions,
)
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.pipeline.vlm_pipeline import VlmPipeline
from docling.datamodel.accelerator_options import AcceleratorDevice, AcceleratorOptions


def configure_docling_converter() -> DocumentConverter:
    """
    Configura o conversor docling para pipeline VLM com modelo Qwen/Qwen3-VL-8B-Instruct (local).
    Outras opções para testar:
    (ollama)
    - qwen3-vl:8b
    """

    # pipeline_options: VlmPipelineOptions = __options_openrouter(
    #     "qwen/qwen2.5-vl-72b-instruct"
    # )
    pipeline_options: VlmPipelineOptions = __options_ollama(
        # "qwen3-vl:8b"
        # "gemma3:27b"
        "mistral-small3.2:24b"
        # "qwen3-vl:32b"
        # "llava:34b"
        # "granite3.2-vision:2b"
        # "deepseek-ocr:3b"
    )

    return DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_cls=VlmPipeline, pipeline_options=pipeline_options
            )
        }
    )


def __options_ollama(model: str) -> VlmPipelineOptions:
    return VlmPipelineOptions(
        enable_remote_services=True,
        do_formula_enrichment=True,
        do_table_structure=True,
        do_code_enrichment=True,
        # do_picture_description=True,
        table_structure_options=TableStructureOptions(
            do_cell_matching=True,
            model_name="TableFormer++",
        ),
        vlm_options=ApiVlmOptions(
            url="http://localhost:11434/v1/chat/completions",
            params={
                "model": model,
                "temperature": 0.3,
                "top_p": 0.8,
                "top_k": 40,
                "repeat_penalty": 1.1,
                "max_tokens": 16384,
            },
            prompt=__get_prompt(),
            response_format=ResponseFormat.MARKDOWN,
            timeout=1_200,
            ocr_options=RapidOcrOptions(
                backend="paddle",
                force_full_page_ocr=True,
                lang=[
                    "portuguese",
                    "english",
                ],
                print_verbose=True,
            ),
        ),
    )


def __options_openrouter(model: str) -> VlmPipelineOptions:
    """
    Configuração funcional e segura do pipeline Docling para uso com OpenRouter.
    - Endpoint remoto autenticado
    - Parâmetros de modelo ajustados
    - OCR multilíngue robusto
    - Estrutura de tabelas avançada

    Modelos que são bons e que testei:
    - qwen/qwen3-vl-235b-a22b-instruct
    - qwen/qwen2.5-vl-72b-instruct
    """
    api_key: Final[str] = __get_openrouter_api_key()
    return VlmPipelineOptions(
        enable_remote_services=True,
        do_formula_enrichment=True,
        do_table_structure=True,
        do_code_enrichment=True,
        table_structure_options=TableStructureOptions(
            do_cell_matching=True,
            model_name="TableFormer++",
        ),
        vlm_options=ApiVlmOptions(
            url="https://openrouter.ai/api/v1/chat/completions",
            params={
                "model": model,  # Substitua por outro modelo OpenRouter se necessário
                "temperature": 0.3,
                "top_p": 0.8,
                "top_k": 40,
                "repeat_penalty": 1.1,
                "max_tokens": 16384,
            },
            prompt=__get_prompt(),
            response_format=ResponseFormat.MARKDOWN,
            timeout=1200,  # Timeout ampliado para API remota
            ocr_options=RapidOcrOptions(
                backend="paddle",
                force_full_page_ocr=True,
                lang=["portuguese", "english"],
                print_verbose=True,
            ),
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
        ),
    )


def __get_openrouter_api_key() -> str:
    """
    Recupera a chave de API do OpenRouter de variável de ambiente.
    Função pura, defensiva, nunca expõe segredo em logs.
    """
    api_key: str | None = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Variável de ambiente OPENROUTER_API_KEY não definida. "
            "Defina sua chave de API do OpenRouter para autenticação segura."
        )
    return api_key


def __options_lmstudio(model: str) -> VlmPipelineOptions:
    """
    Configuração do pipeline Docling para uso com LM Studio (API local OpenAI-compatible).
    - Endpoint local, sem custo, privacidade total
    - Parâmetros ajustados para performance local
    - OCR multilíngue robusto
    - Estrutura de tabelas avançada
    """
    return VlmPipelineOptions(
        enable_remote_services=True,
        do_formula_enrichment=True,
        do_table_structure=True,
        do_code_enrichment=True,
        table_structure_options=TableStructureOptions(
            do_cell_matching=True,
            model_name="TableFormer++",
        ),
        vlm_options=ApiVlmOptions(
            url="http://localhost:1234/v1/chat/completions",
            params={
                "model": model,
                "temperature": 0.3,
                "top_p": 0.8,
                "top_k": 40,
                "repeat_penalty": 1.1,
                "max_tokens": 16384,
            },
            prompt=__get_prompt(),
            response_format=ResponseFormat.MARKDOWN,
            timeout=300,  # Timeout otimizado para local
            ocr_options=RapidOcrOptions(
                backend="paddle",
                force_full_page_ocr=True,
                lang=["portuguese", "english"],
                print_verbose=True,
            ),
            headers={
                "Content-Type": "application/json",
                # "Authorization": "Bearer lm-studio",  # Opcional, só se quiser forçar compatibilidade
            },
        ),
    )


def __get_prompt() -> str:
    return """
        # INSTRUÇÃO CRÍTICA
        - Analise e converta este documento para o formato Markdown com FIDELIDADE ABSOLUTA. 
        - Reconstrua fielmente todos os elementos, preservando rigorosamente a estrutura, hierarquia e cada detalhe do conteúdo original.

        # REGRAS GERAIS
        - Não omita, resuma ou modifique nenhum conteúdo  
        - Mantenha a ordem, posicionamento e formatação exatos de todos os elementos  
        - O resultado deve ser apenas o conteúdo Markdown convertido, sem explicações extras

        # ESPECIFICAÇÕES DE CONVERSÃO

        ## Estrutura e Hierarquia  
        - Converta todos os títulos e subtítulos para cabeçalhos Markdown, mantendo a hierarquia original sem pular níveis
        - Preserve a ordem de leitura e posicionamento dos elementos

        ## Código e Blocos Técnicos  
        - Extraia todos os blocos de código, comandos de terminal, scripts e exemplos de qualquer linguagem
        - Use fenced code blocks com a linguagem correta (ex: ```python, ```bash, ```asm)
        - Preserve shebangs, comentários, docstrings, outputs de terminal, exemplos de erro e metadados
        - Mantenha a indentação e espaçamento exatos

        ## Tabelas
        - Converta tabelas simples para Markdown (pipe tables), mantendo cabeçalhos, alinhamento e formatação
        - Para tabelas complexas (células mescladas, múltiplos cabeçalhos), use HTML (<table>, <tr>, <td>, <th>)

        ## Fórmulas Matemáticas
        - Converta todas as fórmulas para sintaxe LaTeX
        - Use `$...$` para inline e `$$...$$` para display
        - Não altere símbolos, índices, expoentes ou operadores

        ## Listas, Citações e Outros Elementos
        - Mantenha listas ordenadas, não ordenadas, listas de tarefas e listas aninhadas com indentação correta
        - Preserve blocos de citação, links, notas de rodapé e HTML embutido

        ## Outputs, Erros e Metadados 
        - Preserve outputs de terminal, exemplos de erro, tracebacks, logs e metadados

        ## Elementos Avançados  
        - Use `---` para linhas horizontais
        - Preserve quebras de linha e parágrafos
        - Aplique escapes onde necessário

        # INSTRUÇÃO EXTRA  
        Nunca deixe páginas vazias. Se não houver elementos estruturais, extraia todo o texto como parágrafos Markdown.

        # OUTPUT ESPERADO  
        Apenas o conteúdo Markdown convertido, sem qualquer texto adicional, introdução ou conclusão.
        """


def convert_chunk_to_markdown(chunk: ChunkInfo, converter: DocumentConverter) -> None:
    """
    Converte um chunk PDF em Markdown usando docling e salva na pasta cache.
    """
    result = converter.convert(str(chunk.pdf_path))
    markdown = result.document.export_to_markdown()
    chunk.md_path.write_text(markdown, encoding="utf-8")
