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
    return """
# Prompt Definitivo para LLM Multimodal: Conversão de Imagens em Diagramas Mermaid e Tabelas Markdown

**IMPORTANTE:** Analise cuidadosamente a imagem fornecida e siga as instruções abaixo, respondendo exclusivamente em português.

---

## 1. Se a imagem for uma **TABELA** (linhas e colunas de dados organizados):

- Transcreva fielmente como tabela Markdown, preservando cabeçalhos, alinhamento e todos os valores.
- Use pipes (`|`) para separar colunas e hifens (`-`) para a linha de cabeçalho.
- Se uma célula contiver o caractere pipe (`|`), escape usando `&#124;`.
- Para tabelas complexas (células mescladas, múltiplos cabeçalhos), utilize HTML (`<table>`, `<tr>`, `<td>`, `<th>`).

**Exemplo de tabela Markdown:**
```
| Produto     | Preço (R$) | Estoque |
|-------------|------------|---------|
| Notebook X  | 3500.00    | 15      |
| Smartphone Y| 1800.00    | 40      |
| Tablet Z    | 1200.00    | 22      |
```

**Exemplo de tabela complexa em HTML:**
```
<table>
  <tr>
    <th>Produto</th><th>Preço (R$)</th><th>Estoque</th>
  </tr>
  <tr>
    <td rowspan="2">Notebook X</td><td>3500.00</td><td>15</td>
  </tr>
  <tr>
    <td>Promoção</td><td>10</td>
  </tr>
</table>
```

---

## 2. Se a imagem for um **diagrama ou gráfico técnico**, identifique o tipo e transcreva em Mermaid. Use a descrição e o exemplo correspondente:

- **Fluxograma (`flowchart`)**  
  *Modela processos, decisões e fluxos de trabalho com caixas, setas e rótulos.*
  ```
  ```mermaid
  flowchart TD
      Start([Início]) --> Decision{Decisão?}
      Decision -- Sim --> Action1[Executar ação 1]
      Decision -- Não --> Action2[Executar ação 2]
      Action1 --> End([Fim])
      Action2 --> End
  ```
  ```

- **Diagrama de Sequência (`sequenceDiagram`)**  
  *Mostra interações temporais entre entidades, útil para APIs, protocolos e fluxos de eventos.*
  ```
  ```mermaid
  sequenceDiagram
      participant Alice
      participant Bob
      Alice->>Bob: Olá, Bob!
      Bob-->>Alice: Olá, Alice!
  ```
  ```

- **Diagrama de Classe (`classDiagram`)**  
  *Descreve estruturas de sistemas orientados a objetos, incluindo classes, atributos e métodos.*
  ```
  ```mermaid
  classDiagram
      class Pessoa {
          +String nome
          +comprar()
      }
      Pessoa <|-- Cliente
  ```
  ```

- **Diagrama de Estados (`stateDiagram-v2`)**  
  *Mostra estados e transições de sistemas, como máquinas de estados e ciclos de vida.*
  ```
  ```mermaid
  stateDiagram-v2
      [*] --> Estado1
      Estado1 --> Estado2
      Estado2 --> [*]
  ```
  ```

- **Diagrama ER (`erDiagram`)**  
  *Modela entidades e relacionamentos de banco de dados, incluindo atributos e cardinalidade.*
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
  ```

- **Gráfico de Gantt (`gantt`)**  
  *Visualiza cronogramas de projetos, tarefas, prazos e dependências.*
  ```
  ```mermaid
  gantt
      title Projeto Exemplo
      dateFormat  YYYY-MM-DD
      section Planejamento
      Tarefa1 :a1, 2025-01-01, 10d
      Tarefa2 :after a1, 5d
  ```
  ```

- **Gráfico de Pizza (`pie`)**  
  *Mostra proporções de um todo, ideal para distribuição percentual de categorias.*
  ```
  ```mermaid
  pie
      title Consumo de Recursos
      "Processamento" : 45
      "Armazenamento" : 30
      "Rede" : 15
      "Outros" : 10
  ```
  ```

- **Gráfico de Barras/Linha (XY Chart) (`xychart-beta`)**  
  *Exibe dados quantitativos em eixos cartesianos, útil para séries temporais e comparações.*
  ```
  ```mermaid
  xychart-beta
      title Vendas Mensais
      x-axis "Mês" ["Jan", "Fev", "Mar", "Abr"]
      y-axis "Vendas (R$)" 0 --> 1000
      bar Jan : 500
      bar Fev : 700
      line Mar : 600
      line Abr : 900
  ```
  ```

- **Sankey (`sankey-beta`)**  
  *Visualiza fluxos quantitativos entre nós, ideal para análise de processos e distribuição de recursos.*
  ```
  ```mermaid
  sankey-beta
      Ingestão,Limpeza,1000
      Limpeza,Transformação,950
      Transformação,Armazenamento,900
      Transformação,Rejeitados,50
  ```
  ```

- **Timeline (`timeline`)**  
  *Exibe eventos em ordem cronológica, útil para históricos e releases.*
  ```
  ```mermaid
  timeline
      title Histórico de Releases
      section 2024
        2024-12-01 : Release v1.0 - MVP
        2025-01-15 : Release v1.1 - Suporte a Pix
      section 2025
        2025-03-10 : Release v2.0 - Open Banking
        2025-05-05 : Release v2.1 - Correções de Segurança
  ```
  ```

- **Quadrant Chart (`quadrantChart`)**  
  *Classifica entidades em duas dimensões, útil para análise SWOT e priorização de tarefas.*
  ```
  ```mermaid
  quadrantChart
      title Priorização de Iniciativas de IA
      x-axis Baixo Impacto --> Alto Impacto
      y-axis Baixo Esforço --> Alto Esforço
      quadrant 1 Investir
      quadrant 2 Monitorar
      quadrant 3 Reavaliar
      quadrant 4 Descartar
      "Chatbot LLM": [0.8, 0.4]
      "Análise Preditiva": [0.9, 0.7]
      "Automação de Testes": [0.6, 0.3]
      "Reconhecimento de Imagem": [0.7, 0.8]
  ```
  ```

- **Mindmap (`mindmap`)**  
  *Organiza ideias hierarquicamente, ideal para brainstorming e planejamento.*
  ```
  ```mermaid
  mindmap
      root((Ideia Principal))
          Subtópico 1
          Subtópico 2
  ```
  ```

- **Git Graph (`gitGraph`)**  
  *Visualiza fluxos de branches e commits Git, útil para versionamento e onboarding.*
  ```
  ```mermaid
  gitGraph
      commit
      branch develop
      commit
      checkout main
      merge develop
  ```
  ```

- **User Journey (`journey`)**  
  *Mapeia etapas e experiências do usuário, útil em UX e mapeamento de jornadas.*
  ```
  ```mermaid
  journey
      title Jornada do Usuário
      section Planejamento
      Usuário: 5: Planejar
      Usuário: 3: Executar
  ```
  ```

- **C4 Diagram (`C4Context`)**  
  *Descreve arquitetura de software em diferentes níveis de contexto.*
  ```
  ```mermaid
  C4Context
      Person(user, "Usuário")
      System(system, "Sistema")
      user -> system : Usa
  ```
  ```

---

## 3. **Filtragem rigorosa**:

- Ignore completamente imagens que sejam logotipos, marcas d'água, fotografias, ilustrações artísticas, elementos decorativos ou figuras sem valor informativo ou estrutural.
- Ignore gráficos sem estrutura clara de nós, conexões ou dados quantitativos.
- Ignore elementos puramente textuais sem componentes visuais estruturais.
- Ignore figuras ambíguas ou de qualidade insuficiente para identificação precisa.
- Se a imagem não contiver tabela, diagrama ou gráfico relevante, não produza nenhuma saída.

---

## 4. **Formato de saída obrigatório**:

- Responda exclusivamente com o bloco de código Mermaid (delimitado por ```mermaid) ou a tabela Markdown/HTML.
- NÃO inclua explicações, comentários, legendas ou texto adicional.

---

## 5. **Casos especiais**:

- Para diagramas híbridos, priorize o tipo estrutural predominante.
- Em imagens de baixa qualidade, foque nos elementos estruturais visíveis.
- Para múltiplos diagramas ou tabelas, transcreva apenas o principal/mais relevante.

---

## 6. **Checklist de Validação (interno ao modelo):**

- [ ] O output está em português, sem texto extra?
- [ ] O tipo de diagrama/tabela foi corretamente identificado?
- [ ] A sintaxe Mermaid/Markdown/HTML está correta e válida?
- [ ] Não há explicações, comentários ou legendas extras?
- [ ] O conteúdo irrelevante foi filtrado conforme instruções?
- [ ] O output está pronto para integração em documentação técnica auditável?

---

Proceda com a análise da imagem fornecida.
"""
