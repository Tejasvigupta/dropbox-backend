# Dropbox-backend
Requirements:
1. Python version 3.10
2. Git

Steps:
1. Clone the repository using git clone in the terminal.
git clone https://github.com/Tejasvigupta/dropbox-backend.git
2. Cd into the dropbox-backend folder if not already.
3. Create a virtual environment using virtualenv package.
If not installed install virtualenv package using : ```pip install virtualenv```
Type virtualenv venv to create a virtual environment nameD venv.
4. To activate the virtual environment
   a. Windows: venv/scripts/activate
   b. Linux: venv/bin/activate
5. Installing dependencies:
pip install -r requiremnts.txt
6. Run the webapp using
   ```fastapi dev main.py``` (for development mode) or
   ```uvicorn main:app --host 127.0.0.1 --port 8000```
   you can use any host and port

Note:
I have used sqlite DB and local storage for storing files.
On starting the app, DB and "Files" folder will be created by itself.

Endpoints available:
1. POST /files/upload :
This endpoint saves file to local storage and meta data to DB and returns "file_id" for referencing that particular file.
Takes input file from form-data with ```key="file"``` 

2. GET /files/{file_id} :
This endpoint returns the file saved in DB if it exists.

3. PUT /files/{file_id} :
This endpoint is used to update either the file or filename.
Takes input from form-data ```key="new_filename"``` and ```value=str``` to chnange file name
and ``key="file"``

4. DELETE /files/{file_id} :
This endpoint deletes file from local storage and metadata from DB if it exists

5. GET /files :
This end point return all the files currently present in local storage.

6. GET / :
This endpoint returns ```Hello World!```

For more documentation : You can simply use ```host:port/docs```
