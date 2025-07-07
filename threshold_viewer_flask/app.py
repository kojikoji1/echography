from flask import Flask, render_template, request
import os
import cv2
import numpy as np

app = Flask(__name__)

# ===== フォルダ設定 =====
INPUT_FOLDER = 'static/images'         # 元画像（jpg）
TEMP_FOLDER = 'static/temp'            # 表示用一時保存（png）
OUTPUT_FOLDER = 'static/processed'     # 最終保存（pngのみ）
os.makedirs(TEMP_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ===== 入力画像の一覧取得（jpg限定）=====
image_files = sorted([f for f in os.listdir(INPUT_FOLDER) if f.lower().endswith('.jpg')])
total_images = len(image_files)

@app.route("/")
def index():
    index = int(request.args.get('index', 0))
    low = int(request.args.get('low', 3))
    high = int(request.args.get('high', 20))

    index = max(0, min(index, total_images - 1))
    filename = image_files[index]

    # 入出力パス
    input_path = os.path.join(INPUT_FOLDER, filename)
    temp_name = os.path.splitext(filename)[0] + ".png"
    temp_path = os.path.join(TEMP_FOLDER, temp_name)

    # 画像処理（グレースケール→しきい値で2値化→pngで保存）
    img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
    mask = np.where((img >= low) & (img <= high), 255, 0).astype(np.uint8)
    cv2.imwrite(temp_path, mask)

    return render_template("index.html",
        input_file=os.path.join('static/images', filename),
        result_file=os.path.join('static/temp', temp_name),
        index=index,
        total=total_images,
        low=low,
        high=high
    )

@app.route("/save_all")
def save_all():
    low = int(request.args.get('low', 3))
    high = int(request.args.get('high', 20))

    for filename in image_files:
        input_path = os.path.join(INPUT_FOLDER, filename)

        # 保存時のファイル名は .png に変更
        base_name = os.path.splitext(filename)[0] + ".png"
        output_path = os.path.join(OUTPUT_FOLDER, base_name)

        img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
        mask = np.where((img >= low) & (img <= high), 255, 0).astype(np.uint8)
        cv2.imwrite(output_path, mask)

    return f"{len(image_files)} 枚のPNGを保存しました（Low={low}, High={high}）"

if __name__ == "__main__":
    app.run(debug=True)
