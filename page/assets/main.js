document.addEventListener('DOMContentLoaded', () => {
    const apiUrl = 'http://localhost:5000';  // Update this URL with your Flask API base URL

    const queryBtn = document.getElementById('queryBtn');
    const uploadBtn = document.getElementById('uploadBtn');
    const chatWindow = document.getElementById('chatWindow');  // Target chat window element
    const uploadResponse = document.getElementById('uploadResponse');
    const fileList = document.getElementById('fileList');

    async function loadFileList() {
        try {
            console.log('Loading file list');
            const response = await axios.get(`${apiUrl}/files`);
            const files = response.data.files;
            console.log(files);
    
            const fileList = document.getElementById('fileList');
            fileList.innerHTML = '';  // Clear the current list
    
            files.forEach(file => {
                const listItem = document.createElement('li');
                listItem.classList.add('list-group-item');
                listItem.textContent = file;
    
                // Add a delete button for each file
                const deleteButton = document.createElement('button');
                deleteButton.textContent = 'Delete';
                deleteButton.classList.add('btn', 'btn-danger', 'btn-sm', 'ml-2');
                deleteButton.onclick = () => deleteFile(file);
    
                listItem.appendChild(deleteButton);
                fileList.appendChild(listItem);
            });
        } catch (error) {
            console.error('Error loading file list:', error);
        }
    }

    // Function to append messages to the chat window
    function appendMessage(sender, message) {
        const messageDiv = document.createElement('div');
        
        // Add class based on sender type (user or bot)
        messageDiv.classList.add('message', sender === 'user' ? 'message-user' : 'message-bot');
        
        // Create a text node for the message and append it
        const textNode = document.createTextNode(message);
        messageDiv.appendChild(textNode);
        
        // Append the message to the chat window
        chatWindow.appendChild(messageDiv);

        // Ensure the chat window auto-scrolls to the latest message
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    // Handle query request (now displayed as a chat)
    queryBtn.addEventListener('click', async () => {
        const queryText = document.getElementById('queryText').value;

        if (!queryText) {
            appendMessage('bot', 'Please enter a query!');
            return;
        }

        // Display user's query in the chat window
        
        try {
            appendMessage('user', queryText);
            document.getElementById('queryText').value = '';
            // Make the API request to Flask
            const response = await axios.post(`${apiUrl}/query`, { query_text: queryText });

            // Display API's response in the chat window
            appendMessage('bot', response.data.response);
        } catch (error) {
            appendMessage('bot', 'Error: ' + error.response.data.error);
        }

        // Clear input field after sending the query
        
    });

    // Handle file upload
    uploadBtn.addEventListener('click', async () => {
        const fileInput = document.getElementById('fileInput');
        const file = fileInput.files[0];
        const loadingSymbol = document.getElementById('loadingSymbol');
        const uploadResponse = document.getElementById('uploadResponse');
    
        if (!file) {
            uploadResponse.textContent = 'Please select a file!';
            uploadResponse.classList.remove('d-none');
            return;
        }
    
        const formData = new FormData();
        formData.append('file', file);
    
        try {
            // Show loading symbol
            loadingSymbol.classList.remove('d-none');
            uploadResponse.classList.add('d-none');
    
            const response = await axios.post(`${apiUrl}/upload`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });
    
            // Hide loading symbol
            loadingSymbol.classList.add('d-none');
    
            // Display success message
            uploadResponse.textContent = 'File uploaded successfully!';
            uploadResponse.classList.remove('d-none');
            uploadResponse.classList.remove('alert-info');
            uploadResponse.classList.add('alert-success');
    
            // Reload the file list
            loadFileList();
        } catch (error) {
            // Hide loading symbol
            loadingSymbol.classList.add('d-none');
    
            // Display error message
            uploadResponse.textContent = 'Error: ' + error.response.data.error;
            uploadResponse.classList.remove('d-none');
            uploadResponse.classList.remove('alert-success');
            uploadResponse.classList.add('alert-danger');
        }
    });

    // Handle file deletion
    async function deleteFile(filename) {
        try {
            const response = await axios.post(`${apiUrl}/delete`, { filename });
            alert(response.data.success);
            loadFileList();  // Reload the file list after successful deletion
        } catch (error) {
            alert('Error: ' + error.response.data.error);
        }
    }

    // Load the files list on page load
    loadFileList();
    console.log('BATATA ASSADA');
    
});
