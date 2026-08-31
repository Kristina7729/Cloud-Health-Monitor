import requests
import time
from datetime import datetime

services = {
    "Google": "https://google.com",
    "GitHub": "https://github.com",
    "Amazon": "https://amazon.com"
}
def check_health(url):
    start_time = time.time()

    try:
        response = requests.get(url, timeout=5)
        response_time = time.time() - start_time

        if response.status_code ==200:
           return"HEALTHY", response_time
        else:
           return"DOWN", response_time

    except requests. RequestException:
        return "DOWN", None
    
print("\n=== CLOUD SERVICE HEALTH MONITOR ===")
print("Check time:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print("------------------------------------") 
print()

for name, url in services.items():
    status, response_time = check_health(url)
    print(name, ":",status)

if response_time is not None:
    print("Response time:",response_time, "seconds")
print()