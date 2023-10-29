from typing import Any
import logging


api_logger = logging.getLogger('API_logger')

def get_request_data(request):
    pass

class LogMiddleWare :
    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request):
        # some code before view
        response = self.get_response(request)
        api_logger.info(get_request_data(request))
        # some code after view
        return response

    def process_exception(self, request, exception):
        """
        called when a view raise an exception
        """
        api_logger.error(msg=get_request_data(request)+ str(exception))
        return None

    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        called before django calls the view
        """
        return None

    def process_template_response(self, request, response):
        """
        called just after the view has finished executing
        """