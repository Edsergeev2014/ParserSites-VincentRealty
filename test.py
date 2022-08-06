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

def check_404_page(driver):
    if driver.find_element(By.TAG_NAME, 'h1').text == 'Ошибка 404':
        print('h1: ', driver.find_element(By.TAG_NAME, 'h1').text)
        return True
    return False

def parsing_num_of_cards_on_page(driver):
    return driver.find_elements(By.XPATH, "//div[div/@class='catalog-card__detail']")
    # return get_elements_from_card(driver)

def parsing_cards_from_page(driver):
    cards_on_page = driver.find_elements(By.XPATH, "//div[div/@class='catalog-card__detail']")
    print('cards_on_page: ', len(cards_on_page), type(cards_on_page), cards_on_page)
    card_content = list()
    # card_content = [('ЖК «Проба»', 'г. Сочи, Проба, улица Проба', '5 эт.', '300 000', '04.11.2021')]
    # Проходим по всем карточкам и добавляем данные в список:
    print('cards_on_page: ', cards_on_page)
    i = 0
    for card_ in cards_on_page:
        print('card_: ', card_)
        print(f'cards_on_page[{i}]: ', cards_on_page[i])
        cont = get_elements_from_card(driver=cards_on_page[i])
        card_content.append(cont)
        i += 1
    print('card_content: ', card_content)
    # Возвращаем список:
    return card_content
    # return get_elements_from_card(driver)

def get_elements_from_card(driver):
    name_zhk: str = ''
    adress_zhk: str = ''
    adress_zhk_city: str = ''
    adress_zhk_region: str = ''
    adress_zhk_street: str = ''
    floors_zhk: int = 0
    price_zhk: int = 0
    update_zhk: str = ''

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
    update_zhk = driver.find_element(By.XPATH, "//div[@class='catalog-card__update-value']").text
    print('get_elements_from_card: ', name_zhk, adress_zhk, floors_zhk, price_zhk, update_zhk)
    return [name_zhk, adress_zhk, floors_zhk, price_zhk, update_zhk]

def parsing():
    return

def prepare_DF():
    df = pd.DataFrame({'Жилищный комплекс': [], 'Район города': [], 'Адрес:': [], 'Этажность': [], 'Цена за кв.м.': [], 'Актуальность на дату:': []})
    return df



if __name__ == '__main__':
    # Страница для обработки:
    site_page = "https://www.vincent-realty.ru/offers/novostroyki-v-sochi/"
    # 'https://www.vincent-realty.ru/offers/novostroyki-v-sochi/?PAGEN_1=1'
    router = '?PAGEN_1='
    # С какой страницы начинать парсинг:
    score = 15
    # Карточка:
    cards = list()


    # Открываем браузер и страницу с Новостройками в Сочи:
    driver = open_first_page_for_parsing(site_page=site_page)
    # Проверяем тег H1:
    # print('h1: ', driver.find_element(By.TAG_NAME, 'h1').text)

    # Get element with tag name 'div'
    element = driver.find_elements(By.TAG_NAME, 'div')
    print('element: ', len(element))
    # Get all the elements available with tag name 'p'
    elements = element[-1].find_elements(By.TAG_NAME, 'p')
    for e in elements:
        print('e.text:', e, e.text)
    driver.quit()
