import cv2
import numpy as np

# === 対象画像（例：1枚のスライス画像）===
image_path = "frames_arc/frame_0108.jpg"  # ← 適宜パスを変更してください
img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# ウィンドウ作成
cv2.namedWindow("Threshold Adjuster", cv2.WINDOW_NORMAL)  # サイズ変更可能に

# スライダー初期化
cv2.createTrackbar("Min", "Threshold Adjuster", 20, 255, lambda x: None)
cv2.createTrackbar("Max", "Threshold Adjuster", 40, 255, lambda x: None)

while True:
    min_val = cv2.getTrackbarPos("Min", "Threshold Adjuster")
    max_val = cv2.getTrackbarPos("Max", "Threshold Adjuster")

    # 範囲内を白、それ以外を黒に
    mask = cv2.inRange(img, min_val, max_val)

    # ==== 表示用に拡大（2倍） ====
    img_resized = cv2.resize(img, (img.shape[1]*2, img.shape[0]*2))
    mask_resized = cv2.resize(mask, (mask.shape[1]*2, mask.shape[0]*2))

    # 2画面並べて表示
    combined = np.hstack([img_resized, mask_resized])
    cv2.imshow("Threshold Adjuster", combined)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

cv2.destroyAllWindows()
