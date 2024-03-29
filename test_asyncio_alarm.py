import asyncio
import datetime

# Устанавливаем время будильникам:
alarm_time_1 = datetime.datetime.now() + datetime.timedelta(seconds=5) # days, seconds, then other fields.
alarm_time_2 = datetime.datetime.now() + datetime.timedelta(seconds=10)
alarm_time_3 = datetime.datetime.now() + datetime.timedelta(seconds=3)
start_time = datetime.datetime.now()

# Отслеживаем сигнал активации для каждого будильника:
async def check_alarm_time(alarm_time, task, start_time):
    print(f"Будильник №{task} поставлен на зарядку на время: {alarm_time.strftime('%H:%M %d.%m.%Y')}")
    sleep_time = alarm_time - start_time
    sleep_time = int(sleep_time.total_seconds())
    await asyncio.sleep(sleep_time)
    print(f"Будильник {task} сработал! {datetime.datetime.now().strftime('%H:%M %Sсек.')}")
    return

async def input_alarm():
    get_alarm = int(input("Введите число: "))
    await asyncio.sleep(2)
    print("Спасибо, число принято: ", get_alarm)
    return

# Заряжаем все будильники:
async def main():
    taskA = loop.create_task (check_alarm_time(alarm_time_1, 1, start_time))
    taskB = loop.create_task (check_alarm_time(alarm_time_2, 2, start_time))
    taskC = loop.create_task (check_alarm_time(alarm_time_3, 3, start_time))
    taskZ = loop.create_task(input_alarm())
    await asyncio.wait([taskA,taskB,taskC,taskZ])

if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
        # asyncio.run(main())
        loop.close()
    except :
        pass