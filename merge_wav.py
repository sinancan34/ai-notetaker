import os
import glob
import argparse
import subprocess

def merge_wav_segments(tab_dir):
    wav_files = sorted(glob.glob(os.path.join(tab_dir, "*.wav")))
    if not wav_files:
        print(f"No wav files found in {tab_dir}")
        return

    input_list_path = os.path.join(tab_dir, "inputs.txt")
    with open(input_list_path, "w") as f:
        for wav in wav_files:
            f.write(f"file '{os.path.abspath(wav)}'\n")

    output_path = os.path.join(tab_dir, "merged.wav")
    subprocess.run([
        "ffmpeg",
        "-f", "concat",
        "-safe", "0",
        "-i", input_list_path,
        "-c", "copy",
        output_path
    ], check=True)

    print(f"merged file: {output_path}")

    os.remove(input_list_path)

if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument('-t', '--tab_id', type=str, required=True)

    arguments = argument_parser.parse_args()

    RECORDINGS_DIR = "recordings"

    tab_dir = os.path.join(RECORDINGS_DIR, arguments.tab_id)

    merge_wav_segments(tab_dir)
