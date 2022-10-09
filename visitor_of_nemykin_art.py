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

import pandas as pd
import time
import threading
import xlsxwriter

class Visitor:

    def __init__(self):
        self.site_object = 'http://nemykin-art.ru'
        self.site_object_pages = [
            'http://nemykin-art.ru/gallery.html',
            'http://nemykin-art.ru/about.html',
            # 'http://nemykin-art.ru/exhibition.html',
            # 'http://nemykin-art.ru/index.html'
        ]
        self.driver_set = None  # Запись драйвера в переменную класса после первого открытия браузера

    def open_first_page_for_parsing(self, site_page: str = None):
        service_obj = Service("venv\Lib\Chrome\chromedriver.exe")
        option = Options()
        option.add_argument("--disable-infobars")
        # Запись драйвера в переменную класса:
        self.driver_set = webdriver.Chrome(service=service_obj,
                                  # chrome_options=option
                                  )
        # driver.get("https://www.google.com")
        self.driver_set.get(site_page)
        return

    def pause(self, time_period=2):
        # threading.Event.wait(2)
        time.sleep(time_period)  # Pause (time_period) seconds
        return

    def scroll(self, scroll_target):
        try:
            ActionChains(self.driver_set).scroll_to_element(scroll_target).perform()
            return True
        except:
            return False

    def close_non_original_windows(self, original_window):
        for handle in self.driver_set.window_handles:
            self.driver_set.switch_to.window(handle)
            if handle != original_window:
                self.driver_set.close()
        return

    def amulation_moving(self):
        # Переход на рекламный сайт и эмуляция движения в нем:
        print(f'{bcolors.BOLD}Url рекламного сайта: {bcolors.ENDC}', self.driver_set.current_url)
        tags = ['h1', 'h2', 'footer', 'title', 'form', 'head', 'button', 'nav', 'a']
        count = 0
        for tag in tags:
            print(f'Поиск тега "{bcolors.HEADER}{tag}{bcolors.ENDC}" - ', end='')
            try:
                scroll_target = self.driver_set.find_element(By.TAG_NAME, tag)
                print(f'{bcolors.OKGREEN} найден на странице.{bcolors.ENDC}')
                print(f'{bcolors.OKCYAN} -> cкролинг страницы{bcolors.ENDC}', end='')
                let_me_visit.scroll(scroll_target)
                print(' -> пауза', end='')
                let_me_visit.pause(3)  # Pause 2 seconds
                print(' -> пауза завершена.')
                if tag == (tags[-1] or tags[-2]):     # 'button', 'a'
                    print(f'Переход по ссылке {tag} с рекламного сайта...', end='')
                    try:
                        scroll_target.click()
                        print('  ...пауза.')
                        self.pause()
                        print(f'Возвращаемся к рекламному сайту.')
                        self.driver_set.back()
                    except:
                        print(f'{bcolors.WARNING} Выполнение прервано.{bcolors.ENDC}')
                        self.driver_set.switch_to.window(let_me_visit.driver_set.window_handles[-1])
                else:
                    continue
            except Exception:
                print(f'{bcolors.WARNING}не найден на странице.{bcolors.ENDC}')
        return

    def open_new_window(self):
        self.driver_set.execute_script("window.open('');")
        self.driver_set.switch_to.window(self.driver_set.window_handles[1]) #  есть только 1 открытая вкладка:
        # driver.switch_to.window(len(driver.window_handles)-1)   # Если уже открыто более 1 вкладки, вы должны сначала получить индекс последней вновь созданной вкладки и переключиться на вкладку, прежде чем вызывать URL-адрес (заслуга tylerl) :
        return

    def page_for_parsing(self, page, router, score):
        site_page = ''.join([page, router, str(score)])
        print('site_page: ', site_page)
        return site_page

    # Проверка на несуществующую страницу:
    def check_404_page(self, driver):
        if driver.find_element(By.TAG_NAME, 'h1').text == 'Ошибка 404':
            # print('h1: ', driver.find_element(By.TAG_NAME, 'h1').text)
            print('Сбор данных с сайта завершен.')
            return True
        return False

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

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
    let_me_visit.pause()

    # Проверяем количество открытых окон в браузере:
    print(f'{bcolors.OKBLUE}Кол-во открытых окон в браузере (1о): {len(let_me_visit.driver_set.window_handles)}{bcolors.ENDC}')

    try:        # Если рекламный блок найден
        print('Находим рекламу на странице сайта ->', end='')
        block_advert = let_me_visit.driver_set.find_element(By.XPATH, "//div[@id='yandex_rtb_R-A-1786435-3']")
        # print('block_advert: ', type(block_advert), block_advert)
        print(f'{bcolors.OKGREEN}{bcolors.BOLD} переходим на рекламу. {bcolors.ENDC}')
        try:
            block_advert.click()
        except:
            print(f'{bcolors.FAIL} Click на рекламу не сработал.{bcolors.ENDC}')
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

        # Переход на рекламный сайт и эмуляция движения пользователя на нём:
        let_me_visit.amulation_moving()

        # Возвращаемся на исходную страницу браузера:
        # let_me_visit.driver_set.switch_to.window(let_me_visit.driver_set.window_handles[0])
        print('Возвращаемся на исходную страницу.')
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
        print(f'{bcolors.FAIL} Рекламного блока на этой странице сайта не найдено.{bcolors.ENDC}')

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