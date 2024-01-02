#
# For licensing see accompanying LICENSE file.
# Copyright (C) 2021 Apple Inc. All Rights Reserved.
#

"""
For each podcast episode:
* Get all clip information for that episode
* Save each clip as a new wav file.
"""

import os
import pathlib
from scipy.io import wavfile
import pandas as pd
import argparse
import sys

parser = argparse.ArgumentParser(description='Extract clips from SEP-28k or FluencyBank.')
parser.add_argument('--labels', type=str, required=True,
                   help='Path to the labels csv files (e.g., labels.csv)')
parser.add_argument('--wavs', type=str, default="dataset",
                   help='Path where audio files from download_audio.py are saved')
parser.add_argument('--clips', type=str, default="clips",
                   help='Path where clips should be extracted')
parser.add_argument("--progress", action="store_true",
                    help="Show progress")

args = parser.parse_args()
label_file = args.labels
data_dir = args.wavs
output_dir = args.clips

# Load label/clip file
data = pd.read_csv(label_file, dtype={"EpId": str})

# Get label columns from the data file
shows = data.Show
episodes = data.EpId
clip_idxs = data.ClipId
starts = data.Start
stops = data.Stop
labels = data.iloc[:, 5:].values

n_items = len(shows)

loaded_wav = ""
cur_iter = range(n_items)
if args.progress:
    from tqdm import tqdm
    cur_iter = tqdm(cur_iter)

for i in cur_iter:
    clip_idx = clip_idxs[i]
    show_abrev = shows[i]
    episode = episodes[i].strip()

    # Setup paths
    wav_path = f"{data_dir}/{shows[i]}/{episode}.wav"
    clip_dir = pathlib.Path(f"{output_dir}/{show_abrev}/{episode}/")
    clip_path = f"{clip_dir}/{shows[i]}_{episode}_{clip_idx}.wav"

    if not os.path.exists(wav_path):
        print("Missing", wav_path)
        continue

    # Verify clip directory exists
    os.makedirs(clip_dir, exist_ok=True)

    # Load audio. For efficiency reasons, don't reload if we've already opened the file.
    if wav_path != loaded_wav:
        sample_rate, audio = wavfile.read(wav_path)

        # Updated sample rate handling
        if sample_rate == 32000:
            print(f"Adjusting sample rate for file {wav_path} from {sample_rate} Hz to 16000 Hz.")
            sample_rate //= 2  # Divide sample rate by 2 to make it 16 kHz
        elif sample_rate == 44100:
            print(f"Adjusting sample rate for file {wav_path} from {sample_rate} Hz to 16000 Hz.")
            sample_rate = int(sample_rate / 2.75625)  # Adjust sample rate to 16 kHz
        elif sample_rate != 16000:
            print(f"Warning: Sample rate for file {wav_path} is {sample_rate} Hz. Expected 16 kHz.")
            # Handle other cases if needed

        # Keep track of the open file
        loaded_wav = wav_path

    # Save clip to file
    clip = audio[starts[i]:stops[i]]
    wavfile.write(clip_path, sample_rate, clip)