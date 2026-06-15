#cupons.py
#cupons de desconto

cupons_validos ={
    "PRIMEIRACOMPRA10": 10,
    "VERAO15": 15,
    "BLACKFRIDAY20": 20,
    "SEMANADOCONSUMIDOR15": 15,
}

cupom_aplicado = {"codigo": None, "percentual": 0.0}

def validar_cupom(codigo):
    codigo = codigo.strip().upper()
    if codigo in cupons_validos:
        return True, cupons_validos[codigo]
    return False, 0.0

def aplicar_cupom(codigo):
    valido, percentual = validar_cupom(codigo)
    if not valido:
        return False, f"Cupom '{codigo.upper()}' é inválido ou expirado."
    cupom_aplicado["codigo"] = codigo.upper()
    cupom_aplicado["percentual"] = percentual
    return True, f"Cupom '{codigo.upper()}' aplicado com sucesso! Desconto de {percentual}%."

def remover_cupom():
    cupom_aplicado["codigo"] = None
    cupom_aplicado["percentual"] = 0.0
    return "Cupom removido com sucesso."

def obter_desconto_aplicado():
    return cupom_aplicado["percentual"]

def obter_cupom_atual():
    return cupom_aplicado["codigo"]