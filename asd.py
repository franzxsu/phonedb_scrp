import requests
from bs4 import BeautifulSoup

TO_IGNORE_THESE={"sample","asd"}

def main():
    url = 'https://phonedb.net/index.php?m=device&s=list'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    print(f"Main page title: {soup.title.text}")

    #get "see detailed datasheet for one device" element
    link = soup.find('a', {'title': 'See detailed datasheet'})
    if link:
        details_url = 'https://phonedb.net/' + link['href']
        print(f'Found "All details" link, navigating to: {details_url}\n')
        
        #get details
        details_response = requests.get(details_url)
        details_soup = BeautifulSoup(details_response.text, 'html.parser')

        print(f"TITLE: {details_soup.title.text}\n")
        
        #get 4th container element (this element container will contain the data needed)
        # tbody = details_soup.select_one('div.container:nth-of-type(4) div.canvas table tbody')
        tbody = details_soup.select_one('div.container:nth-of-type(4)')
   
        if tbody:
            print("tbody found...")
            
            # find every tr element with  exactly 2 <td> elements
            rows = tbody.find_all('tr')
            print(f"Number of <tr> elements found: {len(rows)}\n")
            
            
            for row in rows:
                tds = row.find_all('td')
                if len(tds) == 2:
                    
                    first_td_strong = tds[0].find('strong')
                    if first_td_strong:
                        first_td_text = first_td_strong.text.strip()
                        second_td_text = tds[1].get_text(separator='', strip=True)
                        print(f'{first_td_text}: {second_td_text}')

        else:
            print(f'tbody not found for {soup.title.text}')
    else:
        print('Device details link not found.\n')

if __name__ == "__main__":
    main()
