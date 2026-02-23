document.getElementById('uploadForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    const file = fileInput.files[0];
    if (!file) {
        alert('Please select an image file.');
        return;
    }

    const button = event.target.querySelector('button');
    const loading = document.getElementById('loading');
    const resultDiv = document.getElementById('result');

    // Disable button and show loading message
    button.disabled = true;
    loading.style.display = 'block';
    resultDiv.innerHTML = '';

    // Prepare form data to send to the backend
    const formData = new FormData();
    formData.append('file', file);

    try {
        // Make the POST request to the API
        const response = await fetch('http://localhost:5000/predict', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Prediction failed');
        }

        const result = await response.json();
        const confidence = result.confidence; // Assuming confidence is a number (percentage)

        // Check if confidence is less than 95%
        if (confidence < 95) {
            resultDiv.innerHTML = `<p style="color:red;">Prediction confidence is too low (${confidence}%). Please retake the photo for a more accurate prediction.</p>`;
        } else {
            // Display the result with highlighted prediction
            resultDiv.innerHTML = `
                Predicted Class: <span class="highlight">${result.predicted_class}</span><br>
                Confidence: <span class="highlight">${confidence}%</span>`;
        }
    } catch (error) {
        resultDiv.innerHTML = `<p style="color:red;">Error: ${error.message}</p>`;
    } finally {
        // Re-enable the button and hide the loading message
        button.disabled = false;
        loading.style.display = 'none';
    }
});
