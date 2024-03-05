import json
from requests import Response


class BaseCase:
    def get_cookie(self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f"Cannot find cookie name '{cookie_name}' in the response"
        return response.cookies[cookie_name]

    def get_header(self, response: Response, header_name):
        assert header_name in response.headers, f"Cannot find header name '{header_name}' in the response"
        return response.headers[header_name]

    def get_json_value(self, response: Response, name):
        try:
            response_dict = response.json()
        except json.decoder.JSONDecoder:
            assert False, f"Response is not in json format. Response text is '{response.text}'"

        assert name in response_dict, f"Response JSON doesn't have '{name}' key"

        return response_dict[name]
