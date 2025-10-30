import pickle
import pyautogui
from pynput import *
import sys
import time

def on_press(key):
    pass

def on_release(key):
    global mouse_coordinates
    try:
        if key.char == 'p':
            position = pyautogui.position()
            mouse_coordinates = (position[0], position[1])
            return False
        
    except AttributeError:
        pass

mouse_coordinates = ()

achaar = open("data.pkl", "rb")
data:dict
try:
    data = pickle.load(achaar)
except EOFError:
    print("Achaar empty")
    sys.exit()

while(True):
    print("CHOOSE (-1 for exit)\n\n")
    for key in data.keys():
        print(key, end=" ")

    print("\n")
    choice = input(": ")
    while(choice not in data.keys()):
        if choice == "-1":
            sys.exit()
        choice = input(": ")

    print("\nCHOSEN: ", choice, "\n")

    relative_coordinates_list = data[choice]['coordinates']
    max_x, max_y = data[choice]['max']

    print("Whenever ready, press P to draw using the mouse\n\n")

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    print("Drawing\n\n")

    min_x, min_y = mouse_coordinates
    # print(min_x,min_y)
    absolute_coordinates_list = []
    for coordinates in relative_coordinates_list:
        absolute_coordinates_list.append((coordinates[0] + min_x, coordinates[1] + min_y))

    pyautogui.moveTo(absolute_coordinates_list[0])
    pyautogui.mouseDown(button="left")
    for coordinates in absolute_coordinates_list:
        pyautogui.moveTo(coordinates)
    pyautogui.mouseUp(button="left")