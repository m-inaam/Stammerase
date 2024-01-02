'''
This script recursively traverses through all subdirectories within the specified "dataset" folder.
For each .mp3 or .m4a file found, it converts the audio file to .wav format using the pydub library.

The conversion process involves the following steps:
1. The input file path is constructed based on the current file being processed.
2. The output file path is created by replacing the file extension with ".wav".
3. The audio file is converted to the .wav format using the convert_to_wav function.
4. Information about the conversion is printed to the console, indicating the original and converted file names.
5. The original audio file is removed to conserve storage space.

To use the script, set the main_folder variable to the path of the "dataset" folder containing subdirectories with audio files.
The script will automatically detect and process all subdirectories, converting audio files to .wav format and removing the original files.
'''

from pydub import AudioSegment
import os

def convert_to_wav(input_file, output_file):
    sound = AudioSegment.from_file(input_file)
    sound.export(output_file, format="wav")

def batch_convert_and_remove(main_folder):
    for root, subdirs, files in os.walk(main_folder):
        for filename in files:
            if filename.endswith(".mp3") or filename.endswith(".m4a"):
                input_path = os.path.join(root, filename)
                output_path = os.path.join(root, os.path.splitext(filename)[0] + ".wav")

                convert_to_wav(input_path, output_path)
                print(f"Converted: {filename} to {os.path.basename(output_path)}")

                # Remove the original file after conversion
                os.remove(input_path)
                print(f"Removed: {filename}")

if __name__ == "__main__":
    main_folder = "./dataset/"  # Replace with the path to your "dataset" folder
    batch_convert_and_remove(main_folder)
