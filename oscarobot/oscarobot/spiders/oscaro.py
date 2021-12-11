import scrapy
from scrapy.crawler import CrawlerProcess
section_name = ""
subcategory_name = ""
product_section = ""
# impodsdrt os

# main_category = 'downloaded'
# sub_category = ""
# parent_dir = 'C:/'
# try:
#     path = os.path.join(parent_dir, main_category)
#
#     os.mkdir(path)
#     new_directory = parent_dir + main_category
#
#     with open(f"{new_directory}/filename.txt", "w+") as f:
#         f.write("this will create a folder 'downloaded' in drive C with a text inside")
#
# except FileExistsError:
#     new_directory = parent_dir + main_category
#     with open(f"{new_directory}/filename.txt", "w") as f:
#         f.write("this will create a folder 'downloaded' in drive C with a text inside")

category = {

}
class OscaroSpider(scrapy.Spider):
    name = 'oscaro'
    # allowed_domains = ['x']
    start_urls = ["https://www-oscaro-com.translate.goog/?_x_tr_sl=fr&_x_tr_tl=en&_x_tr_hl=en&_x_tr_pto=sc"]

    # start_urls = ["https://www-oscaro-com.translate.goog/outils-de-mesure-et-controle-702661-sc?_x_tr_sl=fr&_x_tr_tl=en&_x_tr_hl=en&_x_tr_pto=sc"]

    def parse(self, response):
        sections = response.css(".subcat div")
        global section_name
        for section in sections:
            section_name = section.css("h2 a font font::text").get()
            # getting main category links
            url = section.css("h2 a").css("::attr(href)").get()
            yield response.follow(url=url, callback=self.parse_category)
            break


    def parse_category(self, response):
        sections = response.css(".subcat")
        global subcategory_name
        for section in sections:
            # getting subcategory links
            subcategory_name = section.css("h2 a font font::text").get()
            urls = section.css("ul li a").css("::attr(href)").getall()[:-1]
            for url in urls:
                yield response.follow(url=url, callback=self.parse_products)
                # break

            break


    def parse_products(self, response):
        global product_section
        product_section = response.css(".boxed-title font font ::text").get()
        product_urls = response.css("h1 > a").css("::attr(href)").getall()
        for product_url in product_urls:
            yield response.follow(url=product_url, callback=self.parse_details)

        # handle pagination
        next_page = response.css("a.ico-chevron-right::attr(href)").get()
        if next_page is not None:
            yield response.follow(url=next_page, callback=self.parse_details)

    def parse_details(self, response):
        product_name = response.css(".product-title span:nth-child(2) span:nth-child(1) ::text").get() + " " + \
                       response.css(".product-title span:nth-child(2) span:nth-child(2) ::text").get()
        with open(f"{product_name}.txt", "w") as f:
            f.write(str(response.text.encode("UTF-8")))
        yield None
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
