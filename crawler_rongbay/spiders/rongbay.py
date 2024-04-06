import scrapy
from scrapy.exceptions import CloseSpider

from crawler_rongbay.items import RoomItem
from crawler_rongbay.utils import address_conversion, date_conversion


class RongbaySpider(scrapy.Spider):
    name = "rongbay"

    def start_requests(self):
        i = 1
        while True:
            yield scrapy.Request(url=f"https://rongbay.com/Ha-Noi/Nha-tro-Phong-tro-Cho-thue-nha-c272-t788-trang{i}.html", callback=self.parse)
            i += 1

    def parse(self, response):
        room_items = response.css(".list_content_bds .subCateBDS:not(.ad_vip)")
        if not room_items:
            raise CloseSpider("No more room items to scrape")
        for item in room_items:
            room_href = item.css("::attr(href)").get()
            yield response.follow(room_href, callback=self.parse_room_detail)

    def parse_room_detail(self, response):
        item = RoomItem()

        # Địa chỉ
        address = response.css("p.cl_666::text").get()
        if address:
            (item["street"], item["ward"], item["district"]) = address_conversion(address)
        else:
            item["street"] = item["ward"] = item["district"] = ""

        # Giá : 2,5 Triệu/tháng
        price_str = response.css("li.li_100:nth-child(1) > span:nth-child(1)::text").get()
        try:
            item["price"] = float(price_str.split()[0].replace(',', '.'))
        except ValueError:  # Giá thỏa thuận
            item["price"] = 0

        # Diện tích : 20m2
        area_str = response.css("li.li_100:nth-child(2) > span:nth-child(1)::text").get()
        item["area"] = int(area_str[:-1]) if area_str else 0

        # Thời gian: 06/04/2024
        post_date_str = response.css("span.note_gera:nth-child(1) > span:nth-child(1)::text").get()
        item["post_date"] = date_conversion(post_date_str)

        # Link
        item["url"] = response.url

        # Điền các trường còn thiếu
        item["num_bedroom"] = 0
        item["num_diningroom"] = 0
        item["num_kitchen"] = 0
        item["num_toilet"] = 0
        item["num_floor"] = 0
        item["current_floor"] = 0
        item["direction"] = ""
        item["street_width"] = 0
        item["description"] = ""

        yield item
