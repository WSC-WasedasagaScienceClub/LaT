import flet as ft
import qrcode
import cv2
from PIL import Image
import numpy as np
import sqlite3

def main(page: ft.Page):
    page.title = "QRコード整理券システム"
    page.window_center()  # ウィンドウを中央に配置

    # データベースの初期化
    conn = sqlite3.connect('tickets.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_number TEXT NOT NULL
        )
    ''')
    conn.commit()

    def generate_qr(data):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        img.save("ticket.png")
        return img

    def read_qr():
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("カメラが開けませんでした。")
            return

        detector = cv2.QRCodeDetector()

        while True:
            ret, img = cap.read()
            if not ret:
                print("フレームを取得できませんでした。")
                break

            data, bbox, _ = detector.detectAndDecode(img)
            if data:
                print("QRコードの内容:", data)
                break
            cv2.imshow("QRコードリーダー", img)
            if cv2.waitKey(1) == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()

    def on_generate_click(e):
        # 整理券番号をデータベースに保存
        ticket_number = "整理券番号: 12345"
        cursor.execute('INSERT INTO tickets (ticket_number) VALUES (?)', (ticket_number,))
        conn.commit()

        generate_qr(ticket_number)
        page.add(ft.Text("QRコードが生成されました。"))

        # QRコード画像を表示
        qr_image = ft.Image(src="ticket.png", width=200, height=200)
        page.add(qr_image)

    def on_read_click(e):
        read_qr()
        page.add(ft.Text("QRコードが読み取られました。"))

    page.add(
        ft.Column(
            [
                ft.Text("QRコード整理券システム", size=30),
                ft.ElevatedButton("QRコードを生成", on_click=on_generate_click),
                ft.ElevatedButton("QRコードを読み取る", on_click=on_read_click),
            ],
            alignment=ft.MainAxisAlignment.CENTER,  # 中央揃え
            horizontal_alignment=ft.CrossAxisAlignment.CENTER  # 中央揃え
        )
    )

    # アプリ終了時にデータベース接続を閉じる
    page.on_close = lambda e: conn.close()

ft.app(target=main)
