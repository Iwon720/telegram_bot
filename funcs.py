import time
import requests

def try_except(func):
    def wrapper(*args, **kwargs):
        retry_timer = [5, 15]
        for i in retry_timer:
            try:
                return func(*args, **kwargs)
            except KeyError:
                print(f"хуйню написал")
                break
            except requests.exceptions.ConnectionError:
                print(f"Something goes wrong, we will retry in {i} seconds")
                time.sleep(i)
            except requests.exceptions.ReadTimeout:
                print("requests.exceptions.ReadTimeout")
                break

    return wrapper


def if_none(var) -> str:
    if var is None:
        return "Извините, произошла ошибка. И вообще нахуй иди, я рот твой ебал"
    else:
        return var
