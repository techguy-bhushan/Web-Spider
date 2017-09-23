import threading
from queue import Queue

from docutils.nodes import target

from spider import Spider
from domain import *
from util import *

PROJECT_NAME = 'your project run'
HOME_PAGE = 'home url of web site'
DOMAIN_NAME = get_domain_name(HOME_PAGE)
QUEUE_FILE = PROJECT_NAME +'/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.text'
NUMBER_OF_THREAD = 5

queue = Queue()
Spider(PROJECT_NAME, HOME_PAGE, DOMAIN_NAME)

def create_spider():
    for _ in range(NUMBER_OF_THREAD):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()

def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()

def create_job():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link);
    queue.join()
    crawl()

def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print("link remain in queue:"+str(len(queued_links)))
        create_job()

create_spider()
crawl()