import requests
from sqlalchemy import create_engine, Column, String, DateTime, Float, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Float, Integer
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class ImageData(Base):
    __tablename__ = 'image_data'
    id = Column(Integer, primary_key=True, autoincrement=True)
    class_type = Column(String)
    image = Column(String)
    date_imported = Column(DateTime, default=datetime.utcnow)
    latitude = Column(Float, default=0.0)
    longitude = Column(Float, default=0.0)
    status = Column(String, default='1')

# ... rest of the code remains unchanged ...


# Create a SQLite database in memory (you can replace this URL with your actual database URL)
engine = create_engine('sqlite:///instance/site.db')

# Create the table in the database
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Replace this URL with the actual API endpoint
api_url = 'http://127.0.0.1:5002/api/contents'

# Make a request to the API
response = requests.get(api_url)

# Print the API response for debugging
print(response.text)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the JSON data from the API response
    api_data = response.json()

    # Check if the response has a "contents" key and it is a list
    if "contents" in api_data and "contents" in api_data["contents"]:
        # Insert data into the database
        for content in api_data["contents"]["contents"]:
            if isinstance(content, str):

                new_row = ImageData(class_type=content, image='')
                # Will try to mege the data from formx
                session.add(new_row)
                print("in if statement")
            elif isinstance(content, dict):
                # Assuming "class_type" and "image" are keys in the dictionary
                new_row = ImageData(class_type=content.get('class_type', ''), image=content.get('image', ''))
                session.add(new_row)
                print("in eliif statement")
            else:
                print(f"Warning: Invalid data format for content: {content}")

        # Commit the changes
        session.commit()
    else:
        print("Error: Invalid API response format.")
else:
    print(f"Error: Unable to fetch data from the API. Status code: {response.status_code}")

# Close the session
session.close()


#note: This code will upload the detected classes. Each classes will be assigned a specific row. 