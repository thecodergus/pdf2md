Abstracções e Tecnologias Computacionais

A civilização avança ampliando o número de operações importantes que podem ser realizadas sem se pensar nelas. Alfred North Whitehead Uma Introdução à Matemática, 1911

1.1 Introdução 1.2 Oito grandes ideias sobre arquitetura de computadores 1.3 Por trás do programa 1.4 Sob as tampas 1.5 Tecnologias para a montagem de processadores e memória 1.6 Desempenho 1.7 A barreira da potência 1.8 Mudança de mares: Passando de processadores para multiprocessadores 1.9 Vida real: Fabricação e benchmarking do Intel Core i7 1.10 Falácias e armadilhas 1.11 Comentários finais 1.12 Exercícios

# 1.1. Introdução

Bem-vindo a este livro! Estamos felizes por ter a oportunidade de compartilhar o entusiasmo do mundo dos sistemas computacionais. Esse não é um campo árido e monótono, no qual o progresso é glacial e as novas ideias se atrofiam pelo esquecimento. Não! Os computadores são o produto da impressionante e vibrante indústria da tecnologia da informação, cujos aspectos são responsáveis por quase 10% do produto interno bruto dos Estados Unidos, e cuja economia em parte tornou-se dependente dos rápidos avanços na tecnologia da informação, prometidos pela Lei de Moore. Essa área incomum abraca a inovação com uma velocidade surpreendente. Nos últimos 30 anos, surgiram inúmeros novos computadores que prometiam revolucionar a indústria da computação; essas revoluções foram interrompidas porque alguém sempre construía um computador ainda melhor.

Essa corrida para inovar levou a um progresso sem precedentes desde o início da computação eletrônica no final da década de 1940. Se o setor dos transportes, por exemplo, tivesse tidido o mesmo desenvolvimento da indústria da computação, hoje nós poderíamos viajar de Nova York até Londres em aproximadamente um segundo por apenas alguns centavos. Imagine, por alguns instantes, como esse progresso mudaria a sociedade – morar no Taiti e trabalhar em São Francisco, indo para Moscou no início da noite a fim de assistir a uma apresentação do balé de Bolshoi. Não é difícil imaginar as implicações dessa mudança.

Os computadores levaram a humanidade a enfrentar um a terceira revolução, a revolução da informação, que assumiu seu lugar junto das revoluções industrial e agrícola. A multiplicação da força e do alcance intelectual do ser humano naturalmente afetou muito nossas vidas cotidianas, além de ter mudado a maneira como conduzimos a busca de novos conhecimentos. Agora, existe uma nova via de investigação científica, com a ciência da computação unindo os cientistas teóricos e experimentais na exploração de novas fronteiras na astronomia, biologia, química, física etc.

A revolução dos computadores continua. Cada vez que o custo da computação melhora por um fator de 10, as oportunidades para os computadores se multiplicam. As aplicações que eram economicamente proibitivas, de repente se tornam viáveis. As seguintes aplicações, em um passado recente, eram “ficção científica para a computação”:

- Computação em automóveis: até os microprocessadores melhorarem

### Classes de aplicações de computador e suas características

Embora um conjunto comum de tecnologias de hardware (discutidas nas Seções 1.4 e 1.5) seja usado em computadores, variando dos dispositivos domésticos inteligentes e telefones celulares aos maiores supercomputadores, essas diferentes aplicações possuem diferentes necessidades de projeto e empregam os

fundamentos das tecnologias de hardware de diversas maneiras. Genericamente falando, os computadores são usados em três diferentes classes de aplicações.

Os **computadores desktop (PCs)** são possivelmente os modelos mais conhecidos de computação e caracterizam-se pelo computador pessoal, que a maioria dos leitores deste livro provavelmente já usou extensivamente. Os computadores desktop enfatizam o bom desempenho a um único usuário por um baixo custo e normalmente são usados para executar software independente. A evolução de muitas tecnologias de computação é motivada por essa classe da computação, que só tem cerca de 35 anos!

**computadores desktop** Um computador projetado para uso por uma única pessoa, normalmente incorporando um monitor gráfico, um teclado e um mouse.

Os **servidores** são a forma moderna do que, antes, eram computadores muito maiores, e, em geral, são acessados apenas por meio de uma rede. Os servidores são projetados para suportar grandes cargas de trabalho, que podem consistir em uma única aplicação complexa, normalmente científica ou de engenharia, ou manipular muitas tarefas pequenas, como ocorreria no caso de um grande servidor Web. Essas aplicações muitas vezes são baseadas em software de outra origem (como um banco de dados ou sistema de simulação), mas, frequentemente, são modificadas ou personalizadas para uma função específica. Os servidores são construídos a partir da mesma tecnologia básica dos computadores desktop, mas fornecem uma maior capacidade de expansão, tanto da capacidade de processamento quanto de entrada/saída. Em geral, os servidores também não têm grande ênfase à estabilidade, já que uma falha normalmente é mais prejudicial do que seria em um computador desktop de um único usuário.

**servidor** Um computador usado para executar grandes programas para múltiplos usuários, quase sempre de maneira simultânea e normalmente acessado apenas por meio de uma rede.

Os servidores abrangem a faixa mais ampla em termos de custo e capacidade.

Na sua forma mais simples, um servidor pode ser pouco mais do que o que uma máquina desktop sem monitor ou teclado e com um custo de mil dólares. Esses servidores de baixa capacidade normalmente são usados para armazenamento de arquivos, pequenas aplicações comerciais ou serviço Web simples (Secção 6.10). No outro extremo, está o **supercomputadores** , que, atualmente, consistem em dezenas de milhares de processadores e, em geral, de terabytes de memória, e custam desde dezenas até centenas de milhões de dólares. Os supercomputadores normalmente são usados para cálculos científicos e de engenharia de alta capacidade, como previsão do tempo, exploração de petróleo, determinação da estrutura da proteína e outros problemas de grande porte. Embora esses supercomputadores representem o máximo da capacidade de computação, eles são uma fração relativamente pequena dos servidores e do mercado de computadores em termos de receita total.

## supercomputador

Uma classe de computadores com desempenho e custo mais altos; eles são configurados como servidores e normalmente custam de dezenas a centenas de milhões de dólares.

## terabyte (TB)

Originalmente, 1.099.511.627.776 (2⁴⁰) bytes, embora alguns desenvolvedores de sistemas de comunicações e de armazenamento secundário o tenham redefinido como significando 1.000.000.000.000 (10¹²) bytes. Para diminuir a confusão, agora usamos o termo tebibyte ('TiB') para 2⁴⁰ bytes, definindo terabyte (TB) para indicar 10¹² bytes. A Figura 1.1 mostra a faixa completa de valores decimais e binários, com seus nomes.

FIGURA 1.1 A ambiguidade 2ˣ versus 10ʸ bytes foi resolvida acrescentando-se uma notação binária para todos os termos de tamanho comuns.

Na última coluna, observamos como o termo binário é maior do que seu correspondente decimal, o que é visto quando descemos na tabela. Esses prefixos funcionam para bits e também como bytes, portanto gigabit (Gb) é 10⁹ bits, enquanto gibibits (Gib) é 2³⁰ bits.

Os computadores embutidos são a maior classe de computadores e abrangem a faixa mais ampla de aplicações e desempenho. Os computadores embutidos incluem os microprocessadores encontrados em seu carro, os computadores em um aparelho de televisão digital, e as redes de processadores que controlam um avião moderno ou um navio de carga. Os sistemas de computação embutidos são projetados para executar uma aplicação ou um conjunto de aplicações relacionadas como um único sistema; portanto, apesar do grande número de computadores embutidos, a maioria dos usuários nunca vê realmente que está usando um computador!

computador embutido

Um computador dentro de outro dispositivo, usado para executar uma aplicação predeterminada ou um conjunto de softwares.

As aplicações embutidas normalmente possuem necessidades específicas que combinam um desempenho mínimo com limitações rígidas em relação a custo ou potência. Por exemplo, considere um telefone celular: o processador só precisa ser tão rápido quanto o necessário para manipular sua função limitada;

Detalhamento os detalhamentos são seções curtas usadas em todo o texto para fornecer mais detalhes sobre um determinado assunto, que pode ser de interesse. Os leitores que não possuem um interesse específico no tema podem pular essas seções, já que o material subseqüente nunca dependerá do conteúdo desta seção.

Muitos processadores embutidos são projetados usando núcleos de processador, uma versão de um processador escrita em uma linguagem de descrição de hardware como Verilog ou VHDL (Capítulo 4). O núcleo permite que um projetista integre outro hardware específico de uma aplicação com o núcleo do processador para a fabricação em um único chip.

Bem-vindo à era pós-PC O andar contínuo da tecnologia ocasiona mudanças de geração no hardware de computador que agita todo o setor de tecnologia da informação. Desde a última edição do livro, passamos por essa mudança, tão significativa no passado quanto a mudança que começou há 30 anos com os computadores pessoais. O PC está sendo substituído pelo dispositivo móvel pessoal (PMD — Personal Mobile Device). PMDs operam com bateria, com conectividade sem fios com a Internet, e normalmente custam centenas de dólares; como os PCs, os usuários podem baixar software (“apps”) para serem executados meles. Ao contrário dos PCs, eles não possuem mais um teclado e mouse, e provavelmente utilizam uma tela sensível ao toque ou até mesmo entrada de voz. O PMD de hoje é um

smartphone ou um computador tablet, mas amanhã poderá incluir óculos eletrônicos. A Figura 1.2 mostra o rápido crescimento dos tablets e smartphones em comparação ao dos PCs e telefones celulares tradicionais.

FIGURA 1.2 O número de tablets e smartphones fabricados por ano, refletindo a era pós-PC, contra os computadores pessoais e telefones celulares tradicionais. Smartphones representam o crescimento recente no setor de telefone celular, e ultrapassaram os PCs em 2011. Os tablets são a categoria com crescimento mais rápido, quase dobro entre 2011 e 2012. Recentemente, as categorias de PCs e telefones celulares tradicionais estão relativamente planas ou em declínio.

## Personal Mobile Devices (PMDs)

são pequenos dispositivos sem fio para realizar a conexão com a Internet; eles utilizam baterias para gerar energia e o software é instalado baixando aplicativos. Alguns exemplos comuns são smartphones e tablets. Apoderando-se do servidor tradicional está a computação em nuvem, que conta com gigantes centros de dados, conhecidos como Computadores em nuvem

# Escala de Warehouse (WSCs — Warehouse Scale Computadores)

Empresas como Amazon e Google montam esses WSCs contendo 100.000 servidores e depois permitem que as empresas aluguem partes deles para que possam oferecer serviços de software para DMPs, sem a necessidade de montar WSCs próprios. Em vez disso, o Software as a Service (SaaS) implementado por meio da nuvem está revolucionando o setor de hardware, assim como DMPs e WSCs estão revolucionando o setor de hardware.

## Computação em nuvem

se refere a um grande conjunto de servidores que prestam serviço através da Internet. Alguns provedores fornecem um número dinâmico variante de servidores como um serviço.

### Software as a Service (SaaS)

oferece software e dados como um serviço pela Internet, normalmente através de um programa magro, como um navegador, que roda em dispositivos clientes locais, em vez de um código binário que precisa ser instalado e executado totalmente nesse dispositivo. Alguns exemplos são a busca na Web e as redes sociais.

O que você pode aprender neste livro Os bons programadores sempre se preocuparam com o desempenho de seus programas porque geram resultados rapidamente para o usuário e é uma condição essencial na criação bem-sucedida de software. Nas décadas de 1960 e 1970, uma grande limitação no desempenho dos computadores era o tamanho da memória do computador. Assim, os programadores em geral seguiam um princípio simples: minimizar o espaço ocupado na memória para tornar os programas mais rápidos. Na última década, os avanços em arquitetura de computadores e nas tecnologias de fabricação de memórias reduziram drasticamente a importância do tamanho da memória na maioria das aplicações, com exceção dos sistemas embutidos.

Agora, os programadores interessados em desempenho precisam entender os problemas que substituíram o modelo de memória simples dos anos de 1960: a

natureza paralela dos processadores e a natureza hierárquica das memórias. Além do mais, conforme explicamos na Seção 1.7, os programadores de hoje precisam se preocupar com a eficiência em termos de consumo de energia dos seus programas rodando ou no PMD ou na nuvem, o que também requer conhecer o que está por trás do seu código. Os programadores que desejam construir versões competitivas do software precisarão, portanto, aumentar seu conhecimento em organização de computadores.

Sentimo-nos honrados com a oportunidade de explicar o que existe dentro da máquina revolucionária, decifrar o software por trás do seu programa e o hardware sob a tampa do seu computador. Ao concluir este livro, acreditamos que você será capaz de responder às seguintes perguntas:

- Como os programas escritos em uma linguagem de alto nível, como C ou Java, são traduzidos para a língua de máquina e como o hardware executa os programas resultantes? Compreender esses conceitos forma o alicerce para entender os aspectos do hardware e software que afetam o desempenho dos programas.
- O que é a interface entre o software e o hardware, e como o software instrui o hardware a realizar as funções necessárias? Esses conceitos são vitais para entender como escrever muitos tipos de software.
- O que determina o desempenho de um programa e como um programador pode melhorar o desempenho? Como veremos, isso depende do programa original, da tradução desse programa para a língua do computador e da eficiência do hardware em executar o programa.
- Que técnicas podem ser usadas pelos projetistas de hardware para melhorar o desempenho? Este livro apresentará os conceitos básicos do projeto de computador moderno. O leitor interessado encontrará muito mais material sobre esse assunto em nosso livro avançado, Arquitetura de Computadores: Uma abordagem quantitativa.
- Que técnicas podem ser usadas pelos projetistas de hardware para aumentar a economia de energia? O que o programador pode fazer para ajudar ou impedir esse processo?
- Quais são os motivos e as consequências da mudança recente do processamento sequencial para o processamento paralelo? Este livro oferece a motivação, descreve os mecanismos de hardware atual para dar suporte ao paralelismo e estuda a nova geração de microprocessadores “multicore” (Capítulo 6).
- Desde o primeiro computador comercial em 1951, que grandes ideias os

O arquitetos de computador tiveram para estabelecer a base da computação moderna?

Um microprocessador contendo múltiplos processadores ("cores" ou núcleos) em um único circuito integrado.

Sem entender as respostas a essas perguntas, melhorar o desempenho do seu programa em um computador moderno ou avaliar quais recursos podem tornar um computador melhor do que outro para uma determinada aplicação será um complicado processo de tentativa e erro, em vez de um procedimento científico conduzido por consciência e análise.

Este primeiro capítulo é o é base para o resto do livro. Ele apresenta as ideias e definições básicas, coloca os principais componentes de software e hardware em perspectiva, mostra como avaliar o desempenho e a potência, apresenta os circuitos integrados, tecnologia que estimulou a revolução dos computadores, e explica a mudança para as núcleos múltiplos (multicore).

microprocessador multicore Um microprocessador contendo múltiplos processadores ("cores" ou núcleos) em um único circuito integrado.

Sem entender as respostas a essas perguntas, melhorar o desempenho do seu programa em um computador moderno ou avaliar quais recursos podem tornar um computador melhor do que outro para uma determinada aplicação será um complicado processo de tentativa e erro, em vez de um procedimento científico conduzido por consciência e análise.

Este primeiro capítulo é o é base para o resto do livro. Ele apresenta as ideias e definições básicas, coloca os principais componentes de software e hardware em perspectiva, mostra como avaliar o desempenho e a potência, apresenta os circuitos integrados, tecnologia que estimulou a revolução dos computadores, e explica a mudança para as núcleos múltiplos (multicore).

Acrônimo Uma palavra construída tomando-se as letras iniciais das palavras. Por exemplo: RAM é um acrônimo para Random Access Memory (memória de acesso aleatório) e CPU é um acrônimo para Central Processing Unit (Unidade central de Processamento). Acrônimo Uma palavra construída tomando-se as letras iniciais das palavras. Por exemplo: RAM é um acrônimo para Random Access Memory (memória de acesso aleatório) e CPU é um acrônimo para Central Processing Unit (Unidade central de Processamento).

Entendendo o desempenho dos programas

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

# Na categoria de otimização da hierarquia de memória, no Capítulo 5, usamos o bloqueio de cache para aumentar o desempenho em grandes matrizes por outro fator de 2,5.

- Na categoria de paralelismo em nível de thread, no Capítulo 6, usamos loops for paralelos no OpenMP para explorar o hardware multicore a fim de aumentar o desempenho por outro fator de 14.

## Verifique você mesmo

As Seções “Verifique você mesmo” destinam-se à ajudar os leitores a avaliar se compreenderam os principais conceitos apresentados em um capítulo e se entenderam as implicações desses conceitos. Algumas questões “Verifique você mesmo” possuem respostas simples; outras são para discussão em grupo. As respostas às questões específicas podem ser encontradas no final do capítulo. As questões “Verifique você mesmo” aparecem apenas no final de uma seção, fazendo com que fique mais fácil pulá-las se você estiver certo de que entendeu o assunto.

1. O número de processadores embutidos vendidos a cada ano supera, e muito, o número de processadores para PC e até mesmo pós-PC. Você pode confirmar ou negar isso com base em sua própria experiência? Tente contar o número de processadores embutidos na sua casa. Compare esse número com o número de computadores convencionais em sua casa.
2. Como mencionado anteriormente, tanto o software quanto o hardware afetam o desempenho de um programa. Você pode pensar em exemplo nos quais cada um dos fatores a seguir é o responsável pelo gargalo no desempenho?

- O algoritmo escolhido
- A linguagem de programação ou compilador
- O sistema operacional
- O processador
- O sistema de E/S e os dispositivos

