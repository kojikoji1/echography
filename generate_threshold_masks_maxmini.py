import os
import cv2
import numpy as np

# ===== 設定 =====
input_dir = "frames_arc"               # JPG画像が入っているフォルダ
output_dir = "arc_masks"     # マスク画像の出力フォルダ
os.makedirs(output_dir, exist_ok=True)

# ===== 閾値の範囲（この範囲を白に、それ以外は黒）=====
min_val = 0  # 下限（含む）
max_val = 52  # 上限（含む）

# ===== マスク処理 =====
for filename in sorted(os.listdir(input_dir)):
    if filename.lower().endswith((".jpg", ".jpeg", ".png")):
        filepath = os.path.join(input_dir, filename)
        img = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)

        if img is None:
            print(f"❌ 読み込み失敗: {filepath}")
            continue

        # 指定範囲内を白（255）、それ以外を黒（0）に
        mask = np.where((img >= min_val) & (img <= max_val), 255, 0).astype(np.uint8)

        # 出力ファイル名（.png）
        out_name = os.path.splitext(filename)[0] + ".png"
        out_path = os.path.join(output_dir, out_name)
        cv2.imwrite(out_path, mask)

        print(f"✅ 作成: {out_path}")
