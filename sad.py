import requests
from bs4 import BeautifulSoup
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import time

TO_IGNORE_THESE_COLS = {"OEM ID", "asd"}
# DATA_LIMIT = 60 #for the sake of testing
DATA_LIMIT = 9999999999

def scrape_device_details(details_url):
    print(f'scraping: {details_url}')
    
    #get details
    details_response = requests.get(details_url)
    details_soup = BeautifulSoup(details_response.text, 'html.parser')

    print(f"TITLE: {details_soup.title.text}")
    
    #get 4th container element (this element container will contain the data needed)
    # tbody = details_soup.select_one('div.container:nth-of-type(4) div.canvas table tbody')
    tbody = details_soup.select_one('div.container:nth-of-type(4)')
    
    device_info = {}
    
    if tbody:
        # print("tbody found...")
        
        # find every tr element with exactly 2 <td> elements
        rows = tbody.find_all('tr')
        
        for row in rows:
            tds = row.find_all('td')
            if len(tds) == 2:
                
                first_td_strong = tds[0].find('strong')
                if first_td_strong:
                    first_td_text = first_td_strong.text.strip()
                    second_td_text = tds[1].get_text(separator='', strip=True)
                    device_info[first_td_text] = second_td_text
    else:
        print(f'tbody not found for {details_soup.title.text}')
    
    return device_info

def main():
    start_time = time.time()
    devices_data = []
    url = 'https://phonedb.net/index.php?m=device&s=list'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    print(f"MAIN TITLE: {soup.title.text}")

    while len(devices_data) < DATA_LIMIT:
        print(f"data length: {len(devices_data)}")
        #get "see detailed datasheet for one device" element
        links = soup.find_all('a', {'title': 'See detailed datasheet'})
        if links:
            print(f'found {len(links)} links, processing...')

            detail_urls = ['https://phonedb.net/' + link['href'] for link in links]
            detail_urls = detail_urls[:DATA_LIMIT - len(devices_data)]
            
            with ThreadPoolExecutor(max_workers=10) as executor:  # Adjust number of workers as needed
                devices_info = list(executor.map(scrape_device_details, detail_urls))

            devices_data.extend(devices_info)  # Combine the results
            print("data scraped...")
        else:
            print('link not found')

        next_page_link = soup.find('a', {'title': 'Next page'})
        if next_page_link:
            next_url = 'https://phonedb.net/' + next_page_link['href']
            response = requests.get(next_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            print(f'next page: {next_url}\n')
        else:
            print('no more pages to navigate.\n')
            break

    devices_df = pd.DataFrame(devices_data)
    devices_df.to_excel('real.xlsx', index=False)
    print("DATA EXPORTED TO XLSX")
    elapsed_time = time.time() - start_time
    minutes, seconds = divmod(elapsed_time, 60)
    print(f"time elapsed: {int(minutes)} m {int(seconds)} s")

if __name__ == "__main__":
    main()
