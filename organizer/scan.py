import re

from loguru import logger


# flake8: noqa: C901
def search_time(text: str) -> int:
    """осуществляет поиск времени в предложении."""
    text = re.sub(r"и ", "", text)
    text = re.sub(r"через ", "", text)
    time_from_hour: int = 0
    time_from_min: int = 0
    time_from_sec: int = 0
    patterns_hour: tuple = ("часов", "часа", "час", "ч")
    patterns_minute: tuple = ("минута", "минуты", "минуту", "минут", "мин", "м")
    patterns_second: tuple = ("секунда", "секунды", "секунду", "секунд", "сек", "с")

    try:
        for pattern in patterns_hour:
            if re.search(pattern, text, flags=re.IGNORECASE):
                result = re.split(pattern, text, flags=re.IGNORECASE)
                time_from_hour = re.search(r"\d{1,3}", result[0]).group(0)  # поиск времени
                time_from_hour = 3600 * int(time_from_hour)  # перевод времени в секунды
                text = str(result[1])  # второй элемент передаётся дальше
                break
    except AttributeError:
        time_from_hour = 0
        logger.debug("Error - no pattern(hour) found")

    try:
        for pattern in patterns_minute:
            if re.search(pattern, text, flags=re.IGNORECASE):
                result = re.split(pattern, text, flags=re.IGNORECASE)
                time_from_min = 60 * int(re.search(r"\d{1,3}", result[0]).group(0))
                text = str(result[1])
                break
    except AttributeError:
        time_from_min = 0
        logger.debug("Error - no pattern(minute) found")

    try:
        for pattern in patterns_second:
            if re.search(pattern, text, flags=re.IGNORECASE):
                result = re.split(pattern, text, flags=re.IGNORECASE)
                time_from_sec = int(re.search(r"\d{1,6}", result[0]).group(0))
                break
    except AttributeError:
        time_from_sec = 0
        logger.debug("Error - no pattern(second) found")

    time_wait = time_from_hour + time_from_min + time_from_sec
    return time_wait
