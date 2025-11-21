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
        Converta esta página ou documento para Markdown, preservando rigorosamente toda a estrutura, hierarquia e conteúdo original, incluindo fórmulas matemáticas, tabelas (simples e complexas), blocos de código de múltiplas linguagens, shebangs, comentários, outputs de terminal, metadados, diagramas ASCII, exemplos de erros, listas, citações, links, notas de rodapé, HTML embutido e qualquer outro elemento técnico. Siga as especificações técnicas abaixo:

        # ESTRUTURA E HIERARQUIA
        - Cabeçalhos: Detecte e converta TODOS os títulos e subtítulos para o nível correto de cabeçalho Markdown (#, ##, ###, ####, #####, ######), mantendo a hierarquia original sem pular níveis.
        - Ordem de leitura: Mantenha exatamente a mesma sequência e posicionamento de todos os elementos do documento.

        # CÓDIGO E BLOCOS TÉCNICOS
        - Blocos de código: Extraia TODOS os blocos de código, comandos de terminal, trechos de configuração, scripts e exemplos de qualquer linguagem (Python, TypeScript, Bash, Assembly, SQL, HTML, CSS, JSON, YAML, TOML, INI, Dockerfile, Makefile, etc.).
        - Identificação de linguagem: Use fenced code blocks (três backticks) especificando corretamente a linguagem:
        - ```python (para Python)
        - ```typescript (para TypeScript/JavaScript)
        - ```bash (para terminal/shell)
        - ```assembly (para Assembly)
        - ```mermaid (para diagramas Mermaid)
        - ```r, ```sql, ```yaml, ```json, ```html, ```css, ```ini, ```toml, ```dockerfile, ```makefile, ```xml, ```c, ```cpp, ```java, ```go, ```rust, etc.
        - Shebangs: Preserve linhas shebang no início de scripts (ex: #!/usr/bin/env python3, #!/bin/bash).
        - Comentários e docstrings: Preserve TODOS os comentários de linha, comentários de bloco, docstrings e anotações de tipo.
        - Indentação: Preserve a indentação e o espaçamento exatos do código, inclusive em exemplos Mermaid, listas aninhadas, diagramas em texto e chunks de código R Markdown.

        # TABELAS
        - Tabelas simples: Converta para a sintaxe Markdown (pipe tables), mantendo cabeçalhos, alinhamento, conteúdo das células e formatação.
        - Tabelas complexas: Utilize HTML (`<table>`, `<tr>`, `<td>`, `<th>`) para tabelas com células mescladas, múltiplos níveis de cabeçalho ou formatação especial.
        - Alinhamento: Mantenha alinhamento à esquerda, direita ou centro usando `:---`, `---:` ou `:---:`.

        # FÓRMULAS MATEMÁTICAS
        - Fórmulas inline: Preserve usando sintaxe LaTeX `$...$` (ex: `$E = mc^2$`).
        - Fórmulas display: Preserve usando sintaxe LaTeX `$$...$$` para fórmulas centralizadas.
        - Símbolos especiais: Não altere símbolos, índices, expoentes, operadores, frações, integrais ou matrizes.
        - Escapes: Aplique escapes necessários para evitar conflitos de sintaxe Markdown.

        # DIAGRAMAS E REPRESENTAÇÕES VISUAIS EM MERMAID
        - CONVERSÃO OBRIGATÓRIA: TODOS os diagramas, fluxogramas, esquemas, gráficos e representações visuais devem ser convertidos para código Mermaid usando fenced code blocks. NUNCA use a sintaxe padrão de imagens Markdown `` para diagramas.
        - IDENTIFICAÇÃO DO TIPO DE DIAGRAMA: Analise o conteúdo visual e escolha o tipo Mermaid apropriado:
        - Fluxogramas/Processos: `flowchart TD` ou `flowchart LR`
        - Interações/APIs: `sequenceDiagram`
        - Banco de dados: `erDiagram`
        - Classes/OOP: `classDiagram`
        - Estados: `stateDiagram-v2`
        - Cronogramas: `gantt`
        - Proporções: `pie`
        - Jornadas de usuário: `journey`
        - Versionamento: `gitGraph`
        - Arquitetura: `C4Context`, `C4Container`, etc.
        - Mapas mentais: `mindmap`
        - Cronologias: `timeline`
        - Fluxos quantitativos: `sankey-beta`
        - Categorização: `quadrantChart`
        - Formato obrigatório: Use blocos de código delimitados por três crases:
        ```mermaid
        flowchart TD
            A[Início] --> B{Decisão}
            B -->|Sim| C[Ação 1]
            B -->|Não| D[Ação 2]
            C --> E[Fim]
            D --> E
        ```
        - Caracteres especiais: Use entidades HTML para escapar caracteres reservados:
        - `&quot;` para aspas duplas
        - `#124;` para pipe (|)
        - `&lt;` e `&gt;` para < e >
        - `&amp;` para &
        - `#59;` para ponto e vírgula
        - `#35;` para cerquilha (#)
        - `#40;` e `#41;`  para parenteses 
        - Subgrafos: Use subgrafos para agrupar elementos relacionados quando apropriado.
        - Diagramas complexos: Para diagramas muito grandes, considere dividi-los em múltiplos diagramas Mermaid menores.
        - Diagramas ASCII: Se um diagrama não puder ser representado em Mermaid, preserve como ASCII art em blocos `text` ou `ascii`.
        - Validação: Todos os diagramas Mermaid gerados devem ser sintaticamente válidos.
        - DICA: Priorize a estrutura lógica e semântica do diagrama, não a reprodução visual pixel a pixel.

        ## LISTAS, CITAÇÕES E OUTROS ELEMENTOS
        - Listas: Mantenha listas ordenadas (1. 2. 3.), não ordenadas (- * +), listas de tarefas (- [ ] - [x]) e listas aninhadas, usando a indentação correta.
        - Citações: Preserve todos os blocos de citação, inclusive citações aninhadas, usando o símbolo `>` conforme o nível.
        - Links: Preserve todos os links, tanto inline `[texto](URL)` quanto referência `[texto][ref]`, sem modificar URLs.
        - Notas de rodapé: Use a sintaxe Markdown para notas de rodapé `[^1]` e definições `[^1]: Texto da nota`.
        - HTML embutido: Preserve qualquer HTML embutido (ex: `<dl>`, `<dt>`, `<dd>`, `<table>`, `<span>`, `<div>`, etc.) caso não seja possível converter para Markdown puro.

        ## OUTPUTS, ERROS E METADADOS
        - Outputs de terminal: Preserve exemplos de execução, logs, outputs de compilação e resultados de comandos, mantendo prompts ($, >>>, #), espaçamento e formatação originais.
        - Exemplos de erro: Preserve tracebacks, mensagens de exceção, warnings e outputs de erro exatamente como aparecem.
        - Metadados: Preserve cabeçalhos de arquivo, informações de versão, autor, licença, data, permissões e disclaimers.

        ## ELEMENTOS AVANÇADOS
        - Linhas horizontais: Use três ou mais hífens `---` para separar seções.
        - Quebras de linha: Preserve quebras de linha e parágrafos conforme o original.
        - Caracteres especiais: Aplique escapes onde necessário para evitar conflitos de sintaxe, especialmente em fórmulas, tabelas e código.
        - Blocos de configuração: Preserve arquivos de configuração (pyproject.toml, setup.cfg, requirements.txt, pytest.ini, Dockerfile, Makefile) com a linguagem apropriada.

        ## REGRAS CRÍTICAS
        - Não omita: Não omita, resuma ou modifique nenhum conteúdo.
        - Não reescreva: Não reescreva, interprete ou altere a ordem dos elementos.
        - Máxima fidelidade: O resultado deve ser um arquivo Markdown pronto para uso, com máxima fidelidade ao documento de origem.
        - Preservar contexto: Mantenha o contexto técnico e a funcionalidade de todos os exemplos.

        ## INSTRUÇÃO EXTRA CRÍTICA
        - Nunca deixe páginas vazias: Se não houver elementos estruturais (cabeçalhos, listas, tabelas, etc.), extraia TODO o texto da página como parágrafos Markdown. Nunca deixe páginas vazias.
        - Fallback de conteúdo: Se a página contém apenas texto corrido sem estrutura aparente, preserve-o integralmente como parágrafos Markdown.

        ## EXEMPLOS (para referência)

        ### Diagrama Mermaid (Fluxograma):
        ```mermaid
        flowchart TD
            A[Início] --> B{Condição}
            B -->|Sim| C[Ação 1]
            B -->|Não| D[Ação 2]
            C --> E[Fim]
            D --> E
        ```

        ### Diagrama Mermaid (Sequência):
        ```mermaid
        sequenceDiagram
            participant User
            participant Server
            User->>Server: Request data
            Server-->>User: Return data
        ```

        ### Diagrama Mermaid (Classe):
        ```mermaid
        classDiagram
            class User {
                +String name
                +login()
            }
            User <|-- Admin
        ```

        ### Diagrama Mermaid (ER):
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

        ### Diagrama Mermaid (Gantt):
        ```mermaid
        gantt
            title Projeto Exemplo
            dateFormat  YYYY-MM-DD
            section Planejamento
            Tarefa1 :a1, 2025-01-01, 10d
            Tarefa2 :after a1, 5d
        ```

        ### Diagrama ASCII (fallback):
        ```text
        +-----+     +-----+     +-----+
        |  A  | --> |  B  | --> |  C  |
        +-----+     +-----+     +-----+
        ```

        ---

        Aplique estas especificações rigorosamente para garantir conversão completa e fiel do documento técnico para Markdown, substituindo todas as imagens de diagramas por código Mermaid válido no local original.
        """


def convert_chunk_to_markdown(chunk: ChunkInfo, converter: DocumentConverter) -> None:
    """
    Converte um chunk PDF em Markdown usando docling e salva na pasta cache.
    """
    result = converter.convert(str(chunk.pdf_path))
    markdown = result.document.export_to_markdown()
    chunk.md_path.write_text(markdown, encoding="utf-8")
