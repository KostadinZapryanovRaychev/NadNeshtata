from django.http import JsonResponse

class HandleResponseUtils(object):
    """This class holds methods related to views.py:
    1. The methods here are related to response handling
    """
    @staticmethod
    def handle_response(status_code, message) -> JsonResponse:
        """
        Returns proper response data
        :param status_code: http status code
        :type status_code: http status code
        :param message: function that contains response
        :rType: JsonResponse
        :returns: JsonResponse
        """
        # If the obj is type set return list(obj)
        if isinstance(message, set):
            return JsonResponse(data=list(message), status=status_code, safe=False)
        else:
            return JsonResponse(data=message, status=status_code, safe=False)

    @staticmethod
    def handle_response_data(status_code, message):
        """
        Returns proper response data
        :param status_code: http status code
        :type status_code: http status code
        :param message: function that contains response
        :rType: JsonResponse
        :returns: JsonResponse
        """
        if isinstance(message, set):
            return JsonResponse(data=list(message).data, status=status_code, safe=False)
        else:
            return JsonResponse(data=message.data, status=status_code, safe=False)