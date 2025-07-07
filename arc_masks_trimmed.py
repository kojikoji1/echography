import cv2
import numpy as np
import os

# === 入力・出力フォルダ設定 ===
input_dir = "arc_masks"
output_dir = "arc_masks_trimmed"
os.makedirs(output_dir, exist_ok=True)

# === 代表画像でポリゴンを描画 ===
sample_path = os.path.join(input_dir, "frame_0027.png")  # 代表画像（調整可）
img = cv2.imread(sample_path, cv2.IMREAD_GRAYSCALE)
clone = img.copy()
points = []

def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        cv2.circle(clone, (x, y), 3, 255, -1)
        if len(points) > 1:
            cv2.line(clone, points[-2], points[-1], 255, 1)
        cv2.imshow("Draw Polygon - Press 'q' when done", clone)

cv2.imshow("Draw Polygon - Press 'q' when done", clone)
cv2.setMouseCallback("Draw Polygon - Press 'q' when done", click_event)

while True:
    key = cv2.waitKey(1)
    if key == ord('q') and len(points) >= 3:
        break

cv2.destroyAllWindows()

# === ポリゴンマスクを作成 ===
mask = np.zeros_like(img, dtype=np.uint8)
cv2.fillPoly(mask, [np.array(points, dtype=np.int32)], 255)
cv2.imwrite("poly_mask.png", mask)
print("✅ ポリゴンマスク poly_mask.png を保存しました。")

# === 200枚のマスク画像に一括適用 ===
for filename in sorted(os.listdir(input_dir)):
    if filename.lower().endswith(".png"):
        img_path = os.path.join(input_dir, filename)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        trimmed = cv2.bitwise_and(img, mask)
        out_path = os.path.join(output_dir, filename)
        cv2.imwrite(out_path, trimmed)
        print(f"✅ 適用完了: {filename}")

print("🎉 すべての画像にポリゴンマスクを適用しました。")
