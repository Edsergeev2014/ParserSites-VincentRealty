import threading
from time import sleep

# Переменная для завершения потоков
stop = False

# Выводим текст через заданную для каждого потока паузу:
def my_func_1(text: str = '', pause: int = 0):
    global stop
    while not stop:
        print(f'{text} : активный.')
        sleep(pause)
    print(f'{text} - остановлен.')
    return

# Ввод с клавиатуры
def my_func_2(text: str = '', pause: int = 0):
    global stop
    print(f'{text} : активный. ', end='')
    try:
        # Вариант с input(), альтернативые: sys.stdin() или fileinput.input():
        get_alarm = input('Введите что-либо с клавиатуры для завершения всех потоков: \n')

        if get_alarm:
            print('Вы установили будильник на время: ', get_alarm)
        else:
            print('Будильник не установлен')
    except:
        print(f'{text}: ожидание клавиатуры прервано.')
    print(f'{text} - остановлен.')
    stop = True
    return

# Поток, который отключает все потоки через заданный период.
def my_func_3(text: str = '', pause: int = 0, alive: int = 0):
    global stop
    score: int = 0
    print(text, f': активный. Время работы программы - {alive} сек.\n')
    # Проверка активности других потоков и контроль за временем жизни программы:
    while not stop:
        sleep(pause)
        score = score + pause
        # print('score = ', score)1

        if (score >= alive):
            print(text, ' - программа остановлена по заданному времени.')
            stop = True
            break
    # stop = True
    sleep(3)
    print(f'{text} - остановлен.')
    return

def main():
    # Ограничиваем время работы программы на время эксперимента (сек.):
    long_time_poccess = 10
    # Подготавливаем потоки:
    my_thread_2 = threading.Thread(target=my_func_1, args=('Поток 1', 2), name='Th2', daemon=True)
    my_thread_3 = threading.Thread(target=my_func_1, args=('Поток 2', 3), name='Th3', daemon=True)
    my_thread_4 = threading.Thread(target=my_func_2, args=('Поток 3', 1), name='Th4', daemon=True)
    my_thread_5 = threading.Thread(target=my_func_3, args=('Поток 4', 1, long_time_poccess), name='Th5')
    # Стартуем потоки:
    my_thread_2.start()
    my_thread_3.start()
    my_thread_4.start()
    my_thread_5.start()

if __name__ == '__main__':
    print('Основной поток: активный.')
    main()

