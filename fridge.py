import datetime
from decimal import Decimal

DATE_FORMAT = '%Y-%m-%d'

def add(items, title, amount, expiration_date=None):
    """Добавляет продукт в словарь."""
    exp_date_not_str = None
    if expiration_date:
        exp_date_not_str = datetime.datetime.strptime(expiration_date, DATE_FORMAT).date()

    if title in items:
        # Проверяем, есть ли партия с такой же датой
        found_equal_date_flag = False
        for dict_ in items[title]:
            if dict_['expiration_date'] == exp_date_not_str:
                found_equal_date_flag = True
                dec_amount = Decimal(str(amount))
                dict_['amount'] += dec_amount
                break  # Выходим из цикла, если нашли совпадающую партию

        # Если партия с такой датой не найдена, добавляем новую
        if not found_equal_date_flag:
            items[title].append({
                'amount': Decimal(str(amount)),
                'expiration_date': exp_date_not_str
            })
    else:  # Продукт отсутствует в словаре
        items[title] = [{
            'amount': Decimal(str(amount)),
            'expiration_date': exp_date_not_str
        }]


def add_by_note(items, note):
    """Добавляет продукт в словарь по строке с описанием."""
    list_info = note.split(' ')
    date_str = None
    count = -1
    title = ''
    minus_size = 1

    if '-' in list_info[-1]:
        date_str = list_info[-1]
        minus_size += 1

    try:
        count = Decimal(list_info[-minus_size])
        title = ' '.join(list_info[:len(list_info)-minus_size])
        add(items=items, title=title, amount=count, expiration_date=date_str)
    except (ValueError, IndexError):
        print("Неверный формат строки.")


def find(items, needle):
    """Ищет продукты по названию."""
    needle_lower = needle.lower()
    result_list = list()
    for name in items:
        if needle_lower in name.lower():
            result_list.append(name)
    return result_list


def amount(items, needle):
    """Вычисляет общее количество продуктов."""
    needle_lower = needle.lower()
    result = Decimal()
    for name in items:
        if needle_lower in name.lower():
            for element in items[name]:
                result += element['amount']
    return result


def expire(items, in_advance_days=0):
    """Определяет продукты, срок годности которых истекает."""
    date_now = datetime.date.today()
    delta_time = datetime.timedelta(days=in_advance_days)
    date_expiration = date_now + delta_time

    result = list()

    for product in items:
        sum_ = Decimal()
        for dict_element in items[product]:
            if dict_element['expiration_date'] and dict_element['expiration_date'] <= date_expiration:
                sum_ += dict_element['amount']
        if sum_ != 0:
            result.append((product, sum_))

    return result
