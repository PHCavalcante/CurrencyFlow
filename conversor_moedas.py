def converter_moeda(valor, moeda_origem, moeda_destino):

    taxas = {
        'BRL': {'USD': 0.18, 'EUR': 0.17},
        'USD': {'BRL': 5.48, 'EUR': 0.91},
        'EUR': {'BRL': 6.03, 'USD': 1.10}
    }

    if moeda_origem == moeda_destino:

        return valor

    try:
        taxa = taxas[moeda_origem][moeda_destino]
        return valor * taxa
    except KeyError:
        print("Conversão não suportada para as moedas fornecidas.")


valor = float(input("Digite o valor que deseja converter [BRL]: "))
tipo_moeda = str(input("Digite o tipo da moeda que deseja converter [USD] ou [EUR]: "))

moeda_origem = 'BRL'
moeda_destino_usd = 'USD'
moeda_destino_eur = 'EUR'

if tipo_moeda == moeda_destino_usd:
    valor_convertido_usd = converter_moeda(valor, moeda_origem, moeda_destino_usd)
    print(f"{valor} reais [{moeda_origem}] equivalem a {valor_convertido_usd:.2f} dólares [{moeda_destino_usd}]")

else:
    valor_convertido_eur = converter_moeda(valor, moeda_origem, moeda_destino_eur)
    print(f"{valor} reais [{moeda_origem}] equivalem a {valor_convertido_eur:.2f} euros [{moeda_destino_eur}]")
