import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

base_url = "https://www.amazon.in/s?k=dresses"  # Changing the URL to dresses category

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
}

max_retries = 5
retry_delay = 5  # seconds

for retry in range(max_retries):
    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()
        break  # Exit the loop if the request is successful
    except requests.RequestException as e:
        print(f"Request error (Retry {retry + 1}/{max_retries}):", e)
        if retry < max_retries - 1:
            print(f"Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
        else:
            print("Max retries reached. Exiting.")
            exit()

soup = BeautifulSoup(response.content, "html.parser")
dress_cards = soup.find_all("div", class_="s-result-item")  # Adjusting the variable name

dress_data = []  # Changing the variable name

for dress_card in dress_cards:  # Adjusting the loop variable name
    try:
        dress_name = dress_card.find("span", class_="a-text-normal").text.strip()
        dress_price = dress_card.find("span", class_="a-offscreen").text if dress_card.find("span", class_="a-offscreen") else "N/A"
        dress_rating = dress_card.find("span", class_="a-icon-alt").text if dress_card.find("span", class_="a-icon-alt") else "N/A"
        
        dress_data.append({
            "Name": dress_name,
            "Price": dress_price,
            "Rating": dress_rating
        })
    except Exception as e:
        print("Error in extracting dress data:", e)

df = pd.DataFrame(dress_data)  # Changing the DataFrame variable name
df.to_csv("amazon_dresses.csv", index=False)  # Changing the CSV file name

print("Data successfully extracted and CSV saved.")
