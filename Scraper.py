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
        final_revs = re.findall(r'\d+', reviews)[0]
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


def write_to_csv(file, data, url):

    with open(file, 'a') as csvFile:
        write = csv.writer(csvFile)
        rows = [data['name'], data['price'], data['reviews'], data['sold'], url]
        write.writerow(rows)


def make_csv(query):

    query = query.replace('+', '_')

    file_in_Docs = os.path.join(os.path.expanduser('~'), 'Documents', str(query) + '.csv')

    file_ctr = 1
    while os.path.isfile(file_in_Docs):
        new_name = str(query) + '(' + str(file_ctr) + ')' + '.csv'
        file_in_Docs = os.path.join(os.path.expanduser('~'), 'Documents', str(new_name) + '.csv')
        file_ctr+=1

    return file_in_Docs
    

def main():

    query = str(input("What product are you looking for? ")).replace(' ', '+')
    query_split = query.split('+')
    min = second_min = float('inf')
    curr_page, num_pages = 1, 3

    best_deals = []
    csv_name = make_csv(query)

    while curr_page < num_pages:

        url = 'https://www.ebay.com/sch/i.html?_nkw=' + str(query) + '&_pgn=' + str(curr_page)
        links = get_links(get_page(url))

        for link in links:
            data = get_prod_info(get_page(link))
            write_to_csv(csv_name, data, link)
            valid_item = True

            for word in query_split:
                if word.lower() not in data['name'].lower():
                    valid_item = False

            if data['price'] != '' and data['reviews'] != '' and valid_item:
                converted_price = float(data['price'].replace('US $', ''))
                num_revs = int(data['reviews'])

                if (converted_price <= min or converted_price <= second_min) and num_revs > 10:
                    second_min = min
                    min = converted_price
                    best_deals.append(link)

            elif data['price'] != '' and data['sold'] != '' and valid_item:
                converted_price = float(data['price'].replace('US $', ''))
                num_sold = int(data['sold'])

                if (converted_price <= min or converted_price <= second_min) and num_sold > 100:
                    second_min = min
                    min = converted_price
                    best_deals.append(link)

        curr_page+=1

    if len(best_deals) >= 3:
        for i in range(1,4):
            deals = best_deals[int('-' + str(i))]
            webbrowser.open_new_tab(deals)
    else:
        best_deal = best_deals[-1]
        webbrowser.open_new_tab(best_deal)



if __name__ == '__main__':
    main()