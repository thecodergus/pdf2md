
# pdf2md

Conversor robusto, modular e incremental de PDF para Markdown, com chunking, cache persistente, interface Rich e pipeline VLM GraniteDocling. Pronto para retomada automática, uso em GPU (NVidia CUDA recomendado, mas não obrigatório) e automação documental.

---

## Sumário

- [Visão Geral](#visão-geral)
- [Funcionalidades](#funcionalidades)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Uso](#uso)
- [Fluxo de Processamento](#fluxo-de-processamento)
- [Arquitetura Modular](#arquitetura-modular)
- [Dependências](#dependências)
- [FAQ](#faq)
- [Contribuindo](#contribuindo)
- [Licença](#licença)
- [Agradecimentos](#agradecimentos)
- [Links Úteis](#links-úteis)

---

## Visão Geral

O **pdf2md** é uma ferramenta moderna para conversão de arquivos PDF em Markdown, com extração semântica avançada via docling VLM GraniteDocling, chunking incremental, cache persistente e interface CLI elegante baseada em Rich. O pipeline é resiliente a falhas, permite retomada automática e foi projetado para fluxos de trabalho profissionais, pesquisa, automação e integração com IA.

---

## Funcionalidades

- Conversão PDF → Markdown com pipeline VLM GraniteDocling (OCR, tabelas, fórmulas, imagens)
- Chunking incremental: divide PDFs em blocos de 1 páginas para processamento eficiente
- Cache persistente: evita retrabalho e permite retomada automática do ponto de parada
- Interface CLI Rich: barra de progresso visual, sem poluição de prints
- Validação de integridade: detecta PDFs corrompidos antes de processar
- Arquitetura modular: separação clara de responsabilidades, fácil manutenção e extensão
- Pronto para GPU: recomendado uso em máquinas com NVidia CUDA, mas não obrigatório
- Execução moderna com uv: ambiente reprodutível, rápido e seguro

---

## Estrutura do Projeto

```
pdf2md/
├── main.py
├── src/
│   ├── __init__.py
│   ├── cache_manager.py
│   ├── chunking.py
│   ├── conversion.py
│   ├── merge.py
│   ├── types.py
│   ├── ui.py
│   └── validation.py
├── cache/
│   ├── .gitignore
│   └── .gitkeep
├── inputs/
│   └── .gitkeep
├── outputs/
│   └── .gitkeep
├── .python-version
├── .gitignore
├── LICENSE
├── pyproject.toml
└── README.md
```

---

## Pré-requisitos

- **Python 3.13+** (recomendado)
- **uv** (https://github.com/astral-sh/uv) — gerenciador de ambientes ultrarrápido
- **NVidia CUDA** (opcional, recomendado para aceleração VLM/docling)
- **Dependências**: gerenciadas automaticamente via `pyproject.toml` e `uv`

---

## Instalação

1. Instale o [uv](https://github.com/astral-sh/uv):

   ```bash
   pip install uv
   ```

2. Clone o repositório:

   ```bash
   git clone <repository-url>
   cd pdf2md
   ```

3. Instale as dependências:

   ```bash
   uv sync
   ```

> **Dica:** Se você possui GPU NVidia com CUDA, o docling pode usar aceleração para modelos VLM.

---

## Uso

1. Execute o pipeline:

   ```bash
   uv run main.py
   ```

2. Digite o caminho do PDF quando solicitado.

3. O progresso será exibido na interface Rich.

4. O Markdown final será salvo em `outputs/` com o mesmo nome do PDF original.

---

## Fluxo de Processamento

1. **Validação**: Verifica se o PDF existe e está íntegro (PyMuPDF)
2. **Chunking**: Divide o PDF em blocos de 10 páginas, salvos em `cache/`
3. **Cache**: Verifica se cada chunk já foi convertido (diskcache + existência do `.md`)
4. **Conversão**: Converte cada chunk para Markdown usando docling VLM GraniteDocling
5. **Merge**: Junta todos os arquivos Markdown em um único arquivo final
6. **Retomada**: Se interrompido, ao reiniciar, processa apenas os chunks pendentes

---

## Arquitetura Modular

| Módulo                | Responsabilidade                                      |
|-----------------------|------------------------------------------------------|
| `validation.py`       | Validação de integridade do PDF                      |
| `chunking.py`         | Divisão do PDF em chunks                             |
| `cache_manager.py`    | Gerenciamento de cache persistente                   |
| `conversion.py`       | Conversão PDF→Markdown com docling                   |
| `merge.py`            | Merge dos arquivos Markdown                          |
| `ui.py`               | Interface Rich para barra de progresso               |
| `types.py`            | Tipos, dataclasses e aliases                         |
| `main.py`             | Orquestra o pipeline completo                        |

---

## Dependências

As dependências principais estão especificadas no `pyproject.toml`:

- `diskcache >= 5.6.3`
- `docling[vlm] >= 2.62.0`
- `pymupdf >= 1.26.6`
- `rich >= 14.2.0`

---

## FAQ

**O pipeline retoma do ponto de parada?**  
Sim. O sistema de cache persistente garante que, ao reiniciar, apenas os chunks pendentes sejam processados.

**Preciso de GPU NVidia?**  
Não é obrigatório, mas recomendado para aceleração do pipeline VLM/docling.

**Posso usar outros chunk sizes?**  
O padrão é 10 páginas por chunk, mas pode ser ajustado no código.

**O pipeline funciona em Windows, Linux e macOS?**  
Sim, desde que Python 3.13+ e as dependências estejam corretamente instaladas.

---

## Contribuindo

Contribuições são bem-vindas!

1. Fork o repositório
2. Crie uma branch para sua feature ou correção
3. Envie um Pull Request detalhado
4. Adicione testes e documentação para novas funcionalidades

---

## Licença

MIT License. Veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## Agradecimentos

- [Docling](https://github.com/docling-project/docling): Extração semântica e pipeline VLM GraniteDocling
- [PyMuPDF](https://github.com/pymupdf/PyMuPDF): Manipulação e chunking de PDFs
- [Rich](https://github.com/Textualize/rich): Interface CLI elegante
- [DiskCache](https://github.com/grantjenks/python-diskcache): Cache persistente

---

## Links Úteis

- [Documentação Docling](https://docling-project.github.io/docling/)
- [Documentação PyMuPDF](https://pymupdf.readthedocs.io/)
- [Documentação Rich](https://rich.readthedocs.io/)
- [Documentação DiskCache](https://grantjenks.com/docs/diskcache/)
- [uv — Python package manager](https://github.com/astral-sh/uv)
