from typing import Optional, List, Dict
import time
from fastapi import FastAPI
from pydantic import BaseModel
from server_controller import ServerController

app = FastAPI()
SEEDS_URLS = [
    # "https://www.gamer.com.tw/",
    # "https://english.ftvnews.com.tw/",
    "https://www.taiwannews.com.tw/en/index",
    'https://www.icrt.com.tw/',
    'https://features.ltn.com.tw/english',
    'https://www.taipeitimes.com/',
    'https://acg.gamer.com.tw/anime/'
]
controller = ServerController(SEEDS_URLS, "")
start_time = time.time()

class CrawledPages(BaseModel):
    pages: List[Dict[str, str]]
    crawled_urls: List[str]


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/register/{cli_id}")  # client register
def register_client(cli_id: str):
    try:
        controller.add_client(cli_id)
        return {'status': "ok"}
    except KeyError as e:
        return {"status": "error", "message": str(e)}


@app.get("/fetchurls/{cli_id}")  # client fetch url
def fetch_url(cli_id: str, num: int):
    try:
        urls = controller.get_urls(cli_id, num)
        return {"status": "ok", "urls": urls, 'nums': len(urls)}  # List[str]
    except KeyError as e:
        return {"status": "error", "message": str(e)}


@app.get('/client-num')  # numbers of clients
def client_num():
    return {"status": "ok", "nums": len(controller.clients_que)}


@app.get('/url-in-queue-num')  # numbers of urls in queue
def url_in_queue():
    num = sum(map(lambda x: len(x), controller.clients_que.values()))
    return {
        "status": "ok",
        "nums": num
    }

@app.get('/crawled-url-num')  # numbers of urls in queue
def crawled_url_num():
    return {
        "status": "ok",
        "nums": controller.crawled_num,
        "times": time.time() - start_time
    }

@app.post('/save/{cli_id}')  # save crawled webpage
def save(cli_id: str, pages: CrawledPages):
    controller.push_to_db(pages.pages)
    controller.add_urls(pages.crawled_urls)
    return {'status': 'ok'}