import os
import re
import csv
import requests
import webbrowser
from bs4 import BeautifulSoup


def get_page(url):

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    
    return soup


def get_prod_info(soup):
    
    try:
        final_name = soup.select("h1.it-ttl")[0].text.replace('\xa0', '').replace('Details about  ', '')
    except:
        final_name = ''


    try:
        reviews = soup.find('a', id='_rvwlnk').text
        num_revs = [int(i) for i in reviews.split() if i.isdigit()]
        final_revs = num_revs[0]
    except:
        final_revs = ''


    try:
        sold = soup.find('a', class_='vi-txt-underline').text
        num_sold = re.findall(r'\d+', sold)

        if len(num_sold) > 1:
            check = ""
            final_sold = check.join(num_sold)
        else:
            final_sold = num_sold[0]

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



def get_links(soup):

    try:
        links = soup.find_all('a', class_='s-item__link')
    except:
        links = []

    urls = [url.get('href') for url in links]

    return urls


def make_csv(data, url):

    file_in_Docs = os.path.join(os.path.expanduser('~'), 'Documents', 'products.csv')

    with open(file_in_Docs, 'a') as csvFile:
        write = csv.writer(csvFile)
        rows = [data['name'], data['price'], data['reviews'], data['sold'], url]
        write.writerow(rows)
  

def main():

    query = str(input("What product are you looking for? "))
    query_split = query.split(' ')
    min = float('inf')
    curr_page, num_pages = 1, 3

    best_deals = []

    while curr_page < num_pages:

        query = query.replace(' ', '+')
        url = 'https://www.ebay.com/sch/i.html?_nkw=' + str(query) + '&_pgn=' + str(curr_page)
        links = get_links(get_page(url))

        for link in links:
            soup = get_page(link)
            data = get_prod_info(soup)
            make_csv(data, link)
            valid_item = True

            for word in query_split:
                if word.lower() not in data['name'].lower():
                    valid_item = False

            if data['price'] != '' and valid_item:
                converted_price = float(data['price'].replace('US $', ''))

                if data['reviews'] != '':
                    num_revs = int(data['reviews'])

                    if converted_price <= min and num_revs >= 15:
                        min = converted_price
                        best_deals.append(link)

                elif data['sold'] != '':
                    num_sold = int(data['sold'])

                    if converted_price <= min and num_sold >= 50:
                        min = converted_price
                        best_deals.append(link)

        curr_page+=1

    if len(best_deals) >= 3:
        best_deal = best_deals[-1]
        second_best = best_deals[-2]
        third_best = best_deals[-3]

        webbrowser.open_new_tab(best_deal)
        webbrowser.open_new_tab(second_best)
        webbrowser.open_new_tab(third_best)
    else:
        best_deal = best_deals[-1]
        webbrowser.open_new_tab(best_deal)


    
if __name__ == '__main__':
    main()