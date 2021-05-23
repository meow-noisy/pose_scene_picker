import sys

from pose_scene_picker import diff_frame


def main():
    argvs = sys.argv

    movie_file = argvs[1]
    output_dir = argvs[2]

    diff_frame.pick_pose_frame(movie_file, output_dir)
