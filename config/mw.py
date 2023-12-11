import json
import logging
import ipaddress

from django.utils.timezone import now


api_logger = logging.getLogger('API_logger')

class GetRequestData :
    def __init__(self, request, response=None) -> None:
        self.request = request
        self.response = response

    def get_ip_address(self, request):
        ipaddr = request.META.get('HTTP_X_FORWARDED_FOR', None)

        if ipaddr:
            ipaddr = ipaddr.split(',')[0]
        else:
            ipaddr = request.META.get('REMOTE_ADDR', '').split(',')[0]

        possibles = (ipaddr.lstrip('[').split(']')[0], ipaddr.split(':')[0])

        for ip_addr in possibles:
            try:
                return str(ipaddress.ip_address(ip_addr))
            except ValueError:
                pass
        return ipaddr
        
    def get_request_data(self):
        req_data = {}
        req_data['ip_address'] = self.get_ip_address(self.request)
        req_data['method'] = self.request.method
        req_data['user'] = self.request.user.username if self.request.user else None
        req_data['status'] = self.response.status_code if self.response else None
        req_data['time'] = str(now())
        req_data['endpoint'] = self.request.get_full_path()
        return req_data

class LogMiddleWare :
    def __init__(self, get_response) -> None:
        self.get_response = get_response
        self.log_info = {}

    def __call__(self, request):
        response = self.get_response(request)
        getdata = GetRequestData(request, response)
        self.log_info.update(getdata.get_request_data())
        api_logger.info(json.dumps(self.log_info))
        return response

    def process_exception(self, request, exception):
        """
        called when a view raise an exception
        """
        getdata = GetRequestData(request)
        self.log_info.update(getdata.get_request_data())
        self.log_info["exception"] = str(exception)
        api_logger.error(msg=json.dumps(self.log_info))
        return None
