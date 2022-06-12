import asyncio
import json
import logging
from utils.parser3 import HtmlParser
from typing import List
from urllib.parse import urlencode, urljoin

import aiohttp

from item import PageItem, ResponseItem
from utils.function import get_domain


class PipelineBase:
    def __init__(self):
        """init"""
        self.logger = logging.getLogger('[Pipeline]')

    def open_spider(self):
        """
        run when open spider
        """
        pass

    def in_resp_queue(self, data):
        """call from resp_queue

        Arguments:
            resp {ResponseItem}
        return:
            {ResponseItem}
        """
        return data

    def convert_resp_to_page(self, resp):
        """convert resp_item to page_item

        Arguments:
            resp {RespItem} -- responseItem
        """
        return None

    def in_page_queue(self, data):
        """call from resp_queue

        Arguments:
            data {PageItem}
        return:
            {pageItem}
        """
        return data

    def save(self, data):
        """save data to db

        Arguments:
            data {PageItem} -- data
        """

    def close(self):
        pass


class PipelineMainContent(PipelineBase):
    def __init__(self):
        super().__init__()

    def convert_resp_to_page(self, resp):
        item = PageItem()

        item.url = resp.url
        item.depth_from_root = resp.depth_from_root

        parser = HtmlParser(resp.html)

        item.title = parser.get_title()
        item.domain = get_domain(item.url)
        item.body = parser.get_main_content()
        item.a = []
        for href in parser.get_hrefs():
            if not href:
                continue
            item.a.append(urljoin(item.url, href))
        return item


class PipelineToDB(PipelineBase):
    def __init__(self, host: str = 'http://nudb1.ddns.net:5804/nudb', db_name: str = 'search_engine'):
        super().__init__()
        self.host = host
        self.db_name = db_name
        self.pool = []
        self.pushed_cnt = 0

    def save(self, data):
        self.pool.append(dict(data))

        if len(self.pool) > 1000:
            self.logger.warning('batch push to DB')
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.batch_rput())
            self.pushed_cnt += len(self.pool)
            self.pool.clear()
            self.logger.warning(f'Numbers of finish Items: {self.pushed_cnt}')

    async def batch_rput(self):
        async with aiohttp.ClientSession() as session:
            batch_data = []
            tasks = []
            for data in self.pool:
                batch_data.append(data)
                if len(batch_data) == 20:
                    task = asyncio.create_task(self.rput(session, batch_data))
                    tasks.append(task)
                    batch_data = []
            task = asyncio.create_task(self.rput(session, batch_data))
            tasks.append(task)
            result = await asyncio.gather(*tasks)

    async def rput(self, session, data: list, format: str = 'json'):
        if format == 'json':
            data = json.dumps(data, ensure_ascii=False)
        url = f'{self.host}/rput?{urlencode({"db": self.db_name, "format": format, "record": data})}'
        try:
            async with session.get(url, verify_ssl=False) as resp:
                js = await resp.json()
                resp_code = resp.status
            return resp_code
        except Exception:
            pass
