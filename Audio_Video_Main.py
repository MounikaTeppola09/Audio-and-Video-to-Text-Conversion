import os
from pydub import AudioSegment
import moviepy.editor as mp
import speech_recognition as sr
import tempfile
import shutil
import logging

# Configure logging
logging.basicConfig(filename='conversion_log.txt', level=logging.INFO)

#Convert MP3 to WAV
def convert_mp3_to_wav(mp3_file_path):
    try:
        # Load the MP3 file
        audio = AudioSegment.from_mp3(mp3_file_path)

        # Create a temporary WAV file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
            wav_file_path = temp_wav.name
            # Export as WAV
            audio.export(wav_file_path, format="wav")

        logging.info(f"Conversion successful. Temporary WAV file created at: {wav_file_path}")
        return wav_file_path
    except Exception as e:
        logging.error(f"Error converting MP3 to WAV: {str(e)}")
        return None

#Convert Video to WAV 
def convert_video_to_wav(video_file_path):
    try:
        # Load the video file
        video = mp.VideoFileClip(video_file_path)

        # Extract audio from the video
        audio = video.audio

        # Create a temporary WAV file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
            wav_file_path = temp_wav.name
            audio.write_audiofile(wav_file_path, codec='pcm_s16le')

        logging.info(f"Conversion successful. Temporary WAV file created at: {wav_file_path}")
        return wav_file_path
    except Exception as e:
        logging.error(f"Error converting video to WAV: {str(e)}")
        return None
    
#Identify Text from WAV
def recognize_text_from_wav(wav_file_path):
    try:
        # Initialize the recognizer
        recognizer = sr.Recognizer()

        # Load the WAV file
        with sr.AudioFile(wav_file_path) as source:
            audio_data = recognizer.record(source)

        # Recognize speech using the Sphinx recognizer
        text_result = recognizer.recognize_sphinx(audio_data)

        return text_result
    except sr.UnknownValueError:
        logging.warning("Speech recognition could not understand audio.")
        return None
    except sr.RequestError as e:
        logging.error(f"Error with Sphinx recognizer; {str(e)}")
        return None
    
#Indexing for the text Files
def index_text_files(directory):
    index = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith("_detected_text.txt"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as text_file:
                    content = text_file.read()
                    index[file] = {"path": file_path, "content": content}
    return index
 
#ChatBot for a interactive Conversation
def ask_question_from_index(index, question):
    for file_name, data in index.items():
        content = data["content"]
        if question.lower() in content.lower():
            logging.info(f"Question: {question}")
            logging.info(f"Answer from {file_name}: {content}\n")

#Main Function to call 
def main(input_path):
    if input_path.lower().endswith(".mp3"):
        # Convert MP3 to WAV
        converted_wav_file_path = convert_mp3_to_wav(input_path)
    elif input_path.lower().endswith((".mp4", ".avi", ".mov")):
        # Convert video to WAV (temporary file)
        converted_wav_file_path = convert_video_to_wav(input_path)
    else:
        logging.error("Unsupported file format. Please provide either an MP3 or a video file.")
        return

    if converted_wav_file_path:
        try:
            # Recognize text from the converted WAV file using Sphinx recognizer
            text_result = recognize_text_from_wav(converted_wav_file_path)

            if text_result:
                # Display the detected text in the console
                print("Detected Text:")
                print(text_result)

                # Example question
                question = "What is discussed in this conversation?"

            else:
                logging.warning("No text detected.")

        except Exception as e:
            logging.error(f"Error processing text: {str(e)}")
        finally:
            # Clean up: Remove the temporary WAV file
            shutil.rmtree(os.path.dirname(converted_wav_file_path), ignore_errors=True)
    else:
        logging.error("Conversion failed.")

#Input File Path
if __name__ == "__main__":
    # Example usage with either a video or an audio file
    input_path = r"C:\Users\teppo\Desktop\Audio_Video\Video\Chat with new friends _ Learn English conversation.mp4"
    main(input_path)
