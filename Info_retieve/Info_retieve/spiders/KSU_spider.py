import scrapy
import requests
from lxml import etree, html
from bs4 import BeautifulSoup as BS
import re
import uuid


class KSU_Spider(scrapy.Spider):
    name ="spider"

    custom_settings = {
        'USER_AGENT': 'KSU CS4422-IRbot/0.1',
        'DEPTH_PRIORITY': '1',
        'AUTOTHROTTLE_START_DELAY' : '2',
        'CONCURRENT_REQUESTS' : '5',
        'SCHEDULER_DISK_QUEUE': 'scrapy.squeues.PickleFifoDiskQueue',
        'SCHEDULER_MEMORY_QUEUE': 'scrapy.squeues.FifoMemoryQueue',
        'CLOSESPIDER_PAGECOUNT': '10'
    }


    def start_requests(self):
        urls = [
            'https://www.kennesaw.edu/',
            'https://ccse.kennesaw.edu/',
            'https://counseling.kennesaw.edu/index.php',
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        temp=[]
        entry = dict.fromkeys(['Page_ID', 'Title', 'url', 'Body', 'Emails'])
        start = response.url
        resp = requests.get(start, 'html.parser')
        x = BS(resp.content, 'lxml')
        x_1 = x.text
        x_2 = re.sub("[^A-Za-z0-9.@']+", ' ', x_1).strip()
        entry['Page_ID'] = str(uuid.uuid1())
        entry['Title'] = response.css('title::text').get()
        entry['url'] = response.url
        entry['Body'] = x_2
        form = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
        emails = re.findall(form, x_2)
        entry['Emails']= str(emails)
        yield entry

        next_page = response.css('a::attr(href)').re("https://.*[\.]kennesaw.edu.*")
        for next_page in next_page:
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)
            else:
                continue