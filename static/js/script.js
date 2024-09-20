document.addEventListener('DOMContentLoaded', function() {
    const apiCallForm = document.getElementById('apiCallForm');
    const saveCallForm = document.getElementById('saveCallForm');
    const verifyApiKeyForm = document.getElementById('verifyApiKeyForm');
    const predefinedCallsSelect = document.getElementById('predefinedCalls');
    const loadPredefinedCallButton = document.getElementById('loadPredefinedCall');

    apiCallForm.addEventListener('submit', makeApiCall);
    saveCallForm.addEventListener('submit', savePredefinedCall);
    verifyApiKeyForm.addEventListener('submit', verifyApiKey);
    loadPredefinedCallButton.addEventListener('click', loadPredefinedCall);

    fetchPredefinedCalls();

    function makeApiCall(e) {
        e.preventDefault();
        const url = document.getElementById('url').value;
        const method = document.getElementById('method').value;
        const headers = JSON.parse(document.getElementById('headers').value || '{}');
        const body = JSON.parse(document.getElementById('body').value || '{}');

        fetch('/make_request', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url, method, headers, body })
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('response').textContent = JSON.stringify(data, null, 2);
        })
        .catch(error => {
            document.getElementById('response').textContent = 'Error: ' + error.message;
        });
    }

    function savePredefinedCall(e) {
        e.preventDefault();
        const name = document.getElementById('callName').value;
        const url = document.getElementById('saveUrl').value;
        const method = document.getElementById('saveMethod').value;
        const headers = JSON.parse(document.getElementById('saveHeaders').value || '{}');
        const body = JSON.parse(document.getElementById('saveBody').value || '{}');

        fetch('/save_predefined_call', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name, url, method, headers, body })
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            fetchPredefinedCalls();
        })
        .catch(error => {
            alert('Error: ' + error.message);
        });
    }

    function verifyApiKey(e) {
        e.preventDefault();
        const apiKey = document.getElementById('apiKey').value;

        fetch('/verify_api_key', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ api_key: apiKey })
        })
        .then(response => response.json())
        .then(data => {
            const statusElement = document.getElementById('apiKeyStatus');
            statusElement.textContent = data.is_valid ? 'API Key is valid' : 'API Key is invalid';
            statusElement.style.color = data.is_valid ? 'green' : 'red';
        })
        .catch(error => {
            alert('Error: ' + error.message);
        });
    }

    function fetchPredefinedCalls() {
        fetch('/get_predefined_calls')
        .then(response => response.json())
        .then(calls => {
            predefinedCallsSelect.innerHTML = '<option value="">Select a predefined call</option>';
            calls.forEach(call => {
                const option = document.createElement('option');
                option.value = JSON.stringify(call);
                option.textContent = call.name;
                predefinedCallsSelect.appendChild(option);
            });
        })
        .catch(error => {
            alert('Error fetching predefined calls: ' + error.message);
        });
    }

    function loadPredefinedCall() {
        const selectedCall = JSON.parse(predefinedCallsSelect.value);
        if (selectedCall) {
            document.getElementById('url').value = selectedCall.url;
            document.getElementById('method').value = selectedCall.method;
            document.getElementById('headers').value = JSON.stringify(selectedCall.headers, null, 2);
            document.getElementById('body').value = JSON.stringify(selectedCall.body, null, 2);
        }
    }
});
