import pyautogui
import math

# 🧭 GeoGuessr visible bounds
MAP_LAT_TOP = 79.60718209187159
MAP_LAT_BOTTOM = -75.13436080504677
MAP_LNG_LEFT = -180+(180-177.41022961230206)   # West (left)
MAP_LNG_RIGHT = 180+(180-159.59726616037182) # East (right), wraps around

def mercator_project(lat):
    lat = max(min(lat, 89.9999), -89.9999)
    rad = math.radians(lat)
    return math.log(math.tan(rad) + 1 / math.cos(rad))

def normalize_longitude(lng, left, right):
    width = right - left
    return (lng - left) / width







def latlng_to_map_pixel(lat, lng, map_left, map_top, map_width, map_height):
    # Normalize X (longitude)
    x = normalize_longitude(
        lng,
        MAP_LNG_LEFT,
        MAP_LNG_RIGHT
    )

    # Normalize Y (latitude using Mercator)
    merc_y = mercator_project(lat)
    merc_top = mercator_project(MAP_LAT_TOP)
    merc_bot = mercator_project(MAP_LAT_BOTTOM)
    y = (merc_top - merc_y) / (merc_top - merc_bot)

    # Scale to pixels
    px = int(map_left + x * map_width)
    py = int(map_top + y * map_height)
    return px, py

def click_on_map(lat, lng):
    # Your calibrated values

    map_left = 558
    map_top = 240
    map_width = 1089
    map_height = 713
    px, py = latlng_to_map_pixel(lat, lng, map_left, map_top, map_width, map_height)

    print(f"🗺️ Clicking on map at: ({px}, {py}) for lat/lng: ({lat}, {lng})")
    pyautogui.moveTo(px, py, duration=0.2)
    pyautogui.click()
    pyautogui.moveTo(1099, 972, duration=0.2)
    pyautogui.click()
