import wandb
import time
import requests
from urllib.parse import urljoin
SERVER = 'http://localhost:8087'
wandb.init(project="searchEngineSpider")
while 1:
    wandb.log({'url-in-queue-num': requests.get(urljoin(SERVER, '/url-in-queue-num')['nums']),
            'crawled-page-num': requests.get(urljoin(SERVER, '/crawled-url-num')['nums'])
    })
    time.sleep(10)