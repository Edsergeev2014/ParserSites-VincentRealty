import time

import aiohttp
import asyncio

async def site_content(task, site_url):
    async with aiohttp.ClientSession() as session:
        check_time = time.time()
        async with session.get(site_url) as response:
            assert response.status == 200
            print(task, "Real url:", response.real_url)
            print(task, "Status:", response.status)
            print(task, "Content-type:", response.headers['content-type'])
            print(task, "Cookies:", response.cookies)
            print(task, "Headers:", response.headers)
            html = await response.text()
            print(task, "Body:", html[:15], "...")
            print(f"Время для запроса данных от '{site_url}': ", "%.2f" % round(time.time()-check_time,2))
            print()

async def trimer(period):
    print("Запуск таймера")
    return 


async def main():
    task1 = loop.create_task(site_content(task='1', site_url='http://roma-masha.ru'))
    task2 = loop.create_task(site_content(task='2', site_url='http://venera-mart.ru'))
    task3 = loop.create_task(site_content(task='3', site_url='http://orgcompany.ru'))
    task4 = loop.create_task(site_content(task='4', site_url='http://nemykin-art.ru'))
    await asyncio.wait([task1,task2,task3,task4])

if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except :
        pass