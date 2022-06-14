user_dict = {}


class User:
    """Модель пользователя с параметрами поиска"""
    def __init__(self, sort_order: str, command: str) -> None:
        self.sort_order = sort_order
        self.command = command
        self.locale = 'ru_RU'
        self.currency = 'RUB'
        self.city_dict = {}
        self.city_name = None
        self.city_id = None
        self.hotels_list = []
        self.check_in = None
        self.check_out = None
        self.price_min = None
        self.price_max = None
        self.max_distance = None
        self.photo = False
        self.count_photo = None


class Hotel:
    """Модель отеля с информацией о нем"""
    def __init__(self) -> None:
        self.name = None
        self.id = None
        self.stars = None
        self.address = None
        self.price = None
        self.city_center_distance = None
        self.count_night = None
        self.photo_list = []
        self.count_photo = None

    @property
    def url(self) -> str:
        """Возвращает ссылку на страницу бронирование отеля"""
        return f'https://ru.hotels.com/ho{self.id}'

    def __str__(self) -> str:
        return f"Отель {self.name}" \
               f"\nКласс: {int(self.stars)} &#9733;" \
               f"\nАдрес: {self.address}" \
               f"\nЦена за {self.count_night} ночей: {round(self.price)}руб" \
               f"\nЦена за ночь: {round(int(self.price) / self.count_night)}руб" \
               f"\nРасстояние до центра города: {self.city_center_distance} км"


