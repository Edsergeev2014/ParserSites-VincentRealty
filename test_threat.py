import schedule, time, threading, queue

# def message(pause_time: int = 10):
#    print(f"-> 3. Вызов из Потока #1 каждые {pause_time} сек.")

def thread_message(pause_time: int = 7):
   print(f"-> 2. Вызов из функции thread_flow каждые {pause_time} сек. => Поток {threading.current_thread()}")


def thread_flow(job_func):
   job_thread = threading.Thread(target=job_func)
   job_thread.start()


def worker_main():
   while 1:
      job_func = jobqueue.get()
      job_func()
      jobqueue.task_done()

jobqueue = queue.Queue()

# def thread_run(pause_time):
#    # while True:
#    for i in range(0, 10):
#       # schedule.run_pending()
#       print(f'Вызов из Потока #3: каждые {pause_time} сек. Thread #{threading.current_thread()}')
#       time.sleep(pause_time)

# Поток #1
# Вызов Schedule_1
# schedule.every(1).minutes.do(mess)
# pause_time = 7
# schedule.every(pause_time).seconds.do(message, pause_time)
# # schedule.every(pause_time).seconds.do(message(pause_time))
# print("Запущен Поток #1")

# Поток #2
# pause_time = 5
# schedule.every(pause_time).seconds.do(thread_flow, thread_message(pause_time))
# schedule.every(pause_time).seconds.do(thread_flow, thread_message(pause_time))
# schedule.every(pause_time).seconds.do(thread_flow, thread_message(pause_time))
# schedule.every(pause_time).seconds.do(thread_flow, thread_message(pause_time))
# print("Запущен Поток #2")

# Поток #3
# Отдельный поток-1 со своим циклом
# pause_time = 9
# thread_start = threading.Thread(target=thread_run(pause_time))
# print("Запущен Поток #3")
# thread_start.setName("Potok#3")
# thread_start.start()
# thread_start.join()

# # Поток #4
# # Отдельный поток-2 со своим циклом
# threading.Thread(target=thread_flow(thread_message)).start()
# print("Запущен Поток #4")

# Поток #5
pause_time = 7
schedule.every(pause_time).seconds.do(jobqueue.put, thread_message(pause_time))
schedule.every(pause_time).seconds.do(jobqueue.put, thread_message(pause_time))
schedule.every(pause_time).seconds.do(jobqueue.put, thread_message(pause_time))
threading.Thread(target=worker_main()).start()

# Поток #6
# Основной поток
pause_time = 1
while True:
   print(f'-> 1. Вызов из Потока #6: каждые {pause_time} сек.')
   schedule.run_pending()
   # print("Запущен Поток #5")
   time.sleep(pause_time)
