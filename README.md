### Setup project
```sh
mkdir amazon_scraper
cd amazon_scraper/
python3 -m venv env
source env/bin/activate
pip install scrapy
scrapy startproject tutorial .
scrapy crawl amazon -o amazon_products.json
scrapy crawl amazon -o amazon_products.csv
```

### Install dependencies
```sh
pip install scraperapi-sdk 
pip install fake-useragent 
pip install sqlite3 
pip install jsonlines
```

### Check project structure
```sh
tree -P "_.py|_.sqlite3" -I "env"
```

#### Product struture
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

### Run project
```sh
scrapy crawl amazon -o amazon_products.json
```

### Command relate to database sqlite3
```sh
sqlite3 tutorial/databases/amazon_products.sqlite3
.tables
SELECT \* FROM products LIMIT 5;
.quit
```