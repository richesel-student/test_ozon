import requests


def find_tallest_hero(gender: str, has_work: bool):

    if not isinstance(gender, str):
        raise TypeError(f"gender must be a str, got {type(gender).__name__}")
    if not isinstance(has_work, bool):
        raise TypeError(
            f"has_work must be a bool, got {type(has_work).__name__}")

    url = 'https://akabab.github.io/superhero-api/api/all.json'

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print("Ошибка 404: ресурс не найден")
        elif e.response.status_code == 500:
            print("Ошибка 500: внутренняя ошибка сервера")
        else:
            print(f"Произошла HTTP ошибка: {e}")
        return None
    except requests.RequestException as e:
        print(f"Ошибка запроса: {e}")
        return None

    heroes = {}
    meters = ''

    for hero in range(len(data)):

        hero_gender = data[hero]['appearance']['gender']
        hero_has_work = data[hero]['work']['occupation'] != '-'

        if hero_gender != gender or hero_has_work != has_work:
            continue

        if (data[hero]['appearance']['height'][-1].endswith('meters')):
            meters = data[hero]['appearance']['height'][-1]\
                .strip('meters').strip()
        elif (data[hero]['appearance']['height'][-1].endswith('cm')):
            cm = data[hero]['appearance']['height'][-1]\
                .strip('cm').strip()
            cm = float(cm)
            if cm == 0:
                continue
            meters = cm / 100

        try:
            meters = float(meters)
        except ValueError:
            continue

        if meters == 0:
            continue

        heroes[data[hero]['name']] = {
            "gender": gender, "has_work": has_work, "meters": meters}

    if not heroes:
        print("No heroes found matching criteria")
        return None

    tallest = max(
        heroes,
        key=lambda n: heroes[n]["meters"]
    )
    return tallest
