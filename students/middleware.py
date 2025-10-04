# students/middleware.py
class RefreshTokenMiddleware:
    """
    Middleware to automatically include a new access token
    in the response if `request.new_access_token` exists.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if hasattr(request, "new_access_token"):
            # Option 1: add to response JSON (if JSONResponse)
            if hasattr(response, "data") and isinstance(response.data, dict):
                response.data["new_access_token"] = request.new_access_token
                response._is_rendered = False  # re-render response

            # Option 2: add as a header
            response["X-New-Access-Token"] = request.new_access_token

        return response
