const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const { spawn } = require('child_process');
const path = require('path');

const app = express();
const PORT = 9000;

// Middleware to parse JSON bodies and handle CORS
app.use(bodyParser.json());
app.use(cors());

// Endpoint to get AQI based on latitude and longitude
app.post('/get-aqi', (req, res) => {
  const { latitude, longitude } = req.body;
  
  // Check if latitude and longitude are provided
  if (!latitude || !longitude) {
      return res.status(400).json({ status: 'error', message: 'Latitude and longitude required' });
  }

  // Spawn a Python process to run AQI_map.py with lat and lon
  const aqiProcess = spawn('python3', ['AQI_map.py', latitude.toString(), longitude.toString()]);

  let aqiOutput = '';

  // Capture output from the Python script
  aqiProcess.stdout.on('data', (data) => {
      aqiOutput += data.toString().trim();
  });

  // Log any errors from the Python script
  aqiProcess.stderr.on('data', (data) => {
      console.error(`stderr: ${data}`);
  });

  // Handle the closing of the Python process
  aqiProcess.on('close', (code) => {
      if (code !== 0) {
          console.error(`Python process exited with code ${code}`);
          return res.status(500).json({ status: 'error', message: 'AQI script error' });
      }

      // Send the AQI result back to the client
      res.json({ status: 'success', aqi: aqiOutput });
  });
});

// Endpoint to handle general queries
app.post('/query', (req, res) => {
  const query = req.body.query;
  
  // Check if a query is provided
  if (!query) {
      return res.status(400).json({ status: 'error', message: 'No query provided' });
  }

  console.log('Received query:', query);

  // Spawn a Python process to run combined.py with the query
  const intentProcess = spawn('python3', ['combined.py', query]);

  let intentOutput = '';

  // Capture output from the Python script
  intentProcess.stdout.on('data', (data) => {
      intentOutput += data.toString().trim();
  });

  // Log any errors from the Python script
  intentProcess.stderr.on('data', (data) => {
      console.error(`stderr: ${data}`);
  });

  // Handle the closing of the Python process
  intentProcess.on('close', (code) => {
      if (code !== 0) {
          console.error(`Python process exited with code ${code}`);
          return res.status(500).json({ status: 'error', message: 'Intent recognition script error' });
      }

      try {
          // Parse the last line of output as JSON
          const lastLine = intentOutput.split('\n').pop().trim();
          let response;

          try {
              response = JSON.parse(lastLine);
              console.log("Parsed JSON response:", response);
          } catch (jsonError) {
              console.log("Output is not valid JSON, treating as plain text.");
              response = lastLine;
          }

          // Send the response back to the client
          res.json({ status: 'success', response });
      } catch (err) {
          console.error("Error parsing response from Python script:", err);
          res.status(500).json({ status: 'error', message: 'Error parsing response from Python script' });
      }
  });
});

// Serve static files (like heatmap images) from the /heatmaps directory
app.use('/heatmaps', express.static(path.join(__dirname, 'heatmaps')));

// Start the server and listen on the specified port
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
