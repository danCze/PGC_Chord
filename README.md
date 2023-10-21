### PGC_Chord

Projeto de Graduação em Computação pela UFABC sob orientação do Prof. Dr. Vladimir E. M. Rocha

O foco do projeto é analisar a convergência de buscas baseada em saltos no protocolo Chord utilizando o simulador PeerSim. Adaptado de https://peersim.sourceforge.net/code/chord.tar.gz

### Como usar

Utilizar arquivo de configuração, conforme especificação do PeerSim.

### Geração de dados

**Argumentos da linha de comandos**

Todos os scripts utilizam o módulo "argparse" do python. Para verificar possíveis argumentos chamar um script com a opção "-h". Todos os scripts podem ser chamados sem argumentos.

```bash
python <scriptname>.py -h
```

**Arquivo de dados**

O script verifica todos os subdiretórios para o diretório indicado pelo arquivo "keys.cfg" e gera um arquivo de dados (maiores nós e pareto) para cada subdiretório.

```bash
python amount.py
```

**Geração de gráficos**

O script verifica os arquivo de dados gerado no passo anterior e cria dois gráficos (% maiores nós e % pareto) para cada arquivo de dados.

```bash
python gen_charts.py
```

**Demais scripts**

counter.py - mostra a distribuição de simulações por tamanho da árvore de convergência\
getkeys.py - utilitário para ler "keys.cfg"\
high_level.py - tentativa de mostrar uma relação entre ser um nível alto e algum dado\
low_level.py - tentativa de mostrar uma relação entre ser um nível baixo e algum dado\
stats.py - converte os dados gerados por "amount.py" em %\
subpath.py - quantidade de nós com ou sem subcaminhos em cada nível, e total de subcaminhos