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
    responseType: 'stream'
};

app.use(express.json());
app.get('/get-data', async (req, res) => {
    res.set("Content-Type", "text/event-stream");


    let full = "";
    const response = await axios.request(config);

    // Log data chunks
    response.data.on('data', (chunk) => {
        
        const eventData = chunk.toString().split('\n');
        eventData.forEach((event) => {
            if (event.startsWith('data:')) {
                const dataValue = event.replace('data: ', '');
                full += JSON.stringify(`${dataValue}`);
                console.clear();
                console.log(full);
                res.write(`data: ${dataValue}\n\n`);
            }
        });
    });

    // Handle the end of the stream
    response.data.on('end', () => {
        console.log('Stream ended');
        //res.end();
    });

});

const port = process.env.PORT || 3000;

app.listen(port, () => {
    console.log(`Node.js server is running on port ${port}`);
});
