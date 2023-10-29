from typing import List

from utils.function import get_domain


class PageItem:
    body: str = None
    url: str = None
    domain: str = None
    title: str = None
    depth_from_root: int = None
    a: List[str] = []
    ip: str = None

    def __iter__(self):
        yield 'body', self.body
        yield 'url', self.url
        yield 'domain', self.domain
        yield 'title', self.title


class ResponseItem:
    resp_code: int = None
    html: str = None
    url: str = None
    depth_from_root: int = 0
    drop: bool = False

    def __repr__(self):
        return f"""
                resp_code: {self.resp_code}
                url: {self.url}
                """


if __name__ == '__main__':
    print(get_domain('https://google.com/'))
