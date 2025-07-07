import cv2
import os

VIDEO_PATH = "14574_20250704_Adult-_Abd-U_0002.MP4"  # あなたの動画ファイル名
OUTPUT_DIR = "frames_arc"  # 扇形再構成用
NUM_FRAMES = 200  # 合計フレーム数（回転角度スキャンに対応）

os.makedirs(OUTPUT_DIR, exist_ok=True)

cap = cv2.VideoCapture(VIDEO_PATH)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = cap.get(cv2.CAP_PROP_FPS)
interval = max(int(total_frames / NUM_FRAMES), 1)

print(f"🎥 FPS: {fps}, Total Frames: {total_frames}, Interval: {interval}")

frame_idx = 0
saved_idx = 0

while cap.isOpened() and saved_idx < NUM_FRAMES:
    ret, frame = cap.read()
    if not ret:
        break

    if frame_idx % interval == 0:
        # 現在の角度θを計算（−22.5°〜+22.5°まで等間隔）
        theta = -22.5 + (45 * saved_idx / (NUM_FRAMES - 1))
        label = f"θ = {theta:.1f}°"

        overlay = frame.copy()
        cv2.putText(overlay, label, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), 2)

        filename = f"frame_{saved_idx:04d}.jpg"
        cv2.imwrite(os.path.join(OUTPUT_DIR, filename), overlay)
        print(f"✅ Saved: {filename} ({label})")
        saved_idx += 1

    frame_idx += 1

cap.release()
print("🎉 200フレームの切り出しと角度付与が完了しました。")
