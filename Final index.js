const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const { spawn } = require('child_process');
const path = require('path');

const app = express();
const PORT = 9000;

app.use(bodyParser.json());
app.use(cors());
app.post('/get-aqi', (req, res) => {
  const { latitude, longitude } = req.body;
  if (!latitude || !longitude) {
      return res.status(400).json({ status: 'error', message: 'Latitude and longitude required' });
  }

  const aqiProcess = spawn('python3', ['AQI_map.py', latitude.toString(), longitude.toString()]);

  let aqiOutput = '';

  aqiProcess.stdout.on('data', (data) => {
      aqiOutput += data.toString().trim();
  });

  aqiProcess.stderr.on('data', (data) => {
      console.error(`stderr: ${data}`);
  });

  aqiProcess.on('close', (code) => {
      if (code !== 0) {
          console.error(`Python process exited with code ${code}`);
          return res.status(500).json({ status: 'error', message: 'AQI script error' });
      }

      res.json({ status: 'success', aqi: aqiOutput });
  });
});


// Endpoint to handle queries
app.post('/query', (req, res) => {
  const query = req.body.query;
  if (!query) {
      return res.status(400).json({ status: 'error', message: 'No query provided' });
  }

  console.log('Received query:', query);

  const intentProcess = spawn('python3', ['combined.py', query]);

  let intentOutput = '';

  intentProcess.stdout.on('data', (data) => {
      intentOutput += data.toString().trim();
  });

  intentProcess.stderr.on('data', (data) => {
      console.error(`stderr: ${data}`);
  });

  intentProcess.on('close', (code) => {
      if (code !== 0) {
          console.error(`Python process exited with code ${code}`);
          return res.status(500).json({ status: 'error', message: 'Intent recognition script error' });
      }

      try {
          const lastLine = intentOutput.split('\n').pop().trim();
          let response;

          try {
              response = JSON.parse(lastLine);
              console.log("Parsed JSON response:", response);
          } catch (jsonError) {
              console.log("Output is not valid JSON, treating as plain text.");
              response = lastLine;
          }

          res.json({ status: 'success', response });
      } catch (err) {
          console.error("Error parsing response from Python script:", err);
          res.status(500).json({ status: 'error', message: 'Error parsing response from Python script' });
      }
  });
});

// Serve static files for heatmaps
app.use('/heatmaps', express.static(path.join(__dirname, 'heatmaps')));

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
