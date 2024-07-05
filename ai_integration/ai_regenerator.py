import os
import json
import websockets
from loguru import logger
from ai_integration.openai import OpenAIHTMLParser
# from ai_integration.anthropic import Anthropic
# from ai_integration.claude_opus import ClaudeOpus
# from ai_integration.sonnet import Sonnet

class AIRegenerator:
    def __init__(self, api_key=None, model="openai", model_name="davinci"):
        self.api_key = api_key or os.getenv(f"{model.upper()}_API_KEY")
        self.model = model
        self.model_name = model_name

        if model == "openai":
            self.parser = OpenAIHTMLParser(self.api_key, model_name)
        elif model == "anthropic":
            self.parser = Anthropic(self.api_key)
        elif model == "claude_opus":
            self.parser = ClaudeOpus(self.api_key)
        elif model == "sonnet":
            self.parser = Sonnet(self.api_key)
        else:
            raise ValueError("Unsupported AI model")

    async def analyze_and_notify(self, html_content, prompt=None):
        logger.info(f"Analyzing HTML content with {self.model}")
        important_data = self.parser.parse(html_content, prompt)
        async with websockets.connect("ws://localhost:6789") as websocket:
            await websocket.send(json.dumps({"important_data": important_data}))

    def parse(self, html_content, prompt=None):
        return self.parser.parse(html_content, prompt)

    def generate_site(self, data):
        site_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Generated Site</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                .container { max-width: 800px; margin: auto; }
                h1 { text-align: center; }
                .data-point { background: #f4f4f4; padding: 10px; margin: 10px 0; border-radius: 5px; }
                .chart-container { width: 100%; height: 400px; }
            </style>
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
            <script>
                const socket = new WebSocket("ws://localhost:6789");
                socket.onmessage = function(event) {
                    const data = JSON.parse(event.data);
                    const container = document.getElementById("data-container");
                    data.forEach(point => {
                        const div = document.createElement("div");
                        div.className = "data-point";
                        div.innerHTML = `<strong>${point.label}:</strong> ${point.value}`;
                        container.appendChild(div);
                    });
                    // Update charts if applicable
                    updateCharts(data);
                };

                function updateCharts(data) {
                    // Implement chart update logic here using Chart.js
                }
            </script>
        </head>
        <body>
            <div class="container">
                <h1>Scraped Data</h1>
                <div id="data-container">
                    {data_points}
                </div>
                <div class="chart-container">
                    <canvas id="chart"></canvas>
                </div>
            </div>
            <script>
                const ctx = document.getElementById('chart').getContext('2d');
                const chart = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: {labels},
                        datasets: [{
                            label: 'Data Points',
                            data: {values},
                            backgroundColor: 'rgba(75, 192, 192, 0.2)',
                            borderColor: 'rgba(75, 192, 192, 1)',
                            borderWidth: 1
                        }]
                    },
                    options: {
                        scales: {
                            y: {
                                beginAtZero: true
                            }
                        }
                    }
                });
            </script>
        </body>
        </html>
        """
        labels = [k for k, v in data.items()]
        values = [v for k, v in data.items()]
        data_points_html = "".join([f'<div class="data-point"><strong>{k}:</strong> {v}</div>' for k, v in data.items()])
        return site_template.format(data_points=data_points_html, labels=json.dumps(labels), values=json.dumps(values))
