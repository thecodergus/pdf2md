# Abstrações e Tecnologias Computacionais

A civilização avança ampliando o número de operações importantes que podem ser realizadas sem se pensar nelas.

*Alfred North Whitehead Uma Introdução à Matemática, 1911*

1.1 Introdução 1.2 Oito grandes ideias sobre arquitetura de computadores 1.3 Por trás do programa 1.4 Sob as tampas 1.5 Tecnologias para a montagem de processadores e memória 1.6 Desempenho 1.7 A barreira da potência 1.8 Mudança de mares: Passando de processadores para multiprocessadores 1.9 Vida real: Fabricação e benchmarking do Intel Core i7 1.10 Falácias e armadilhas 1.11 Comentários finais 1.12 Exercícios

# 1.1. Introdução

Bem-vindo a este livro! Estamos felizes por ter a oportunidade de compartilhar o entusiasmo do mundo dos sistemas computacionais. Esse não é um campo árido e monótono, no qual o progresso é glacial e as novas ideias se atrofiam pelo esquecimento. Não! Os computadores são o produto da impressionante e vibrante indústria da tecnologia da informação, cujos aspectos são responsáveis por quase 10% do produto interno bruto dos Estados Unidos, e cuja economia em parte tornou-se dependente dos rápidos avanços na tecnologia da informação, prometidos pela Lei de Moore. Essa área incomum abraça a inovação com uma velocidade surpreendente. Nos últimos 30 anos, surgiram inúmeros novos computadores que prometiam revolucionar a indústria da computação; essas revoluções foram interrompidas porque alguém sempre construía um computador ainda melhor.

Essa corrida para inovar levou a um progresso sem precedentes desde o início da computação eletrônica no final da década de 1940. Se o setor de transportes, por exemplo, tivesse tido o mesmo desenvolvimento da indústria da computação, hoje nós poderíamos viajar de Nova York até Londres em aproximadamente um segundo por apenas alguns centavos. Imagine, por alguns instantes, como esse progresso mudaria a sociedade – morar no Taiti e trabalhar em São Francisco, indo para Moscou no início da noite a fim de assistir a uma apresentação do balé de Bolshoi. Não é difícil imaginar as implicações dessa mudança.

Os computadores levaram a humanidade a enfrentar uma terceira revolução, a revolução da informação, que assumiu seu lugar junto das revoluções industrial e agrícola. A multiplicação da força e do alcance intelectual do ser humano naturalmente afetou muito nossas vidas cotidianas, além de ter mudado a maneira como conduzimos a busca de novos conhecimentos. Agora, existe uma nova veia de investigação científica, com a ciência da computação unindo os cientistas teóricos e experimentais na exploração de novas fronteiras na astronomia, biologia, química, física etc.

A revolução dos computadores continua. Cada vez que o custo da computação melhora por um fator de 10, as oportunidades para os computadores se multiplicam. As aplicações que eram economicamente proibitivas, de repente se tornam viáveis. As seguintes aplicações, em um passado recente, eram “ficção científica para a computação”:

- Computação em automóveis: até os microprocessadores melhorarem

significativamente de preço e desempenho no início dos anos 80, o controle dos carros por computadores era considerado um absurdo. Hoje, os computadores reduzem a poluição e melhoram a eficiência do combustível, usando controles no motor, além de aumentarem a segurança por meio da prevenção de derrapagens perigosas e pela ativação de air-bags para proteger os passageiros em caso de colisão.

- Telefones celulares: quem sonharia que os avanços dos sistemas computacionais levariam aos telefones portáteis, permitindo a comunicação entre pessoas em quase todo lugar do mundo?
- Projeto do genoma humano: o custo do equipamento computacional para mapear e analisar as sequências do DNA humano é de centenas de milhões de dólares. É improvável que alguém teria considerado esse projeto se os custos computacionais fossem 10 a 100 vezes mais altos, como há 15 ou 25 anos. Além do mais, os custos continuam a cair; você poderá adquirir seu próprio genoma, permitindo que a assistência médica seja ajustada a você mesmo.
- World Wide Web: ainda não existe na época da primeira edição deste livro, a World Wide Web transformou nossa sociedade. Para muitos, a Web substituiu as bibliotecas e os jornais.
- Motores de busca: à medida que o conteúdo da Web crescia em tamanho e em valor, encontrar informações relevantes tornou-se cada vez mais importante. Hoje, muitas pessoas contam com ferramentas de busca para tantas coisas em suas vidas que seria muito difícil viver sem elas.

Claramente, os avanços dessa tecnologia hoje afetam quase todos os aspectos da nossa sociedade. Os avanços de hardware permitiram que os programadores criassem softwares maravilhosamente úteis e explicassem por que os computadores são onipresentes. A ficção científica de hoje sugere as aplicações que fazem sucesso amanhã: já a caminho estão os mundos virtuais, a sociedade sem dinheiro em espécie e carros que podem dirigir sem auxílio humano.

# Classes de aplicações de computador e suas características

Embora um conjunto comum de tecnologias de hardware (discutidas nas Seções 1.4 e 1.5) seja usado em computadores, variando dos dispositivos domésticos inteligentes e telefones celulares aos maiores supercomputadores, essas diferentes aplicações possuem diferentes necessidades de projeto e empregam os

fundamentos das tecnologias de diversas maneiras. Genericamente, os computadores são usados em três diferentes classes.

Os computadores desktop (PCs) são possivelmente os modelos mais conhecidos de computação, que a maioria dos leitores já usou extensivamente. Os computadores desktop enfatizam o bom desempenho por um baixo custo e normalmente são usados para executar software de computação, que só tem cerca de 35 anos!

## computadores desktop

Um computador projetado para uso por uma única pessoa, normalmente incorporando um monitor e um mouse.

Os servidores são computadores muito maiores, e, em geral, são acessados por meio de uma rede. Os servidores são projetados para suportar grandes cargas de trabalho, como uma única aplicação complexa, ou manipular muitas tarefas de engenharia, mas frequentemente são modificados para uma função específica, como um banco de dados ou um sistema de simulação. Em geral, os servidores são construídos com uma grande capacidade de processamento, mas também fornecem uma grande capacidade de entrada/saída. Em geral, os servidores são construídos com uma grande capacidade de processamento, mas também fornecem uma grande capacidade de entrada/saída.

## servidor

Um computador usado para executar grandes programas, quase sempre acessado por uma rede.

Na sua forma mais simples, um servidor pode ser pouco mais do que uma máquina desktop sem monitor ou teclado e com um custo de mil dólares. Esses servidores de baixa capacidade normalmente são usados para armazenamento de arquivos, pequenas aplicações comerciais ou serviço Web simples (Seção 6.10). No outro extremo, estão os supercomputadores, que, atualmente, consistem em dezenas de milhares de processadores e, em geral, de terabytes de memória, e custam desde dezenas até centenas de milhões de dólares. Os supercomputadores normalmente são usados para cálculos científicos e de engenharia de alta capacidade, como previsão do tempo, exploração de petróleo, determinação da estrutura da proteína e outros problemas de grande porte. Embora esses supercomputadores representem o máximo da capacidade de computação, eles são uma fração relativamente pequena dos servidores e do mercado de computadores em termos de receita total.

## supercomputador

Uma classe de computadores com desempenho e custo mais altos; eles são configurados como servidores e normalmente custam de dezenas a centenas de milhões de dólares.

## terabyte (TB)

Originalmente, 1.099.511.627.776 ($2^{40}$) bytes, embora alguns desenvolvedores de sistemas de comunicações e de armazenamento secundário o tenham redefinido como significando 1.000.000.000.000 ($10^{12}$) bytes. Para diminuir a confusão, agora usamos o termo tebibyte (TiB) para $2^{40}$ bytes, definindo terabyte (TB) para indicar $10^{12}$ bytes. A Figura 1.1 mostra a faixa completa de valores decimais e binários, com seus nomes.

| Termo decimal   | Abreviação   | Valor     | Termo binário   | Abreviação   | Valor    | % maior   |
|-----------------|--------------|-----------|-----------------|--------------|----------|-----------|
| kilobyte        | KB           | $10^3$    | kibibyte        | KiB          | $2^{10}$ | 2%        |
| megabyte        | MB           | $10^6$    | mebibyte        | MiB          | $2^{20}$ | 5%        |
| gigabyte        | GB           | $10^9$    | gibibyte        | GiB          | $2^{30}$ | 7%        |
| terabyte        | TB           | $10^{12}$ | tebibyte        | TiB          | $2^{40}$ | 10%       |
| petabyte        | PB           | $10^{15}$ | pebibyte        | PiB          | $2^{50}$ | 13%       |
| exabyte         | EB           | $10^{18}$ | exbibyte        | EiB          | $2^{60}$ | 15%       |
| zettabyte       | ZB           | $10^{21}$ | zebibyte        | ZiB          | $2^{70}$ | 18%       |
| yottabyte       | YB           | $10^{24}$ | yobibyte        | YiB          | $2^{80}$ | 21%       |

**FIGURA 1.1** A ambiguidade $2^x$ versus $10^y$ bytes foi resolvida acrescentando-se uma notação binária para todos os termos de tamanho comuns. Na última coluna, observamos como o termo binário é maior do que seu correspondente decimal, o que é visto quando descemos na tabela. Esses prefixos funcionam para bits e também como bytes, portanto gigabit (Gb) é $10^9$ bits, enquanto gibibits (Gib) é $2^{30}$ bits.

Os computadores embutidos são a maior classe de computadores e abrangem a faixa mais ampla de aplicações e desempenho. Os computadores embutidos incluem os microprocessadores encontrados em seu carro, os computadores em um aparelho de televisão digital, e as redes de processadores que controlam um avião moderno ou um navio de carga. Os sistemas de computação embutidos são projetados para executar uma aplicação ou um conjunto de aplicações relacionadas como um único sistema; portanto, apesar do grande número de computadores embutidos, a maioria dos usuários nunca vê realmente que está usando um computador!

### computador embutido

Um computador dentro de outro dispositivo, usado para executar uma aplicação predeterminada ou um conjunto de softwares.

As aplicações embutidas normalmente possuem necessidades específicas que combinam um desempenho mínimo com limitações rígidas em relação a custo ou potência. Por exemplo, considere um telefone celular: o processador só precisa ser tão rápido quanto o necessário para manipular sua função limitada;

além disso, minimizar custo e potência é o objetivo mais importante. Apesar do seu baixo custo, os computadores embutidos podem variar desde um simples televisor falho, até o completo desastre quando o poderia ocorrer em um avião ou em um navio falho. Nas aplicações embutidas ao consumidor, a estabilidade é obtida por meio da simplicidade possível. Nos computadores embutidos, a maioria dos conceitos é obtida diretamente – ou com ligeiras modificações.

### Detalhamento

os detalhamentos são usados em todo o texto para fornecer mais detalhes sobre o tema. Muitos processadores são projetados usando o mesmo núcleo de processador, que pode ser de um único chip. O núcleo permite que um projetista integre outro hardware de uma aplicação com o núcleo do processador em um único chip.

## Bem-vindo à página

O andar da tecnologia de computador tem mudado o mundo. Desde a última edição do livro, passou-se 30 anos com o desenvolvimento de computadores móveis (PMDs). Os PMDs operam com bateria, e normalmente os usuários podem baixar e utilizar apps para serem executados neles. Ao contrário dos PCs, os PMDs são sensíveis ao toque e provavelmente têm uma tela de voz. O PMD de hoje é um dispositivo móvel (personal device).

## Personal Mobile Devices (PMDs)

são pequenos dispositivos com a Internet; eles utilizam baterias para gerar energia e o software é instalado comuns aplicativos. Alguns exemplos são smartphones e tablets.

Apoderando-se do servidor está a computação em nuvem, que conta com centros de dados conhecidos como Computadores em

Escala de Warehouse (WSCs). Empresas como Amazon e Google montam esses WSCs e depois permitem que as empresas aluguem partes deles para que possam oferecer serviços de software, sem a necessidade de montar WSCs próprios. Em vez disso, o Software as a Service (SaaS) implementado por meio da nuvem está revolucionando o setor de software. Os desenvolvedores de software atualmente possuem uma parte de sua aplicação rodando na nuvem.

## Computação em nuvem

se refere a um grande conjunto de servidores que prestam serviços através da Internet, normalmente por meio de um programa que roda em dispositivos clientes, como um navegador, em vez de ser instalado e executado totalmente no dispositivo. Alguns exemplos são fornecidos na Web e as redes sociais.

## Software as a Service (SaaS)

oferece software como um serviço pela Internet, normalmente por meio de um programa que roda em dispositivos clientes, como um navegador, em vez de ser instalado e executado totalmente no dispositivo. Alguns exemplos são fornecidos na Web e as redes sociais.

## O que você pode aprender neste livro

Os bons programadores sempre se preocupam com o desempenho dos programas, pois gerar resultados rapidamente é uma condição essencial. Nas últimas décadas, os programadores em geral se preocuparam com o tamanho da memória ocupada por programas. Na última década, os programadores em geral se preocuparam com o tamanho da memória ocupada por programas. Assim, os avanços em arquitetura de computadores e nas tecnologias de memória reduziram drasticamente o tamanho das aplicações, com exceção dos sistemas embutidos.

Agora, os programadores interessados em entender os problemas que substituíram o modelo de memória dos anos 1960: a

natureza paralela e a natureza hierárquica das memórias. Além do mais, conforme explicamos na Seção 1.7, os programadores de hoje precisam se preocupar com a eficiência em termos de energia dos seus programas rodando no PMD, o que também requer o que está por trás do seu código. Os programadores que desejam construir versões competitivas do software precisam de conhecimento em organização de computadores.

Sentimo-nos honrados com a oportunidade de, dentro da máquina revolucionária, decifrando o que você será capaz de responder às seguintes perguntas:

- Como os programas escritos em uma linguagem de alto nível, como C ou Java, são traduzidos para a linguagem de máquina e como o hardware executa os programas? Compreender esses conceitos é vital para entender como o hardware e o software se comunicam e como o software influencia o desempenho dos programas.
- O que é a interface entre o hardware e o software, e como o software instrui o hardware a realizar as funções necessárias? Esses conceitos são fundamentais para entender como os programas são executados.
- O que determina o desempenho de um programa e como o programador pode melhorar o desempenho do programa? Isso depende do desempenho do hardware e da eficiência do software. Este livro apresentará os conceitos básicos de computadores modernos, e o leitor interessado poderá encontrar mais material sobre esse assunto em nosso livro: *Arquitetura de Computadores: Uma abordagem quantitativa* .
- Que técnicas podem ser usadas pelos projetistas de hardware para aumentar a economia de energia? Este livro oferece os mecanismos de hardware atuais para ajudar a dar suporte ao processamento paralelo e estuda a nova geração de microprocessadores (Capítulo 6).
- Desde o primeiro computador comercial em 1951, que grandes ideias e inovações foram feitas no campo da computação?

arquitetos de computador tiveram para estabelecer a base da computação moderna?

## microprocessador multicore

Um microprocessador contendo múltiplos processadores (“cores” ou núcleos) em um único circuito integrado.

Sem entender as respostas a essas perguntas, melhorar o desempenho do seu programa em um computador moderno ou avaliar quais recursos podem tornar um computador melhor do que outro para uma determinada aplicação será um complicado processo de tentativa e erro, em vez de um procedimento científico conduzido por consciência e análise.

Este primeiro capítulo é a base para o restante do livro. Ele apresenta as ideias e definições básicas, coloca os principais componentes de software e hardware em perspectiva, mostra como avaliar o desempenho e a potência, apresenta os circuitos integrados, a tecnologia que estimula a revolução dos computadores, e explica a mudança para núcleos múltiplos (multicores).

Neste capítulo e em capítulos seguintes, você provavelmente verá muitas palavras novas ou palavras que já pode ter ouvido, mas não sabe ao certo o que significam. Não entre em pânico! Sim, há muita terminologia especial usada para descrever os computadores modernos, mas ela realmente ajuda, uma vez que nos permite descrever precisamente uma função ou capacidade. Além disso, os projetistas de computador (inclusive estes autores) adoram usar acrônimos, que são fáceis de entender quando se sabe o que as letras significam! Para ajudá-lo a lembrar e localizar termos, incluímos na margem uma definição destacada de cada termo novo na primeira vez que aparece no texto. Após um pequeno período trabalhando com a terminologia, você será fluente e seus amigos ficarão impressionados quando você usar corretamente palavras como BIOS, CPU, DIMM, DRAM, PCIe, SATA e muitas outras.

## Acrônimo

Uma palavra construída tomando-se as letras iniciais das palavras. Por exemplo: RAM é um acrônimo para Random Access Memory (memória de acesso aleatório) e CPU é um acrônimo para Central Processing Unit (Unidade Central de Processamento).

Para enfatizar como os sistemas de software e hardware usados para executar um programa irão afetar o desempenho, usamos uma seção especial, "Entendendo o desempenho dos programas", em todo o livro, para resumir importantes conceitos quanto ao desempenho do programa. A primeira aparece a seguir.

## Entendendo o desempenho dos programas

O desempenho de um programa depende de uma combinação entre a eficácia dos algoritmos usados no programa, os sistemas de software usados para criar e traduzir o programa para instruções de máquina e da eficácia do computador em executar essas instruções, que podem incluir operações de entrada/saída (E/S). A tabela a seguir descreve como o hardware e o software afetam o desempenho.

| Componente de hardware ou software                 | Como este componente afeta o desempenho                                                    | Onde este assunto é abordado?   |
|----------------------------------------------------|--------------------------------------------------------------------------------------------|---------------------------------|
| Algoritmo                                          | Determina o número de instruções do código-fonte e o número de operações de E/S realizadas | Outros livros!                  |
| Linguagem de programação, compilador e arquitetura | Determina o número de instruções de máquina para cada instrução em nível de fonte          | Capítulos 2 e 3                 |
| Processador e sistema de memória                   | Determina a velocidade em que as instruções podem ser executadas                           | Capítulos 4, 5 e 6              |
| Sistema de E/S (hardware e sistema operacional)    | Determina a velocidade em que as operações de E/S podem ser executadas                     | Capítulos 4, 5 e 6              |

Para demonstrar o impacto das ideias neste livro, melhoramos o desempenho de um programa em C que multiplica uma matriz por um vetor em uma sequência de capítulos. Cada etapa é baseada no conhecimento de como o hardware subjacente realmente funciona em um microprocessador moderno para melhorar o desempenho por um fator de 200!

- Na categoria de paralelismo em nível de dados, no Capítulo 3, usamos o paralelismo de subword por meio de C intrínseco para aumentar o desempenho por um fator de 3,8.
- Na categoria de paralelismo em nível de instrução, no Capítulo 4, usamos o desdobramento de loop para explorar a questão de instruções múltiplas e hardware de execução fora de ordem para melhorar o desempenho por outro fator de 2,3.

- Na categoria de otimização da hierarquia de memória, no Capítulo 5, usamos o bloco de cache para aumentar o desempenho em grandes matrizes por outro fator de 2,5.
- Na categoria de paralelismo em nível de thread, no Capítulo 6, usamos loops for paralelos no OpenMP para explorar o hardware multicore a fim de aumentar o desempenho por outro fator de 14.

## Verifique você mesmo

As Seções “Verifique você mesmo” destinam-se a ajudar os leitores a avaliar se compreenderam os principais conceitos apresentados em um capítulo e se entenderam as implicações desses conceitos. Algumas questões “Verifique você mesmo” possuem respostas simples; outras são para discussão em grupo. As respostas às questões específicas podem ser encontradas no final do capítulo. As questões “Verifique você mesmo” aparecem apenas no final de uma seção, fazendo com que fique mais fácil pulá-las se você estiver certo de que entendeu o assunto.

1. O número de processadores embutidos vendidos a cada ano supera, e muito, o número de processadores para PC e até mesmo pós-PC. Você pode confirmar ou negar isso com base em sua própria experiência? Tente contar o número de processadores embutidos na sua casa. Compare esse número com o número de computadores convencionais em sua casa.
2. Como mencionado anteriormente, tanto o software quanto o hardware afetam o desempenho de um programa. Você pode pensar em exemplo nos quais cada um dos fatores a seguir é o responsável pelo gargalo no desempenho?
    - O algoritmo escolhido
    - A linguagem de programação ou compilador
    - O sistema operacional
    - O processador
    - O sistema de E/S e os dispositivos

