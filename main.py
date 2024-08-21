import flet as ft
import requests

url = "https://open.er-api.com/v6/latest/USD"
response = requests.get(url)

bandeiras_moedas = {
    "us": "USD",
    "ca": "CAD",
    "gb": "GBP",
    "eu": "EUR",
    "br": "BRL",
    "jp": "JPY",
    "au": "AUD",
    "cn": "CNY",
    "in": "INR",
    "ru": "RUB",
    "za": "ZAR",
    "mx": "MXN",
    "ar": "ARS",
    "ch": "CHF",
    "se": "SEK",
    "no": "NOK",
    "dk": "DKK",
    "kr": "KRW",
    "sg": "SGD",
    "nz": "NZD",
    "hk": "HKD",
    "sa": "SAR",
    "ae": "AED",
    "tr": "TRY",
    "eg": "EGP",
}

moedas_bandeiras = {valor: chave for chave, valor in bandeiras_moedas.items()}


if response.status_code == 200:
    try:
        dados = response.json()
        # print(dados["rates"])
        taxa_eur = dados.get('rates', {}).get('EUR', 'Não disponível')
        print(f"Taxa de câmbio USD para EUR: {taxa_eur}")
    except ValueError:
        print("erro ao tentar parsear para json")

enxchange_logo = ft.Image(src="./assets/exchange-logo.png", color="#000000", width=100, height=100)

def main(page: ft.Page):
    page.title = "Conversor de Moedas"
    page.theme_mode = "light"
    page.window_width = 400
    page.window_height = 600
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.update()

    botao_temas = ft.IconButton(icon=ft.icons.DARK_MODE, icon_size=30, on_click=lambda handle: handle_theme())

    def handleFlags(flag):
        flag = moedas_bandeiras.get("BRL")
        page.update
        return flag

    def mudar_bandeira(value):
        handleFlags(moedas_bandeiras[value])
        page.update()

    dropdown = ft.Dropdown(width=100, label="Moeda", value=bandeiras_moedas["br"], on_change=mudar_bandeira(), options=[])
    def handle_theme():
        if page.theme_mode == "dark":
            page.theme_mode = "light"
            botao_temas.icon = ft.icons.DARK_MODE
            enxchange_logo.color = "#000000"
            page.update()
        else:
            page.theme_mode = "dark"
            botao_temas.icon = ft.icons.LIGHT_MODE
            enxchange_logo.color = "#ffffff"
            page.update()

    def carregar_moedas():
        for x in dados["rates"]:
            dropdown.options.append(ft.dropdown.Option(x))

        page.update()

    carregar_moedas()
    page.add(
        ft.Column(
            [
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text("Powered by",
                                    style=ft.TextThemeStyle.LABEL_SMALL
                                    ),
                            enxchange_logo,
                           botao_temas
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        # vertical_alignment=ft.alignment.top_left
                    )
                ),
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Image(f"https://flagcdn.com/64x48/{handleFlags()}.png",
                                     fit=ft.ImageFit.COVER,
                                     border_radius=100
                                     ),
                            dropdown,
                            ft.TextField(width=100, height=45, value="1000", tooltip="Selecione a quatidade", label="Quantidade")
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        # horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )
                ),
                ft.Container(
                    content=ft.IconButton(icon=ft.icons.SWAP_VERT, icon_size=40, tooltip="Aperte para converter"),
                ),
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Image("https://flagcdn.com/64x48/us.png", border_radius=100),
                            dropdown,
                            ft.TextField(width=100, height=45, value="1000", tooltip="Selecione a quatidade", label="Quantidade")
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                       # horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )
                ),
                ft.Container(
                    content=ft.Column([ft.Text("Taxa de conversão", style=ft.TextThemeStyle.LABEL_SMALL), ft.Text("1 USD = 5.66322 USD")])
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )


ft.app(main)
