import os
import re
import csv
import requests
import webbrowser
from bs4 import BeautifulSoup

# Parses the lxml page from teh given url
# and returns the BeautifulSoup object.
def get_page(url):

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    
    return soup


# Attempts to scrape the name, price, # of reviews,
# and # sold of a product from eBay. 
def get_prod_info(soup):

    try:
        final_name = soup.select("h1.it-ttl")[0].text.replace('\xa0', '').replace('Details about  ', '')
    except:
        final_name = ''


    try:
        reviews = soup.find('a', id='_rvwlnk').text
        final_revs = re.findall(r'\d+', reviews)[0]
    except:
        final_revs = ''


    try:
        sold = soup.find('a', class_='vi-txt-underline').text
        num_sold = re.findall(r'\d+', sold)
        check = ''
        
        final_sold = check.join(num_sold) if len(num_sold) > 1 else num_sold[0]
    except:
        final_sold = ''


    try:
        try: 
            final_price = soup.find('span', id='prcIsum').text
        except:
            final_price = soup.find('span', id='mm-saleDscPrc').text

        if '/ea' in final_price:
            final_price = final_price.replace('/ea', '')

        if ',' in final_price:
            final_price = final_price.replace(',', '')
    except:
        final_price = ''


    data = {
        'name': final_name,
        'price': final_price,
        'reviews': final_revs,
        'sold': final_sold
    }

    return data


# Scrapes all the links of each product's page
# from a user input eBay search.
def get_links(soup):

    try:
        links = soup.find_all('a', class_='s-item__link')
    except:
        links = []

    urls = [url.get('href') for url in links]

    return urls


# Writes to a created csv file each product's
# name, price, # of reviews, # sold, and link
# with each product's info being in one row.
def write_to_csv(file, data, url):

    with open(file, 'a') as csvFile:
        write = csv.writer(csvFile)
        rows = [data['name'], data['price'], data['reviews'], data['sold'], url]
        write.writerow(rows)


# Creates a csv file and stores it in the users 
# 'Documents' folder, also handles duplicate file names.
def make_csv(query):

    query = query.replace('+', '_')

    file_in_Docs = os.path.join(os.path.expanduser('~'), 'Documents', str(query) + '.csv')

    file_ctr = 1
    while os.path.isfile(file_in_Docs):
        new_name = str(query) + '(' + str(file_ctr) + ')' + '.csv'
        file_in_Docs = os.path.join(os.path.expanduser('~'), 'Documents', str(new_name))
        file_ctr+=1

    return file_in_Docs
    

# Scrapes the wanted data for each product in the first couple
# pages of a user input eBay search. Compares the data of each product
# and returns the three cheapest products that have at least 10 reviews
# or have been bought over 100 times.
def main():

    query = str(input("What product are you looking for? ")).replace(' ', '+')
    query_split = query.split('+')
    curr_page, num_pages = 1, 3

    best_deals = []
    csv_name = make_csv(query)

    while curr_page < num_pages:

        url = 'https://www.ebay.com/sch/i.html?_nkw=' + str(query) + '&_pgn=' + str(curr_page)
        links = get_links(get_page(url))

        for link in links:
            data = get_prod_info(get_page(link))
            write_to_csv(csv_name, data, link)
            name = data['name'].lower().split() 
            valid_item = True

            for word in query_split:
                if word.lower() not in name:
                    valid_item = False

            if data['price'] != '' and data['reviews'] != '' and valid_item:
                converted_price = float(data['price'].replace('US $', ''))
                data['price'] = converted_price
                data['link'] = str(link)

                if int(data['reviews']) >= 10: best_deals.append(data)

            elif data['price'] != '' and data['sold'] != '' and valid_item:
                converted_price = float(data['price'].replace('US $', ''))
                data['price'] = converted_price
                data['link'] = str(link)

                if int(data['sold']) >= 50: best_deals.append(data)

        curr_page+=1

    best_deals.sort(key=lambda x: x['price'], reverse=False)

    for i in range (0,3):
        deals = best_deals[i]
        webbrowser.open_new_tab(deals['link'])


if __name__ == '__main__':
    main()