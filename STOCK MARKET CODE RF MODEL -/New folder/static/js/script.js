document.addEventListener('DOMContentLoaded', function () {
    const stockSymbol = 'AAPL';  // Default stock symbol
    let isPlaying = true;
    let animationSpeed = 5;
    let animationInterval;
    let currentDataIndex = 0;
    let fullData = { dates: [], prices: [] };

    // Initialize Chart.js
    const ctx = document.getElementById('stockChart').getContext('2d');
    const stockChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [], // Dates will go here
            datasets: [{
                label: `${stockSymbol} Price`,
                data: [], // Prices will go here
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1,
                fill: false
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            aspectRatio: 2, /* Set a reasonable aspect ratio */
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Date'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Price ($)'
                    }
                }
            },
            layout: {
                padding: {
                    top: 10,
                    bottom: 10,
                    left: 10,
                    right: 10
                }
            }
        }
    });

    // Fetch Prediction Data
    async function fetchPredictionData() {
        try {
            console.log('Fetching prediction data...');
            const response = await fetch('/api/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ stockSymbol: stockSymbol }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            console.log('Prediction data received:', data);

            // Store full data for animation
            fullData = {
                dates: data.dates || [],  // Ensure dates array is populated
                prices: data.prices || []  // Ensure prices array is populated
            };

            console.log('Full Data:', fullData);  // Debugging line to check data

            currentDataIndex = 0;

            // Start animation
            startAnimation();

            // Update live stock price (using the latest predicted price as a placeholder)
            document.getElementById('liveStockPrice').textContent = `$${data.prices[data.prices.length - 1].toFixed(2)}`;

        } catch (error) {
            console.error('Error fetching prediction data:', error);
            document.getElementById('liveStockPrice').textContent = 'N/A';
        }
    }

    // Animation functions for the chart
    function startAnimation() {
        console.log('Starting animation...');
        if (animationInterval) clearInterval(animationInterval);

        if (isPlaying && fullData.dates.length > 0) {
            animationInterval = setInterval(() => {
                if (currentDataIndex < fullData.dates.length) {
                    // Show data up to current index
                    stockChart.data.labels = fullData.dates.slice(0, currentDataIndex + 1);  // Update the labels
                    stockChart.data.datasets[0].data = fullData.prices.slice(0, currentDataIndex + 1);  // Update the data

                    // Update live price
                    document.getElementById('liveStockPrice').textContent = `$${fullData.prices[currentDataIndex].toFixed(2)}`;

                    stockChart.update();  // Update the chart with new data

                    currentDataIndex++; // Move to the next data point
                } else {
                    // Animation complete, restart from the beginning
                    currentDataIndex = 0;
                    console.log('Animation complete, restarting...');
                }
            }, 1000 / animationSpeed); // Speed control
        }
    }

    function stopAnimation() {
        if (animationInterval) {
            clearInterval(animationInterval);
            animationInterval = null;
        }
    }

    // Control event listeners for play/pause and speed control
    document.getElementById('playPauseBtn').addEventListener('click', function () {
        isPlaying = !isPlaying;
        this.textContent = isPlaying ? '⏸️ Pause' : '▶️ Play';

        if (isPlaying) {
            startAnimation();
        } else {
            stopAnimation();
        }
    });

    document.getElementById('speedSlider').addEventListener('input', function () {
        animationSpeed = parseInt(this.value);
        document.getElementById('speedValue').textContent = animationSpeed + 'x';

        if (isPlaying) {
            startAnimation(); // Restart with new speed
        }
    });

    // Download chart data as CSV
    document.getElementById('downloadBtn').addEventListener('click', function () {
        if (fullData.dates.length > 0) {
            // Create CSV content
            let csvContent = "Date,Price\n";
            for (let i = 0; i < fullData.dates.length; i++) {
                csvContent += `${fullData.dates[i]},${fullData.prices[i]}\n`;
            }

            // Download CSV
            const blob = new Blob([csvContent], { type: 'text/csv' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `${stockSymbol}_stock_data.csv`;
            a.click();
            window.URL.revokeObjectURL(url);
        }
    });

    // Fetch Historical Data
async function fetchHistoricalData() {
    try {
        console.log('Fetching historical data...');
        const response = await fetch('/api/historical_data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ stockSymbol: stockSymbol, period: '1y' }), // Fetch 1 year data
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log('Historical data received:', data);

        if (data.error) {
            document.getElementById('historicalDataTable').innerHTML = `<p>Error: ${data.error}</p>`;
            return;
        }

        // Populate the table with the historical data
        let tableHtml = '<table><thead><tr><th>Date</th><th>Close Price</th></tr></thead><tbody>';

        // Slice the last 10 data points for display (you can change this as needed)
       // const displayData = data.slice(-10); // Get the last 10 entries
        
        data.forEach(row => {
            tableHtml += `<tr><td>${row.Date}</td><td>$${row.Close.toFixed(2)}</td></tr>`;
        });
        //displayData.forEach(row => {
        //    tableHtml += `<tr><td>${row.Date}</td><td>$${row.Close.toFixed(2)}</td></tr>`;
        //});
        tableHtml += '</tbody></table>';
        document.getElementById('historicalDataTable').innerHTML = tableHtml;

        // Update the chart with historical data
        const labels = data.map(item => item.Date);
        const prices = data.map(item => item.Close);

        stockChart.data.labels = labels;
        stockChart.data.datasets[0].data = prices;
        stockChart.update();

    } catch (error) {
        console.error('Error fetching historical data:', error);
        document.getElementById('historicalDataTable').innerHTML = '<p>Could not load historical data.</p>';
    }
}

    // Update current time
    function updateTime() {
        const now = new Date();
        const timeString = now.toLocaleTimeString('en-US', {
            hour12: true,
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });
        document.getElementById('currentTime').textContent = timeString;
    }

    // Update time every second
    setInterval(updateTime, 1000);
    updateTime(); // Initial call

    // Fetch the data
    fetchPredictionData();  // Initial call for prediction data
    fetchHistoricalData();  // Initial call for historical data
});
