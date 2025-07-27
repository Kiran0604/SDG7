document.addEventListener('DOMContentLoaded', () => {
    // Initialize Chart.js for Energy Consumption Trend
    const ctx = document.getElementById('energy-chart').getContext('2d');
    const energyChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            datasets: [{
                label: 'Energy Consumption (kWh)',
                data: [12, 19, 3, 5, 2, 3, 9],
                borderColor: 'rgb(13, 148, 136)',
                backgroundColor: 'rgba(13, 148, 136, 0.2)',
                fill: true,
                tension: 0.4,
                pointBackgroundColor: 'rgb(13, 148, 136)',
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: 'rgb(13, 148, 136)'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        font: {
                            family: 'Poppins',
                            size: 14
                        }
                    }
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Day of Week',
                        font: {
                            family: 'Poppins',
                            size: 14
                        }
                    },
                    grid: {
                        display: false
                    }
                },
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Energy (kWh)',
                        font: {
                            family: 'Poppins',
                            size: 14
                        }
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.1)'
                    }
                }
            }
        }
    });

    // Handle Appliance Form Submission
    document.getElementById('appliance-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(e.target);
        const response = await fetch('/add_appliance', {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        
        // Add appliance to real-time display
        const applianceList = document.getElementById('appliance-list');
        const applianceDiv = document.createElement('div');
        applianceDiv.className = 'border-b pb-2 animate-fade-in';
        applianceDiv.innerHTML = `
            <p class="font-medium">${data.name}</p>
            <p class="text-sm text-gray-600">Power: ${data.power}W, Hours: ${data.hours}</p>
        `;
        applianceList.appendChild(applianceDiv);

        // Update total power
        const totalPower = document.getElementById('total-power');
        totalPower.textContent = parseInt(totalPower.textContent) + parseInt(data.power);

        e.target.reset();
    });

    // Handle Feedback Form Submission
    document.getElementById('feedback-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(e.target);
        const response = await fetch('/submit_feedback', {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        alert(data.message);
        e.target.reset();
    });
});