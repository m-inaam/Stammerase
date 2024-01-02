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
