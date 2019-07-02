from decimal import Decimal

import pendulum


def parse_data(data, year=4):
    if data == "000000" or data == "00000000":
        return data

    if year == 4:
        return pendulum.date(
            day=int(data[0:2]),
            month=int(data[2:4]),
            year=int(data[4:8])
        )
    else:
        return pendulum.date(
            day=int(data[0:2]),
            month=int(data[2:4]),
            year=int(data[4:6])
        )


def conta_total_linhas(arquivo):
    return sum(1 for line in arquivo)


def parse_to_decimal(string):
    return Decimal("{}.{}".format(string[:-2], string[-2:]))


class BancoDoBrasil:
    HEADER = {}
    DETALHES = []
    TRAILLER = {}
    TOTAL_LINHAS_ARQUIVO = 0

    def __init__(self):
        self.HEADER = {}
        self.DETALHES = []
        self.TRAILLER = {}
        self.TOTAL_LINHAS_ARQUIVO = 0

    def conta_total_linhas_arquivo(self, arquivo):
        self.TOTAL_LINHAS_ARQUIVO = conta_total_linhas(arquivo)

    def processa_arquivo(self, arquivo):
        try:
            self.__processa(arquivo)
        except:
            self.__processa(arquivo, decode=True)

    def __processa(self, arquivo, decode=False):
        for line_number, line in enumerate(arquivo, 1):
            if decode is True:
                line = str(line.decode("utf-8"))

            if line_number == 1:
                print("ENTROU HEADER")
                self.HEADER = self.registro_header_retorno(line)
            elif line_number == self.TOTAL_LINHAS_ARQUIVO:
                print("ENTROU TRAILLER")
                self.TRAILLER = self.registro_trailler_retorno(line)
            else:
                print("ENTROU DETALHES")
                self.DETALHES.append(self.monta_detalhes_linha(line))

    def registro_header_retorno(self, linha):
        return {
            "01_identificacao_registro_header_0": linha[0:1],
            "02_tipo_operacao": linha[1:2],
            "03_tipo_operacao_identificacao": linha[2:9],
            "04_identificacao_tipo_servico": linha[9:11],
            "05_identificacao_tipo_servico_por_extenso": linha[11:19],
            "06_complemento_registro": linha[19:26],
            "07_prefixo_agencia": linha[26:30],
            "08_prefixo_agencia_digito_verificador": linha[30:31],
            "09_numero_conta_corrente": linha[31:39],
            "10_numero_conta_corrente_digito_verificador": linha[39:40],
            "11_zeros": linha[40:46],
            "12_nome_cedente": linha[46:76],
            "13_identificacao_banco": linha[76:94],
            "14_data_gravacao": parse_data(linha[94:100], 2),
            "15_sequencial_retorno": linha[100:107],
            "16_complemento_registro": linha[107:149],
            "17_numero_convenio": linha[149:156],
            "18_complemento_registro": linha[156:394],
            "19_numero_sequencial_registro": linha[394:400],
        }

    def monta_detalhes_linha(self, linha: str) -> dict:
        return {
            "01_identificacao_registro_detalhe_7": linha[0:1],
            "02_zeros": linha[1:3],
            "03_zeros": linha[3:17],
            "04_prefixo_agencia": linha[17:21],
            "05_prefixo_agencia_digito_verificador": linha[21:22],
            "06_numero_conta_corrente_cedente": linha[22:30],
            "07_numero_conta_corrente_cedente_digito_verificador": linha[30:31],
            "08_numero_convenio_cobranca_cedente": linha[31:38],
            "09_numero_controle_participante": linha[38:63],
            "10_nosso_numero": linha[63:80],
            "11_tipo_cobranca": linha[80:81],
            "12_tipo_cobranca_especifico_cmd_72": linha[81:82],
            "13_dias_calculo": linha[82:86],
            "14_natureza_recebimento": linha[86:88],
            "15_prefixo_boleto": linha[88:91],
            "16_variacao_carteira": linha[91:94],
            "17_conta_caucao": linha[94:95],
            "18_taxa_desconto": linha[95:100],
            "19_taxa_iof": linha[100:105],
            "20_branco": linha[105:106],
            "21_carteira": linha[106:108],
            "22_comando": linha[108:110],
            "23_data_liquidacao": parse_data(linha[110:116], 2),
            "24_numero_boleto_cedente": linha[116:126],
            "25_branco": linha[126:146],
            "26_data_vencimento": parse_data(linha[146:152], 2),
            "27_valor_boleto": parse_to_decimal(linha[152:165]),
            "28_codigo_banco_recebedor": linha[165:168],
            "29_prefixo_agencia_recebedora": linha[168:172],
            "30_agencia_recebedora_digito_verificador": linha[172:173],
            "31_especie_boleto": linha[173:175],
            "32_data_credito": parse_data(linha[175:181], 2),
            "33_valor_tarifa": parse_to_decimal(linha[181:188]),
            "34_outras_despesas": linha[188:201],
            "35_juros_desconto": linha[201:214],
            "36_iof_desconto": linha[214:227],
            "37_valor_abatimento": linha[227:240],
            "38_desconto_concedido": linha[240:253],
            "39_valor_recebido_parcial": parse_to_decimal(linha[253:266]),
            "40_juros_mora": linha[266:279],
            "41_outros_recebimentos": linha[279:292],
            "42_abatimento_nao_aproveitado_sacado": linha[292:305],
            "43_valor_lancamento": parse_to_decimal(linha[305:318]),
            "44_indicativo_debito_credito": linha[318:319],
            "45_indicador_valor": linha[319:320],
            "46_valor_ajuste": linha[320:332],
            "47_bancos": linha[332:333],
            "48_brancos": linha[333:342],
            "49_zeros": linha[342:349],
            "50_zeros": linha[349:358],
            "51_zeros": linha[358:365],
            "52_zeros": linha[365:374],
            "53_zeros": linha[374:381],
            "54_zeros": linha[381:390],
            "55_indicativo_autorizacao_liquidacao_parcial": linha[390:391],
            "56_branco": linha[391:392],
            "57_canal_pagamento_utilizado_pelo_sacado": linha[392:394],
            "58_numero_sequencial_registro": linha[394:400],
        }

    def registro_trailler_retorno(self, linha):
        return {
            "01_identificacao_registro_trailler_9": linha[0:1],
            "02_2": linha[1:3],
            "03_01": linha[3:17],
            "04_001": linha[17:21],
            "05_brancos": linha[21:22],
            "06_cob_simples_quantidade_boletos": linha[22:30],
            "07_cob_simples_valor_total": linha[30:31],
            "08_cob_simples_numero_aviso": linha[31:38],
            "09_cob_simples_brancos": linha[38:63],
            "10_cob_vinculada_quantidade_boletos": linha[63:80],
            "11_cob_vinculada_valor_total": linha[80:81],
            "12_cob_vinculada_numero_aviso": linha[81:82],
            "13_cob_vinculada_brancos": linha[82:86],
            "14_cob_caucionada_quantidade_boletos": linha[86:88],
            "15_cob_caucionada_valor_total": linha[88:91],
            "16_cob_caucionada_numero_aviso": linha[91:94],
            "17_cob_caucionada_brancos": linha[94:95],
            "18_cob_descontada_quantidade_boletos": linha[95:100],
            "19_cob_descontada_valor_total": linha[100:105],
            "20_cob_descontada_numero_aviso": linha[105:106],
            "21_cob_descontada_brancos": linha[106:108],
            "22_cob_vendor_quantidade_boletos": linha[108:110],
            "23_cob_vendor_valor_total": linha[110:116],
            "24_cob_vendor_numero_aviso": linha[116:126],
            "25_cob_vendor_brancos": linha[126:146],
            "26_numero_sequencial_registro": linha[146:152],
        }
