# Программа-Будильник.
# Три потока: 1.Основной, 2.Контроль за временем, 3.Ввод нового будильника
import asyncio
import threading
from threading import Thread

import datetime
from time import sleep
from time import strftime
import winsound

# Переменные:
# Устанавливаем время будильникам:
start_time = datetime.datetime.now()
# Таймер будильника:
alarm_time = [
    start_time + datetime.timedelta(seconds=2), # days, seconds, then other fields.
    start_time + datetime.timedelta(seconds=3),
    start_time + datetime.timedelta(seconds=4),
    start_time + datetime.timedelta(seconds=5),
    start_time + datetime.timedelta(seconds=6),
    start_time + datetime.timedelta(seconds=7)
]
alarm_time_1 = start_time + datetime.timedelta(seconds=5) # days, seconds, then other fields.
stop = False
timer_list = []

# first, we need a loop running in a parallel Thread
class AsyncLoopThread(Thread):
    def __init__(self, name: str=None, daemon: bool=True):
        super().__init__(name=name, daemon=daemon)
        self.loop = asyncio.new_event_loop()

    def run(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

class AlarmClock:
    # Отслеживаем сигнал активации для каждого будильника:
    async def control_alarm_time(self, alarm_time_unit, task, start_time, tone='short'):
        # Доступ к списку будильников для управления им:
        global alarm_time
        # Длительность и тональность сигнала:
        def alarm_tone(tone):
            # return winsound.Beep(350, 300) if tone == 'short' else winsound.Beep(400, 700)
            # return winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
            return winsound.PlaySound("SystemExit", winsound.SND_ALIAS) if tone == 'short' \
                else winsound.PlaySound("SystemQuestion", winsound.SND_ALIAS)
        print(f"Будильник №{task} заведен на время: {alarm_time_unit.strftime('%H:%M:%S %d.%m.%Y')}")
        # Устанавливаем таймер:
        sleep_time = alarm_time_unit - start_time
        sleep_time = int(sleep_time.total_seconds())
        # print(f"Время ожидания (сек.): {sleep_time}")
        # Устанавливаем паузу на время паузы:
        await asyncio.sleep(sleep_time)
        # Действия по срабатыванию будильника:
        print(f"Будильник {task} сработал! {datetime.datetime.now().strftime('%H:%M:%S')}")
        alarm_tone(tone)    # Издаем звуковой сигнал
        # Проверка работы будильников:
        # print(f"Работает цикл будильников: {loop_for_alarm_control.is_alive()} {datetime.datetime.now().strftime('%H:%M:%S')}")
        # print(f"Количество будильников: {len(alarm_time)}")

        # Удаляем из списка сработавший таймер:
        try:
            alarm_time.remove(alarm_time_unit)
            print(f"Удален будильник {task}")
        except:
            print(f"Не удалось удалить будильник {task}")
        return

    # Добавляем новый будильник - псевдо-добавление:
    async def input_alarm(self, text: str = 'Поток', pause: int = 0):
        global stop
        global timer_list
        print(f'Старт input_alarm - {text}')
        # while stop is not True:
        # while threading.main_thread().is_alive() is True:
        while loop_for_alarm_control.is_alive() is True:
            # pass
            try:
                # Проверка состояния будильников и потоков:
                # print(f"Работает цикл будильников: {loop_for_alarm_control.is_alive()} {datetime.datetime.now().strftime('%H:%M:%S')}")
                # print(f"Работает основной цикл: {threading.main_thread().is_alive()} {datetime.datetime.now().strftime('%H:%M:%S')}")

                get_alarm = int(input("Введите число: "))
                print("Спасибо, число принято: ", get_alarm)
                # Составляем список значений для таймеров:
                timer_list.append(get_alarm)
                print(f"Список полученных таймеров: {timer_list}")  # Проверка таймеров
                sleep(3)
                # stop = True
            except:
                print("Выход из режима input")
        print('--> Выход из функции input_alarm')
        return


# example coroutine
# async def coroutine(num, sec):
#     await asyncio.sleep(sec)
#     print(f'Coro {num} has finished')


if __name__ == '__main__':
    # init a loop in another Thread
    # Остальным потокам назначаем Daemon, чтобы процесс завершался:
    loop_for_alarm_control = AsyncLoopThread(name="Thr-1",daemon=True)
    loop_for_alarm_control.start()

    loop_for_input_alarm = AsyncLoopThread(name="Thr-2",daemon=True)
    # loop_for_input_alarm.start()

    alarm_clock = AlarmClock()
    # adding first 5 coros
    print('\nПервая серия будильников запускается:')
    for i in range(4):
        # print(f'Add Coro {i} to the loop')
        asyncio.run_coroutine_threadsafe(alarm_clock.control_alarm_time(alarm_time[i], i, start_time, tone='short'),
                                         loop_for_alarm_control.loop)
    sleep(5)
    # print('Adding 5 more coros')
    # Контрольная проверка активных потоков:
    # print("Список потоков:", threading.enumerate())

    # Запуск ввода данных:
    asyncio.run_coroutine_threadsafe(alarm_clock.input_alarm(text='Поток ввода данных'),
                                     loop_for_input_alarm.loop)

    # Контрольная проверка активных потоков:
    # print("Список потоков:", threading.enumerate())
    sleep(2)

    # adding 5 more coros
    print('\nВторая серия будильников запускается:')
    # for i in range(4, 7):
    for i in range(len(alarm_time)):
        # print(f'Add Coro {i} to the loop')
        # asyncio.run_coroutine_threadsafe(coroutine(i, 4), loop_for_main_thread.loop)
        asyncio.run_coroutine_threadsafe(alarm_clock.control_alarm_time(alarm_time[i], i, start_time, tone='long'),
                                         loop_for_alarm_control.loop)
    # let them all finish
    # sleep(20)

    # Пока поток с будильниками работает - продолжать работу программы:
    # while loop_for_alarm_control.is_alive() is True:
    # Пока в списке есть будильники - продолжать работу:
    while len(alarm_time):
        pass
    stop = True
    # sleep(10)
    print("--> Цикл main - завершен основной поток.")
    print("Список потоков:", threading.enumerate())
    print(f"Список будильников: {len(alarm_time)}, {alarm_time}")

    quit()