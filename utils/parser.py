import re

from html5_parser import parse
from lxml.etree import tostring


class HtmlParser:
    def __init__(self, html: str):

        self.title = ''
        self.urls = []
        self.text = []
        
        self.re_pattern = re.compile(r'\s+')

        self.root = parse(html)
        self.__travel(self.root)
        
    def __travel(self, now):
        for node in now:
            if node.tag == 'script':
                continue

            if node.tag == 'title':
                self.title = node.text if node.text else ''
            elif node.tag == 'a':
                href = node.get('href')
                if href:
                    self.urls.append(href)
        
            if node.tag in ['a', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'span', 'div']:
                result = f'{node.text if node.text else ""}{self.__extract_all_children(node)}{node.tail if node.tail else ""}'
                self.text.append(self.remove_space(result))
                continue
            self.__travel(node)

    def remove_space(self, text):
        return re.sub(self.re_pattern, ' ', text)

    def __extract_all_children(self, now):
        tmp = ''
        for node in now:
            if node.tag == 'a':
                self.urls.append(node.get('href'))
            tmp += node.text if node.text else '' + node.tail if node.tail else ''
            try:
                tmp += self.__extract_all_children(node)
            except RecursionError:
                return tmp
        return tmp

    def get_hrefs(self):
        return self.urls

    def get_title(self):
        return self.title
    
    def get_main_content(self):
        result = ''
        for t in self.text:
            if len(t) > len(result):
                result = t
        
        return result[:200]


if __name__ == '__main__':
    with open('test.html', 'r') as f:
        html = f.read()
    parser = HtmlParser(html)
    print(parser.get_main_content())
