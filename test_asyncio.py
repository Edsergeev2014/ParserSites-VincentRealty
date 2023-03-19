import asyncio


async def async_func(task_no):
    print(f'{task_no}: Запуск ...')
    await asyncio.sleep(1)
    print(f'{task_no}: ... Готово!')


async def main():
    taskA = loop.create_task (async_func('taskA'))
    taskB = loop.create_task(async_func('taskB'))
    taskC = loop.create_task(async_func('taskC'))
    await asyncio.wait([taskA,taskB,taskC])


if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except :
        pass