from pathlib import Path

import cv2
import numpy as np


def pick_pose_frame(
        movie_file: str,
        output_dir: str,
        binalization_threshold: int = 30,
        next_frame_pixel_threshold: int = 20_000):
    """動画から変化の内部分を抽出し、画像化する。

    Args:
        movie_file (str): 動画ファイルへのパス
        output_dir (str): 画像を出力するディレクトリ
        binalization_threshold (int, optional): 2値化のしきい値。この値未満は黒となる. Defaults to 30.
        next_frame_pixel_threshold (int, optional): 2つの画像の変化量のしきい値. Defaults to 20_000.

    Raises:
        FileNotFoundError: movie_fileが存在しない時に投げられる。
    """
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
