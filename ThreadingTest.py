import threading
import datetime
import time

x = 0

## This is a test to check threading works
def thread_a():
    global x
    
    while True:
        time.sleep(1)
        print(x)

def thread_b():
    global x
    while True:
        time.sleep(0.8)
        x += 1

thread1 = threading.Thread( target=thread_a )
thread2 = threading.Thread( target=thread_b)

thread1.start()
thread2.start()

## Ok threading works
