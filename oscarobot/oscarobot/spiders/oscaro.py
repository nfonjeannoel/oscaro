import json
from random import randint
# from time import sleep
from urllib.parse import urlencode
import scrapy
from scrapy.crawler import CrawlerProcess
import os
from os import path
from scraper_api import ScraperAPIClient

# client = ScraperAPIClient(API_KEY)
section_name = ""
subcategory_name = ""
product_section = ""
section_number = 1
sub_section_number = 4


# todo red sec1 sub 3, sec1 sub 3 Cu 3

def get_proxy():
    ROTATING_PROXY_LIST = [

        'http://162.55.163.74:19993',
        'http://162.55.163.74:19994',
        'http://162.55.163.74:19995',
        'http://162.55.163.74:19996',
        'http://162.55.163.74:19997',
        'http://162.55.163.74:19998',
        'http://162.55.163.74:19999',
        'http://162.55.163.74:20000'
    ]
    size = len(ROTATING_PROXY_LIST) - 1
    return ROTATING_PROXY_LIST[randint(0, size)]


# parent_dir = "C:/Users/JEANNOEL/PycharmProjects/oscaro"


def create_path_section(my_section_name):
    parent_dir = "C:/Users/JEANNOEL/PycharmProjects/oscaro"  # os.path.dirname(__file__)
    path = os.path.join(parent_dir, str(my_section_name))
    try:
        os.makedirs(path, exist_ok=True)
        print("Directory '%s' created successfully" % my_section_name)

    except OSError as error:
        print("Directory '%s' can not be created" % my_section_name)


def create_path_sub_section(my_section_name):
    parent_dir = f"C:/Users/JEANNOEL/PycharmProjects/oscaro/{section_name}"
    path = os.path.join(parent_dir, str(my_section_name))
    try:
        os.makedirs(path, exist_ok=True)
        print("Directory '%s' created successfully" % my_section_name)

    except OSError as error:
        print("Directory '%s' can not be created" % my_section_name)


def create_path_product_section(my_section_name):
    parent_dir = f"C:/Users/JEANNOEL/PycharmProjects/oscaro/{section_name}/{subcategory_name}"
    path = os.path.join(parent_dir, str(my_section_name))

    try:
        os.makedirs(path, exist_ok=True)
        print("Directory '%s' created successfully" % my_section_name)

    except OSError as error:
        print("Directory '%s' can not be created" % my_section_name)


def log_text(param):
    print("*" * 20)
    print(str(param))
    print("*" * 20)


def save_page_html(page_html, product_name, my_json):
    # file_path = path.relpath(f"{section_name}/{subcategory_name}/{product_section}/{product_name}.txt")
    # with open(file_path, "w") as f:
    #     f.write(str(page_html))
    path = f"C:/Users/JEANNOEL/PycharmProjects/oscaro"
    with open(f"{path}/{section_name}/{subcategory_name}/{product_section}/{product_name}.txt", "w") as f:
        f.write(str(page_html))

    with open(f"{path}/{section_name}/{subcategory_name}/{product_section}/{product_section}.json", "a+") as f:
        f.write(json.dumps(my_json))


# def get_scraperapi_url(url):
#     payload = {'api_key': API_KEY, 'url': url}
#     proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
#     return proxy_url


class OscaroSpider(scrapy.Spider):
    name = 'oscaro'

    # allowed_domains = ['x']
    # start_urls = ["https://www-oscaro-com.translate.goog/?_x_tr_sl=fr&_x_tr_tl=en&_x_tr_hl=en&_x_tr_pto=sc"]
    # start_urls = ["https://www-oscaro-es.translate.goog/?_x_tr_sl=es&_x_tr_tl=es&_x_tr_hl=es&_x_tr_pto=sc"]

    # start_urls = ["https://www-oscaro-com.translate.goog/outils-de-mesure-et-controle-702661-sc?_x_tr_sl=fr&_x_tr_tl=en&_x_tr_hl=en&_x_tr_pto=sc"]

    def start_requests(self):
        url = "https://www-oscaro-es.translate.goog/?_x_tr_sl=es&_x_tr_tl=es&_x_tr_hl=es&_x_tr_pto=sc"
        yield scrapy.Request(url=url, meta={"proxy": get_proxy()}, callback=self.parse)

    #     urls = ["https://www-oscaro-es.translate.goog/?_x_tr_sl=es&_x_tr_tl=es&_x_tr_hl=es&_x_tr_pto=sc"]
    #     for url in urls:
    #         yield scrapy.Request(client.scrapyGet(url=url), callback=self.parse)

    def parse(self, response):
        # log_text(response.text.encode("UTF-8"))
        # sections = response.css(".subcat div")
        # contains a list of all the cards in the home screen [contains the first element]
        sections = response.css(f".subcat div:nth-child({section_number})")
        # global section_name
        # looping through all the cards in sections
        for section in sections:
            global section_name
            section_name = section.css("h2 a").css("::text").get()
            # log_text(section_name)
            # getting main category links
            url = section.css("h2 a").css("::attr(href)").get()
            # log_text(url)
            # creating path with name as the current section title - section_name
            create_path_section(section_name)
            yield response.follow(url=url, callback=self.parse_category, meta={"proxy": get_proxy()})

            # optional break in case more than one section is returned
            break

    def parse_category(self, response):
        # sections = response.css(".subcat")
        # get all the cards in the subcategory page [gets the first card]
        sections = response.css(f".subcat:nth-child({sub_section_number})")
        global subcategory_name
        # get all the links in a particular card
        for section in sections:
            # getting subcategory links
            subcategory_name = section.css("h2 a").css("::text").get()
            # get all urls excluding the last as it is the url for see more
            urls = section.css("ul li a").css("::attr(href)").getall()
            # log_text(urls[-1])
            # create directory for this sub category
            create_path_sub_section(subcategory_name)
            # break
            # code to get single url
            start_url_num = 1
            end_url_num = len(urls)
            # before saving the variable, try to read the same file,
            # if you get a file not found error error, then go ahead and create a new file
            try:
                with open("CurrentUrl.txt", "r") as f:
                    # data is of the form "x of n"
                    # split to get a list
                    data = f.read().split()
                    start_url_num = int(data[0])
                    end_url_num = int(data[-1])
                    f.close()
            except FileNotFoundError:
                # create new file
                with open("CurrentUrl.txt", "w") as f:
                    f.write(f"{start_url_num} of {end_url_num}")
                    f.close()
            # current url to scrape
            if start_url_num > end_url_num:
                for j in range(10):
                    log_text("scraping is done")
                return
            url = urls[start_url_num - 1]
            yield response.follow(url=url, callback=self.parse_products, meta={"proxy": get_proxy()})
            # update the size of the file and current url number
            with open("CurrentUrl.txt", "w") as f:
                f.write(f"{start_url_num + 1} of {end_url_num}")
                f.close()

            # create variable start_url_num : int = 0
            # create variable end_url_num : int = 0
            # try to save size of the the url variable in a file
            # before saving the variable, try to read the same file,
            # if you get a file not found error error, then go ahead and create a new file
            # update the size of the file and current url number
            # eg 1 out of 5
            # now read the file
            # check that the first element eg here is [1 = x] is not greater than the last element
            # eg here is 5
            # access the url at the x position and scrape the data
            # then save again the file with x + 1 out of n url [n = max size]

            # to follow only one url
            # break

            # optional break in case sub category returns more than one
            # break

    def parse_products(self, response):
        global product_section
        product_section = response.css("h1.boxed-title ::text").get()
        # is page structure is different
        if product_section is None:
            product_section = response.css("div.boxed-title h1 ::text").get()
        product_urls = response.css("h1 > a").css("::attr(href)").getall()
        # page structured different eg https://www.oscaro.es/tubo-flexible-de-combustible-609-gu?__cf_chl_jschl_tk__=aIdG1Oq6Z_lBSDYAFnq8rdASXF5pLhfvAgCKdmPp8J8-1639546723-0-gaNycGzNCZE
        if not product_urls:
            product_urls = response.css(".product-title a").css("::attr(href)").getall()
        # log_text(product_section)
        create_path_product_section(product_section)
        #
        for product_url in product_urls:
            yield response.follow(url=product_url, callback=self.parse_details, meta={"proxy": get_proxy()})
        #
        # break

        # # handle pagination
        # get the total number of pages
        max_pages = int(response.css(".pager li:not(:last-child):nth-last-child(-n+2) a ::text").get())
        # log_text(f"max pages - {max_pages}")
        # loop n times and create new url
        # looping through all the pagination
        # n = 41
        for i in range(2, max_pages + 1):
            # if i > n:
            #     print("sleeping 10 munites")
            #     n += 41
            #     sleep(600)
            # log_text(f"scraped {len(product_urls) * i} of {len(product_urls) * max_pages + 1}")
            log_text(f"page {i}")
            paginated_url = response.url + "&page=" + str(i)
            yield response.follow(url=paginated_url, callback=self.parse_products_pagination,
                                  meta={"proxy": get_proxy()})
            # sleep(5)
            # break

        # next_page = response.css("a.ico-chevron-right::attr(href)").get()
        # if next_page is not None:
        #     yield response.follow(url=next_page, callback=self.parse_details)

    def parse_products_pagination(self, response):
        global product_section
        product_section = response.css("h1.boxed-title ::text").get()
        product_urls = response.css("h1 > a").css("::attr(href)").getall()
        # log_text(product_section)
        for product_url in product_urls:
            yield response.follow(url=product_url, callback=self.parse_details, meta={"proxy": get_proxy()})
            # break
            # sleep(1)

    def parse_details(self, response):
        # product_name = response.css(".product-title span:nth-child(2) span:nth-child(1) ::text").get() + " " + \
        #                response.css(".product-title span:nth-child(2) span:nth-child(2) ::text").get()
        # log_text(product_name)

        def get_selector(sel):
            return response.css(sel).get()

        def get_all_selector(sel):
            return response.css(sel).getall()

        product_name = get_selector(".navigation-breadcrumb li:last-child meta:last-child ::attr(content)")
        price = get_selector(".price span::text")
        value = price.split()[0]
        currency = price.split()[-1]
        product_price = {
            "value": value,
            "currency": currency
        }

        category_levels = " > ".join(get_all_selector(".navigation-breadcrumb li a span ::text")[1:-1])
        # brand = get_selector(".about dd:last-child  li  ul li:nth-child(2) span:nth-child(2)::text")
        brand = "NA"
        brands = response.css(".about > dl > dd:nth-child(5) > ul > li:nth-child(1) > ul  li:not(:first-child)")
        for brand_i in brands:
            title = brand_i.css(".title-def::text").get()
            if "Gama" in title:
                brand = brand_i.css("span:last-child ::text").get()
                break

        product_code = get_selector(".ref-piece::text").replace("-", "").strip()
        product_page_url = response.url
        rrp = get_selector(".public-price span::text")
        ref_dict = {}

        list_ref = response.css(".list-ref")
        for lr in list_ref:
            mkey = lr.css(".bold ::text").get()
            if mkey is None:
                mkey = lr.css("b ::text").get()
            mkey = mkey.replace(":", "").strip()
            mvalue = " ".join(lr.css("span:nth-child(n+2) ::text").getall()).replace("  ", " ").strip()
            ref_dict[mkey] = mvalue
        images = response.css(".thumbnail img::attr(src)").getall()
        meta_data = {
            "rrp": rrp,
            "references": ref_dict,
            "images": images
        }

        data = {
            "product_name": product_name,
            "price": product_price,
            "product_code": product_code,
            "product_page_url": product_page_url,
            "category_levels": category_levels,
            "brand": brand,
            "meta_data": meta_data

        }

        save_page_html(response.text.encode("UTF-8"), product_name, data)


process = CrawlerProcess()
process.crawl(OscaroSpider)
process.start()
