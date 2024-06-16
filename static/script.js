document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('executeButton').addEventListener('click', submitForm);
});

function submitForm() {
    const pais = document.getElementById('pais').value;
    const renta = document.getElementById('renta').value;

    fetch('/process', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ pais: pais, renta: renta })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            throw new Error(data.error);
        }
        document.getElementById('resultDiv').innerText = 'Result: ' + data.result;
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('resultDiv').innerText = 'An error occurred: ' + error.message;
    });
}
