from src.api.errors.error_response import Error


class UnauthorizedError(Error):
    code = 'missing_or_invalid_api_key'
    message = 'The API key is missing or not recognized'
    status_code = 401


class ForbiddenError(Error):
    code = 'action_forbidden'
    message = 'The specified user does not have permission to perform this action'
    status_code = 403
