from strictaccess import strict_access_control, public

@strict_access_control()
class Router:
    def __init__(self, service):
        self._service = service

    @public
    def get(self, path):
        def decorator(func):
            self._service.app.get(path)(func)
            return func
        return decorator

    @public
    def post(self, path):
        def decorator(func):
            self._service.app.post(path)(func)
            return func
        return decorator

    @public
    def put(self, path):
        def decorator(func):
            self._service.app.put(path)(func)
            return func
        return decorator

    @public
    def delete(self, path):
        def decorator(func):
            self._service.app.delete(path)(func)
            return func
        return decorator
