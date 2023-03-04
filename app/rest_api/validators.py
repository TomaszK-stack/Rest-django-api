from django.core.exceptions import ValidationError
import json

def validata_json_data(dict):
    try:
        for key in dict:
            if not isinstance(dict[key], int) or not  key.isdigit():
                raise ValidationError("Invalid type of json data, exapmle: {1: 200} where 1 is number of thumbnail and 200 is size.")
                data = json.dumps(dict)

    except ValueError:
        raise ValidationError("Enter a valid json")

