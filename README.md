## Description

Using the BeautifulSoup module, Scraper.py scrapes a product's name, price, link, number of reviews, and the number sold for each product in the first couple pages of a user input eBay search. It then compares each product's price, number of reviews, and number sold and opens up the links (each in a new tab) of the top three products that have the lowest prices and over 10 reviews or have at least been bought over 100 times. It also ouputs the scraped data of each product to a .csv file, that is saved to the user's 'Documents' folder, with each product's info being stored in its own row.

## Requirements

To install all the needed python packages, just run this command in the same directory that you stored the file 'requirements.txt': **pip install -r requirements.txt**

## Usage

Just run Scraper.py in any python3 interpreter and input the product you would like to search for when prompted. To access the created .csv file, just go to your 'Documents' folder and look for a .csv file that is named after the product you searched for.
