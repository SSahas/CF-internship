# CF-internship

Built an fastapi server for which the users can send request and can get the data in the form of stream like chatgpt.The FastAPI server was built using asyncronous programming for efficient use of resources and fast responses.

## Tech stack

- Python
- Javascript
- sqlite

# To run the model 
1. clone the model
   - `https://github.com/SSahas/CF-internship.git`
2. Run the main.py file using the command inside the folder directory
   - `uvicorn main:app --host localhost --port 8000`
3. Run the js_server.js file and make a get request to -`http://localhost:3000/get-data` in postman or any other api testing platform.
4. stream output is produced in postman and also in the terminal in  which js_server.js is running.
   
## Libraries to run main.py 
- fastapi
- pydantic
- uvicorn
- sse-starlette
- psutil
- uuid

## Libraries to run js_server.js
- express
- axios
