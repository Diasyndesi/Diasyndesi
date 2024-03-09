<p align="middle">
  <img src="/Images/415768736_3741005119546423_4449621087855576190_n.png" style="border-radius: 18px"/>
</p>
This project is a chatbot that can interact with users based on custom data. The chatbot can use any data source, such as PDFs and TXT files to generate relevant and engaging responses. The chatbot can also handle different types of user inputs, such as text and voice and provide appropriate feedback. 

[comment]: <> (The project is open-source and available on GitHub for anyone who wants to use it or contribute to it.)

# Technical Stuff: The "how" of this project
## Packages
- Flask: `pip inatall flask`
  - Imports: Flask, render_template, jsonify, request
- OpenAI: `pip install openai`
- Pyaudio: `pip install pyaudio`
- Langchain: `pip install langchain, langchain_community`
## Other imports
- OS
- Audioop
- Wave

## AI Models
The AI models we used in order to create this project. (All requests are made through APIs although the code can be easily adjusted in order to run local models ex. through gradio)
- Whisper (The model we used for transcribing the recorded text. [Model from OpenAI])
- GPT-3.5-Turbo-16k (The text generation AI used to generate responses, with up to 16k tokens context. [Model from OpenAI])

# About the UI
The user interface is designed to be simple and intuitive. It consists of a main page with an input box and two buttons that allow users to access different functionalities:
- The "Input Box" is where the users can type out their request to the chatbot. As of yet there is no "press enter to send" support
- The "Send Button", so that members can send their typed request
- The "Record Button" which automatically records audio and incerts it in the input box so that the user can edit it. NOTE: The recording ends automatically when a certain silence threshold is met.

## About the Design
The design is simple and clean. It has a dark background with white text and a font (Tektur) that has good readability.

## Images:
### The buttons
<p align="left">
    <img src="/Images/buttons.png" style="border-radius: 18px"/>
</p>

### The chat-box
<p align="left">
    <img src="/Images/chat-box.png" style="border-radius: 18px" width=50%, height=50%/>
</p>
