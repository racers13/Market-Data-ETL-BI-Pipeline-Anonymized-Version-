import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime

class Database:
    def __init__(self):
        # НАСТРОЙКИ ПОДКЛЮЧЕНИЯ (ОБЕЗЛИЧЕНО ДЛЯ GITHUB)
        self.config = {
            "dbname": "portfolio_db",
            "user": "postgres",
            "password": "YOUR_POSTGRES_PASSWORD", 
            "host": "127.0.0.1",
            "port": "5432"
        }
        # self.init_db() # Раскомментируйте при первом запуске

    def get_connection(self):
        try:
            return psycopg2.connect(**self.config)
        except Exception as e:
            print(f"Ошибка подключения к БД: {e}")
            raise

    def save_products(self, products):
        if not products:
            return

        conn = self.get_connection()
        cursor = conn.cursor()
        
        for p in products:
            try:
                data = p if isinstance(p, dict) else p.to_dict()
                query = '''
                    INSERT INTO market_data (
                        source_name, category, product_name, raw_price, adjusted_price, 
                        stock_status, current_stock, created_at, updated_at
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                '''
                cursor.execute(query, (
                    data['source_name'], data['category'], data['product_name'], 
                    data['raw_price'], data['adjusted_price'], data['stock_status'], 
                    data['current_stock'], data['created_at'], datetime.now()
                ))
            except Exception as e:
                print(f"Ошибка при вставке: {e}")
        
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Сохранено {len(products)} записей в PostgreSQL.")
