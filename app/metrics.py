from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter(
    "grade_api_requests_total",
    "Total number of HTTP requests",
    ["method", "endpoint"],
)

REQUEST_LATENCY = Histogram(
    "grade_api_request_latency_seconds",
    "HTTP request latency in seconds",
    ["method", "endpoint"],
)

PREDICTION_COUNT = Counter(
    "grade_api_predictions_total",
    "Total number of grade predictions",
    ["grade_letter"],
)
