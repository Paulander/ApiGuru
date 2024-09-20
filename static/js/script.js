document.addEventListener('DOMContentLoaded', function() {
    const apiCallForm = document.getElementById('apiCallForm');
    const saveCallForm = document.getElementById('saveCallForm');
    const verifyApiKeyForm = document.getElementById('verifyApiKeyForm');
    const predefinedCallsSelect = document.getElementById('predefinedCalls');
    const loadPredefinedCallButton = document.getElementById('loadPredefinedCall');
    const refreshHistoryButton = document.getElementById('refreshHistory');
    const refreshDashboardButton = document.getElementById('refreshDashboard');

    apiCallForm.addEventListener('submit', makeApiCall);
    saveCallForm.addEventListener('submit', savePredefinedCall);
    verifyApiKeyForm.addEventListener('submit', verifyApiKey);
    loadPredefinedCallButton.addEventListener('click', loadPredefinedCall);
    refreshHistoryButton.addEventListener('click', fetchApiCallHistory);
    refreshDashboardButton.addEventListener('click', fetchDashboardData);

    fetchPredefinedCalls();
    fetchApiCallHistory();
    fetchDashboardData();

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
            fetchApiCallHistory();
            fetchDashboardData();
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

    function fetchApiCallHistory() {
        fetch('/get_api_call_history')
        .then(response => response.json())
        .then(history => {
            const historyList = document.getElementById('historyList');
            historyList.innerHTML = '';
            if (history.length === 0 || (history.length === 1 && history[0].message)) {
                const emptyMessage = document.createElement('p');
                emptyMessage.textContent = history[0]?.message || 'No API call history available.';
                historyList.appendChild(emptyMessage);
            } else {
                history.forEach(call => {
                    const callElement = document.createElement('div');
                    callElement.className = 'history-item';
                    callElement.innerHTML = `
                        <h3>${call.method} ${call.url}</h3>
                        <p>Status: ${call.response_status}</p>
                        <p>Response Time: ${call.response_time.toFixed(2)} seconds</p>
                        <p>Timestamp: ${new Date(call.timestamp).toLocaleString()}</p>
                        <details>
                            <summary>Request Details</summary>
                            <pre>${JSON.stringify({headers: call.headers, body: call.body}, null, 2)}</pre>
                        </details>
                        <details>
                            <summary>Response Details</summary>
                            <pre>${JSON.stringify({headers: call.response_headers, body: call.response_body}, null, 2)}</pre>
                        </details>
                    `;
                    historyList.appendChild(callElement);
                });
            }
        })
        .catch(error => {
            console.error('Error fetching API call history:', error);
            alert('Error fetching API call history: ' + error.message);
        });
    }

    function fetchDashboardData() {
        fetch('/get_dashboard_data')
        .then(response => response.json())
        .then(data => {
            updateDashboard(data);
        })
        .catch(error => {
            console.error('Error fetching dashboard data:', error);
            alert('Error fetching dashboard data: ' + error.message);
        });
    }

    function updateDashboard(data) {
        try {
            document.getElementById('totalCalls').textContent = data.total_calls !== undefined ? data.total_calls : 'N/A';
            document.getElementById('avgResponseTime').textContent = data.avg_response_time !== undefined ? `${data.avg_response_time.toFixed(2)} seconds` : 'N/A';

            const methodChartCanvas = document.getElementById('methodChart');
            if (methodChartCanvas.chart) {
                methodChartCanvas.chart.destroy();
            }

            if (data.usage_by_method && Object.keys(data.usage_by_method).length > 0) {
                methodChartCanvas.chart = new Chart(methodChartCanvas, {
                    type: 'pie',
                    data: {
                        labels: Object.keys(data.usage_by_method),
                        datasets: [{
                            data: Object.values(data.usage_by_method),
                            backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF']
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false
                    }
                });
            } else {
                methodChartCanvas.getContext('2d').clearRect(0, 0, methodChartCanvas.width, methodChartCanvas.height);
                methodChartCanvas.getContext('2d').font = '14px Arial';
                methodChartCanvas.getContext('2d').fillText('No data available', 10, 50);
            }

            const topApisList = document.getElementById('topApis');
            topApisList.innerHTML = '';
            if (data.top_apis && data.top_apis.length > 0) {
                data.top_apis.forEach(api => {
                    const listItem = document.createElement('li');
                    listItem.textContent = `${api.url || 'Unknown URL'}: ${api.count || 0} calls`;
                    topApisList.appendChild(listItem);
                });
            } else {
                const listItem = document.createElement('li');
                listItem.textContent = 'No data available';
                topApisList.appendChild(listItem);
            }
        } catch (error) {
            console.error('Error updating dashboard:', error);
            alert('Error updating dashboard: ' + error.message);
        }
    }
});