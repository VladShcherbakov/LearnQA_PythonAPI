import json.decoder
from requests import Response


class Assertions:
    @staticmethod
    def assert_json_value_by_name(response: Response, name, expected_value, error_message):
        try:
            response_dict = response.json()
        except json.decoder.JSONDecoder:
            assert False, f"Response is not in json format. Response text is '{response}'"

        assert name in response_dict, f"Response json does not have '{name}' key"
        assert response_dict[name] == expected_value, error_message
