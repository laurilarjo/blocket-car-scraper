import scrapy

# Run this file:
# scrapy runspider main.py -o cars.csv

# For doing testing in Scrapy Shell
# scrapy shell "https://www.blocket.se/annonser/stockholm/fordon/bilar?cb=41&cbl1=10&cg=1020&mye=2017&mys=2010&r=11"

SEARCH_PAGE = 'https://www.blocket.se/annonser/stockholm/fordon/bilar?cb=41&cbl1=10&cg=1020&mye=2017&mys=2010&r=11'

class BlocketCarSpider(scrapy.Spider):
    name = 'blocketcarspider'
    start_urls = [SEARCH_PAGE]
    custom_settings = {
        # 'LOG_FILE': 'log.txt',
        'FORMAT' : 'csv',
        'DOWNLOAD_DELAY' : '3'
    }
    

    def parse(self, response):
        for car in response.xpath('//*[@id="root"]/div[2]/main/div[3]/div[1]/div[2]/div[1]/div'):
            if (car.xpath('article/div[2]/div[2]/h2/a/span/text()').get()):
                yield {
                    'title' : car.xpath('article/div[2]/div[2]/h2/a/span/text()').get(),

                    'year' : car.xpath('article/div[2]/div[last()-1]/div[1]/ul/li[1]/text()').get(),
                    'gastype' : car.xpath('article/div[2]/div[last()-1]/div[1]/ul/li[2]/text()').get(),
                    'miles' : self.formatMiles(car.xpath('article/div[2]/div[last()-1]/div[1]/ul/li[3]/text()').get()),
                    'transmission' : car.xpath('article/div[2]/div[last()-1]/div[1]/ul/li[4]/text()').get(),

                    'price' : self.formatPrice(car.xpath('article/div[2]/div[last()]/div/div/span/text()').get()),
                    'company' : self.formatCompany(car.xpath('article/div[2]/div[1]/div[1]/span/text()').get()),
                    'location' : car.xpath('article/div[2]/div[1]/p/a[2]/text()').get(),
                    'link' : car.xpath('article/div[2]/div[2]/h2/a/@href').get(),
                }

        next_page = response.xpath('//*[@id="root"]/div[2]/main/div[3]/div[1]/div[3]/div/div[2]/a[last()]/@href').get()
        print('link: ' + next_page)
        if next_page is not None:
            
            yield response.follow(next_page, self.parse)

    def formatPrice(self, value):
        return value.replace('kr', '').replace(' ', '')

    def formatMiles(self, value):
        return value.split('-')[0].replace(' ', '')
    
    def formatCompany(self, value):
        if (value == 'Butik'):
            return value
        else:
            return 'Privat'
