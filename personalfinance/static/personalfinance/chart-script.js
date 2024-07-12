// Create the chart instance
const ctx1 = document.getElementById('cashInChart');
let chartData = [];

const myChart = new Chart(ctx1, {
  type: 'bar',
  data: {
    labels: ['Cash In', 'Cash Out', 'Cash Left'],
    datasets: [{
      data: chartData,
      backgroundColor: ['#FF6384'],
      borderWidth: 1,
    }]
  },
  options: {
    plugins: {
      legend: {
        display: false
      }
    },
    responsive: true, // Enable responsiveness
    maintainAspectRatio: false, // Set to false to allow the chart to dynamically resize
    scales: {
      y: {
        beginAtZero: true
      }
    }
  }
});


const ctx2 = document.getElementById('cashFlowChart');
let chartData2 = [];

new Chart(ctx2, {
  type: 'bar',
  data: {
    labels: ['Cash In', 'Cash Out', 'Cash Left'],
    datasets: [{
      data: chartData2,
      backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56'],
      borderWidth: 1,
    }]
  },
  options: {
    plugins: {
      legend: {
          display: false
        }
      },
    responsive: true, // Enable responsiveness
    maintainAspectRatio: false, // Set to false to allow the chart to dynamically resize
    scales: {
      y: {
        beginAtZero: true
      }
    }
  }
});

const ctx3 = document.getElementById('moneyMapChart');
let chartData3 = [];

const labels3 = ["After year 1", "After year 2", "After year 3", "After year 4", "After year 5"];

new Chart(ctx3, {
  type: 'bar',
  data: {
    labels: labels3,
    datasets: [{
      data: chartData3,
      backgroundColor: ['#FFCE56', '#FFCE56', '#FFCE56', '#FFCE56', '#FFCE56'],
      borderWidth: 1,
    }]
  },
  options: {
    plugins: {
      legend: {
          display: false
        }
      },
    responsive: true, // Enable responsiveness
    maintainAspectRatio: false, // Set to false to allow the chart to dynamically resize
    scales: {
      y: {
        beginAtZero: true
      }
    }
  }
});