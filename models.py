import random
from datetime import datetime

class UniversalProduct:
    def __init__(self, name, source, category, raw_price=None, stock_status="В наличии"):
        self.product_name = name.strip() if name else "Unknown Product"
        self.source_name = source
        self.category = category
        
        if raw_price is None or raw_price == 0:
            self.raw_price = float(random.randint(200, 1000))
        else:
            try:
                self.raw_price = float(str(raw_price).replace(' ', '').replace('\xa0', '').replace('₽', '').strip())
            except:
                self.raw_price = float(random.randint(200, 1000))
        
        self.adjusted_price = self.raw_price * 0.5
        self.stock_status = stock_status
        self.created_at = datetime.now()
        self.current_stock = random.randint(500, 1000)

    def to_dict(self):
        return self.__dict__
