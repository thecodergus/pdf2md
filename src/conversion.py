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

    pipeline_options: VlmPipelineOptions = __options_openrouter()

    return DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_cls=VlmPipeline, pipeline_options=pipeline_options
            )
        }
    )


def __options_ollama() -> VlmPipelineOptions:
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
                "model": "qwen3-vl:8b",
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


def __options_openrouter() -> VlmPipelineOptions:
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
                "model": "qwen/qwen2.5-vl-72b-instruct",  # Substitua por outro modelo OpenRouter se necessário
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


def __get_prompt() -> str:
    return """
        # INSTRUÇÃO CRÍTICA
        Analise visualmente e converta este documento técnico para Markdown com FIDELIDADE ABSOLUTA. Reconstrua fielmente todos os elementos, preservando rigorosamente a estrutura, hierarquia e cada detalhe do conteúdo original.

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
        - Use fenced code blocks com a linguagem correta (ex: ```python, ```bash, ```mermaid)
        - Preserve shebangs, comentários, docstrings, outputs de terminal, exemplos de erro e metadados
        - Mantenha a indentação e espaçamento exatos

        ## Tabelas
        - Converta tabelas simples para Markdown (pipe tables), mantendo cabeçalhos, alinhamento e formatação
        - Para tabelas complexas (células mescladas, múltiplos cabeçalhos), use HTML (<table>, <tr>, <td>, <th>)

        ## Fórmulas Matemáticas
        - Converta todas as fórmulas para sintaxe LaTeX
        - Use `$...$` para inline e `$$...$$` para display
        - Não altere símbolos, índices, expoentes ou operadores

        ## Diagramas e Representações Visuais (PRIORIDADE MÁXIMA)  
        - **TODOS os diagramas, fluxogramas, esquemas e gráficos DEVEM ser convertidos para código Mermaid**
        - **NUNCA use sintaxe de imagem Markdown para diagramas**
        - Interprete o layout visual e escolha o tipo Mermaid apropriado (flowchart, sequenceDiagram, erDiagram, classDiagram, stateDiagram-v2, gantt, etc.)
        - Use entidades HTML para escapar caracteres especiais dentro do Mermaid
        - Se um diagrama for impossível de representar em Mermaid, preserve como ASCII art em bloco de código `text` ou `ascii`
        - O código Mermaid gerado deve ser sintaticamente válido

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

        # EXEMPLOS DE MERMAID (PARA REFERÊNCIA)

        ```mermaid
        flowchart TD
            A[Início] --> B{Condição}
            B -->|Sim| C[Ação 1]
            B -->|Não| D[Ação 2]
            C --> E[Fim]
            D --> E
        ```
        ```mermaid
        sequenceDiagram
            participant User
            participant Server
            User->>Server: Request data
            Server-->>User: Return data
        ```
        ```mermaid
        classDiagram
            class User {
                +String name
                +login()
            }
            User <|-- Admin
        ```
        ```mermaid
        erDiagram
            CLIENTE ||--o{ PEDIDO : faz
            CLIENTE {
                int id PK
                string nome
            }
            PEDIDO {
                int id PK
                date data
            }
        ```
        ```mermaid
        gantt
            title Projeto Exemplo
            dateFormat  YYYY-MM-DD
            section Planejamento
            Tarefa1 :a1, 2025-01-01, 10d
            Tarefa2 :after a1, 5d
        ```

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
