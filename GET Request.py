import os
import json
import requests
import hashlib
import pandas as pd
import time

# Function to send request and return response content
def send_request(url, username, password):
    # Set up Basic Authentication
    auth = (username, password)
    
    # Print request URL for debugging
    print("Request URL:", url)
    
    # Send the request
    response = requests.get(url, auth=auth)
    #time.sleep(5)
    
    # Check if request was successful
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve data from {url}. Status code: {response.status_code}")
        return None

# Get the desktop path
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# Specify the full path to the Excel file
excel_file = os.path.join(desktop_path, "URLs.xlsx")

# Specify the output directory for JSON files
output_directory = os.path.join(os.path.expanduser("~"), "Documents", "responses")

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

username = 'username'
password = 'password'

# Read URLs from Excel file
df = pd.read_excel(excel_file, header=None, names=["URL"])

# Create a list to store URLs without data
urls_without_data = []

# Iterate over URLs
for index, row in df.iterrows():
    url = row["URL"].strip()  # Extract URL
    if url:
        response = send_request(url, username, password)
        if response:
            # Generate a unique filename based on URL content
            filename = hashlib.md5(url.encode()).hexdigest() + ".json"
            # Save the response as JSON
            output_file = os.path.join(output_directory, filename)
            with open(output_file, 'w') as file:
                json.dump(response, file)
            print(f"Response for {url} saved to {output_file}")
        else:
            # If no response, add URL to list
            urls_without_data.append(url)

# Save URLs without data to a separate sheet in the Excel file
if urls_without_data:
    with pd.ExcelWriter(excel_file, mode='a', engine='openpyxl') as writer:
        pd.DataFrame({"URL": urls_without_data, "Status": ["No data"] * len(urls_without_data)}).to_excel(writer, sheet_name='No_Data', index=False)

print("All responses saved as separate JSON files in 'Documents/responses'.")
