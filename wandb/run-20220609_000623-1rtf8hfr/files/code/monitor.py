import wandb
import time
import requests
from urllib.parse import urljoin

SERVER = 'http://localhost:8087'
wandb.init(project="searchEngineSpider")
while 1:
    print(urljoin(SERVER, '/url-in-queue-num'))
    wandb.log({
        'url-in-queue-num':
        requests.get(urljoin(SERVER, '/url-in-queue-num')).json()['nums'],
        'crawled-page-num':
        requests.get(urljoin(SERVER, '/crawled-url-num')).json()['nums']
    })
    time.sleep(10)