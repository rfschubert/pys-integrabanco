from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Any

import pendulum


@dataclass
class BoletoSantander:
    nome: str
    seu_numero: str
    nosso_numero: str
    vencimento: datetime
    data_pagamento: datetime
    valor: Decimal
    valor_pago: Decimal
    tarifa: Decimal

    @staticmethod
    def from_dict(obj: Any) -> 'BoletoSantander':
        assert isinstance(obj, dict)
        nome = obj.get("nome")
        seu_numero = obj.get("seu_numero")
        nosso_numero = obj.get("nosso_numero")
        vencimento = obj.get("vencimento")
        data_pagamento = obj.get("data_pagamento")
        valor = obj.get("valor")
        valor_pago = obj.get("valor_pago")
        tarifa = obj.get("tarifa")
        return BoletoSantander(nome, seu_numero, nosso_numero, vencimento, data_pagamento, valor, valor_pago, tarifa)


class ProcessaFrancesinha:
    BOLETOS = []
    LIQUIDACAO_LINHA_INICIAL = 0
    LIQUIDACAO_LINHA_FINAL = 0

    def __repr__(self):
        return "ProcessaFrancesinha::LIQ_LIN_INICIAL {}   LIQ_LIN_FINAL {}".format(
            self.LIQUIDACAO_LINHA_INICIAL,
            self.LIQUIDACAO_LINHA_FINAL
        )

    def processa_arquivo(self, endereco):
        with open(endereco, 'r') as f:
            for line_number, line in enumerate(f, 1):
                self.set_linha_inicial_boletos(line, line_number)
                self.set_linha_final_boletos(line, line_number)

        print("LINHA INICIAL = ", self.LIQUIDACAO_LINHA_INICIAL)
        print("LINHA FINAL   = ", self.LIQUIDACAO_LINHA_FINAL)

        with open(endereco, 'r') as f:
            for line_number, line in enumerate(f, 1):
                self.parse_linha_para_boleto(line, line_number)

        return self

    def set_linha_final_boletos(self, linha, linha_numero):
        if self.LIQUIDACAO_LINHA_INICIAL != 0:
            if linha_numero > self.LIQUIDACAO_LINHA_INICIAL and "TOTAL " in linha:
                self.LIQUIDACAO_LINHA_FINAL = linha_numero

        return self

    def set_linha_inicial_boletos(self, linha, linha_numero):
        if "- LIQUIDACOES -" in linha:
            self.LIQUIDACAO_LINHA_INICIAL = linha_numero + 3

        return self

    def parse_linha_para_boleto(self, linha, linha_numero):
        if self.LIQUIDACAO_LINHA_INICIAL != 0:
            if self.LIQUIDACAO_LINHA_FINAL != 0:
                if linha_numero >= self.LIQUIDACAO_LINHA_INICIAL:
                    if linha_numero < self.LIQUIDACAO_LINHA_FINAL:
                        vencimento = linha[41:47]
                        data_pagamento = linha[48:54]

                        boleto = {
                            "nome": linha[0:15].strip(),
                            "seu_numero": linha[16:26],
                            "nosso_numero": linha[27:40],
                            "vencimento": pendulum.date(year=int("20" + vencimento[4:6]), month=int(vencimento[3:4]), day=int(vencimento[0:2])),
                            "data_pagamento": pendulum.date(year=int("20" + data_pagamento[4:6]), month=int(data_pagamento[3:4]), day=int(data_pagamento[0:2])),
                            "valor": Decimal("{}.{}".format(linha[55:67].replace('.', ''), linha[68:70])),
                            "valor_pago": Decimal("{}.{}".format(linha[93:105].replace('.', ''), linha[106:108])),
                            "tarifa": Decimal("{}.{}".format(linha[109:115].replace('.', ''), linha[116:118])),
                        }
                        self.BOLETOS.append(BoletoSantander.from_dict(boleto))
                        return BoletoSantander.from_dict(boleto)
