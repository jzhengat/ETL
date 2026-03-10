# --- Custom middleware to allow Azure health check IPs dynamically ---
# mlopmiddleware.py
def is_azure_healthcheck(host):
    """Return True if host is an Azure health check internal IP."""
    host_ip = host.split(':')[0]
    return host_ip.startswith('169.254.')

class AzureHealthCheckMiddleware:
    """Middleware to allow Azure health check requests from 169.254.*.*"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.META.get('HTTP_HOST', '')  # <-- use META, not get_host()
        if is_azure_healthcheck(host):
            request.META['HTTP_HOST'] = 'localhost'
        return self.get_response(request)