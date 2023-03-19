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
        self.time_set_recorded = None
        logging.basicConfig(filename='assets/logs/nemykin_art_adv_robot.log', level=logging.INFO,
                            filemode="a",  # a - append, w - write (стереть старое, написать новое)
                            format="%(asctime)s %(levelname)s %(message)s")

    def open_first_page_for_parsing(self, site_page: str = None):
        service_obj = Service("venv\Lib\Chrome\chromedriver.exe")
        option = Options()
        # option.add_argument("--disable-infobars")
        # option.add_argument("window-size=560,700")
        # Запись драйвера в переменную класса:
        self.driver_set = webdriver.Chrome(service=service_obj,
                                  # chrome_options=option
                                  )
        self.driver_set.set_window_size(560, 700)
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

    def scroll_page(self, y_size: int = 1920):
        try:
            # print('Скролинг страницы.')
            self.driver_set.execute_script(f"window.scrollTo(0, {y_size})")
        except:
            # print('Скролинг страницы не удался.')
            pass
        return

    def close_non_original_windows(self, original_window):
        for handle in self.driver_set.window_handles:
            self.driver_set.switch_to.window(handle)
            if handle != original_window:
                self.driver_set.close()
        return

    def amulation_moving(self):
        # Переход на рекламный сайт и эмуляция движения в нём
        # скролингом и паузами:
        print(f'{bcolors.BOLD}Url рекламного сайта: {bcolors.ENDC}', self.driver_set.current_url)
        tags = ['h1', 'h2',
                # 'footer', 'title', 'form', 'head', 'nav',
                'button', 'a']
        set_of_links = list()
        count = 0
        for tag in tags:
            print(f'Поиск тега "{bcolors.HEADER}{tag}{bcolors.ENDC}" - ', end='')
            try:
                scroll_target = self.driver_set.find_element(By.TAG_NAME, tag)
                print(f'{bcolors.OKGREEN} найден на странице.{bcolors.ENDC}')
                print(f'{bcolors.OKCYAN} -> cкролинг страницы{bcolors.ENDC}', end='')
                self.scroll(scroll_target)
                print(' -> пауза', end='')
                self.pause(3)  # Pause 2 seconds
                print(' -> пауза завершена.')
                if tag == (tags[-1] or tags[-2]):     # 'button', 'a'
                    print(f'Переход по ссылке "{bcolors.HEADER}{tag}{bcolors.ENDC}" на рекламном сайте... ')
                    try:
                        # Проводим валидацию url и печатаем его:
                        print('Текст ссылки: ', self.get_url(scroll_target.get_attribute('href')))
                        # Получаем список ссылок на сайте:
                        try:
                            # # Запоминаем текущий url:
                            # if self.driver_set.current_url:
                            #     clear_current_url = re.search('https?://([A-Za-z_0-9.-]+).*', self.driver_set.current_url)
                            #     if clear_current_url:
                            #         print('clear_current_url: ', clear_current_url.group(1))

                            # Получаем список ссылок с рекламного сайта:
                            set_of_links = self.get_tags_with_href_to_http(tag=tag)
                            # print('set_of_links: ', type(set_of_links), set_of_links)

                            # Переходим по ссылке:
                            # print('✓') # Галочка
                            try:
                                # print(bcolors.OKBLUE + f"Пробуем Enter по ссылке -> {set_of_links[0]}", end='')
                                # if self.find_scroll_pause_click(tag=tag, pause=2, href=set_of_links[0], click_or_enter="Enter"):
                                #     print("Enter!", end='')
                                # # set_of_links[0].send_keys(Keys.RETURN)
                                # # scroll_target.send_keys(Keys.RETURN)
                                # print('-> переход состоялся.', end='')
                                print()
                                print(bcolors.OKCYAN + f"Пробуем Click по ссылке {set_of_links[0]}", end='')
                                if self.find_scroll_pause_click(tag=tag, pause=2, href=set_of_links[0], click_or_enter="Click"):
                                    print("Click!", end='')
                                # set_of_links[0].click()
                                # scroll_target.click()
                                print(bcolors.OKGREEN + ' -> переход состоялся.', bcolors.ENDC)
                                try:
                                    # Записываем в лог посещение рекламы
                                    # если это другой рекламный сайт:
                                    if len(set_of_links) > 1:
                                        clear_current_url = re.search('https?://([A-Za-z_0-9.-]+).*',
                                                                      self.driver_set.current_url)
                                        if clear_current_url:
                                            # Записываем, если найдена новая уникальная ссылка на другой сайт:
                                            clear_current_url = clear_current_url.group(1)

                                            for link in set_of_links:
                                                if clear_current_url not in link:
                                                    logging.info(f'{link}')
                                                    # logging.info(f'{set_of_links[0]}')
                                except:
                                    print(f'Запись в лог "{set_of_links[0]}" не удалась')
                            except:
                                print('\n' + bcolors.FAIL + " Не удается кликнуть по ссылке.", end='')
                            else:
                                # Выполняется в любом случае:
                                print('  ...пауза.' + bcolors.ENDC)
                                self.pause()
                                print(f'Возвращаемся к рекламному сайту.')
                                self.driver_set.back()
                        except:
                            print(bcolors.WARNING + 'Что-то пошло не так со списком ссылок.' + bcolors.ENDC)
                    except:
                        print(f'{bcolors.WARNING} Выполнение прервано.{bcolors.ENDC}')
                        self.driver_set.switch_to.window(self.driver_set.window_handles[-1])
                else:
                    continue
            except Exception:
                print(f'{bcolors.WARNING} -> не найден на странице.{bcolors.ENDC}')

        return

    # Метод выполняем поиск тега, скролинг до него, пауза и клик по элементу
    def find_scroll_pause_click(self, tag: str = None, pause: int = 2, href: str = None, click_or_enter: str = 'Click'):
        try:
            # Находим элемент с указанным тегом и ссылкой:
            print(f'-> Находим элемент с указанным тегом "{tag}" и ссылкой: "{href}".', end='')
            target_element = self.driver_set.find_element(By.XPATH, f"//{tag}[contains(@href,'{href}')]")
            # Производим скролинг страницы до этого элемента:
            print(' -> Производим скролинг страницы до этого элемента. ', end='')
            self.scroll(scroll_target=target_element)
            # Держим паузу:
            print(' -> Держим паузу.', end='')
            self.pause(time_period=pause)
            # Кликаем по ссылке:
            if click_or_enter ==  "Enter по ссылке. ":
                print(' -> Enter по ссылке. ', end='')
                target_element.send_keys(Keys.RETURN)
            else:
                print(' -> Кликаем по ссылке. ', end='')
                target_element.click()
            # Возвращаем удачное выполнение метода
            print(f'{bcolors.OKGREEN} -> удачное выполнение.{bcolors.ENDC}')
            self.pause(2)
            return True
        except:
            # Возвращаем неудачное выполнение метода
            print(f'{bcolors.FAIL} -> неудачное выполнение.{bcolors.ENDC}')
            return False

    # Поиск самой длинной url:
    def longest_home_site_url(self, links: list, home_site_url: str):
        # Обработка запроса на самую длинную url текущего сайта:
        len_of_long_home_site_url: int() = len(home_site_url)  # Длина самой длинной ссылки
        long_home_site_url_str = home_site_url  # Самая длинная ссылка
        for link in links:
            if home_site_url in link:
                if len(link) > len_of_long_home_site_url:
                    long_home_site_url_str = link
                    len_of_long_home_site_url = len(long_home_site_url_str)
        return long_home_site_url_str

    # Удаление лишних адресов из списка
    def remove_useless_urls(self, links: set, home_site_url: str = None, long_home_site_url: bool = False):
        list_of_links = list()  # Переменная для сбора подходящих ссылок из links
        # Обработка запроса на самую длинную url текущего сайта:
        longest_home_site_url = str(None)
        if long_home_site_url:
            if home_site_url:
                longest_home_site_url = self.longest_home_site_url(links=list(links), home_site_url=home_site_url)
            else:
                print('Ошибка: отсутствует аргумент home_site_url при запросе длины url текущего сайта')
                return False
        try:
            print('Начало очистки ссылок.')
            links = list(links)
            # Список сайтов соц.сетей и прочих:
            useless_urls: list = ['vk.com', 'yandex.ru', 'yandex.net', 'google', 'whatsapp',
                                 'wa.me', 'instagram', 'youtube', 't.me', 'ok.ru'
                                 'metrika', 'twitter', 'facebook', '2gis.com']
            # Если присутствует в запросе тек.сайт - добавляем в список неиспользуемых :
            if home_site_url:
                useless_urls.append(home_site_url)

            print('Ссылки links (до удаления): ', len(links), links)
            print('Сбор подходящих ссылок.')
            check = False
            for link in links:
                for useless_url in useless_urls:
                    if not str(useless_url) in str(link):
                        check = True
                    else:
                        check = False
                        break
                # Если в ссылке нет ссылок-исключений, то добавляем:
                if check: list_of_links.append(str(link))
            # Добавляем в список самый длинный url текущего сайта:
            if longest_home_site_url:
                list_of_links.append(longest_home_site_url)
            print('Cписок links после очистки: ', len(list_of_links), list_of_links)
        except Exception as e:
            print('Сбой очистки:', e)

        return list_of_links

    # Распознавание url-адресов:
    def get_url(self, link):
        # url_link = re.search(r'://([\w.]+)', link)
        # Источник очищения url: https://daringfireball.net/2009/11/liberal_regex_for_matching_urls
        url_link = re.search(r'\b(([\w-]+://?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([^[:punct:]\s]|/)))', link)
        if url_link:
            # return 'очищенный url - ' + url_link.group(1)
            return url_link.group(1)
        else:
            return None

    # Поиск всех ссылок a. Выводит аттрибут href:
    def get_all_tags_a_with_href(self, tag='a'):
        tag_elements = self.driver_set.find_elements(By.TAG_NAME, tag)
        # [print(f'href: "{tag_element.get_attribute("href")}') for tag_element in tag_elements]
        [print(f'href: {self.get_url(link=tag_element.get_attribute("href"))}') for tag_element in tag_elements]
        return

    # Поиск внешних ссылок на рекламном сайте:
    def get_tags_with_href_to_http(self, tag):
        # Поиск всего списка ссылок:
        links = None
        try:
            tag_elements = self.driver_set.find_elements(By.TAG_NAME, tag)
            if len(tag_elements) > 0:
                print('Количество ссылок в списке (необработанных): ', len(tag_elements))
                # Печать списка ссылок без валидации:
                # [print(f'href: "{tag_element.get_attribute("href")}') for tag_element in tag_elements]
                # Печать списка ссылок с учетом их валидации url:
                # [print(f'href: {self.get_url(tag_element.get_attribute("href"))}') for tag_element in tag_elements]
                # Готовим set для уникального списка:
                links = set()
                # Перебираем список, выбираем только содержащие url, удаляем дубликаты:
                [links.add(self.get_url(tag_element.get_attribute("href"))) for tag_element in tag_elements]
                if len(links) > 0:
                    print('Список url без дубликатов и None: ', links)
                    # Удаляем пустые ссылки:
                    links.discard(None)
                    # print('Список url без None: ', links)
                    # Запоминаем текущий url:
                    clear_current_url = None
                    if self.driver_set.current_url:
                        clear_current_url = re.search('https?://([A-Za-z_0-9.-]+).*', self.driver_set.current_url)
                        if clear_current_url:
                            # Записываем первое совпадение:
                            clear_current_url = clear_current_url.group(1)
                            print('clear_current_url: ', clear_current_url)
                            # Отфильтровать из списка адреса, содержащие текущий домен:
                            # for link in links:
                            #     if str(clear_current_url) in str(link):
                            #         links.discard(link)
                            #         print(f'Удалена ссылка "{link}".')
                    # Очищение url-списка от соц.сетей и метрики
                    # И запрос самой длинной строки url текущего сайта:
                    links = self.remove_useless_urls(links=links, home_site_url=clear_current_url, long_home_site_url=True) # links - list()
                    # Очищение списка от текущего url
                    print(f'Список url очищенный: {len(links), links}')
                else:
                    print(f"После очистки список ссылок {tag} с аттрибутом href - пуст.")
            else:
                print('Список url пуст')
        except:
            print('Сброс выполнения. Возможно, не найден тег на рекламном сайте.')
        return list(links)  # Возвращаем для удобста в формате list

    def open_new_window(self):
        self.driver_set.execute_script("window.open('');")
        self.driver_set.switch_to.window(self.driver_set.window_handles[1]) #  есть только 1 открытая вкладка:
        # driver.switch_to.window(len(driver.window_handles)-1)   # Если уже открыто более 1 вкладки, вы должны сначала получить индекс последней вновь созданной вкладки и переключиться на вкладку, прежде чем вызывать URL-адрес (заслуга tylerl) :
        return

    def page_for_parsing(self, page, router, score):
        site_page = ''.join([page, router, str(score)])
        print('site_page: ', site_page)
        return site_page

    def check_time_for_adv_site(self, wish_time_period: float = 16.1):
        print(f'Время на рекламном сайте: {int(self.get_current_time()-self.get_time())} из {wish_time_period} сек.')
        return True if wish_time_period < (self.get_current_time()-self.get_time()) else False

    def get_current_time(self):
        return time.time()

    def set_time(self):
        self.time_set_recorded = self.get_current_time()
        return

    def get_time(self):
        return self.time_set_recorded

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
