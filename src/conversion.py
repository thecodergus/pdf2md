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

    pipeline_options: VlmPipelineOptions = __options_ollama()

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


def __options_ollama() -> VlmPipelineOptions:
    return VlmPipelineOptions(
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
            prompt=__get_prompt(),
            response_format=ResponseFormat.MARKDOWN,
            scale=1.0,
            timeout=300,  # Timeout ampliado para documentos extensos
        ),
        enable_remote_services=True,
    )


def __get_prompt() -> str:
    return """
            Converta esta página ou documento para Markdown, preservando rigorosamente toda a estrutura, hierarquia, fórmulas matemáticas, tabelas, imagens, diagramas, listas, citações, links, notas de rodapé, HTML embutido e qualquer outro conteúdo original. Siga as especificações técnicas abaixo:

            ## ESTRUTURA E HIERARQUIA
            - Cabeçalhos: Detecte e converta TODOS os títulos e subtítulos para o nível correto de cabeçalho Markdown (#, ##, ###, ####, #####, ######), mantendo a hierarquia original sem pular níveis.
            - Ordem de leitura: Mantenha exatamente a mesma sequência e posicionamento de todos os elementos do documento.

            ## CÓDIGO E BLOCOS TÉCNICOS
            - Blocos de código: Extraia TODOS os blocos de código, comandos de terminal, trechos de configuração, scripts e exemplos de qualquer linguagem.
            - Identificação de linguagem: Use fenced code blocks (três backticks) especificando corretamente a linguagem:
            - ```python (para Python)
            - ```javascript (para JavaScript)
            - ```bash (para terminal/shell)
            - ```mermaid (para diagramas Mermaid)
            - ```assembly (para Assembly)
            - ```r, ```sql, ```yaml, ```json, ```html, ```css, etc.
            - Indentação: Preserve a indentação e o espaçamento exatos do código, inclusive em exemplos Mermaid, listas aninhadas e chunks de código R Markdown.

            ## TABELAS
            - Tabelas: Converta todas as tabelas para a sintaxe Markdown (pipe tables), mantendo cabeçalhos, alinhamento, conteúdo das células e formatação. Se necessário, utilize HTML para tabelas complexas ou com células mescladas.

            ## FÓRMULAS MATEMÁTICAS
            - Fórmulas: Preserve todas as fórmulas matemáticas, convertendo para sintaxe LaTeX inline `$...$` ou display `$$...$$` conforme o original. Não altere símbolos, índices ou operadores.

            ## IMAGENS E DIAGRAMAS
            - Imagens: Extraia e insira todas as imagens e diagramas no local correto, usando a sintaxe Markdown padrão:  
            `![texto alternativo](caminho/para/imagem "título opcional")`
            - Diagramas: Para diagramas em código, use Mermaid com a linguagem apropriada.

            ## LISTAS E CITAÇÕES
            - Listas: Mantenha listas ordenadas, não ordenadas, listas de tarefas e listas aninhadas, usando a indentação correta.
            - Citações: Preserve todos os blocos de citação, inclusive citações aninhadas, usando o símbolo `>` conforme o nível.

            ## LINKS, NOTAS DE RODAPÉ E HTML
            - Links: Preserve todos os links, tanto inline quanto referência, sem modificar URLs.
            - Notas de rodapé: Use a sintaxe Markdown para notas de rodapé. 
            - HTML embutido: Preserve qualquer HTML embutido (ex: `<dl>`, `<table>`, `<span>`, etc.) caso não seja possível converter para Markdown puro.

            ## ELEMENTOS AVANÇADOS
            - Linhas horizontais: Use três ou mais hífens `---` para separar seções.
            - Quebras de linha: Preserve quebras de linha e parágrafos conforme o original.
            - Caracteres especiais: Aplique escapes onde necessário para evitar conflitos de sintaxe, especialmente em fórmulas, tabelas e código.

            ## REGRAS CRÍTICAS
            - Não omita, resuma ou modifique nenhum conteúdo.
            - Não reescreva, interprete ou altere a ordem dos elementos.
            - O resultado deve ser um arquivo Markdown pronto para uso, com máxima fidelidade ao documento de origem.

            ## EXEMPLOS (para referência do modelo)
            - Tabela Markdown:
            ```
            | Variável | Valor | Descrição         |
            |----------|-------|------------------|
            | x        | 10    | Valor de entrada |
            | y        | 20    | Valor de saída   |
            ```
            - Fórmula matemática:
            ```
            $E = mc^2$
            $$
            \int_{a}^{b} f(x) dx = F(b) - F(a)
            $$
            ```
            - Imagem:
            ```
            ![Diagrama de fluxo](imagens/fluxo.png "Fluxo do processo")
            ```
            - Nota de rodapé:
            ```
            Texto com nota1]

            ^1]: Esta é uma nota de rodapé.
            ```
            - HTML embutido:
            ```
            <dl>
                <dt>Termo</dt>
                <dd>Definição do termo.</dd>
            </dl>
            ```
            """
