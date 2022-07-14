# Импортируем необходимые библиотеки
import requests
from bs4 import BeautifulSoup as BS
from tqdm import tqdm
from art import *
import re

animals = []
characters = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о',
              'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']

def take_data():
    # Указываем страницу, данные с которой будем считывать
    url = "https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту"
    page = requests.get(url).text

    flag = True

    while flag:
        for i in tqdm(range(100), desc="Загрузка"): # Отображение прогресса выполнения программы
            # Получаем список слов с n-ой страницы
            soup = BS(page, 'lxml')
            names = soup.find('div', class_='mw-category-columns').find_all('ul')
            names = names[0].text.split('\n')
            for name in names:
                if name[0] != 'A': # Прекращаем работу, если имена животных начинаются с английских букв
                    animals.append(re.sub(r'.*(ый|ой|ий|ое|её|ая|яя|ья) ', '', name)) # Добавляем элемент в финальный список
                    # Также убираем из названия животного прилагательные
                else:
                    flag = False # Слова кончились --> Выходим из цикла и переходим к подсчёту букв

            # Переход на следующую страницу
            links = soup.find('div', id='mw-pages').find_all('a')
            for a in links:
                if a.text == 'Следующая страница':
                    url = 'https://ru.wikipedia.org/' + a.get('href')
                    page = requests.get(url).text

def count():
    print('')
    # Считаем количество слов на каждую букву алфавита и выводим эти числа
    for character in characters:
        res = [idx for idx in animals if idx[0].lower() == character]
        print(f"{character}: {len(res)}")

def main():
    tprint("Animals Counter", "big") # Выводим красиво написанное название программы
    take_data()
    count()

if __name__ == "__main__":
    main()



