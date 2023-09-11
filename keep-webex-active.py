import pyautogui
import time

def keep_desktop_active():
    while True:
        # Get the current mouse position
        x, y = pyautogui.position()
        
        # Move the mouse pointer to a slightly different position
        pyautogui.moveTo(x + 5, y + 5, duration=1)  # Move the mouse pointer in a smooth manner
        
        # Wait for a few seconds
        time.sleep(5)
        
        # Move the mouse pointer back to the original position
        pyautogui.moveTo(x, y, duration=1)  # Move the mouse pointer in a smooth manner
        
        # Wait for a few seconds
        time.sleep(5)

if __name__ == "__main__":
    try:
        keep_desktop_active()
    except KeyboardInterrupt:
        print("Script terminated by user.")
