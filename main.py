import flet as ft

def main(page: ft.Page):
    page.fonts = {
        "KiwiMaru": "./assets/fonts/KiwiMaru-Medium.ttf",
        "JetBrainsMono": "./assets/fonts/JetBrainsMono-BoldItalic.ttf"
    }

    page.theme = ft.Theme(font_family="KiwiMaru")
    
    page.add(
        ft.Text("JetBrainsMono", font_family="JetBrainsMono"),
        ft.Text("だよ")
    )

ft.app(main, assets_dir ="assets")

    