import requests
from bs4 import BeautifulSoup

def main():
    # Step 1: Fetch the main page with device list
    url = 'https://phonedb.net/index.php?m=device&s=list'
    response = requests.get(url)
    
    # Debug: Print title of the main page
    soup = BeautifulSoup(response.text, 'html.parser')
    print(f"Main page title: {soup.title.text}\n")

    # Step 2: Find the first "All details" link
    link = soup.find('a', {'title': 'See detailed datasheet'})
    if link:
        details_url = 'https://phonedb.net/' + link['href']
        print(f'Found "All details" link, navigating to: {details_url}\n')
        
        # Step 3: Fetch the details page
        details_response = requests.get(details_url)
        details_soup = BeautifulSoup(details_response.text, 'html.parser')
        
        # Debug: Print title of the details page
        print(f"Details page title: {details_soup.title.text}\n")
        
        # Step 4: Locate the desired table body (4th div class container -> div class canvas -> table -> tbody)
        # tbody = details_soup.select_one('div.container:nth-of-type(4) div.canvas table tbody')
        tbody = details_soup.select_one('div.container:nth-of-type(4)')
   
        if tbody:
            print("Table body found!\n")
            
            # Step 5: Find all <tr> with exactly 2 <td> elements
            rows = tbody.find_all('tr')
            print(f"Number of <tr> elements found: {len(rows)}\n")

            for row in rows:
                tds = row.find_all('td')
                if len(tds) == 2:
                    # Get text inside the <strong> tag in the first <td>
                    first_td_strong = tds[0].find('strong')
                    if first_td_strong:
                        first_td_text = first_td_strong.text.strip()
                    
                        # Get all the text in the second <td>
                        second_td_text = tds[1].get_text(separator='', strip=True)
                        
                        # Print the final formatted output
                        print(f'{first_td_text}: {second_td_text}')

        else:
            print('Table body not found.\n')
    else:
        print('Device details link not found.\n')

if __name__ == "__main__":
    main()
