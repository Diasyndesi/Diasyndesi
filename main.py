"""
{main.py}
LICENSE: GNU GENERAL PUBLIC LICENSE
"""
###############################################
##                                             Imports                                                        ##
###############################################
from flask import Flask, render_template, jsonify, request, Response # Importing Flask server requirements for this project
from openai import OpenAI
import pyaudio
import os
import wave
import audioop
# from gradio_client import Client # Client for opensource models

###############################################
##                                   Envirtonment Variables                                     ##
###############################################
client = OpenAI(
    api_key='KEY HERE'
)
app = Flask(__name__)


###############################################
##                                            Recording                                                    ##
###############################################
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
OUTPUT_FILENAME = "output.wav"

def record_audio():
       
    audio = pyaudio.PyAudio()

    # Start recording
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                       input=True, frames_per_buffer=CHUNK)
    frames = []
    print("Recording...")

    # Initialize pause detection parameters
    silence_threshold = 25  # This value should be adjusted as needed. Depending on environmental conditions and recording device. (Initial conditions for this setting: -Silent room, -Galaxy Buds 2 Pro) 
    silence_count = 0

    while True:
        data = stream.read(CHUNK)
        frames.append(data)

        # Detect pauses in audio
        rms = audioop.rms(data, 2)  # Calculate root mean square (RMS)
        if rms < silence_threshold:
            silence_count += 1
        else:
            silence_count = 0

        # If silence continues for a certain duration, stop recording
        if silence_count > 45:  # his value should be adjusted as needed. Depending on environmental conditions and recording device. (Initial conditions for this setting: -Silent room, -Galaxy Buds 2 Pro) 
            break

    # Stop recording
    stream.stop_stream()
    stream.close()
    audio.terminate() 

    print('File Saved') # Should be removed in production so it doesn't spam the console
    # Remove existing audio file
    if os.path.exists(OUTPUT_FILENAME):
        os.remove(OUTPUT_FILENAME) # 

    # Save the recorded audio as a WAV file
    wf = wave.open(OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    pass
###############################################


###############################################
##                                  Rendering the website                                       ##
###############################################
@app.route('/')
def index():
    return render_template('index.html')

###############################################
##                                              Record                                                        ##
###############################################
@app.route('/api/record', methods=['GET', 'POST'])
def record_and_transcribe():
    if request.method == 'POST':
        # Record audio
        record_audio()
        audio_file = "output.wav"

        # Transcribe audio
        try:
            with open(audio_file, "rb") as file:
                transcript = client.Audio.transcribe("whisper-1", file, language="el")
            os.remove(audio_file)
            return jsonify({"transcript": transcript.text}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"message": "This endpoint supports both GET and POST methods."})

###############################################
##               ChatBot API                                                                             ##
###############################################
from langchain_community.document_loaders import DirectoryLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from openai import OpenAI
client = OpenAI()
###############################################
@app.route('/api/chat', methods=['POST'])
def chat_with_gpt():
    try:
        data = request.json
        user_message = data['user_message']

        # Load documents from directory
        loader = DirectoryLoader('../', glob="**/*.txt", use_multithreading=True, show_progress=True)
        raw_documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1500, chunk_overlap=0)
        documents = text_splitter.split_documents(raw_documents)
        db = Chroma.from_documents(documents, OpenAIEmbeddings())
        docs = db.similarity_search(user_message)
        #print(docs[0].page_content) !!Information retrieved!!
        #print(docs[0].metadata) !!File location!!
        prompt = "Retrieved information/Data: " + docs[0].page_content + " User Message: " + user_message
        ai_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a conversational AI assistant designed to help high school students. Your name is “Diasyndesi”, it was inspired by your ability to link information from both the school’s website as well as context provided to you by the person you are talking with. Assist them and create personalised recommendations. Your job is to answer any questions that the student asks you. Your main purpose will be to answer questions related to the school’s programmes, policies, schedules, events and announcements. You will be as friendly as possible. You are not allowed to talk or engage in conversations with: illegal activities, drugs or promote any harmful behaviour. You will speak in a semi-formal manner unless instructed otherwise, but you will try to avoid using bad words/language no matter the circumstances. Your base model is from OpenAI, but you were trained to provide information about the school by a team of high school students to increase ease of use for the school’s website and assist students with various questions and tasks, the students are not affiliated with OpenAI, you were just made by them as an extension of the website. All your responses should be in greek, you will not speak in any other language except greek unless you get asked to speak another language speficially. This means that even if the prompt is in another language you will respond in greek.  You will also never make things up about the school, all information you provide must be from the context provided to you and nowhere else. Feel free to use any emojis or expressions to make the conversation feel more natural. Try not to use the same emojis and use emojis throughout the text you generate, even between the sentences. You will also use the markdown format ONLY, use it as much as possible, meaning try to use different headers, lists codes embedings etc! You will also not give answers to homework questions directly, instead prompt the student to solve the problem on his/her own and provide them with questions that will make them think the answer for themselves. In each message you will recieve `data` retrieved from a database using a similarity search (which you may or may not have to use and they may not always be relevant) and then the user message to you."}, 
                {"role": "user", "content": prompt}
            ]
        )
        ai_response = ai_response.choices[0].message
        ai_response_content = ai_response.content
        return jsonify({"ai_response": ai_response_content}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

## 
#
#   EXAMPLE OF USING  FREE OPEN-SOURCE LLMs 
#
##
"""
def chat_with_gpt():
    try:
        data = request.json
        user_message = data['user_message']
        loader = DirectoryLoader('../', glob="**/*.txt", use_multithreading=True, show_progress=True)
        raw_documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1500, chunk_overlap=0)
        documents = text_splitter.split_documents(raw_documents)
        db = Chroma.from_documents(documents, OpenAIEmbeddings())
        #query = "εξάρτηση από το κάπνισμα και τα προϊόντα καπνού "
        docs = db.similarity_search(user_message)
        print(docs[0].page_content)
        print(docs[0].metadata)
        client = Client("https://osanseviero-mistral-super-fast.hf.space/")
        ai_response = client.predict(
        				"You are a frienly AI assistant called Diasyndesi. Here is the "+ user_message + docs[0].page_content,
                        0.9,	# int | float (numeric value between 0.0 and 1.0)
        				1024,	# int | float (numeric value between 0 and 1048)
        				0.9,	# int | float (numeric value between 0.0 and 1)
        				1.2,	# int | float (numeric value between 1.0 and 2.0)
        				api_name="/chat"
        )
        print(ai_response)
        return jsonify({"ai_response": ai_response}), 200
"""

###############################################
##                                    Running the Server                                           ##
###############################################
if __name__ == '__main__':
    app.run(debug=True)