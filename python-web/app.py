from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    """Return the main webpage."""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CSE644 Python Docker App</title>

        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f4f7fb;
                margin: 0;
                color: #1f2937;
            }

            .container {
                max-width: 760px;
                margin: 80px auto;
                padding: 40px;
                background: white;
                border-radius: 12px;
                box-shadow: 0 8px 22px rgba(0, 0, 0, 0.12);
                text-align: center;
            }

            h1 {
                color: #2563eb;
            }

            .status {
                margin-top: 25px;
                color: #166534;
                font-weight: bold;
            }
        </style>
    </head>

    <body>
        <main class="container">
            <h1>CSE644 Python Web Server</h1>

            <p>
                This Flask application is running inside a Docker container.
            </p>

            <p>
                The application is configured to use port 8888.
            </p>

            <p>
                Student: Rod Raemon Alvero
            </p>

            <div class="status">
                Python Container Running Successfully
            </div>
        </main>
    </body>
    </html>
    """


@app.route("/health")
def health():
    """Return a health-check response."""
    return jsonify(
        status="healthy",
        service="cse644-python-web",
        port=8888
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888)