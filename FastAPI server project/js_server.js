const express = require('express');

const axios = require('axios');

const app = express();

let data = JSON.stringify({
  "query": "Hello, I am sahas. i am here for an interview.",
  "stream": "True"
});

let config = {
  method: 'get',
  maxBodyLength: Infinity,
  url: 'http://localhost:8000/question',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer asmamMSKksaksapSKmskasssmlkappi'
  },
  data: data,
  responseType: 'stream'  // Set the responseType to 'stream'
};

app.use(express.json());
app.get('/get-data', async (req, res) => {

    res.set("Content-Type", "text/event-stream");
  axios.request(config)
    .then((response) => {
      // Log each chunk of data in the stream
      
      response.data.on('data', (chunk) => {
        console.log(chunk.toString());  // Assuming the data is in string format
        res.write(chunk.toString())
      });

      // Handle the end of the stream
      response.data.on('end', () => {
        console.log('Stream ended');
      });
    })
    .catch((error) => {
      console.error(error);
    });

})

const port = process.env.PORT || 3000;

app.listen(port, () => {
  console.log(`Node.js server is running on port ${port}`);
});
