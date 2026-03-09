class AzureHealthCheckMiddleware:
    """Middleware to allow Azure health check requests from 169.254.*.*"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host()
        if is_azure_healthcheck(host):
            # Temporarily override to a valid host to bypass ALLOWED_HOSTS check
            request.META['HTTP_HOST'] = 'localhost'
        return self.get_response(request)