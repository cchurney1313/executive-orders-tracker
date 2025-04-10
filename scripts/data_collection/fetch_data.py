import pandas as pd
import requests
import json
from datetime import datetime
from io import StringIO
import time
import os
from bs4 import BeautifulSoup
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import spacy


nlp=spacy.load("en_core_web_sm")

def fetch_executive_orders():
    url = "https://www.federalregister.gov/documents/search.csv?conditions%5Bcorrection%5D=0&conditions%5Bpresident%5D=donald-trump&conditions%5Bpresidential_document_type%5D=executive_order&conditions%5Bsigning_date%5D%5Bgte%5D=01%2F20%2F2025&conditions%5Bsigning_date%5D%5Blte%5D=04%2F01%2F2025&conditions%5Bsigning_date%5D%5Byear%5D=2025&conditions%5Btype%5D%5B%5D=PRESDOCU&fields%5B%5D=citation&fields%5B%5D=document_number&fields%5B%5D=end_page&fields%5B%5D=html_url&fields%5B%5D=pdf_url&fields%5B%5D=type&fields%5B%5D=subtype&fields%5B%5D=publication_date&fields%5B%5D=signing_date&fields%5B%5D=start_page&fields%5B%5D=title&fields%5B%5D=disposition_notes&fields%5B%5D=executive_order_number&fields%5B%5D=not_received_for_publication&include_pre_1994_docs=true&maximum_per_page=10000&order=executive_order&per_page=10000"
    timestamp = f"&_={int(time.time())}"
    url= url+timestamp
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
    response = requests.get(url, headers=headers)
    print(response.headers)
    response.raise_for_status()
    df=pd.read_csv(StringIO(response.text))
    df.fillna("", inplace=True)  # Fill NaN values with empty strings

    data = df.to_dict(orient='records')

    json_file_path = "executive_orders.json"
    if os.path.exists(json_file_path):
        with open(json_file_path, "r") as json_file:
            existing_data = json.load(json_file)
    else:
        existing_data = []
    updated_data = existing_data.copy()
    existing_urls = {entry["html_url"]: entry for entry in existing_data}
    for entry in data:
        if entry["html_url"] not in existing_urls:
            updated_data.append(entry)
    with open(json_file_path, "w") as json_file:
        json.dump(updated_data, json_file, indent=4)

    excel_file = "executive_orders.xlsx"
    updated_df = pd.DataFrame(updated_data)
    updated_df.to_excel(excel_file, index=False)
    
    print(f"Data saved to {excel_file}")

    generate_word_cloud_from_content(existing_data, "wordcloud.png")

def fetch_content(document_number):
    document_number = document_number.strip()
    api_url = f"https://www.federalregister.gov/api/v1/documents/{document_number}.json"
    
    try: 
        response = requests.get(api_url, headers={"User-Agent": "Mozilla/5.0"})
        
        response.raise_for_status()
        data=response.json()
        
        content=data.get("raw_text_url", "")
        raw_text_url = data.get("raw_text_url", "")
        raw_text_response = requests.get(raw_text_url, headers={"User-Agent": "Mozilla/5.0"})
        raw_text_response.raise_for_status()
        content = raw_text_response.text
        return content   
        """soup = BeautifulSoup(content, 'html.parser')
        content=soup.get_text(separator = " ", strip=True)
        print(f"{document_number}:{content[:100]}")"""
        
    except Exception as e:
        print(f"Error fetching content from {api_url}: {e}")
        return ""

def extract_nouns(text):
    doc = nlp(text)
    nouns = [token.text for token in doc if token.pos_ == "NOUN"]
    return nouns
def generate_word_cloud_from_content(data, output_image_path):
    print(data)
    print(output_image_path)
    combined_text=""
    for order in data:
        nouns=extract_nouns(order["title"])
        combined_text += " "+" ".join(nouns)
        print({combined_text[:500]})
    wordcloud = WordCloud(width=800, height=400, background_color='white', stopwords={"the", "and", "of", "to", "in", "for", "on", "with", "by", "as", "is", "at", "from", "American", "United States", "restoring", "America", "Amending","Federal", "Duties", "Implementing", "Amendment","Government", "Protecting", "Foreign", "Imposing"}, colormap="viridis").generate(combined_text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(output_image_path)
    plt.close()


if __name__ == "__main__":
    fetch_executive_orders()
    print("Executive orders data has been fetched and saved to executive_orders.json")