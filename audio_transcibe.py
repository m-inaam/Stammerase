'''
    This script transcribes audio files in the specified folder and its subfolders.

    The main functionality includes:
    1. Walking through the directory tree starting from the provided main folder path.
    2. Identifying .wav files within each subfolder.
    3. Using the Google Web Speech API to transcribe each audio file.
    4. Saving the transcriptions in individual text files with the same name as the corresponding audio files.

    Usage:
    - Ensure the 'speech_recognition' library is installed: pip install SpeechRecognition
    - Adjust the 'main_folder_path' variable with the path to your main folder containing subfolders with .wav files.
    - Execute the script, which will process each .wav file, transcribe it, and save the transcription in a text file.

    Note:
    - The script handles exceptions for cases where the Google Web Speech API fails to transcribe the audio.
    - Each transcription is saved in a text file with the same name as the original audio file.
'''

import os
import speech_recognition as sr

def transcribe_audio(audio_file):
    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)  # Record the entire audio file
        try:
            text = recognizer.recognize_google(audio_data)  # Use Google Web Speech API
            return text
        except sr.UnknownValueError:
            print("Google Web Speech API could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Web Speech API; {e}")

def process_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".wav"):
                audio_file_path = os.path.join(root, file)
                transcription = transcribe_audio(audio_file_path)

                if transcription:
                    # Save transcription to a text file with the same name as the audio file
                    output_file_path = os.path.splitext(audio_file_path)[0] + ".txt"
                    with open(output_file_path, "w") as output_file:
                        output_file.write(transcription)
                    print(f"Transcription saved to {output_file_path}")

if __name__ == "__main__":
    main_folder_path = "./clips"  # Replace with the actual path to your "clips" folder
    process_folder(main_folder_path)