import requests

from bs4 import BeautifulSoup


BASE_URL = 'http://m.ettu.ru'


def get_html(url):
    r = requests.get(url)
    return r.text if r.status_code == 200 else None


def get_page_stations(station):
    station = station.strip().upper()
    url = BASE_URL + '/stations/' + station[0].upper()
    html = get_html(url)

    if html:
        html = html[html.find('<h3>Трамваи</h3>'): html.find('<h3>Троллейбусы</h3>')]
        soup = BeautifulSoup(html, 'lxml')

        page_stations = {a.text: {'href': a.get('href')} for a in soup.find_all('a') if station in a.text.upper()}

        return page_stations
    return None


def get_traffic_station(href):
    url = BASE_URL + href
    html = get_html(url)

    if html:
        try:
            soup = BeautifulSoup(html, 'lxml')

            trams = [div.text for div in soup.find_all('div', {'style': 'width: 3em;display:inline-block;text-align:center;'})]
            mins = [div.text for div in soup.find_all('div', {'style': 'width: 4em;display:inline-block;text-align:right;'})]

            traffic = dict(zip(trams, mins))
        except:
            return None
        else:
            return traffic

    return None


def get_letters_stations():
    html = get_html(BASE_URL)
    soup = BeautifulSoup(html, 'lxml')
    
    except_letters = ['X', 'Щ']
    valid_letters_stations = []
    for a in soup.find_all('a', class_='letter-link'):
        letter = a.text.strip().upper() 
        if letter not in except_letters:
            valid_letters_stations.append(letter)

    return valid_letters_stations