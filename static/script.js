/*
{static/script.js}
LICENSE: GNU GENERAL PUBLIC LICENSE
*/
document.getElementById('send-btn').addEventListener('click', function() {
    const userInput = document.getElementById('user-input');
    const chatBox = document.getElementById('chat-box');
    
    function addUserMessage(message) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'user-message';
        messageDiv.textContent = `You: ${message}`;
        chatBox.appendChild(messageDiv);
    }  
    
    
    // Function to handle the click event on the "Send" button
    document.getElementById('send-btn').addEventListener('click', function() {
        const userMessage = userInput.value.trim(); // Get the user's input and trim whitespace
        
        if (userMessage !== '') {
            // Display the user's message in the chat
            addUserMessage(userMessage);

            userInput.value = '';

        }
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const textElement = document.querySelector('.animated-text');
    const displayedText = document.getElementById("displayed-text");
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');

    // Function to handle the click event on the "Send" button
    sendBtn.addEventListener('click', function() {
        const userMessage = userInput.value.trim(); // Get the user's input and trim whitespace

        if (userMessage !== '') {
            // Display the user's message in the chat
            addUserMessage(userMessage);

            // Clear the input field after sending
            userInput.value = '';

            // Send the user message to the chatbot
            chatWithBot(userMessage);
        }
    });

    // Function to add user's message to the chat
    function addUserMessage(message) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'user-message';
        messageDiv.textContent = `You: ${message}`;
        const lineElement = document.createElement('hr');
        chatBox.appendChild(messageDiv);
        chatBox.appendChild(lineElement)
    }

    // Function to send user message to the chatbot API
    function chatWithBot(userMessage) {
        // Define the chat endpoint
        const chatEndpoint = '/api/chat';

        // Prepare the JSON data for the POST request
        const data = {
            user_message: userMessage
        };

        // Send a POST request to the chat endpoint
        fetch(chatEndpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            // Display the AI response in the chat
            const aiResponse = data.ai_response;
            addBotMessage(aiResponse);

        })
        .catch(error => {
            console.error('Error sending user message:', error);
        });
    }

    
    // Function to add bot's message to the chat with Markdown support
    function addBotMessage(message) {
        const messageDiv = document.createElement('div');
        const lineElement = document.createElement('hr');
        // Giving the bot-message class
        messageDiv.className = 'bot-message';
        // Converting Markdown to HTML
        const htmlMessage = marked(message);
        // Setting the innerHTML of the messageDiv with the HTML content
        messageDiv.innerHTML = `Diasyndesi: ${htmlMessage}`;
        chatBox.appendChild(messageDiv);
        chatBox.appendChild(lineElement)
    }


    // Event listener for Enter key press in the input box
    userInput.addEventListener('keydown', function (event) {
        if (event.keyCode === 13) {
            event.preventDefault(); // Prevent the default Enter key behavior
            sendBtn.click(); // Trigger the click event for the "Send" button
        }
    });
});

document.getElementById('record-btn').addEventListener('click', function() {
    // Make the API request
    fetch('/api/record', {
        method: 'POST',
    })
    .then(response => {
        // Handle the response status
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        // Parse the JSON response
        return response.json();
    })
    .then(data => {
        //console.log('Transcript:', data.transcript); // Must be removed in production to not spam the console
        const userInput = document.getElementById('user-input');
        userInput.value = data.transcript;
        // You can perform any additional actions with the transcript here
    })
    .catch(error => {
        console.error('Error fetching transcript:', error);
    });
});