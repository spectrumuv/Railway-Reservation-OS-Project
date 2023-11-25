import threading
import time

# Global semaphore
semaphore = threading.Semaphore(1)  # Initialize semaphore with initial value 1

def thread_function(name):
    print(f'Thread {name} is trying to acquire the semaphore')
    with semaphore:
        print(f'Thread {name} has acquired the semaphore')
        time.sleep(2)
        print(f'Thread {name} is releasing the semaphore')

# Creating multiple threads
threads = []
for i in range(3):
    thread = threading.Thread(target=thread_function, args=(i,))
    threads.append(thread)
    thread.start()

# Wait for all threads to finish
for thread in threads:
    thread.join()

print('All threads have finished')
