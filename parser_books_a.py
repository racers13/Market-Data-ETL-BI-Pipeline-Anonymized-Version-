import scrapy
from models import UniversalProduct

class BookRetailerSpider(scrapy.Spider):
    """Парсер для книжного ритейлера А (обезличено)"""
    name = 'book_retailer_a'
    start_urls = ['https://book-retailer-a.example.com/books/']
    
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'LOG_LEVEL': 'INFO'
    }

    def parse(self, response):
        # Логика парсинга ссылок (обезличено)
        # for link in response.css('div.product__info-wrapper a::attr(href)'):
        #     yield response.follow(link, callback=self.parse_book)
        pass

    def parse_book(self, response):
        # Логика парсинга данных книги (обезличено)
        name = "Sample Book Title"
        price_val = "500.00"
        
        product = UniversalProduct(
            name=name,
            source="Book_Retailer_A",
            category="Книги",
            raw_price=price_val,
            stock_status="В наличии"
        )
        
        yield product.to_dict()
