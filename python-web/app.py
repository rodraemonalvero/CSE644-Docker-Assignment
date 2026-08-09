import os

from flask import Flask, Response, jsonify, request
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest


app = Flask(__name__)


# ---------------------------------------------------------
# Prometheus application metrics
# ---------------------------------------------------------

REQUEST_COUNT = Counter(
    "cse644_http_requests_total",
    "Total HTTP requests received by the CSE644 Python application",
    ["method", "endpoint", "status"],
)

HOME_REQUEST_COUNT = Counter(
    "cse644_home_requests_total",
    "Total requests to the CSE644 application home page",
)


# ---------------------------------------------------------
# Helper functions
# ---------------------------------------------------------

def protected_value_loaded() -> bool:
    """Return whether the protected value was supplied without revealing it."""
    return bool(os.getenv("APP_PROTECTED_VALUE"))


# ---------------------------------------------------------
# Main application page
# ---------------------------------------------------------

@app.route("/")
def home():
    """Return the customized application page."""

    HOME_REQUEST_COUNT.inc()

    public_message = os.getenv(
        "PUBLIC_MESSAGE",
        "Welcome to the CSE644 Kubernetes application.",
    )

    environment_name = os.getenv(
        "APP_ENVIRONMENT",
        "local",
    )

    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>CSE644 GitOps and Observability App</title>

    <style>
        body {{
            font-family: Arial, sans-serif;
            background: #f4f7fb;
            margin: 0;
            color: #1f2937;
        }}

        .container {{
            max-width: 760px;
            margin: 80px auto;
            padding: 40px;
            background: white;
            border-radius: 12px;
            box-shadow: 0 8px 22px rgba(0, 0, 0, 0.12);
            text-align: center;
        }}

        h1 {{
            color: #2563eb;
        }}

        .message {{
            margin: 25px 0;
            padding: 15px;
            background: #eff6ff;
            border-radius: 8px;
            font-weight: bold;
        }}

        .status {{
            margin-top: 20px;
            color: #166534;
            font-weight: bold;
        }}

        .assignment {{
            margin-top: 20px;
            color: #4b5563;
        }}
    </style>
</head>

<body>
    <main class="container">

        <h1>CSE644 Python Web Server</h1>

        <p>Student: Rod Raemon Alvero</p>

        <div class="message">
            {public_message}
        </div>

        <p>
            Environment: {environment_name}
        </p>

        <p>
            Protected application value received:
            <strong>{str(protected_value_loaded()).lower()}</strong>
        </p>

        <div class="status">
            Python Kubernetes Workload Running Successfully
        </div>

        <div class="assignment">
            Assignment 03 - GitOps and Application Observability
        </div>

    </main>
</body>
</html>
"""


# ---------------------------------------------------------
# Kubernetes health endpoints
# ---------------------------------------------------------

@app.route("/health/live")
def liveness():
    """Confirm that the Flask process is running."""

    return jsonify(
        status="alive",
        service="cse644-python-web",
    ), 200


@app.route("/health/ready")
def readiness():
    """Confirm that the application is ready to receive requests."""

    return jsonify(
        status="ready",
        service="cse644-python-web",
        configuration_loaded=bool(os.getenv("PUBLIC_MESSAGE")),
        protected_value_loaded=protected_value_loaded(),
    ), 200


@app.route("/health")
def health():
    """Provide a general application health response."""

    return jsonify(
        status="healthy",
        service="cse644-python-web",
        port=8888,
        protected_value_loaded=protected_value_loaded(),
    ), 200


# ---------------------------------------------------------
# Prometheus metrics endpoint
# ---------------------------------------------------------

@app.route("/metrics")
def metrics():
    """Expose Prometheus metrics for application monitoring."""

    return Response(
        generate_latest(),
        mimetype=CONTENT_TYPE_LATEST,
    )


# ---------------------------------------------------------
# Record HTTP requests for Prometheus
# ---------------------------------------------------------

@app.after_request
def record_request(response):
    """Record request method, endpoint, and HTTP status."""

    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.path,
        status=response.status_code,
    ).inc()

    return response


# ---------------------------------------------------------
# Local development entry point
# ---------------------------------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888)