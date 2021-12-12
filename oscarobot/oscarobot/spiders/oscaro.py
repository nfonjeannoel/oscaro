import scrapy
from scrapy.crawler import CrawlerProcess
import os
from os import path

section_name = ""
subcategory_name = ""
product_section = ""
section_number = 1
sub_section_number = 1


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
    path = os.path.join(parent_dir, my_section_name)
    try:
        os.makedirs(path, exist_ok=True)
        print("Directory '%s' created successfully" % my_section_name)

    except OSError as error:
        print("Directory '%s' can not be created" % my_section_name)


def create_path_product_section(my_section_name):
    parent_dir = f"C:/Users/JEANNOEL/PycharmProjects/oscaro/{section_name}/{subcategory_name}"
    path = os.path.join(parent_dir, my_section_name)

    try:
        os.makedirs(path, exist_ok=True)
        print("Directory '%s' created successfully" % my_section_name)

    except OSError as error:
        print("Directory '%s' can not be created" % my_section_name)


def log_text(param):
    print("*" * 20)
    print(str(param))
    print("*" * 20)


def save_page_html(page_html, product_name):
    # file_path = path.relpath(f"{section_name}/{subcategory_name}/{product_section}/{product_name}.txt")
    # with open(file_path, "w") as f:
    #     f.write(str(page_html))
    path = f"C:/Users/JEANNOEL/PycharmProjects/oscaro"
    with open(f"{path}/{section_name}/{subcategory_name}/{product_section}/{product_name}.txt", "w") as f:
        f.write(str(page_html))


class OscaroSpider(scrapy.Spider):
    name = 'oscaro'
    # allowed_domains = ['x']
    # start_urls = ["https://www-oscaro-com.translate.goog/?_x_tr_sl=fr&_x_tr_tl=en&_x_tr_hl=en&_x_tr_pto=sc"]
    start_urls = ["https://www-oscaro-es.translate.goog/?_x_tr_sl=es&_x_tr_tl=es&_x_tr_hl=es&_x_tr_pto=sc"]

    # start_urls = ["https://www-oscaro-com.translate.goog/outils-de-mesure-et-controle-702661-sc?_x_tr_sl=fr&_x_tr_tl=en&_x_tr_hl=en&_x_tr_pto=sc"]

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
            yield response.follow(url=url, callback=self.parse_category)

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
            if start_url_num == end_url_num:
                for j in range(10):
                    log_text("scraping is done")
                return
            url = urls[start_url_num - 1]
            yield response.follow(url=url, callback=self.parse_products)
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
        product_urls = response.css("h1 > a").css("::attr(href)").getall()
        # log_text(product_section)
        create_path_product_section(product_section)
        #
        for product_url in product_urls:
            yield response.follow(url=product_url, callback=self.parse_details)
        #
            # break

        # # handle pagination
        # get the total number of pages
        max_pages = int(response.css(".pager li:nth-last-child(-n+2) a ::text").get())
        # log_text(f"max pages - {max_pages}")
        # loop n times and create new url
        # looping through all the pagination
        for i in range(2, max_pages + 1):
            # log_text(f"scraped {len(product_urls) * i} of {len(product_urls) * max_pages + 1}")
            log_text(f"page {i}")
            paginated_url = response.url + "&page=" + str(i)
            yield response.follow(url=paginated_url, callback=self.parse_products_pagination)
            # break

        next_page = response.css("a.ico-chevron-right::attr(href)").get()
        if next_page is not None:
            yield response.follow(url=next_page, callback=self.parse_details)

    def parse_products_pagination(self, response):
        global product_section
        product_section = response.css("h1.boxed-title ::text").get()
        product_urls = response.css("h1 > a").css("::attr(href)").getall()
        # log_text(product_section)
        for product_url in product_urls:
            yield response.follow(url=product_url, callback=self.parse_details)
            # break

    def parse_details(self, response):
        product_name = response.css(".product-title span:nth-child(2) span:nth-child(1) ::text").get() + " " + \
                       response.css(".product-title span:nth-child(2) span:nth-child(2) ::text").get()
        # log_text(product_name)
        save_page_html(response.text.encode("UTF-8"), product_name)
        # with open(f"{section_name}/{subcategory_name}/{product_section}/{product_name}.txt", "w") as f:
        #     f.write(str(response.text.encode("UTF-8")))
        # yield None
        # product_name = response.css(".product-title span:nth-child(2) span:nth-child(1) ::text").get() + " " + \
        #                response.css(".product-title span:nth-child(2) span:nth-child(2) ::text").get()
        #
        # price = {
        #     "value": response.css(".price meta:nth-child(2) ::attr(content)").get(),
        #     "currency": response.css(".price meta:nth-child(1) ::attr(content)").get()
        # }
        # category_levels = response.css(".navigation-breadcrumb li a span ::text").getall()[1:]
        # brand = response.css("#productDetail > section > article > div.product-infos > section.about > dl > dd:nth-child(5) > ul > li:nth-child(1) > ul > li:nth-child(2) > span:nth-child(2) ::text").get()
        # images = response.css(".thumbnail img::attr(src)").getall()
        # meta_keys = response.css(".ref ul:last-child li b ::text").getall()
        # meta_values = response.css(".ref ul:last-child li span ::text").getall()
        # meta_dict = {}
        # for key, value in zip(meta_keys, meta_values):
        #     meta_dict[key] = value
        # meta_data = {
        #     "rrp": response.css(".public-price span ::text").get(),
        #     "references": meta_dict
        # }
        #
        # yield {
        #     "product_name": product_name,
        #     "price": price,
        #     "category_levels": category_levels,
        #     "brand": brand,
        #     "images": images,
        #     "meta_data": meta_data
        # }


process = CrawlerProcess()
process.crawl(OscaroSpider)
process.start()
