import argparse

from video_slicing import slice_audio

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This script splits single audio to dataset with noise reduction")
    parser.add_argument("path")
    parser.add_argument("audio")
    args = parser.parse_args()
    slice_audio(args.path, args.audio)