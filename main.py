# Перед запуском проверить, установлен ли браузер Chrome на этом компьютере: https://www.google.com/intl/ru/chrome/
# Chromedriver скачать в соответствии с версией Chrome: https://chromedriver.chromium.org/downloads
# Продублировать его в venv проекта по пути: "venv\Lib\Chrome\chromedriver.exe"

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import pandas as pd
import time
import xlsxwriter

def open_first_page_for_parsing(site_page: str='www.google.com'):
    service_obj = Service("venv\Lib\Chrome\chromedriver.exe")
    option = Options()
    option.add_argument("--disable-infobars")
    driver = webdriver.Chrome(service=service_obj,
                              # chrome_options=option
                              )
    # driver.get("https://www.google.com")
    driver.get(site_page)
    return driver

def open_new_window():
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1]) #  есть только 1 открытая вкладка:
    # driver.switch_to.window(len(driver.window_handles)-1)   # Если уже открыто более 1 вкладки, вы должны сначала получить индекс последней вновь созданной вкладки и переключиться на вкладку, прежде чем вызывать URL-адрес (заслуга tylerl) :
    return

def page_for_parsing(page, router, score):
    site_page = ''.join([page, router, str(score)])
    print('site_page: ', site_page)
    return site_page

# Проверка на несуществующую страницу:
def check_404_page(driver):
    if driver.find_element(By.TAG_NAME, 'h1').text == 'Ошибка 404':
        # print('h1: ', driver.find_element(By.TAG_NAME, 'h1').text)
        print('Сбор данных с сайта завершен.')
        return True
    return False

def parsing_num_of_cards_on_page(driver):
    return driver.find_elements(By.XPATH, "//div[div/@class='catalog-card__detail']")
    # return get_elements_from_card(driver)

# Парсинг карточек ЖК со страницы:
def parsing_cards_from_page(driver):
    # cards_on_page = driver.find_elements(By.XPATH, "//div[div/@class='catalog-card__detail']")
    # cards_on_page = driver.find_elements(By.XPATH, "//div[@class='catalog-card__detail']")

    # cards_on_page = driver.find_elements(By.XPATH, "//*[@id='catalog-list']/div[1]/div[2]")
    # cards_on_page = driver.find_elements(By.XPATH, "//*[@id='catalog-list']/div[2]/div[2]")
    # cards_on_page = driver.find_elements(By.XPATH, "//*[@id='catalog-list']/div[1]")
    # cards_on_page = driver.find_elements(By.XPATH, "//*[@id='catalog-list']/div")

    # Более правильный вариант:
    # cards_on_page = driver.find_elements(By.XPATH, "//div[@class ='catalog-card js-catalog-card']")

    # card_on_page = driver.find_element(By.XPATH, "//*[@id='catalog-list']/div[2]/div[1]")
    # // *[ @ id = "catalog-list"] / div[2] / div[2]
    # cont = get_elements_from_card(driver=card_on_page)
    # print('cont: ', cont)

    # / html / body / div[1] / main / div[2] / div[2] / div / div / div[2] / div[1] / div[1] / div[2]
    # catalog-list > div:nth-child(1) > div.catalog-card__detail
    # // *[ @ id = "catalog-list"] / div[1] / div[2] / div[1]
    # // *[ @ id = "app"] / main / div[2] / div[2] / div / div / div[2]

    # Отдельные элементы карточек с ЖК:
    # fitches_elements_from_cards = driver.find_elements(By.XPATH, "//div[@class ='catalog-card__detail']")

    # Работает:
    # fitches_elements_from_cards = driver.find_elements(By.XPATH, "//a[@class ='catalog-card__name']/div")
    # fitches_elements_from_cards = driver.find_elements(By.XPATH, "//div[@class ='catalog-card__main']/a")
    # fitches_elements_from_cards = driver.find_elements(By.XPATH, "//div[@class ='catalog-card__main']/a[1]")
    # fitches_elements_from_cards = driver.find_elements(By.XPATH, "//div[@class ='catalog-card__main']")
    # fitches_elements_from_cards = driver.find_elements(By.XPATH, "//div[@class ='catalog-card__detail']")
    cards_on_page = driver.find_elements(By.XPATH, "//div[@class='catalog-card__detail']")

    # Тестирование:

    # Блок с объявлениями:
    # block_with_offers = driver.find_element(By.XPATH, "//*[@id='catalog-list']")
    # Карточки:
    # cards_with_offer = block_with_offers.find_elements(By.XPATH, "/div/div")
    # Элементы карточки:
    # name_zhk = cards_with_offer.find_element(By.XPATH, "//a[@class='catalog-card__name']/div[1]").text

    # print('cards_on_page: ', len(cards_on_page), type(cards_on_page), cards_on_page)
    print(f'Обнаружено карточек на странице: {len(cards_on_page)},',
          # '; cards_on_page: ',
          # type(cards_on_page), cards_on_page,
          '\nсобираем данные: '
          )
    # print(f'Обнаружено карточек на странице {len(fitches_elements_from_cards)}; cards_on_page: ', type(fitches_elements_from_cards), fitches_elements_from_cards)
    card_content = list()
    # # card_content = [('ЖК «Проба»', 'г. Сочи, Проба, улица Проба', '5 эт.', '300 000', '04.11.2021')]
    # # Проходим по всем карточкам и добавляем данные в список:
    i = 0
    for card_ in cards_on_page:
        # print('card_: ', card_)
        print('.', end='')
        # print(f'cards_on_page[{i}]: ', cards_on_page[i])
        cont = get_elements_from_card(driver=cards_on_page[i])
        card_content.append(cont)
        i += 1
    # print('card_content: ', card_content)
    # Возвращаем список с карточками:
    return card_content

    # return get_elements_from_card(driver)
    # for fitch_element_card in fitches_elements_from_cards:
    #     print('fitch_element_card: ', get_fitches_elements_from_card(fitch_element_card))
        # print('fitch_element_card: ', fitch_element_card.text)
    # return

# Получаем данные по отдельным элементам:
def get_fitches_elements_from_card(driver):
    # name_zhk = driver.find_element(By.XPATH, "//a[@class='catalog-card__name']/div[1]").text
    # name_zhk = driver.find_element(By.XPATH, "//div[2]/a[1]/div[1]").text
    # name_zhk = driver.text

    # Работает:
    # Получаем название комплекса:
    # name_zhk = driver.find_element(By.XPATH, "a[1]").text
    name_zhk = driver.find_element(By.XPATH, "div[2]/a[1]/div[1]").text

    # Тестирование:
    # name_zhk = driver.find_element(By.XPATH, "div[2]/a[1]").text

    return name_zhk

def get_elements_from_card(driver):
    name_zhk: str = ''
    adress_zhk: str = ''
    adress_zhk_city: str = ''
    adress_zhk_region: str = ''
    adress_zhk_street: str = ''
    floors_zhk: int = 0
    price_zhk: int = 0
    sea_distance: str = ''
    update_zhk: str = ''

    # Название ЖК:
    try:
        # name_zhk = driver.find_element(By.XPATH, "//a[@class='catalog-card__name']/div[1]").text
        name_zhk = driver.find_element(By.XPATH, "div[2]/a[@class='catalog-card__name']/div[1]").text
    except:
        name_zhk = ''

    # Адрес:
    # Город:
    try:
        adress_zhk_city = driver.find_element(By.XPATH, "div[@class='catalog-card__address']/div[@class='catalog-card__address-container']/span[1]").text
    except:
        adress_zhk_city = ''
    # Район (встречаются тегм a или span):
    try:
        adress_zhk_region = driver.find_element(By.XPATH, "div[@class='catalog-card__address']/div[@class='catalog-card__address-container']/a[@class='catalog-card__address-element link']").text
    except:
        adress_zhk_region = driver.find_element(By.XPATH, "div[@class='catalog-card__address']/div[@class='catalog-card__address-container']/span[@class='catalog-card__address-element']").text
    # Улица:
    try:
        adress_zhk_street = driver.find_element(By.XPATH, "div[@class='catalog-card__address']/div[@class='catalog-card__address-container']/span[2]").text
    except:
        adress_zhk_street = ''
    # Сводный адрес:
    # adress_zhk = adress_zhk_city+adress_zhk_region+adress_zhk_street
    adress_zhk = ', '.join([adress_zhk_city, adress_zhk_region, adress_zhk_street])
    try:
        # Этажность:
        floors_zhk = driver.find_element(By.XPATH, "div[@class='catalog-card__main']/div[@class='catalog-card__properties']/div[2]").text
    except:
        floors_zhk = None
    # Цена за метр:
    try:
        price_zhk: int = driver.find_element(By.XPATH, "div[@class='catalog-card__prices']/div[@class='catalog-card__price-alt']/span[@class='value']").text
    except:
        price_zhk = None
    try:
        sea_distance = driver.find_element(By.XPATH, "div[@class='catalog-card__main']/div[@class='catalog-card__properties']/div[@class='catalog-card__property'][3]/div[@itemprop='value']").text
    except:
        sea_distance = None
    try:
        update_zhk = driver .find_element(By.XPATH, "div[@class='catalog-card__update']/div[@class='catalog-card__update-value']").text
    except:
        update_zhk = None
    # Проверка собранных данных:
    # print('get_elements_from_card: ', name_zhk, adress_zhk, floors_zhk, price_zhk, sea_distance, update_zhk, sep=' | ')
    return [name_zhk, adress_zhk, floors_zhk, price_zhk, sea_distance, update_zhk]

def prepare_DF():
    df = pd.DataFrame({'Жилищный комплекс': [], 'Район города': [], 'Адрес:': [], 'Этажность': [], 'Цена за кв.м.': [], 'Расстояние до моря': [], 'Актуальность на дату:': []})
    return df

if __name__ == '__main__':
    # Страница для обработки:
    site_page = "https://www.vincent-realty.ru/offers/novostroyki-v-sochi/"
    # 'https://www.vincent-realty.ru/offers/novostroyki-v-sochi/?PAGEN_1=1'
    router = '?PAGEN_1='
    # С какой страницы начинать парсинг сайта:
    score = 1
    # Карточка:
    cards = list()
    num_of_cards_on_page = int()

    # Открываем браузер и страницу с Новостройками в Сочи:
    driver = open_first_page_for_parsing(site_page=site_page)
    # Проверяем тег H1:
    # print('h1: ', driver.find_element(By.TAG_NAME, 'h1').text)

    # Собираем данные о ЖК из карточки сайта:
    # cards = parsing_cards_from_page(driver)
    # Проверяем на актуальность страницы сайта:
    while not check_404_page(driver):
        # Открываем целевую страницу:
        if score >= 1:
            # open_new_window()
            # driver.close()
            driver.get(page_for_parsing(site_page, router, score))
            # Собираем данные о ЖК из карточки сайта:
            # num_of_cards_on_page = parsing_num_of_cards_on_page(driver)
            # for num_of_card in num_of_cards_on_page:
            #     cards.append(get_elements_from_card(driver))
            cards_from_page = parsing_cards_from_page(driver)
            # Просмотр роутера запрашиваемой страницы:
            # print('\nsite_page, router, score: ', site_page, router, score, sep='\t')
            # Просмотр собранных данных:
            print('my_card: ', cards_from_page, end='\n\n')
            # cards.append(cards_from_page)
            cards.extend(cards_from_page)

        # Добавляем в счетчик для перехода на следующую страницу:
        score += 1
    else:
        # print('h1: ', driver.find_element(By.TAG_NAME, 'h1').text)
        # Закрываем браузер:
        # driver.close()
        pass

    print('Все карточки (cards): ', len(cards), type(cards), cards)

    # Извлекаем карточку:
    # print('Проверка записей карточек: ')
    # card = cards[0]
    # print('card 1: ', card)
    # card = cards[3]
    # print('card 3: ', card)

    # print('cards: ', *card)
    # Получаем элементы карточки:   <class 'tuple'> ('АК «Моне»', 'г. Сочи, Адлер, улица Ленина', '8 эт.', '700 000')
    # card_elements = get_elements_from_card(driver, card)
    # name_zhk = cards[0].find_element(By.XPATH, "//a[@class='catalog-card__name']/div[1]").text
    # print(name_zhk)

    # Печатаем полученные данные:
    # print('card_elements: ', len(card_elements), type(card_elements), card_elements)

    # Закрываем браузер:
    driver.quit()

    # Создаем дата-фрейм:
    df = pd.DataFrame(cards,
                      columns=['Жилищный комплекс', 'Адрес', 'Этажность', 'Цена за кв.м.', 'Расстояние до моря', 'Актуальность на дату'])
    # print(df)
    #
    # Очистка от дубликатов, оставляем только первые (более свежие):
    df = df.drop_duplicates()
    # # Запись в Excel:
    file_xlsx = 'Sochi.Novostroy.xlsx'
    try:
        writer = pd.ExcelWriter(file_xlsx, engine='xlsxwriter')
        df.to_excel(writer, index=False)
        writer.save()
        print("\033[34m{}".format(f'Данные сохранены в файл {file_xlsx}'))
    except:
        print("\033[37m{}".format(f'Ошибка записи данных в файл {file_xlsx}. Возможно, что файл открыт.'))
        # print(f'Ошибка записи данных в файл {file_xlsx}. Возможно, что файл открыт.')
    quit()