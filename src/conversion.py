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

    # Modelos bons:
    (OpenRouter)
    - qwen/qwen2.5-vl-72b-instruct
    - qwen/qwen3-vl-235b-a22b-instruct

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
    -

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
    pipeline_options: VlmPipelineOptions = __options_ollama(
        "bakllava:7b"
        # "llava-phi3:3.8b"
    )

    # pipeline_options: VlmPipelineOptions = __options_lmstudio(
    #     "prithivMLmods/granite-docling-258M-f32-GGUF"
    #     "allenai/olmocr-2-7b"
    #     "Jerry666/GOT-OCR2_0-716M-BF16-GGUF"  # GOT-OCR2
    #     "DevQuasar/falcon2-11B-GGUF"
    #     "lmstudio-community/pixtral-12b-GGUF"
    # )

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
# INSTRUÇÃO CRÍTICA (PROCESSO MODULAR EM 7 ETAPAS)

## ETAPA 1: ANÁLISE VISUAL E ESTRUTURAL
- Analise visualmente a página PDF fornecida.
- Identifique todos os blocos de texto, títulos, listas, tabelas, fórmulas, blocos de código e outros elementos estruturais.

## ETAPA 2: SUPRESSÃO DE CABEÇALHOS E RODAPÉS (HEADERS/FOOTERS)
- NÃO transcreva nenhum elemento que:
  + Apareça no topo ou rodapé da página, separado do corpo principal.
  + Contenha números de página, datas, títulos de capítulo, nomes de autor, logotipos ou qualquer texto repetido em múltiplas páginas.
  + Tenha formatação menor, alinhamento à esquerda/direita, ou esteja isolado por linhas/espaçamento.
- Exemplos de headers/footers a IGNORAR:
  + "Capítulo 2", "Página 15", "Janeiro 2025", "Manual Técnico", "www.empresa.com"
- Se identificar um bloco suspeito, priorize a exclusão. Na dúvida, NÃO transcreva.

## ETAPA 3: VALIDAÇÃO DE HIERARQUIA (TÍTULOS E SUBTÍTULOS)
- Só converta um bloco para cabeçalho Markdown (ex: #, ##, ###) se TODOS os 3 critérios abaixo forem atendidos:
  1. **Tamanho de fonte visivelmente maior** que o texto corrido.
  2. **Destaque visual claro** (negrito, sublinhado, centralizado, ou espaçamento extra acima/abaixo).
  3. **Isolamento**: o bloco está separado do texto anterior e posterior (não é continuação de parágrafo).
- Se o início da página for apenas texto corrido, NÃO promova a título. Mantenha como parágrafo.
- Exemplos negativos:
  + Página inicia com "O sistema proposto apresenta..." → NÃO é título, converta como parágrafo.
- Exemplos positivos:
  + Texto centralizado, grande, negrito: "3. Resultados Experimentais" → Converta para cabeçalho Markdown.

## ETAPA 4: CONVERSÃO ESTRUTURADA PARA MARKDOWN
- Siga as regras abaixo para cada elemento:
  + **Títulos/Subtítulos**: Use cabeçalhos Markdown (#, ##, ###) conforme hierarquia validada.
  + **Parágrafos**: Mantenha como texto simples, preservando ordem e espaçamento.
  + **Blocos de código**: Use fenced code blocks com linguagem correta (ex: ```python).
  + **Tabelas simples**: Use pipe tables Markdown. Tabelas complexas: use HTML (<table>).
  + **Fórmulas matemáticas**: Converta para LaTeX ($...$ inline, $$...$$ display).
  + **Listas**: Mantenha ordenação e indentação.
  + **Citações, links, notas de rodapé**: Preserve formatação.
  + **Outputs, erros, logs**: Preserve integralmente.
  + **Linhas horizontais**: Use `---`.
  + **Quebras de linha e parágrafos**: Preserve.
  + **Aplique escapes** onde necessário.
- Ignore completamente imagens, gráficos, diagramas, legendas e referências visuais.

## ETAPA 5: DETECÇÃO E REMOÇÃO DE REPETIÇÕES INTERNAS
- Após converter a página para Markdown, revise o texto resultante.
- **Detecte e remova qualquer trecho, frase ou parágrafo repetido consecutivamente mais de uma vez na mesma página.**
  + Considere como repetição qualquer sequência de 12 palavras ou mais que ocorra 2 vezes ou mais, mesmo com pequenas variações.
  + Utilize análise de n-gramas (8-12 palavras) e rolling hash para identificar repetições.
  + Ignore repetições legítimas em tabelas, listas ou estruturas de código.
- **Remova todas as repetições, mantendo apenas a primeira ocorrência de cada trecho.**
- Se identificar um padrão de repetição que se estende indefinidamente (loop), interrompa a repetição, limpe o texto e continue normalmente.
- Exemplos de repetição a remover:
  + "sem aplicação de questionários, grupos focal ou outras formas de coleta dirigida de dados, sem aplicação de questionários, grupos focal ou outras formas de coleta dirigida de dados, ..." → Mantenha apenas a primeira ocorrência.

## ETAPA 6: VALIDAÇÃO FINAL (CHECKLIST)
- Antes de finalizar, valide:
  1. Nenhum header/footer foi transcrito.
  2. Nenhum texto corrido foi promovido a título sem atender aos 3 critérios.
  3. Não há frases, sentenças ou parágrafos repetidos consecutivamente na saída final.
  4. Ordem, formatação e hierarquia estão fiéis ao original.
  5. Se a página não contiver elementos estruturais, extraia todo o texto como parágrafos Markdown.
  6. Se absolutamente nada for detectado, retorne apenas: `aaaaa`

## ETAPA 7: LOGGING E CONTINUIDADE
- Se uma repetição crítica for detectada e removida, registre internamente (log) a ocorrência para auditoria e melhoria contínua.
- Após a limpeza, continue normalmente a conversão das próximas páginas, sem interromper o fluxo.

# EXEMPLOS DE CASOS COMUNS

## Exemplo de repetição a remover:
Página:
"sem aplicação de questionários, grupos focal ou outras formas de coleta dirigida de dados, sem aplicação de questionários, grupos focal ou outras formas de coleta dirigida de dados, ..."
→ Markdown:
"sem aplicação de questionários, grupos focal ou outras formas de coleta dirigida de dados, ..."

## Exemplo Negativo (texto corrido no início):
Página:
"O objetivo deste trabalho é apresentar..."
→ Markdown:
O objetivo deste trabalho é apresentar...

## Exemplo Positivo (título real):
Página:
[Centralizado, grande, negrito]
"2. Metodologia"
→ Markdown:
## 2. Metodologia

## Exemplo de header/footer a ignorar:
Página:
[Topo] "Manual Técnico" [Rodapé] "Página 12"
→ Markdown:
[Não transcrever nada desses elementos]

# REGRAS GERAIS
- Não omita, resuma ou modifique nenhum conteúdo do corpo principal.
- Mantenha a ordem, posicionamento e formatação exatos de todos os elementos.
- O resultado deve ser apenas o conteúdo Markdown convertido, sem explicações extras, comentários ou outputs duplicados.

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
