import sqlite3
import os
from datetime import datetime
from itemadapter import ItemAdapter

class TutorialPipeline:
    def process_item(self, item, spider):
        # Data cleaning pipeline
        for k, v in item.items():
            if not v:
                item[k] = ''  # replace empty list or None with empty string
            elif k == 'Title':
                item[k] = v.strip()
            elif k == 'Rating':
                item[k] = v.replace(' out of 5 stars', '')
            elif k in ['AvailableSizes', 'AvailableColors']:
                item[k] = ", ".join(v) if isinstance(v, list) else v
            elif k == 'BulletPoints':
                item[k] = ", ".join([i.strip() for i in v if i.strip()])
            elif k == 'SellerRank':
                item[k] = " ".join([i.strip() for i in v if i.strip()])
        return item

class SaveSQLitePipeline:
    def __init__(self):
        # Ensure the database directory exists
        db_dir = os.path.join(os.path.dirname(__file__), '..', 'databases')
        os.makedirs(db_dir, exist_ok=True)
        
        # Create or connect to SQLite database
        db_path = os.path.join(db_dir, 'amazon_products.sqlite3')
        self.conn = sqlite3.connect(db_path)
        self.cur = self.conn.cursor()

        # Create products table with more comprehensive schema
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            asin TEXT UNIQUE,
            title TEXT,
            image TEXT,
            rating TEXT,
            price TEXT,
            number_of_reviews TEXT,
            available_sizes TEXT,
            available_colors TEXT,
            bullet_points TEXT,
            seller_rank TEXT,
            scraped_at DATETIME
        )
        """)

        # Create index for faster searches
        self.cur.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS idx_asin 
        ON products(asin)
        """)

    def process_item(self, item, spider):
        try:
            # Prepare insert or replace statement
            self.cur.execute("""
            INSERT OR REPLACE INTO products (
                asin, title, image, rating, price, 
                number_of_reviews, available_sizes, 
                available_colors, bullet_points, 
                seller_rank, scraped_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                item.get('asin', ''),
                item.get('Title', ''),
                item.get('MainImage', ''),
                item.get('Rating', ''),
                item.get('Price', ''),
                item.get('NumberOfReviews', ''),
                item.get('AvailableSizes', ''),
                item.get('AvailableColors', ''),
                item.get('BulletPoints', ''),
                item.get('SellerRank', ''),
                datetime.now()
            ))

            # Commit the transaction
            self.conn.commit()
            
            print(f"Saved product: {item.get('Title', 'Unknown')}")
            return item

        except sqlite3.Error as e:
            print(f"Database error: {e}")
            self.conn.rollback()
        except Exception as e:
            print(f"Error processing item: {e}")
            self.conn.rollback()

    def close_spider(self, spider):
        try:
            # Close cursor and connection
            self.cur.close()
            self.conn.close()
            print("Database connection closed successfully")
        except Exception as e:
            print(f"Error closing database: {e}")