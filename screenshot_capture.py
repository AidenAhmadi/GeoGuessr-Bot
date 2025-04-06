import pygetwindow as gw
import pyautogui
import time

def capture_geoguessr_window(output_path="geoguessr_window.png", window_title_contains="GeoGuessr"):
    windows = [w for w in gw.getWindowsWithTitle(window_title_contains) if w.visible]
    if not windows:
        print("❌ No GeoGuessr window found.")
        return None

    window = windows[0]
    window.activate()  # 👈 bring it to the front
    time.sleep(0.5)    # 👈 give the OS time to redraw window on top
    bbox = (window.left, window.top, window.width, window.height)
    screenshot = pyautogui.screenshot(region=bbox)
    screenshot.save(output_path)
    print(f"✅ Screenshot saved to {output_path}")
    # Approximate screen coordinates of the minimap button
# You may need to calibrate this depending on your screen res and window size
    pyautogui.moveTo(1380, 793, duration=0.1) #click on mini map Point(x=1380, y=793)
    pyautogui.click()
    pyautogui.moveTo(1157, 570, duration=0.1)#Point(x=1157, y=570)
    pyautogui.click()
    pyautogui.moveTo(906, 368, duration=0.1)#Point(x=906, y=368)
    pyautogui.click()
    time.sleep(0.4) 

    return output_path
