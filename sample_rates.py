'''
This script processes audio files within subfolders of a main directory named "dataset". It automatically detects the subfolders, then iterates through each subfolder to find all files with the ".wav" extension. For each detected file, the script extracts its sample rate using the "pydub" library. The results, including the folder name, file name, and sample rate, are then saved to a text file named "sample_rates.txt".

Explanation:
- The script defines a function get_sample_rate(file_path) that takes the path to an audio file and returns its sample rate using the pydub library.
- Another function save_sample_rates(main_directory, output_file) processes all subfolders within the specified main_directory. For each subfolder, it iterates through the files with the ".wav" extension, extracts their sample rates, and writes the results to a text file.
- In the __main__ block, the main_folder variable is set to "dataset" as the main directory containing subfolders with audio files.
- The output_txt_file variable is set to "sample_rates.txt" as the file where the results will be saved.
- The save_sample_rates function is called with the specified main_folder and output_txt_file, and the script prints a message indicating that the sample rates have been saved to the output text file.
'''
from pydub import AudioSegment
import os

def get_sample_rate(file_path):
    audio = AudioSegment.from_file(file_path)
    return audio.frame_rate

def save_sample_rates(main_directory, output_file):
    with open(output_file, 'w') as f:
        f.write("Folder Name\tFile Name\tSample Rate\n")
        for folder_name in os.listdir(main_directory):
            folder_path = os.path.join(main_directory, folder_name)
            if os.path.isdir(folder_path):
                for filename in os.listdir(folder_path):
                    if filename.endswith('.wav'):  # Add more file extensions if needed
                        file_path = os.path.join(folder_path, filename)
                        try:
                            sample_rate = get_sample_rate(file_path)
                            f.write(f"{folder_name}\t{filename}\t{sample_rate}\n")
                        except Exception as e:
                            print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    main_folder = "dataset"
    output_txt_file = "sample_rates.txt"
    
    save_sample_rates(main_folder, output_txt_file)
    print(f"Sample rates saved to {output_txt_file}")
