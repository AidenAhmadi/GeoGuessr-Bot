import openai
import base64
import os
import re
from dotenv import load_dotenv
from screenshot_capture import capture_geoguessr_window
from coordinate_clicker import click_on_map

# Load API key
load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def encode_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def send_to_openai(image_path):
    base64_image = encode_image(image_path)

    prompt = (
        "You are playing GeoGuessr. Look at this image and try to guess "
        "where it is in the world. Be as specific as possible. "
        "Enter only longitude and latitude cordinates, nothing else"
        "If you don't know just give it ur best guess in cordinates"
        "its more important u guess cordiantes than give up or say anything else."
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
                ]
            }
        ],
        max_tokens=300,
    )

    return response.choices[0].message.content

def extract_coordinates(text):
    # Match formats like: "37.3° N, 121.9° W"
    match = re.search(
        r'([-+]?\d{1,2}(?:\.\d+)?)°?\s*([NnSs]),?\s*([-+]?\d{1,3}(?:\.\d+)?)°?\s*([EeWw])',
        text
    )
    if match:
        lat = float(match.group(1))
        lat_dir = match.group(2).upper()
        lng = float(match.group(3))
        lng_dir = match.group(4).upper()

        if lat_dir == "S":
            lat = -lat
        if lng_dir == "W":
            lng = -lng

        return lat, lng

    # Fallback: decimal degrees like "37.3, -121.9"
    match = re.search(r'([-+]?\d{1,2}\.\d+)[, ]+\s*([-+]?\d{1,3}\.\d+)', text)
    if match:
        lat = float(match.group(1))
        lng = float(match.group(2))
        return lat, lng

    return None

if __name__ == "__main__":
    image_path = capture_geoguessr_window()

    if image_path:
        result = send_to_openai(image_path)
        print("Prediction:\n", result)
    else:
        print("Could not capture GeoGuessr window.")

    print("Prediction:\n", result)
    coords = extract_coordinates(result)
    print(coords)
    if coords:
        lat, lng = coords
        # You might need to re-access the window object to get .left/.top
        from pygetwindow import getWindowsWithTitle
        window = getWindowsWithTitle("GeoGuessr")[0]  # make sure it's visible
        click_on_map(lat, lng)
    else:
        print("No coordinates detected.")
