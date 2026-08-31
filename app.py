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
        total_services = len(results)
        healthy_services = sum(1 for _, status, _ in results if status == "HEALTHY")
        down_services = sum(1 for _, status, _ in results if status == "DOWN")
        html = """
        <html>
        <head>
            <title>Cloud Health Monitor</title>
            <meta http-equiv="refresh" content="30">
           <style>
    body {
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 40px;
        background: linear-gradient(135deg, #f8f5ff, #fff7fb);
        color: #27233a;
    }

    .container {
        max-width: 900px;
        margin: 0 auto;
    }

    h1 {
        font-size: 38px;
        margin-bottom: 8px;
        color: #30264d;
    }

    .subtitle {
        color: #77718a;
        font-size: 16px;
        margin-bottom: 30px;
    }

    .overview {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 18px;
        margin-bottom: 30px;
    }

    .stat {
        background: white;
        padding: 22px;
        border-radius: 18px;
        box-shadow: 0 8px 25px rgba(80, 60, 120, 0.08);
    }

    .stat-label {
        font-size: 14px;
        color: #817a91;
        margin-bottom: 8px;
    }

    .stat-value {
        font-size: 28px;
        font-weight: bold;
        color: #49366d;
    }

    .service {
        background: white;
        padding: 25px;
        margin: 16px 0;
        border-radius: 18px;
        box-shadow: 0 8px 25px rgba(80, 60, 120, 0.08);
        border: 1px solid #eee9f5;
    }

    .service h2 {
        margin-top: 0;
        color: #30264d;
    }

    .healthy {
        color: #24945a;
        font-weight: bold;
        background: #eaf8f0;
        padding: 6px 12px;
        border-radius: 20px;
        display: inline-block;
    }

    .down {
        color: #d94b68;
        font-weight: bold;
        background: #fff0f3;
        padding: 6px 12px;
        border-radius: 20px;
        display: inline-block;
    }

    button {
        background: #7654a6;
        color: white;
        border: none;
        padding: 12px 22px;
        border-radius: 12px;
        font-size: 15px;
        font-weight: bold;
        cursor: pointer;
        margin-bottom: 25px;
        box-shadow: 0 5px 15px rgba(118, 84, 166, 0.25);
    }

    button:hover {
        opacity: 0.9;
        transform: translateY(-1px);
    }

    .last-check {
        color: #817a91;
        margin-bottom: 15px;
    }
</style>
        </head>

       <body>
<div class="container">

    <h1>☁️ Cloud Health Monitor</h1>

    <p class="subtitle">Real-time cloud service health monitoring</p>

    <p class="last-check">Last checked: %s</p>

    <button onclick="location.reload()">↻ Refresh Now</button>

    <div class="overview">
        <div class="stat">
            <div class="stat-label">Services Monitored</div>
            <div class="stat-value">%d</div>
        </div>

        <div class="stat">
            <div class="stat-label">Healthy</div>
            <div class="stat-value">%d</div>
        </div>

        <div class="stat">
            <div class="stat-label">Down</div>
            <div class="stat-value">%d</div>
        </div>
    </div>
       """ % (total_services, healthy_services, down_services, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

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
