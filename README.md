# Address Book Application
Address Book Application using Python, FastAPI, SQLite, and GeoPy


## Setup

### 1. Clone repository:
git clone https://github.com/AivanChua/address-book-application.git
    
### 2. Install dependencies (if needed)
Terminal command:
pip install fastapi uvicorn geopy
(For issues with above command, can try this line)
python -m pip install fastapi uvicorn geopy

### 3. Running the application
Terminal command:
python -m uvicorn main:app

### 4. FastAPI's Swagger Doc for API testing
Swagger UI: http://127.0.0.1:8000/docs

### APIs

1. Adding address record
Adding a record only needs a name of the location.

2. Updating address record
To update any record, the given name of the address must be provided as well as the new latitude and longitude values in decimal form.

3. Deleting address record
To delete a record, the given name of the address must be provided.

4. Retrieve address records
No specific input needed to retrieve all records.