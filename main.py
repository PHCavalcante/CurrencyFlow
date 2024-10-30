import aiohttp
import flet as ft
import bandeiras_moedas

moedas_bandeiras = {valor: chave for chave, valor in bandeiras_moedas.bandeiras_moedas.items()}
enxchange_logo = ft.Image(src="./exchange-logo.png", color="#000000", width=100, height=100)
url = "https://open.er-api.com/v6/latest/USD"

async def fetch_data():
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                dados = await response.json()
                return dados

async def main(page: ft.Page):
    page.title = "Conversor de Moedas"
    page.theme_mode = "light"
    page.window.width = 400
    page.window.height = 450
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.update()
    dados = await fetch_data()

    botao_temas = ft.IconButton(icon=ft.icons.DARK_MODE, icon_size=30, on_click=lambda handle: handle_theme())

    def mudar_bandeira(e):
        if e.control.label == "Moeda Origem":
            bandeiras1.src = f"https://flagcdn.com/64x48/{moedas_bandeiras[dropdown1.value]}.png"
            texto_cambio.value = f"1 {dropdown2.value} = {'{:.2f}'.format(dados.get('rates').get(dropdown1.value))} {dropdown1.value}"
        else:
            bandeiras2.src = f"https://flagcdn.com/64x48/{moedas_bandeiras[dropdown2.value]}.png"
            texto_cambio.value = f"1 {dropdown2.value} = {'{:.2f}'.format(dados.get('rates').get(dropdown2.value))} {dropdown1.value}"
        page.update()

    dropdown1 = ft.Dropdown(width=110, label="Moeda Origem", value=bandeiras_moedas.bandeiras_moedas["br"], on_change=mudar_bandeira, options=[])
    bandeiras1 = ft.Image(f"https://flagcdn.com/64x48/br.png", fit=ft.ImageFit.COVER, border_radius=100)
    dropdown2 = ft.Dropdown(width=110, label="Moeda Destino", value=bandeiras_moedas.bandeiras_moedas["us"], on_change=mudar_bandeira, options=[])
    bandeiras2 = ft.Image(f"https://flagcdn.com/64x48/us.png", fit=ft.ImageFit.COVER, border_radius=100)
    campo_valor1 = ft.TextField(width=100, height=45, value=str("%.2f" % 1000), tooltip=f"Selecione a quatidade de {dropdown1.value} a ser convertido", label="Quantidade")
    campo_valor2 = ft.TextField(width=100, height=45, value="0", tooltip=f"Valor convertido em {dropdown2.value}", label="Resultado", read_only=True)
    texto_cambio = ft.Text(f"1 {dropdown2.value} = {'{:.2f}'.format(dados.get('rates').get(dropdown1.value))} {dropdown1.value}",
                           style=ft.TextStyle(weight=ft.FontWeight.BOLD))
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
            dropdown1.options.append(ft.dropdown.Option(x))
            dropdown2.options.append(ft.dropdown.Option(x))

        page.update()

    carregar_moedas()

    def calcular_cambio():
        quantidade_a_ser_convertido = float(campo_valor1.value)
        taxas = dados.get("rates")
        taxa_moeda1 = taxas.get(dropdown1.value)
        taxa_moeda2 = taxas.get(dropdown2.value)
        if dropdown1.value == "USD":
            resultado = quantidade_a_ser_convertido * taxa_moeda2
        elif dropdown2.value == "USD":
            resultado = quantidade_a_ser_convertido / taxa_moeda1
        else:
            resultado = (quantidade_a_ser_convertido / taxa_moeda1) * taxa_moeda2
        campo_valor2.value = "%.2f" % resultado
        page.update()

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
                    )
                ),
                ft.Container(
                    content=ft.Row(
                        [
                            bandeiras1,
                            dropdown1,
                            campo_valor1
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    )
                ),
                ft.Container(
                    content=ft.IconButton(
                        icon=ft.icons.SWAP_VERT,
                        icon_size=40,
                        tooltip="Aperte para converter",
                        on_click=lambda calcular: calcular_cambio()
                    ),
                ),
                ft.Container(
                    content=ft.Row(
                        [
                            bandeiras2,
                            dropdown2,
                            campo_valor2
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    )
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Taxa de conversão", style=ft.TextThemeStyle.LABEL_MEDIUM),
                            texto_cambio
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=10
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )


ft.app(target=main, view=ft.AppView.WEB_BROWSER)