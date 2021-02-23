class HttpCode:
    OK: int = 200
    CREATED: int = 201
    NO_CONTENT: int = 204
    
    MOVED_PERMANENTLY: int = 301
    TEMPORARY_REDIRECT: int = 307

    BAD_REQUEST: int = 400
    UNAUTHORIZED: int = 401
    FORBIDDEN: int = 403
    NOT_FOUND: int = 404
    METHOD_NOT_ALLOWED: int = 405
    
    INTERNAL_SERVER_ERROR: int = 500
    NOT_IMPLEMENTED: int = 501
    BAD_GATEWAY: int = 502