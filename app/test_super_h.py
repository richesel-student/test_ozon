from super_h import find_tallest_hero
import pytest
from unittest.mock import patch, MagicMock
from jsonschema import validate, ValidationError


def test_hero_male_false():
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{
            "id": 728,
            "name": "Ymir",
            "appearance": {
                "gender": "Male",
                "height": [
                    "1000",
                    "304.8 meters"
                ]
            },
            "work": {
                "occupation": "-"
            }
        }]
        mock_get.return_value = mock_response
        response = mock_get(
            'https://akabab.github.io/superhero-api/api/all.json')
        assert response.status_code == 200

        result = find_tallest_hero('Male', False)
        assert result == 'Ymir'


def test_hero_male_true():
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{
            "id": 681,
            "name": "Utgard-Loki",
            "appearance": {
                "gender": "Male",
                "height": [
                    "50'0",
                    "15.2 meters"
                ],

            },
            "work": {
                "occupation": "Monarch"
            }
        }]
    mock_get.return_value = mock_response
    response = mock_get('https://akabab.github.io/superhero-api/api/all.json')
    assert response.status_code == 200

    result = find_tallest_hero('Male', True)
    assert result == 'Utgard-Loki'


def test_hero_fmale_true():
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{
            "id": 284,
            "name": "Giganta",
            "appearance": {
                "gender": "Female",
                "height": [
                    "205",
                    "62.5 meters"
                ]
            },
            "work": {
                "occupation": "Criminal, former Scientist, Professor at Ivy University"
            }
        }]
        mock_get.return_value = mock_response
        response = mock_get(
            'https://akabab.github.io/superhero-api/api/all.json')
        assert response.status_code == 200

        result = find_tallest_hero('Female', True)
        assert result == 'Giganta'


def test_hero_binary_false():
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{
            "id": 287,
            "name": "Godzilla",
            "appearance": {
                "gender": "-",
                "height": [
                    "354'4",
                    "108.0 meters"
                ]
            },
            "work": {
                "occupation": "-"
            }
        }]
        mock_get.return_value = mock_response
        response = mock_get(
            'https://akabab.github.io/superhero-api/api/all.json')
        assert response.status_code == 200

        result = find_tallest_hero('-', False)
        assert result == 'Godzilla'


def test_empty_api_response():
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        result = find_tallest_hero('Male', True)
        assert result is None


def test_no_matching_heroes():
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{
            "id": 1,
            "name": "Hero",
            "appearance": {"gender": "Male", "height": ["1.8 meters"]},
            "work": {"occupation": "Programmer"}  # has_work=True
        }]
        mock_get.return_value = mock_response

        result = find_tallest_hero('Female', False)
        assert result is None


def test_invalid_height_units():
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{
            "id": 2,
            "name": "Hero",
            "appearance": {"gender": "Male", "height": ["500 feet"]},
            "work": {"occupation": "Engineer"}
        }]
        mock_get.return_value = mock_response

        result = find_tallest_hero('Male', True)
        assert result is None


def test_height_without_space():
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{
            "id": 3,
            "name": "Hero",
            "appearance": {"gender": "Female", "height": ["62.5meters"]},
            "work": {"occupation": "Teacher"}
        }]
        mock_get.return_value = mock_response

        result = find_tallest_hero('Female', True)
        assert result == 'Hero'


def test_multiple_heroes():
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                "id": 4,
                "name": "Short Hero",
                "appearance": {"gender": "Male", "height": ["10 meters"]},
                "work": {"occupation": "Worker"}
            },
            {
                "id": 5,
                "name": "Tall Hero",
                "appearance": {"gender": "Male", "height": ["20 meters"]},
                "work": {"occupation": "Worker"}
            }
        ]
        mock_get.return_value = mock_response

        result = find_tallest_hero('Male', True)
        assert result == 'Tall Hero'


def test_has_work_filter():
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                "id": 6,
                "name": "Working Hero",
                "appearance": {"gender": "Male", "height": ["2 meters"]},
                "work": {"occupation": "Engineer"}
            },
            {
                "id": 7,
                "name": "Non-Working Hero",
                "appearance": {"gender": "Male", "height": ["3 meters"]},
                "work": {"occupation": "-"}
            }
        ]
        mock_get.return_value = mock_response

        # Проверка для has_work=True
        result = find_tallest_hero('Male', True)
        assert result == 'Working Hero'

        result = find_tallest_hero('Male', False)
        assert result == 'Non-Working Hero'


def test_zero_height():
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{
            "id": 8,
            "name": "Zero Hero",
            "appearance": {"gender": "Female", "height": ["0 meters"]},
            "work": {"occupation": "-"}
        }]
        mock_get.return_value = mock_response

        result = find_tallest_hero('Female', False)
        assert result is None


def test_multiple_height_values():
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{
            "id": 9,
            "name": "Hero",
            "appearance": {
                "gender": "Male",
                "height": ["6'2\"", "1.88 meters"]
            },
            "work": {"occupation": "Doctor"}
        }]
        mock_get.return_value = mock_response

        result = find_tallest_hero('Male', True)
        assert result == 'Hero'


@patch('super_h.requests.get')
def test_handle_500_error(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_get.return_value = mock_response

    result = find_tallest_hero('Male', True)
    assert result is None


@patch('super_h.requests.get')
def test_handle_404_error(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    result = find_tallest_hero('Male', True)
    assert result is None


def test_find_tallest_hero_with_int_gender():
    with pytest.raises(TypeError):
        find_tallest_hero(123, True)


def test_find_tallest_hero_with_none_gender():
    with pytest.raises(TypeError):
        find_tallest_hero(None, True)


def test_find_tallest_hero_with_int_has_work():
    with pytest.raises(TypeError):
        find_tallest_hero("Male", int)


def test_find_tallest_hero_with_none_has_work():
    with pytest.raises(TypeError):

        find_tallest_hero("Male", None)


def test_find_tallest_hero_with_wrong_types_both():

    with pytest.raises(TypeError):
        find_tallest_hero(int, [])


def test_find_tallest_hero_with_float_gender():

    with pytest.raises(TypeError):
        find_tallest_hero(3.14, True)


def test_find_tallest_hero_with_dict_has_work():

    with pytest.raises(TypeError):
        find_tallest_hero({"occupation": "Hero"}, {})


def test_valid_data():
    schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "id": {"type": "number"},
                "name": {"type": "string"},
                "appearance": {
                    "type": "object",
                    "properties": {
                        "gender": {"type": "string"},
                        "height": {
                            "type": "array",
                            "items": {"type": "string"}
                        }
                    },
                    "required": ["gender", "height"]
                },
                "work": {
                    "type": "object",
                    "properties": {
                        "occupation": {"type": "string"}
                    },
                    "required": ["occupation"]
                }
            },
            "required": ["id", "name", "appearance", "work"]
        }
    }
    data = [{
        "id": 284,
        "name": "Giganta",
        "appearance": {
            "gender": "Female",
            "height": [
                "205",
                "62.5 meters"
            ]
        },
        "work": {
            "occupation": "Criminal, former Scientist, Professor at Ivy University"
        }
    }]
    validate(instance=data, schema=schema)  # Не должно выбросить ошибку


def test_invalid_data_missing_field():
    schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "id": {"type": "number"},
                "name": {"type": "string"},
                "appearance": {
                    "type": "object",
                    "properties": {
                        "gender": {"type": "string"},
                        "height": {
                            "type": "array",
                            "items": {"type": "string"}
                        }
                    },
                    "required": ["gender", "height"]
                },
                "work": {
                    "type": "object",
                    "properties": {
                        "occupation": {"type": "string"}
                    },
                    "required": ["occupation"]
                }
            },
            "required": ["id", "name", "appearance", "work"]
        }
    }
    data = [{
        "id": 284,
        "name": "Giganta",
        "appearance": {
            "gender": "Female"
            # отсутствует поле height
        },
        "work": {
            "occupation": "Criminal"
        }
    }]
    with pytest.raises(ValidationError):
        validate(instance=data, schema=schema)


def test_invalid_data_wrong_type():
    schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "id": {"type": "number"},
                "name": {"type": "string"},
                "appearance": {
                    "type": "object",
                    "properties": {
                        "gender": {"type": "string"},
                        "height": {
                            "type": "array",
                            "items": {"type": "string"}
                        }
                    },
                    "required": ["gender", "height"]
                },
                "work": {
                    "type": "object",
                    "properties": {
                        "occupation": {"type": "string"}
                    },
                    "required": ["occupation"]
                }
            },
            "required": ["id", "name", "appearance", "work"]
        }
    }

    data = [{
        "id": "284",  # id должен быть числом, а не строкой
        "name": "Giganta",
        "appearance": {
            "gender": "Female",
            "height": ["205", "62.5 meters"]
        },
        "work": {
            "occupation": "Criminal"
        }
    }]
    with pytest.raises(ValidationError):
        validate(instance=data, schema=schema)
