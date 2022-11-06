# Задача: бот для посещения сайта nemykin-art.ru из поисковика yandex.ru
# с предварительной авторизацией на Яндекс

# Перед запуском проверить, установлен ли браузер Chrome на этом компьютере: https://www.google.com/intl/ru/chrome/
# Chromedriver скачать в соответствии с версией Chrome: https://chromedriver.chromium.org/downloads
# Продублировать его в venv проекта по пути: "venv\Lib\Chrome\chromedriver.exe"

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

import pandas as pd
import time
import re
import threading
import xlsxwriter
import logging
from site_visitor import Visitor as Visitor
from site_visitor import bcolors as bcolors

def prepare_DF():
    return # pd.DataFrame({'Жилищный комплекс': [], 'Район города': [], 'Адрес:': [], 'Этажность': [], 'Цена за кв.м.': [], 'Расстояние до моря': [], 'Актуальность на дату:': []})

let_me_visit = Visitor()
# site_page = let_me_visit.site_object_pages[0]

# Открываем браузер и первую страницу сайта - инициализация веб-драйвера:
let_me_visit.open_first_page_for_parsing(site_page=let_me_visit.site_object_pages[0])
# Открываем новую страницу:
# let_me_visit.open_new_window()
# Запускаем цикл со списком страниц сайта:
for page in let_me_visit.site_object_pages[0:]:
    # Переходим на целевую страницу сайта:
    print('Текущая страница сайта: ', page)
    let_me_visit.driver_set.get(page)
    # Store the ID of the original window
    original_window = let_me_visit.driver_set.current_window_handle
    # Скролинг вниз страницы
    scroll_target = let_me_visit.driver_set.find_element(By.CLASS_NAME, 'footer')
    let_me_visit.scroll(scroll_target)
    let_me_visit.scroll_page(500)  # Скролинг вниз на 500 пикселей
    let_me_visit.pause()

    # Проверяем количество открытых окон в браузере:
    print(f'{bcolors.OKBLUE}Кол-во открытых окон в браузере (1о): {len(let_me_visit.driver_set.window_handles)}{bcolors.ENDC}')

    try:        # Если рекламный блок найден
        print('Находим рекламу на странице сайта ->', end='')
        block_advert = let_me_visit.driver_set.find_element(By.XPATH, "//div[@id='yandex_rtb_R-A-1786435-3']")
        # print('block_advert: ', type(block_advert), block_advert)
        print(f'{bcolors.OKGREEN}{bcolors.BOLD} переходим на рекламу. {bcolors.ENDC}', end='')
        try:
            block_advert.click()
            print(f'{bcolors.OKBLUE} -> Переход выполнен.{bcolors.ENDC}')
        except:
            print(f'{bcolors.FAIL} -> Click на рекламу не сработал.{bcolors.ENDC}')
            continue

        # Проверяем, открылось ли новое окно:
        count_open_windows = len(let_me_visit.driver_set.window_handles)
        print(f'{bcolors.OKBLUE}Кол-во открытых окон в браузере (1о+1р): {count_open_windows}{bcolors.ENDC}')
        if count_open_windows > 1:
            # Последнее открытое окно в списке браузера: window_handles[-1]
            # Переходим в новое окно:
            let_me_visit.driver_set.switch_to.window(let_me_visit.driver_set.window_handles[-1])
            # print(f'Список открытых окон в браузере: {len(let_me_visit.driver_set.window_handles)}')
            # [print(let_me_visit.driver_set.window_handles[www]) for www in len(let_me_visit.driver_set.window_handles)]
        elif let_me_visit.driver_set.current_url == page:
            print(f'{bcolors.FAIL}Рекламный сайт не открылся.{bcolors.ENDC} Переходим на просмотр следующей страницы исходного сайта.')
            continue

        # Фиксируем время захода на рекламный сайт:
        let_me_visit.set_time()

        # Переход на рекламный сайт и эмуляция движения пользователя на нём:
        let_me_visit.amulation_moving()

        # Проверка времени, проведенного на рекамном сайте:
        # Время, отведенное для пребывания на рекламном сайте
        # составляет 16 сек.:
        while not let_me_visit.check_time_for_adv_site(16):
            let_me_visit.scroll_page(905) # Скролинг вниз на (...) пикселей
            let_me_visit.pause(5)
            let_me_visit.scroll_page(-750)
        # print(f'Проведенное время на рекл.сайте: {let_me_visit.get_time() - let_me_visit.time_set_recorded}')

        # Записываем в log-файл о посещении рекламного сайта
        # logging.debug('Hi')
        logging.info(f'{let_me_visit.driver_set.current_url}')
        # logging.warning('exit')

        # Возвращаемся на исходную страницу браузера:
        # let_me_visit.driver_set.switch_to.window(let_me_visit.driver_set.window_handles[0])
        print('Закрываем рекламу и возвращаемся на исходную страницу сайта.')
        print('')
        if count_open_windows > 1:
            # Закрываем лишние окна, оставляем - одно.
            let_me_visit.close_non_original_windows(original_window)
            # # Переходим на исходную страницу:
            let_me_visit.driver_set.switch_to.window(original_window)
        else:
            # Возвращаемся на исходную страницу сайта,
            # если рекламный сайт открыт в исходном окне:
            let_me_visit.driver_set.back()

        # Проверяем количество открытых окон в браузере:
        print(f'{bcolors.OKBLUE}Кол-во открытых окон в браузере (после очистки рекламного сайта): {len(let_me_visit.driver_set.window_handles)}{bcolors.ENDC}')

        # print('a_rel: ', type(a_rel), a_rel.get_attribute("href"))

    except:
        print(f'{bcolors.FAIL}Рекламного блока на этой странице сайта не найдено.{bcolors.ENDC}')

# Завершаем процесс
print('Процесс завершен.')

# Закрываем браузер:
let_me_visit.driver_set.quit()

# try:
#     #WebDriver code here...
# finally:
#     driver.quit()

del let_me_visit
quit()