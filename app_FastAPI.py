import os
import shutil
from fastapi import FastAPI, File, UploadFile, HTTPException
import tempfile
from Audio_Video_Main import convert_mp3_to_wav, convert_video_to_wav, recognize_text_from_wav, ask_question_from_index
import logging

app = FastAPI()

# Configure logging
logging.basicConfig(filename='fastapi_app_log.txt', level=logging.INFO)
@app.post('/process')

#Process for uploading audio or video file to extract text
async def process(input_file: UploadFile = File(...)):
    try:
        # Save the uploaded file to a temporary location
        temp_file_path = os.path.join(tempfile.gettempdir(), input_file.filename)
        with open(temp_file_path, 'wb') as temp_file:
            temp_file.write(input_file.file.read())

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
            raise HTTPException(status_code=400, detail="Unsupported file format. Please provide either an MP3 or a video file.")

        if converted_wav_file_path:
            try:
                # Recognize text from the converted WAV file using Sphinx recognizer
                text_result = recognize_text_from_wav(converted_wav_file_path)

                if text_result:
                    # Display the detected text in the response
                    return {"Message": "Detected Text:", "Text": text_result}
                else:
                    logging.warning("No text detected.")
                    return {"Message": "No text detected."}
            except Exception as e:
                logging.error(f"Error processing text: {str(e)}")
            finally:
                # Clean up: Remove the temporary WAV file
                shutil.rmtree(os.path.dirname(converted_wav_file_path), ignore_errors=True)
        else:
            logging.error("Conversion failed.")
            raise HTTPException(status_code=500, detail="Conversion failed.")

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
#uvicorn app_FastAPI:app --reload