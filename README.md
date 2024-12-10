mkdir amazon_scraper
cd amazon_scraper/
python3 -m venv env
source env/bin/activate
pip install scrapy
scrapy startproject tutorial .
scrapy crawl amazon -o amazon_products.json
scrapy crawl amazon -o test.json
scrapy crawl amazon -o amazon_products.csv


```sh
scrapy crawl amazon -o amazon_products.json
```

pip install scraperapi-sdk fake-useragent sqlite3 jsonlines

tree -P "*.py|*.sqlite3" -I "env"

```sh
├── databases
│   └── amazon_products.sqlite3
└── tutorial
    ├── __init__.py
    ├── items.py
    ├── middlewares.py
    ├── pipelines.py
    ├── __pycache__
    ├── settings.py
    └── spiders
        ├── amazon.py
        ├── __init__.py
        └── __pycache__
```

scrapy crawl amazon -o amazon_products.json
sqlite3 tutorial/databases/amazon_products.sqlite3
.tables
SELECT * FROM products LIMIT 5;
.quit