# pys-integrabanco

SDK para integração de arquivos bancários, normalmente nos padrões `CNAB`

### Como instalar

```shell
$ pip install pysintegrabanco
```

### Como usar BB

```python

from pysintegrabanco.banco_do_brasil import BancoDoBrasil
import os

dirpath = os.getcwd()
endereco = dirpath + '/src/bb_cnab400.ret'

bb = BancoDoBrasil()

# calcula o total de linhas no arquivo
with open(endereco, 'r') as arquivo:
    bb.conta_total_linhas_arquivo(arquivo)

# efetua o processamento
with open(endereco, 'r') as arquivo:
    bb.processa_arquivo(arquivo)


print(bb.TOTAL_LINHAS_ARQUIVO)
# int

print(bb.HEADER)
# dict

print(bb.DETALHES)
# list

print(bb.TRAILLER)
# dict
```

### Como usar Santander

```python
from pysintegrabanco.santander import ProcessaFrancesinha
import os

dirpath = os.getcwd()
arquivo = dirpath + '/src/santander_francesinha_com_liquidacao.txt'

integra = ProcessaFrancesinha()
integra.processa_arquivo(arquivo)

print(integra.BOLETOS)
# [BoletoSantander(...)]

print(integra.TOTAL_BOLETOS)
# 1
```