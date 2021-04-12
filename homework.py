import datetime as dt


class Calculator:
    """Создаем основной(родительский) класс нашего калькулятора. """

    def __init__(self, limit,):
        """Задаем основные свойства класса."""
        self.limit = limit
        self.records = []

    def add_record(self, new_record):
        """Функция добавления нового элемента в список records. """
        self.records.append(new_record)

    def get_today_stats(self):
        """Функция подсчета трат/калорий за текущий день. """
        count = sum(record.amount for record in self.records
                    if record.date == dt.datetime.now().date())
        return count

    def get_week_stats(self):
        """Функция подсчета трат/каллорий за неделю. """
        week_stats = dt.datetime.now().date() - dt.timedelta(days=7)
        week_stat_fut = dt.datetime.now().date() + dt.timedelta(days=1)
        week_count = sum(record.amount for record in self.records
                         if week_stats <= record.date < week_stat_fut)
        return week_count


class Record:
    """Создаем класс для удобного хранения записей. """

    def __init__(self, amount, comment,
                 date=dt.datetime.now().strftime("%d.%m.%Y")):
        """Заполняем его основнвые свойства. """
        self.amount = amount
        self.comment = comment
        self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


class CaloriesCalculator(Calculator):
    """Создаем класс для калькулятора калорий. """
    def get_calories_remained(self):
        """Функция подсчета калорий за день с выводом результата. """
        if self.get_today_stats() < self.limit:
            difference = self.limit - self.get_today_stats()
            return ('Сегодня можно съесть что-нибудь ещё, но с общей '
                    f'калорийностью не более {difference} кКал')
        return ('Хватит есть!')


class CashCalculator(Calculator):
    """Создаем класс для денежного калькулятора """
    EURO_RATE = 91
    USD_RATE = 77
    RUB_RATE = 1

    def __init__(self, limit, EURO_RATE=91, USD_RATE=77, RUB_RATE=1):
        """Заполняем его основные свойства. """
        super().__init__(limit)
        self.EURO_RATE = float(EURO_RATE)
        self.USD_RATE = float(USD_RATE)
        self.RUB_RATE = float(RUB_RATE)

    def get_today_cash_remained(self, currency):
        """Функция подсчета трат за день с выводом результа
        в разной валюте. """

        if self.get_today_stats() == self.limit:
            return ('Денег нет, держись')

        if currency == 'eur':
            diff_eur = (self.limit - self.get_today_stats()) / self.EURO_RATE
            if self.get_today_stats() < self.limit:
                return (f'На сегодня осталось {round(diff_eur, 2)} Euro')
            return ('Денег нет, держись: твой долг - '
                    f'{abs(round(diff_eur, 2))} Euro')

        if currency == 'usd':
            diff_usd = (self.limit - self.get_today_stats()) / self.USD_RATE
            if self.get_today_stats() < self.limit:
                return (f'На сегодня осталось {round(diff_usd, 2)} USD')
            return ('Денег нет, держись: твой долг - '
                    f'{abs(round(diff_usd, 2))} USD')

        if currency == 'rub':
            diff_rub = (self.limit - self.get_today_stats()) / self.RUB_RATE
            if self.get_today_stats() < self.limit:
                return (f'На сегодня осталось {round(diff_rub, 2)} руб')
            return ('Денег нет, держись: твой долг - '
                    f'{abs(round(diff_rub, 2))} руб')
