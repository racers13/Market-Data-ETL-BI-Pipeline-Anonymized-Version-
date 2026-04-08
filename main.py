import time
import json
from database import Database
from parser_metal_a import parse_source_a
# Для запуска Scrapy из скрипта
from scrapy.crawler import CrawlerProcess
from parser_books_a import BookRetailerSpider
from business_logic import BusinessLogic

def run_all_parsers():
    db = Database()
    
    # 1. Metal Provider A
    print("--- Запуск парсинга Metal Provider A ---")
    metal_products = parse_source_a()
    if metal_products:
        db.save_products(metal_products)
    
    # 2. Book Retailer A (Scrapy)
    print("\n--- Запуск парсинга Book Retailer A (Scrapy) ---")
    process = CrawlerProcess(settings={
        'FEEDS': {
            'temp_books.json': {'format': 'json', 'overwrite': True},
        },
        'LOG_LEVEL': 'ERROR'
    })
    
    process.crawl(BookRetailerSpider)
    process.start() 

    # 3. Загрузка данных из Scrapy в БД
    try:
        with open('temp_books.json', 'r', encoding='utf-8') as f:
            books_data = json.load(f)
            if books_data:
                db.save_products(books_data)
                print(f"Данные из Scrapy (Book Retailer A) успешно загружены в БД.")
    except (FileNotFoundError, json.JSONDecodeError):
        print("Файл с данными Scrapy не найден или пуст.")

    # 4. Запуск бизнес-логики
    print("\n--- Запуск бизнес-логики (генерация продаж и рекомендаций) ---")
    bl = BusinessLogic()
    bl.generate_sales()
    bl.update_recommendations()
    bl.weekly_update()
    print("Бизнес-логика успешно выполнена для всех источников.")

if __name__ == "__main__":
    run_all_parsers()
