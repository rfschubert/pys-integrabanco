# pys-integrabanco

SDK para integração de arquivos bancários, normalmente nos padrões `CNAB`

### Como instalar

```shell
$ pip install pysintegrabanco
```

### Como usar

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