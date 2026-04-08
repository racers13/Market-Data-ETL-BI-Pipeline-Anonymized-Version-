import psycopg2
import random
from datetime import datetime

class BusinessLogic:
    def __init__(self):
        # НАСТРОЙКИ ПОДКЛЮЧЕНИЯ (ОБЕЗЛИЧЕНО ДЛЯ GITHUB)
        self.config = {
            "dbname": "portfolio_db",
            "user": "postgres",
            "password": "YOUR_POSTGRES_PASSWORD", 
            "host": "127.0.0.1",
            "port": "5432"
        }

    def get_connection(self):
        return psycopg2.connect(**self.config)

    def generate_sales(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, sales_count, adjusted_price FROM market_data")
        products = cursor.fetchall()
        
        for pid, current_sales, price in products:
            random_val = random.randint(1, 100)
            new_sales = current_sales if current_sales > random_val else random_val
            
            cursor.execute('''
                UPDATE market_data 
                SET sales_count = %s, 
                    revenue = %s * %s,
                    updated_at = %s
                WHERE id = %s
            ''', (new_sales, price, new_sales, datetime.now(), pid))
        
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Продажи и выручка обновлены для {len(products)} товаров.")

    def weekly_update(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, adjusted_price FROM market_data")
        products = cursor.fetchall()
        
        for pid, price in products:
            x_percent = random.uniform(0, 0.10)
            cost_price = float(price) * (1 - x_percent)
            supply = random.randint(50, 200) if x_percent > 0 else 0
            
            cursor.execute('''
                UPDATE market_data 
                SET cost_price = %s, 
                    supply_count = %s,
                    current_stock = current_stock + %s,
                    updated_at = %s
                WHERE id = %s
            ''', (cost_price, supply, supply, datetime.now(), pid))
            
        conn.commit()
        cursor.close()
        conn.close()
        print("Еженедельное обновление себестоимости и поступлений завершено.")

    def update_recommendations(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, current_stock, sales_count FROM market_data")
        products = cursor.fetchall()
        
        for pid, stock, sales in products:
            rec = "Держать цену"
            delta = 0.0
            
            if stock < 100:
                rec = "Повысить цену (Дефицит)"
                delta = 10.0
            elif stock > 800 and sales < 20:
                rec = "Снизить цену (Распродажа)"
                delta = -15.0
            elif sales > 80:
                rec = "Повысить цену (Высокий спрос)"
                delta = 5.0
            
            cursor.execute('''
                UPDATE market_data 
                SET price_recommendation = %s, 
                    price_delta = %s,
                    updated_at = %s
                WHERE id = %s
            ''', (rec, delta, datetime.now(), pid))
            
        conn.commit()
        cursor.close()
        conn.close()
        print("Рекомендации по ценам обновлены.")

if __name__ == "__main__":
    import sys
    bl = BusinessLogic()
    if len(sys.argv) > 2 and sys.argv[1] == "--mode":
        mode = sys.argv[2]
        if mode == "sales":
            bl.generate_sales()
            bl.update_recommendations()
        elif mode == "weekly":
            bl.weekly_update()
    else:
        bl.generate_sales()
        bl.update_recommendations()
        bl.weekly_update()
