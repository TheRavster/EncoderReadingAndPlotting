"""
Created on Fri Sep 20 20:18:56 2024

Script to test multithreading aspect of 'q' to quit idea...

Shows this works fine with a simple function, but something goes wrong when
using this logic with a function that has a serial.inwaiting call like
animPlot() -> see hashed out code in main.py :(
    
    - NOTE 1!! Must run in terminal in sudo to execute this functionality
    - NOTE 2!! On Mac must give terminal permission to control computer
    - If not allowed, q exit will not be recognized
    - GO -> System Settings/Privacy and Security/Accessibility/Terminal ALLOW

@author: brutal_blondie
"""

from multiprocessing import Process
import keyboard
import time

def my_loop(x):
    while True:
        print(str(x))
        time.sleep(3)
    
def f(x):
    y = x*3
    return y

if __name__ == '__main__':
    # test function
    x=2
    y = f(2)
    print('hey heres a thing before the loop!')
    print(y)
    # multithred loop
    process = Process(target=my_loop, args = (x,))
    process.start()
    while process.is_alive():
        if keyboard.is_pressed('q'):
            process.terminate()
            break
    print('hey heres a thing after the loop!')
    
