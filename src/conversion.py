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

    # Outras opções para testar:
    (ollama)
    - qwen3-vl:8b

    # Modelos bons:
    (OpenRouter)
    - qwen/qwen2.5-vl-72b-instruct
    """

    # pipeline_options: VlmPipelineOptions = __options_openrouter(
    #     "qwen/qwen2.5-vl-72b-instruct"
    # )
    pipeline_options: VlmPipelineOptions = __options_ollama(
        "llama3.2-vision:11b"
        # "qwen3-vl:30b"
        # "gemma3:27b"
        # "minicpm-v:8b"
        # "bakllava:7b"
        # "llava-phi3:3.8b"
    )

    # pipeline_options: VlmPipelineOptions = __options_lmstudio(
    #     "Jerry666/GOT-OCR2_0-716M-BF16-GGUF"  # GOT-OCR2
    #     "DevQuasar/falcon2-11B-GGUF"
    #     "allenai/olmocr-2-7b"
    # )

    # pipeline_options: VlmPipelineOptions = __options_localai(

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


def __options_localai(model: str) -> VlmPipelineOptions:
    """
    Configuração funcional e segura do pipeline Docling para uso com LocalAI (API local OpenAI-compatible).

    Parâmetros:
        model (str): Nome do modelo registrado no LocalAI (ex: 'qwen3-vl-8b-instruct').

    Retorna:
        VlmPipelineOptions: Objeto de configuração pronto para uso no pipeline Docling.

    Requisitos:
        - LocalAI rodando em http://localhost:8080 (endpoint padrão).
        - Modelo instalado e disponível no LocalAI.
        - (Opcional) Variável de ambiente LOCALAI_API_KEY definida, se autenticação estiver ativada.

    Observações:
        - Função pura, sem efeitos colaterais.
        - Imutabilidade garantida em todas as estruturas retornadas.
        - Parâmetros de geração e OCR idênticos aos de outros backends para portabilidade.
    """
    # Recupera API Key do LocalAI, se definida (autenticação opcional)
    api_key: str | None = os.getenv("LOCALAI_API_KEY")
    headers: dict[str, str] = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    # Retorna configuração imutável do pipeline
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
            url="http://localhost:8080/v1/chat/completions",
            params={
                "model": model,
                "temperature": 0.3,
                "top_p": 0.8,
                "top_k": 40,
                "repeat_penalty": 1.1,
                "max_tokens": 16384,
            },
            prompt=__get_prompt(),  # Função já existente no seu código-base
            response_format=ResponseFormat.MARKDOWN,
            timeout=1200,  # Timeout generoso para inferência local
            ocr_options=RapidOcrOptions(
                backend="paddle",
                force_full_page_ocr=True,
                lang=["portuguese", "english"],
                print_verbose=True,
            ),
            headers=headers,
        ),
    )


def __get_prompt() -> str:
    return """
            # INSTRUÇÃO CRÍTICA
            - Analise visualmente e converta este documento para Markdown com FIDELIDADE ABSOLUTA.
            - Reconstrua fielmente todos os elementos textuais, preservando rigorosamente a estrutura, hierarquia e cada detalhe do conteúdo original.
            - Ignore e NÃO transcreva cabeçalhos e rodapés repetitivos (headers/footers), números de página, títulos de capítulo recorrentes, datas ou qualquer elemento que se repita em múltiplas páginas e não faça parte do conteúdo principal.
            - Ignore completamente imagens, gráficos, diagramas e qualquer conteúdo visual. Não transcreva legendas, descrições ou referências a esses elementos.
            - Caso nada for encontrado e detectado, entregue um texto com 5 letras 'a'

            # REGRAS GERAIS
            - Não omita, resuma ou modifique nenhum conteúdo do corpo principal.
            - Mantenha a ordem, posicionamento e formatação exatos de todos os elementos.
            - O resultado deve ser apenas o conteúdo Markdown convertido, sem explicações extras, comentários ou outputs duplicados.

            # ESPECIFICAÇÕES DE CONVERSÃO

            ## Estrutura e Hierarquia
            - Converta todos os títulos e subtítulos para cabeçalhos Markdown, mantendo a hierarquia original sem pular níveis.
            - Preserve a ordem de leitura e posicionamento dos elementos.

            ## Código e Blocos Técnicos
            - Extraia todos os blocos de código, comandos de terminal, scripts e exemplos de qualquer linguagem.
            - Use fenced code blocks com a linguagem correta (ex: ```python, ```bash, ```asm).
            - Preserve shebangs, comentários, docstrings, outputs de terminal, exemplos de erro e metadados.
            - Mantenha a indentação e espaçamento exatos.

            ## Tabelas
            - Converta tabelas simples para Markdown (pipe tables), mantendo cabeçalhos, alinhamento e formatação.
            - Para tabelas complexas (células mescladas, múltiplos cabeçalhos), use HTML (<table>, <tr>, <td>, <th>).
            - Escape pipes (|) em células de tabela usando `&#124;` quando necessário.

            ## Fórmulas Matemáticas
            - Converta todas as fórmulas para sintaxe LaTeX.
            - Use `$...$` para inline e `$$...$$` para display.
            - Não altere símbolos, índices, expoentes ou operadores.
            - Escape underscores (_) e asteriscos (*) em fórmulas quando necessário.

            ## Listas, Citações e Outros Elementos
            - Mantenha listas ordenadas, não ordenadas, listas de tarefas e listas aninhadas com indentação correta.
            - Preserve blocos de citação, links, notas de rodapé e HTML embutido.

            ## Outputs, Erros e Metadados
            - Preserve outputs de terminal, exemplos de erro, tracebacks, logs e metadados.

            ## Elementos Avançados
            - Use `---` para linhas horizontais.
            - Preserve quebras de linha e parágrafos.
            - Aplique escapes onde necessário.

            # INSTRUÇÃO EXTRA
            Nunca deixe páginas vazias. Se não houver elementos estruturais, extraia todo o texto como parágrafos Markdown.

            # EXEMPLOS DE SINTAXE

            ## Tabela Markdown:
            | Coluna 1 | Coluna 2 |
            |----------|----------|
            | Valor A  | Valor B  |

            ## Código Python:
            ```python
            def exemplo():
                print("Olá, mundo!")
            ```

            ## Fórmula Matemática:
            Inline: $E = mc^2$
            Display:
            $$int_{a}^{b} f(x) dx = F(b) - F(a)$$

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
