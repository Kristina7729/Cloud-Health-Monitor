import os
import time
import requests
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer

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

        if response.status_code == 200:
            return "HEALTHY", response_time
        else:
            return "DOWN", response_time

    except requests.RequestException:
        return "DOWN", None


def get_results():
    results = []

    for name, url in services.items():
        status, response_time = check_health(url)
        results.append((name, status, response_time))

    return results


class HealthMonitorHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        results = get_results()

        html = """
        <html>
        <head>
            <title>Cloud Health Monitor</title>
            <meta http-equiv="refresh" content="30">
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 40px;
                    background: #f5f7fa;
                }

                h1 {
                    color: #222;
                }

                .service {
                    background: white;
                    padding: 20px;
                    margin: 15px 0;
                    border-radius: 10px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                }

                .healthy {
                    color: green;
                    font-weight: bold;
                }

                .down {
                    color: red;
                    font-weight: bold;
                }
            </style>
        </head>

        <body>
            <h1>Cloud Health Monitor</h1>
            <p>Last checked: %s</p>
            <button onclick="location.reload()">Refresh Now</button>
        """ % datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for name, status, response_time in results:

            if response_time is not None:
                response_text = f"{response_time:.3f} seconds"
            else:
                response_text = "N/A"

            status_class = "healthy" if status == "HEALTHY" else "down"

            html += f"""
            <div class="service">
                <h2>{name}</h2>
                <p>Status:
                    <span class="{status_class}">
                        {status}
                    </span>
                </p>
                <p>Response time: {response_text}</p>
            </div>
            """

        html += """
        </body>
        </html>
        """

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode())


port = int(os.environ.get("PORT", 10000))

server = HTTPServer(("0.0.0.0", port), HealthMonitorHandler)

print("=== CLOUD SERVICE HEALTH MONITOR ===")
print(f"Server running on port {port}")

server.serve_forever()
