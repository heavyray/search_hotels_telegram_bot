import requests
import json
from loader import api_key, api_host
from user import User, Hotel
import re

headers = {
    'X-RapidAPI-Host': api_host,
    'X-RapidAPI-Key': api_key
}
url = 'https://hotels4.p.rapidapi.com/'


def search_city(city: str, user: User) -> None:
    """Поиск города"""
    querystring = {"query": city, "locale": user.locale, "currency": user.currency}

    response = requests.request("GET", url + '/locations/v2/search', headers=headers, params=querystring)
    city_dict = json.loads(response.text)

    for i_city in city_dict['suggestions'][0]['entities']:
        name_city = re.sub(r'<.*?>', '', i_city['caption'])
        user.city_dict[int(i_city['destinationId'])] = name_city


def search_hotel(user: User) -> None:
    """Поиск отелей в городе"""
    querystring = {"destinationId": user.city_id, "pageNumber": "1", "pageSize": "25",
                   "check_in": user.check_in, "check_out": user.check_out, "adults1": "2",
                   "price_min": user.price_min, "price_max": user.price_max, "sort_order": user.sort_order,
                   "locale": user.locale, "currency": user.currency}

    response = requests.request("GET", url + '/properties/list', headers=headers, params=querystring)
    hotels_dict = json.loads(response.text)

    for i_hotel in hotels_dict["data"]["body"]["searchResults"]["results"]:
        distance = float(re.sub(r' км', '', re.sub(r',', '.', i_hotel['landmarks'][0]['distance'])))
        if user.command == '/bestdeal' and \
                user.max_distance < distance:
            continue
        hotel = Hotel()
        hotel.id = i_hotel.get('id')
        hotel.name = i_hotel.get('name')
        hotel.stars = i_hotel.get('starRating')
        hotel.address = i_hotel['address'].get('streetAddress')
        hotel.price = i_hotel['ratePlan']['price'].get('exactCurrent')
        hotel.city_center_distance = distance
        hotel.count_night = (user.check_out - user.check_in).days
        if user.photo:
            search_photo(hotel, user.count_photo)
        user.hotels_list.append(hotel)
    if user.command == '/bestdeal':
        user.hotels_list = sorted(user.hotels_list, key=lambda elem: elem.city_center_distance)


def search_photo(hotel: Hotel, count: int) -> None:
    """Поиск фото отеля"""
    querystring = {"id": hotel.id}

    response = requests.request("GET", url + '/properties/get-hotel-photos', headers=headers, params=querystring)
    photo_dict = json.loads(response.text)['hotelImages'][:10]

    if len(photo_dict) < count:
        count = len(photo_dict)

    for i_photo in photo_dict[:count]:
        url_hotel = i_photo['baseUrl']
        url_hotel = re.sub(r'{size}', 'y', url_hotel)
        hotel.photo_list.append(url_hotel)
