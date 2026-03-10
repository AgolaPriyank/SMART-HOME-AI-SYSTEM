const API_BASE = '/api';

// State
let sensorChart = null;
let historicalData = [];

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    checkStatus();
    initChart();
    
    // Initial fetch
    fetchDevices();
    fetchLogs();
    fetchSensorData();
    
    // Polling intervals
    setInterval(fetchSensorData, 5000); // Poll sensors every 5s
    setInterval(fetchDevices, 10000); // Poll devices every 10s
    setInterval(fetchLogs, 10000);   // Poll logs every 10s
    setInterval(checkStatus, 30000); // Check API status every 30s
});

// --- API Calls ---

async function checkStatus() {
    try {
        const res = await fetch(`${API_BASE}/status`);
        const data = await res.json();
        
        const apiBadge = document.getElementById('api-status');
        const aiBadge = document.getElementById('ai-status');
        
        if (data.status === 'online') {
            apiBadge.className = 'badge bg-success';
            apiBadge.textContent = 'Online';
        }
        
        if (data.ai_enabled) {
            aiBadge.className = 'badge bg-success';
            aiBadge.innerHTML = '<i class="fa-solid fa-brain"></i> Active';
        } else {
            aiBadge.className = 'badge bg-warning text-dark';
            aiBadge.innerHTML = '<i class="fa-solid fa-triangle-exclamation"></i> Model Missing';
        }
    } catch (e) {
        document.getElementById('api-status').className = 'badge bg-danger';
        document.getElementById('api-status').textContent = 'Offline';
    }
}

async function fetchDevices() {
    try {
        const res = await fetch(`${API_BASE}/devices`);
        const devices = await res.json();
        renderDevices(devices);
    } catch (e) {
        console.error('Failed to fetch devices:', e);
    }
}

async function toggleDevice(id) {
    try {
        // Optimistically update UI
        const checkbox = document.getElementById(`toggle-${id}`);
        checkbox.disabled = true;
        
        const res = await fetch(`${API_BASE}/devices/${id}/toggle`, { method: 'POST' });
        const data = await res.json();
        
        // Final update based on server response
        checkbox.checked = data.device.status === 'ON';
        checkbox.disabled = false;
        
        // Check if label exists before updating
        const labelText = document.getElementById(`status-text-${id}`);
        if(labelText) {
             labelText.textContent = data.device.status;
             labelText.className = `badge fw-bold ms-2 ${data.device.status === 'ON' ? 'bg-success' : 'bg-secondary'}`;
        }
        
        // Refresh logs to show the manual action
        fetchLogs();
    } catch (e) {
        console.error('Failed to toggle device:', e);
        const checkbox = document.getElementById(`toggle-${id}`);
        checkbox.disabled = false;
        checkbox.checked = !checkbox.checked; // Revert on failure
        alert("Failed to communicate with device.");
    }
}

async function fetchLogs() {
    try {
        const res = await fetch(`${API_BASE}/logs?limit=15`);
        const logs = await res.json();
        renderLogs(logs);
    } catch (e) {
        console.error('Failed to fetch logs:', e);
    }
}

async function fetchSensorData() {
    try {
        const res = await fetch(`${API_BASE}/sensors/history?limit=15`);
        const data = await res.json();
        
        if (data.length > 0) {
            updateDashboardCards(data[data.length - 1]); // Latest reading
            updateChart(data);
            document.getElementById('last-update').textContent = new Date().toLocaleTimeString();
        }
    } catch (e) {
        console.error('Failed to fetch sensor data:', e);
    }
}

// --- UI Rendering ---

function renderDevices(devices) {
    const list = document.getElementById('device-list');
    list.innerHTML = '';
    
    if (devices.length === 0) {
        list.innerHTML = '<li class="list-group-item text-center text-muted py-4">No devices found.</li>';
        return;
    }
    
    devices.forEach(d => {
        const isOn = d.status === 'ON';
        
        // Icon based on type
        let icon = 'fa-plug';
        if (d.type === 'Light') icon = 'fa-lightbulb';
        if (d.type === 'Appliance') icon = 'fa-fan';
        if (d.type === 'Security') icon = 'fa-lock';
        
        const badgeClass = isOn ? 'bg-success' : 'bg-secondary';
        
        const li = document.createElement('li');
        li.className = 'list-group-item d-flex justify-content-between align-items-center';
        li.innerHTML = `
            <div>
                <i class="fa-solid ${icon} text-muted me-2 border p-2 rounded-circle bg-light" style="width:36px; height:36px; text-align:center; line-height:20px;"></i>
                <span class="fw-bold">${d.name}</span>
                <span class="badge ${badgeClass} ms-2" id="status-text-${d.id}">${d.status}</span>
                <div class="small text-muted ms-5">${d.type}</div>
            </div>
            <div class="form-check form-switch ms-3">
                <input class="form-check-input fs-4" type="checkbox" role="switch" 
                    id="toggle-${d.id}" 
                    ${isOn ? 'checked' : ''} 
                    onchange="toggleDevice(${d.id})">
            </div>
        `;
        list.appendChild(li);
    });
}

function renderLogs(logs) {
    const tbody = document.getElementById('log-table-body');
    tbody.innerHTML = '';
    
    if (logs.length === 0) {
        tbody.innerHTML = '<tr><td colspan="4" class="text-center text-muted py-3">No automation logs yet.</td></tr>';
        return;
    }
    
    logs.forEach(l => {
        // Backend outputs simple ISO string without timezone info since it uses datetime.utcnow
        // We need to tell Javascript this is UTC time by appending 'Z'
        const time = new Date(l.timestamp + 'Z').toLocaleTimeString();
        
        // Styling based on trigger
        let triggerBadge = '';
        if (l.trigger_type === 'AI') {
            triggerBadge = `<span class="badge bg-primary"><i class="fa-solid fa-brain"></i> AI (${(l.confidence_score*100).toFixed(0)}%)</span>`;
        } else {
            triggerBadge = `<span class="badge bg-secondary"><i class="fa-solid fa-hand-pointer"></i> Manual</span>`;
        }
        
        const actionHtml = l.action.includes('ON') ? 
            `<span class="text-success fw-bold">${l.action}</span>` : 
            `<span class="text-secondary fw-bold">${l.action}</span>`;
            
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td class="text-muted small">${time}</td>
            <td class="fw-bold">${l.device_name}</td>
            <td>${actionHtml}</td>
            <td>${triggerBadge}</td>
        `;
        tbody.appendChild(tr);
    });
}

function updateDashboardCards(latest) {
    // Temperature
    document.getElementById('temp-val').textContent = latest.temperature.toFixed(1);
    
    // Humidity
    document.getElementById('hum-val').textContent = latest.humidity.toFixed(1);
    
    // Light
    document.getElementById('light-val').textContent = latest.light;
    
    // Motion
    const mContainer = document.getElementById('motion-val').parentElement;
    if (latest.motion) {
        document.getElementById('motion-val').textContent = "Detected";
        mContainer.className = "card-text fw-bold text-danger motion-active";
    } else {
        document.getElementById('motion-val').textContent = "Clear";
        mContainer.className = "card-text fw-bold text-success";
    }
}

// --- Charts ---

function initChart() {
    const ctx = document.getElementById('sensorChart').getContext('2d');
    sensorChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [], // Timestamps
            datasets: [
                {
                    label: 'Temperature (°C)',
                    borderColor: 'rgb(13, 110, 253)', // Primary
                    backgroundColor: 'rgba(13, 110, 253, 0.1)',
                    data: [],
                    yAxisID: 'y',
                    tension: 0.3,
                    fill: true
                },
                {
                    label: 'Humidity (%)',
                    borderColor: 'rgb(13, 202, 240)', // Info
                    data: [],
                    yAxisID: 'y',
                    tension: 0.3
                },
                {
                    label: 'Light Level (Scaled/10)',
                    borderColor: 'rgb(255, 193, 7)', // Warning
                    data: [],
                    yAxisID: 'y1',
                    tension: 0.3,
                    borderDash: [5, 5]
                }
            ]
        },
        options: {
            responsive: true,
            interaction: {
                mode: 'index',
                intersect: false,
            },
            scales: {
                x: {
                    display: true,
                    title: { display: false }
                },
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    title: { display: true, text: 'Temp / Hum' }
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    title: { display: true, text: 'Light (Scaled)' },
                    grid: { drawOnChartArea: false } // only draw grid lines for one axis
                }
            },
            plugins: {
                legend: { position: 'top' }
            }
        }
    });
}

function updateChart(data) {
    if (!sensorChart) return;
    
    // Extract data
    // Backend sends UTC without 'Z'. Append 'Z' to treat as UTC, so the browser converts to local time.
    const labels = data.map(d => new Date(d.timestamp + 'Z').toLocaleTimeString([], {hour: '2-digit', minute:'2-digit', second:'2-digit'}));
    const temps = data.map(d => d.temperature);
    const hums = data.map(d => d.humidity);
    // Scale light down slightly so it fits reasonably on a secondary axis without dominating visually if lux is 1000
    const lights = data.map(d => parseFloat(d.light) / 10); 
    
    sensorChart.data.labels = labels;
    sensorChart.data.datasets[0].data = temps;
    sensorChart.data.datasets[1].data = hums;
    sensorChart.data.datasets[2].data = lights;
    
    sensorChart.update('none'); // Update without animation for smoother polling
}
