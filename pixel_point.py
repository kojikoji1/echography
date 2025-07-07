import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np

def on_click(event):
    x, y = event.x, event.y
    if 0 <= x < img_array.shape[1] and 0 <= y < img_array.shape[0]:
        pixel_val = img_array[y, x]
        print(f"クリック位置: ({x}, {y}) → ピクセル値: {pixel_val}")
    else:
        print("画像範囲外のクリックです")

# ファイル選択ダイアログ
file_path = filedialog.askopenfilename(
    title="画像を選択", 
    filetypes=[("Image files", "*.png;*.jpg;*.jpeg")]
)

if file_path:
    # Pillowで読み込み → NumPy配列に変換
    img_pil = Image.open(file_path).convert('L')  # グレースケール
    img_array = np.array(img_pil)

    # GUIウィンドウ作成
    root = tk.Tk()
    root.title("クリックでピクセル値表示")

    # Tkinter用の画像データ
    tk_img = ImageTk.PhotoImage(img_pil)
    canvas = tk.Canvas(root, width=tk_img.width(), height=tk_img.height())
    canvas.pack()
    canvas.create_image(0, 0, anchor=tk.NW, image=tk_img)
    canvas.bind("<Button-1>", on_click)

    root.mainloop()
