import numpy as np
import imageio.v2 as imageio
import os
import pyvista as pv
from glob import glob

# === 設定 ===
mask_dir = "arc_masks_trimmed"  # 二値マスク画像フォルダ
angle_range = 45              # 合計スイープ角度（−22.5〜+22.5度）
depth_scale = 1.0             # 縦ピクセル → r 変換スケーリング
width_scale = 1.0             # 横ピクセル → x 変換スケーリング
threshold = 127               # 白黒マスクのしきい値

# === マスク画像の読み込み ===
mask_files = sorted(glob(os.path.join(mask_dir, "*.png")))
num_slices = len(mask_files)
points = []

for idx, file in enumerate(mask_files):
    img = imageio.imread(file, mode='L')  # グレースケール読み込み

    theta_deg = -angle_range / 2 + angle_range * (idx / (num_slices - 1))
    theta_rad = np.deg2rad(theta_deg)

    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            if img[y, x] > threshold:
                r = y * depth_scale
                z = r * np.cos(theta_rad)
                y_ = r * np.sin(theta_rad)
                x_ = x * width_scale
                points.append([x_, y_, z])

# === 点群として表示 ===
points = np.array(points)
cloud = pv.PolyData(points)

plotter = pv.Plotter()
plotter.add_points(cloud, render_points_as_spheres=True, point_size=2, color="white")
plotter.add_axes()
plotter.show()
