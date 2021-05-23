import sys
from pathlib import Path
import unittest
this_file_dir = Path(__file__).parent.resolve()

sys.path += [
    str(this_file_dir / ".."),
]

from pose_scene_picker import diff_frame


class TestFile(unittest.TestCase):

    def test_file_exist(self):
        movie_file = "notexisted_file.mp4"
        output_dir = "/tmp/sample"

        with self.assertRaises(FileNotFoundError):
            diff_frame.pick_pose_frame(movie_file, output_dir)
