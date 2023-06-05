### PGC_Chord

Convergência no protocolo Chord utilizando o simulador PeerSim.

### Como usar

Utilizar arquivo de configuração, conforme especificação do PeerSim.

### Geração de dados

**Arquivo de dados**

O script verifica as pastas com os nomes {"1000","10000","100000","1000000"} e gera um arquivo de dados para cada pasta.

```bash
python statistics_std.py
```

**Geração de gráficos**

O script verifica os arquivo de dados gerado no passo anterior e cria um gráfico para cada arquivo de dados.

```bash
# Exemplo sem desvio padrao
python gen.py
# Exemplo com desvio padrao
python gen.py e
```