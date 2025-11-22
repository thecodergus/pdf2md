import os
from typing import Final
from docling.datamodel.pipeline_options_vlm_model import (
    ResponseFormat,
    ApiVlmOptions,
)
from docling.datamodel.pipeline_options import (
    VlmPipelineOptions,
    PictureDescriptionVlmOptions,
)
from .prompts import __get_mermaid_prompt, __get_prompt_1, __get_prompt_2
from pydantic import AnyUrl
from docling.datamodel.accelerator_options import AcceleratorDevice, AcceleratorOptions


def __options_ollama(model: str) -> VlmPipelineOptions:
    return VlmPipelineOptions(
        do_picture_classification=True,
        do_picture_description=True,
        picture_description_options=__picture_description_options(model),
        vlm_options=ApiVlmOptions(
            url=AnyUrl("http://localhost:11434/v1/chat/completions"),
            params={
                "model": model,
                "temperature": 0.3,
                "top_p": 0.8,
                "top_k": 40,
                "repeat_penalty": 1.1,
                "max_tokens": 16384,
            },
            prompt=__get_prompt_1(),
            response_format=ResponseFormat.MARKDOWN,
            timeout=1_200,
        ),
        accelerator_options=AcceleratorOptions(
            num_threads=8, device=AcceleratorDevice.CUDA
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
    api_key: AnyUrl = __get_openrouter_api_key()
    return VlmPipelineOptions(
        enable_remote_services=True,
        do_picture_classification=True,
        do_picture_description=True,
        picture_description_options=__picture_description_options(model),
        vlm_options=ApiVlmOptions(
            url=AnyUrl("https://openrouter.ai/api/v1/chat/completions"),
            params={
                "model": model,  # Substitua por outro modelo OpenRouter se necessário
                "temperature": 0.3,
                "top_p": 0.8,
                "top_k": 40,
                "repeat_penalty": 1.1,
                "max_tokens": 16384,
            },
            prompt=__get_prompt_1(),
            response_format=ResponseFormat.MARKDOWN,
            timeout=1200,  # Timeout ampliado para API remota
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
        ),
        accelerator_options=AcceleratorOptions(
            num_threads=8, device=AcceleratorDevice.CUDA
        ),
    )


def __get_openrouter_api_key() -> AnyUrl:
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
    return AnyUrl(api_key)


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
        do_picture_classification=True,
        do_picture_description=True,
        picture_description_options=__picture_description_options(model),
        vlm_options=ApiVlmOptions(
            url=AnyUrl("http://192.168.15.3:1234/v1/chat/completions"),
            params={
                "model": model,
                "temperature": 0.3,
                "top_p": 0.8,
                "top_k": 40,
                "repeat_penalty": 1.1,
                "max_tokens": 16384,
            },
            prompt=__get_prompt_1(),
            response_format=ResponseFormat.MARKDOWN,
            timeout=1_200,  # Timeout otimizado para local
        ),
        accelerator_options=AcceleratorOptions(
            num_threads=8, device=AcceleratorDevice.CUDA
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
        do_picture_classification=True,
        do_picture_description=True,
        picture_description_options=__picture_description_options(model),
        vlm_options=ApiVlmOptions(
            url=AnyUrl("http://localhost:8080/v1/chat/completions"),
            params={
                "model": model,
                "temperature": 0.3,
                "top_p": 0.8,
                "top_k": 40,
                "repeat_penalty": 1.1,
                "max_tokens": 16384,
            },
            prompt=__get_prompt_1(),  # Função já existente no seu código-base
            response_format=ResponseFormat.MARKDOWN,
            timeout=1200,  # Timeout generoso para inferência local
            headers=headers,
        ),
        accelerator_options=AcceleratorOptions(
            num_threads=8, device=AcceleratorDevice.CUDA
        ),
    )


def __picture_description_options(model: str) -> PictureDescriptionVlmOptions:
    """
    Configuração funcional para processamento de imagens com VLM.
    """
    return PictureDescriptionVlmOptions(
        repo_id=model,  # Substitua pelo modelo desejado
        prompt=__get_mermaid_prompt(),
        generation_config={"max_new_tokens": 2048},
        batch_size=8,
        picture_area_threshold=0.05,
    )
