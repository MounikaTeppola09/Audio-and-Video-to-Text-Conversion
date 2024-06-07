import os
import shutil
from flask import Flask, request, jsonify
import tempfile
from Audio_Video_Main import convert_mp3_to_wav, convert_video_to_wav, recognize_text_from_wav, ask_question_from_index
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(filename='flask_app_log.txt', level=logging.INFO)
@app.route('/process', methods=['POST'])

#Process for uploading audio or video file to extract text
def process():
    try:
        input_file = request.files['input_file']

        # Save the uploaded file to a temporary location
        temp_file_path = os.path.join(tempfile.gettempdir(), input_file.filename)
        input_file.save(temp_file_path)

        # Pass the filename to the template
        file_name = input_file.filename

        if temp_file_path.lower().endswith(".mp3"):
            # Convert MP3 to WAV
            converted_wav_file_path = convert_mp3_to_wav(temp_file_path)
        elif temp_file_path.lower().endswith((".mp4", ".avi", ".mov")):
            # Convert video to WAV (temporary file)
            converted_wav_file_path = convert_video_to_wav(temp_file_path)
        else:
            logging.error("Unsupported file format. Please provide either an MP3 or a video file.")
            return jsonify({"Error": "Unsupported file format. Please provide either an MP3 or a video file."})

        if converted_wav_file_path:
            try:
                # Recognize text from the converted WAV file using Sphinx recognizer
                text_result = recognize_text_from_wav(converted_wav_file_path)

                if text_result:
                    # Display the detected text in the response
                    return jsonify({"Message": "Detected Text:", "Text": text_result})
                else:
                    logging.warning("No text detected.")
                    return jsonify({"Message": "No text detected."})
            except Exception as e:
                logging.error(f"Error processing text: {str(e)}")
            finally:
                # Clean up: Remove the temporary WAV file
                shutil.rmtree(os.path.dirname(converted_wav_file_path), ignore_errors=True)
        else:
            logging.error("Conversion failed.")
            return jsonify({"Message": "Conversion failed."})

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return jsonify({"Error": f"Error: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)