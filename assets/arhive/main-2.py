# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By

import time

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

def check_404_page(driver):
    if driver.find_element(By.TAG_NAME, 'h1').text == 'Ошибка 404':
        print('h1: ', driver.find_element(By.TAG_NAME, 'h1').text)
        return True
    return False

def parsing_num_of_cards_on_page(driver):
    return driver.find_elements(By.XPATH, "//div[div/@class='catalog-card__detail']")
    # return get_elements_from_card(driver)

def get_elements_from_card(driver):
    name_zhk: str = ''
    adress_zhk: str = ''
    adress_zhk_city: str = ''
    adress_zhk_region: str = ''
    adress_zhk_street: str = ''
    floors_zhk: int = 0
    price_zhk: int = 0

    # Название ЖК:
    name_zhk = driver.find_element(By.XPATH, "//a[@class='catalog-card__name']/div[1]").text
    # Адрес:
    adress_zhk_city = driver.find_element(By.XPATH, "//div[@class='catalog-card__address-container']/span[1]").text
    adress_zhk_region = driver.find_element(By.XPATH, "//div[@class='catalog-card__address-container']/a[@class='catalog-card__address-element link']").text
    adress_zhk_street = driver.find_element(By.XPATH, "//div[@class='catalog-card__address-container']/span[2]").text
    # adress_zhk = adress_zhk_city+adress_zhk_region+adress_zhk_street
    adress_zhk = ', '.join([adress_zhk_city, adress_zhk_region, adress_zhk_street])
    # Этажность:
    floors_zhk = driver.find_element(By.XPATH, "//div[@class='catalog-card__properties']/div[2]").text
    # Цена за метр:
    price_zhk = driver.find_element(By.XPATH, "//div[@class='catalog-card__price-alt']/span[@class='value']").text

    return name_zhk, adress_zhk, floors_zhk, price_zhk

if __name__ == '__main__':
    # Страница для обработки:
    site_page = "https://www.vincent-realty.ru/offers/novostroyki-v-sochi/"
    # 'https://www.vincent-realty.ru/offers/novostroyki-v-sochi/?PAGEN_1=1'
    router = '?PAGEN_1='
    # С какой страницы начинать парсинг:
    score = 14
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
        if score >= 2:
            # open_new_window()
            # driver.close()
            driver.get(page_for_parsing(site_page, router, score))
            # Собираем данные о ЖК из карточки сайта:
            num_of_cards_on_page = parsing_num_of_cards_on_page(driver)
            for num_of_card in num_of_cards_on_page:
                cards.append(get_elements_from_card(driver))

        # Добавляем в счетчик для перехода на следующую страницу:
        score += 1
    else:
        # print('h1: ', driver.find_element(By.TAG_NAME, 'h1').text)
        # Закрываем браузер:
        # driver.close()
        pass

    print('cards: ', len(cards), type(cards), cards)

    # Извлекаем карточку:
    card = cards[0]
    print('card: ', card)
    # Получаем элементы карточки:   <class 'tuple'> ('АК «Моне»', 'г. Сочи, Адлер, улица Ленина', '8 эт.', '700 000')
    # card_elements = get_elements_from_card(driver, card)
    # name_zhk = cards[0].find_element(By.XPATH, "//a[@class='catalog-card__name']/div[1]").text
    # print(name_zhk)

    # Печатаем полученные данные:
    # print('card_elements: ', len(card_elements), type(card_elements), card_elements)

    # Закрываем браузер:
    driver.quit()