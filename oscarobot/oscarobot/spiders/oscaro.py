import scrapy
from scrapy.crawler import CrawlerProcess
import os

section_name = ""
subcategory_name = ""
# product_section = ""
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

#
# def create_path_product_section(my_section_name):
#     parent_dir = f"C:/Users/JEANNOEL/PycharmProjects/oscaro/{section_name}/{subcategory_name}"
#     path = os.path.join(parent_dir, my_section_name)
#     try:
#         os.makedirs(path, exist_ok=True)
#         print("Directory '%s' created successfully" % my_section_name)
#
#     except OSError as error:
#         print("Directory '%s' can not be created" % my_section_name)


def log_text(param):
    print("*" * 20)
    print(str(param))
    print("*" * 20)


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
            log_text(url)
            # creating path with name as the current section title - section_name
            create_path_section(section_name)
            yield response.follow(url=url, callback=self.parse_category)
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
            urls = section.css("ul li a").css("::attr(href)").getall()[:-1]
            # create directory for this sub category
            create_path_sub_section(subcategory_name)
            # break
            for url in urls:
                yield response.follow(url=url, callback=self.parse_products)
                # to follow only one url
                break
            break

    def parse_products(self, response):
        global product_section
        product_section = response.css(".boxed-title font font ::text").get()
        product_urls = response.css("h1 > a").css("::attr(href)").getall()
        # create_path_product_section(product_section)
        for product_url in product_urls:
            yield response.follow(url=product_url, callback=self.parse_details)

        # handle pagination
        next_page = response.css("a.ico-chevron-right::attr(href)").get()
        if next_page is not None:
            yield response.follow(url=next_page, callback=self.parse_details)

    def parse_details(self, response):
        product_name = response.css(".product-title span:nth-child(2) span:nth-child(1) ::text").get() + " " + \
                       response.css(".product-title span:nth-child(2) span:nth-child(2) ::text").get()
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
