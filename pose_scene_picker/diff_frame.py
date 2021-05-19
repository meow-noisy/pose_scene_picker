
import sys
from pathlib import Path

import cv2
import numpy as np

out_dir = Path(sys.argv[2])
out_dir.mkdir(parents=True, exist_ok=True)


th = 30    # 差分画像の閾値

# 動画ファイルのキャプチャ
cap = cv2.VideoCapture(sys.argv[1])

# 最初のフレームを背景画像に設定
ret, frame = cap.read()

# グレースケール変換
bg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

i = 0
filepath = out_dir / f"{str(i).zfill(4)}.jpg"
cv2.imwrite(str(filepath), frame)
i += 1

try:
    while(cap.isOpened()):
        # フレームの取得
        ret, frame = cap.read()

        # グレースケール変換
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 差分の絶対値を計算
        mask = cv2.absdiff(gray, bg)

        # 差分画像を二値化してマスク画像(モノクロ)を算出
        mask[mask < th] = 0
        mask[mask >= th] = 255

        print(i, np.count_nonzero(mask))
        num_of_diff_pixel = np.count_nonzero(mask)

        if num_of_diff_pixel > 20_000:
            filepath = out_dir / f"{str(i).zfill(4)}.jpg"
            cv2.imwrite(str(filepath), frame)
            cap.read()  # なんかゴミが出てるので飛ばす
            i += 1

        bg = gray
finally:
    cap.release()
