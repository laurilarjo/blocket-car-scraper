# Blocket Car Scraper

- Uses Scrapy to crawl car sales data from Blocket.se
- Outputs results into given csv-file.
- Crawls pages every 3s

# How to use

1. Go to Blocket.se and set search criteria for the car model you're looking for.
2. Input the search results page URL into `main.py` variable `SEARCH_PAGE`.
3. Run from command line `scrapy runspider main.py -o cars.csv`.
4. Profit.
