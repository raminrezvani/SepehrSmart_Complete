import jdatetime

def convert_persian_number_to_english(number: str):
    """
    check string if it has persian number, change it to english number
    :param number: any string
    :return:
    """
    numbers = {
        "۱": "1",
        "۲": "2",
        "۳": "3",
        "۴": "4",
        "۵": "5",
        "۶": "6",
        "۷": "7",
        "۸": "8",
        "۹": "9",
        "۰": "0",
    }
    # ---
    result = [
        numbers[num] if num in list(numbers.keys()) else num for num in number
    ]
    # --- response
    return "".join(result)


def convert_persian_date_to_gregorian(date: str, template: str = "%Y-%m-%d") -> dict:
    """
    convert jalali date to gregorian
    :param date: format ==> YYYY/MM/DD
    :param template: output format
    :return: status, message, date
    """
    try:
        year = int(date[:4])
        month = int(date[5:7])
        day = int(date[8:])
        return {
            "status": True,
            "message": "ok",
            "date": jdatetime.date(year=year, month=month, day=day, locale='fa_IR').togregorian().strftime(template)
        }
    except:
        return {"status": False, "message": "something went wrong", "date": None}


def convert_gregorian_date_to_persian(date: str, template: str = "%Y-%m-%d") -> dict:
    """
    convert gregorian date to jalali
    :param date: format ==> YYYY-MM-DD
    :param template: output format
    :return: status, message, date
    """
    try:
        year = int(date[:4])
        month = int(date[5:7])
        day = int(date[8:])
        return {
            "status": True,
            "message": "ok",
            "date": jdatetime.date.fromgregorian(year=year, month=month, day=day).strftime(template)
        }
    except:
        return {"status": False, "message": "something went wrong"}


def ready_price(price: str) -> str:
    """
    delete price noise
    :param price: str
    :return: price without noise
    """
    price = price.replace(',', '')
    price = price.replace('ريال', '')
    return convert_persian_number_to_english(price.strip())


def convert_to_tooman(price) -> int:
    """
    convert rial price to tooman
    :param price: rial price
    :return: tooman price
    """
    return int(float(price) / 10)
