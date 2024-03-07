import json.decoder
from requests import Response


class Assertions:
    @staticmethod
    def assert_json_value_by_name(response: Response, name, expected_value, error_message):
        try:
            response_dict = response.json()
        except json.decoder.JSONDecoder:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        assert name in response_dict, f"Response json does not have '{name}' key"
        assert response_dict[name] == expected_value, error_message

    @staticmethod
    def assert_json_has_key(response: Response, name):
        try:
            response_dict = response.json()
        except json.decoder.JSONDecoder:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        assert name in response_dict, f"Response JSON doesn't have key '{name}'"

    @staticmethod
    def assert_json_has_not_key(response: Response, name):
        try:
            response_dict = response.json()
        except json.decoder.JSONDecoder:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        assert name not in response_dict, f"Response JSON have key '{name}' but should not!"

    @staticmethod
    def assert_json_has_keys(response: Response, names: list):
        try:
            response_dict = response.json()
        except json.decoder.JSONDecoder:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        for name in names:
            assert name in response_dict, f"Response JSON doesn't have key '{name}'"

    @staticmethod
    def assert_json_has_not_keys(response: Response, names: list):
        try:
            response_dict = response.json()
        except json.decoder.JSONDecoder:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        for name in names:
            assert name not in response_dict, f"Response JSON have key '{name}' but should not"

    @staticmethod
    def assert_code_status(response: Response, code_status):
        assert code_status == response.status_code, \
            f"Wrong response code status '{response.status_code}', should be '{code_status}'"
