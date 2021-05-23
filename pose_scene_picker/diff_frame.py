from pathlib import Path

import cv2
import numpy as np


def pick_pose_frame(
        movie_file,
        output_dir,
        binalization_threshold=30,
        next_frame_pixel_threshold=20_000):
    # th = 30    # 差分画像の閾値

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # 動画ファイルのキャプチャ
    if not Path(movie_file).exists():
        raise FileNotFoundError(f'{movie_file}')

    cap = cv2.VideoCapture(movie_file)

    # 最初のフレームを背景画像に設定
    ret, frame = cap.read()

    # グレースケール変換
    bg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    i = 0
    filepath = output_dir / f"{str(i).zfill(4)}.jpg"
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
            mask[mask < binalization_threshold] = 0
            mask[mask >= binalization_threshold] = 255

            print(i, np.count_nonzero(mask))
            num_of_diff_pixel = np.count_nonzero(mask)

            if num_of_diff_pixel > next_frame_pixel_threshold:
                filepath = output_dir / f"{str(i).zfill(4)}.jpg"
                cv2.imwrite(str(filepath), frame)
                cap.read()  # なんかゴミが出てるので飛ばす
                i += 1

            bg = gray
    finally:
        cap.release()
