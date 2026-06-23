from prometheus_client import Counter
from prometheus_client import Histogram


# ==========================================================
# Request Metrics
# ==========================================================

REQUEST_COUNT = Counter(
    "product_intelligence_requests_total",
    "Total product intelligence requests",
    ["method", "path", "status_code"],
)

REQUEST_DURATION = Histogram(
    "product_intelligence_request_duration_seconds",
    "Product intelligence request duration in seconds",
    ["method", "path"],
)


# ==========================================================
# Cache Metrics
# ==========================================================

CACHE_HITS = Counter(
    "product_intelligence_cache_hits_total",
    "Total cache hits",
    ["endpoint"],
)

CACHE_MISSES = Counter(
    "product_intelligence_cache_misses_total",
    "Total cache misses",
    ["endpoint"],
)


# ==========================================================
# Authentication Metrics
# ==========================================================

AUTH_REQUESTS_TOTAL = Counter(
    "product_intelligence_auth_requests_total",
    "Total authentication requests",
)

AUTH_SUCCESS_TOTAL = Counter(
    "product_intelligence_auth_success_total",
    "Total successful authentications",
)

AUTH_MISSING_API_KEY_TOTAL = Counter(
    "product_intelligence_auth_missing_api_key_total",
    "Requests missing API key",
)

AUTH_INVALID_API_KEY_TOTAL = Counter(
    "product_intelligence_auth_invalid_api_key_total",
    "Invalid API key attempts",
)

AUTH_INACTIVE_CLIENT_TOTAL = Counter(
    "product_intelligence_auth_inactive_client_total",
    "Inactive client authentication attempts",
)

AUTH_SERVICE_ERRORS_TOTAL = Counter(
    "auth_service_errors_total",
    "Authentication service errors",
)
