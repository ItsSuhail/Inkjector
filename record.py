import sys 
import pickle
import pyautogui
from pynput import *
import time


coordinates = []

# def record():
#     position = pyautogui.position()
#     coordinates.add((position[0],position[1]))

# def serialize():


ready = False
held = False

def on_press(key):
    global ready
    if key == keyboard.Key.space:
        ready = True

def on_release(key):
    return False

def on_click(x,y, button, pressed):
    global ready, held

    if pressed and ready:
        held = True

    if not pressed and ready:
        ready = False
        held = False
        return False


with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

print("READY")

with mouse.Listener(on_click=on_click) as listener:
    while listener.running:
        if held:
            position = mouse.Controller().position
            if position not in coordinates:
                coordinates.append(position)

print("RELEASED")

print(coordinates)
time.sleep(10)
pyautogui.mouseDown(button="left")
for coords in coordinates:
    pyautogui.moveTo(coords[0], coords[1])
pyautogui.mouseUp(button="left")