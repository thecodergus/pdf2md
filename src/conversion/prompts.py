def __get_prompt_1() -> str:
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
  4. Ordem, formatação e hierarquia estão fiéis ao original no formato Markdown (#, ##, ###, ####).
  5. Se a página não contiver elementos estruturais, extraia todo o texto como parágrafos Markdown.
  6. Se absolutamente nada for detectado, retorne apenas: `aaaaa`

## ETAPA 7: LOGGING E CONTINUIDADE
- Se uma repetição crítica for detectada e removida, registre internamente (log) a ocorrência para auditoria e melhoria contínua.
- Após a limpeza, continue normalmente a conversão das próximas páginas, sem interromper o fluxo.

# REGRAS GERAIS
- Não omita, resuma ou modifique nenhum conteúdo do corpo principal.
- Mantenha a ordem, posicionamento e formatação exatos de todos os elementos.
- O resultado deve ser apenas o conteúdo Markdown convertido, sem explicações extras, comentários ou outputs duplicados.

# OUTPUT ESPERADO
Apenas o conteúdo Markdown convertido, sem qualquer texto adicional, introdução ou conclusão.
"""


def __get_prompt_2() -> str:
    return """
# INSTRUÇÃO CRÍTICA
- Analise visualmente e converta este documento para Markdown com FIDELIDADE ABSOLUTA.
- Reconstrua fielmente todos os elementos textuais, preservando rigorosamente a estrutura, hierarquia e cada detalhe do conteúdo original.
- Ignore e NÃO transcreva cabeçalhos e rodapés repetitivos (headers/footers), números de página, títulos de capítulo recorrentes, datas ou qualquer elemento que se repita em múltiplas páginas e não faça parte do conteúdo principal.
- Ignore completamente imagens, gráficos, diagramas e qualquer conteúdo visual. Não transcreva legendas, descrições ou referências a esses elementos.

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
$$\'int_{a}^{b} f(x) dx = F(b) - F(a)$$

# OUTPUT ESPERADO
Apenas o conteúdo Markdown convertido, sem qualquer texto adicional, introdução ou conclusão.
"""


def __get_mermaid_prompt() -> str:
    """
    Prompt otimizado para transcrição de diagramas e gráficos em Mermaid via Docling.
    Baseado em guias técnicos de Mermaid e melhores práticas de prompt engineering para VLMs.
    """
    return (
        "Analise cuidadosamente a imagem fornecida seguindo estas instruções precisas:\n"
        "\n"
        "## IDENTIFICAÇÃO DE DIAGRAMAS RELEVANTES\n"
        "Identifique se a imagem contém um dos seguintes tipos de diagramas ou gráficos técnicos:\n"
        "- Fluxogramas (flowchart): Caixas conectadas por setas, formas geométricas variadas\n"
        "- Diagramas de Sequência: Participantes com linhas verticais e mensagens horizontais\n"
        "- Diagramas de Classe: Caixas retangulares com atributos/métodos e linhas de herança\n"
        "- Diagramas de Estado: Estados como círculos/elipses conectados por transições\n"
        "- Diagramas ER: Entidades retangulares com relacionamentos e cardinalidade\n"
        "- Gráficos de Gantt: Barras horizontais ao longo de timeline\n"
        "- Gráficos de Pizza: Círculo dividido em fatias com rótulos e valores\n"
        "- Gráficos de Barras/Linha (XY Chart): Eixos cartesianos com dados quantitativos\n"
        "- Diagramas Sankey: Fluxos quantitativos entre nós com larguras proporcionais\n"
        "- Timeline: Eventos dispostos cronologicamente\n"
        "- Quadrant Chart: Matriz 2x2 com eixos e quadrantes definidos\n"
        "- Mindmaps: Estrutura hierárquica ramificada de tópicos\n"
        "- Git Graph: Commits, branches e merges em estrutura de árvore\n"
        "\n"
        "## CRITÉRIOS DE FILTRAGEM RIGOROSA\n"
        "IGNORE completamente se a imagem contém apenas:\n"
        "- Logotipos, marcas d'água ou elementos decorativos\n"
        "- Fotografias, ilustrações artísticas ou imagens sem valor informativo\n"
        "- Gráficos sem estrutura clara de nós, conexões ou dados quantitativos\n"
        "- Elementos puramente textuais sem componentes visuais estruturais\n"
        "- Figuras ambíguas ou de qualidade insuficiente para identificação precisa\n"
        "\n"
        "## TRANSCRIÇÃO EM MERMAID\n"
        "Se identificado um diagrama relevante, transcreva fielmente usando a sintaxe Mermaid correta:\n"
        "- Use a palavra-chave apropriada (flowchart, sequenceDiagram, classDiagram, etc.)\n"
        "- Mantenha todos os nós, conexões, rótulos e propriedades visíveis\n"
        "- Escape caracteres especiais usando entidades HTML quando necessário\n"
        "- Garanta sintaxe válida e compatível com renderizadores Mermaid padrão\n"
        "\n"
        "## EXEMPLOS DE SAÍDA ESPERADA\n"
        "\n"
        "Para fluxograma:\n"
        "```mermaid\n"
        "flowchart TD\n"
        "    A[Início] --> B{Decisão}\n"
        "    B -- Sim --> C[Processo]\n"
        "    B -- Não --> D[Alternativo]\n"
        "    C --> E[Fim]\n"
        "    D --> E\n"
        "```\n"
        "\n"
        "Para gráfico de pizza:\n"
        "```mermaid\n"
        "pie\n"
        '    title "Distribuição de Recursos"\n'
        '    "Desenvolvimento" : 40\n'
        '    "Testes" : 30\n'
        '    "Documentação" : 20\n'
        '    "Outros" : 10\n'
        "```\n"
        "\n"
        "Para diagrama de sequência:\n"
        "```mermaid\n"
        "sequenceDiagram\n"
        "    participant Usuario\n"
        "    participant Sistema\n"
        "    Usuario->>Sistema: Requisição\n"
        "    Sistema-->>Usuario: Resposta\n"
        "```\n"
        "\n"
        "## TRATAMENTO DE CASOS ESPECIAIS\n"
        "- Para diagramas híbridos, priorize o tipo estrutural predominante\n"
        "- Em imagens de baixa qualidade, foque nos elementos estruturais visíveis\n"
        "- Para diagramas muito complexos, mantenha a estrutura principal e conexões críticas\n"
        "- Se múltiplos diagramas estão presentes, transcreva apenas o principal/mais relevante\n"
        "\n"
        "## FORMATO DE SAÍDA OBRIGATÓRIO\n"
        "- Responda EXCLUSIVAMENTE com o bloco de código Mermaid delimitado por ```mermaid\n"
        "- NÃO inclua explicações, comentários, legendas ou texto adicional\n"
        "- Se a imagem não contém diagrama relevante, não produza nenhuma saída\n"
        "- Garanta que o código seja sintática e semanticamente válido\n"
        "\n"
        "Proceda com a análise da imagem fornecida."
    )
