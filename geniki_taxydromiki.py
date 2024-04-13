import sys
import requests
from bs4 import BeautifulSoup

if len(sys.argv) == 4: # To be used along with ntfy
    ntfy_server = sys.argv[1]
    ntfy_topic = sys.argv[2]
    tracking_number = sys.argv[3]
    ntfy_dest = f"http://{ntfy_server}/{ntfy_topic}"
elif len(sys.argv) == 2: # To be used as a standalone script
    tracking_number = sys.argv[1]
else:
    print("Usage: python" + ("3" if sys.platform.startswith('linux') else "") + " geniki_taxydromiki.py <tracking_number>")
    sys.exit(1)

url = f"https://www.taxydromiki.com/en/track/{tracking_number}"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Get the last tracking info
last_info = soup.find("div", class_="tracking-checkpoint last form-wrapper")

status = last_info.find("div", class_="checkpoint-status").text.replace("Status", "")
location = last_info.find("div", class_="checkpoint-location").text.replace("Location", "")
date = last_info.find("div", class_="checkpoint-date").text.replace("Date", "")
time = last_info.find("div", class_="checkpoint-time").text.replace("Time", "") # Encode later because in greek

message = f"Status: {status}\nLocation: {location}\nDate/Time: {date}, {time}"

if len(sys.argv) == 4: # To be used along with ntfy
    requests.post(ntfy_dest, headers={"Title": "Geniki Taxydromiki tracking"}, data=message.encode('utf-8'))
elif len(sys.argv) == 2: # To be used as a standalone script
    print(message)
