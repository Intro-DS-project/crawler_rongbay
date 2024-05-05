import scrapy
from scrapy.exceptions import CloseSpider
from datetime import datetime
from hanoikovoidcdau import standardize

from crawler_rongbay.items import RoomItem
from crawler_rongbay.gemini import extract_description, extract_location


class RongbaySpider(scrapy.Spider):
    name = "rongbay"
    stop = False

    def start_requests(self):
        i = 1
        while i <= 5:
            yield scrapy.Request(url=f"https://rongbay.com/Ha-Noi/Nha-tro-Phong-tro-Cho-thue-nha-c272-t788-trang{i}.html", callback=self.parse)
            if self.stop:
                raise CloseSpider("Completed scraping the current day's item.")
            i += 1

    def parse(self, response):
        room_items = response.css(".list_content_bds .subCateBDS:not(.ad_vip)")
        for item in room_items:
            room_href = item.css("::attr(href)").get()
            yield response.follow(room_href, callback=self.parse_room_detail)

    def parse_room_detail(self, response):
        item = RoomItem()

        # Thời gian: 06/04/2024
        post_date_str = response.css("span.note_gera:nth-child(1) > span:nth-child(1)::text").get()
        post_date_datetime = datetime.strptime(post_date_str, "%d/%m/%Y").date()
        current_date = datetime.now().date()
        if (post_date_datetime < current_date):
            self.stop = True
            return
        item["post_date"] = post_date_datetime.strftime("%Y-%m-%d %H:%M:%S")

        # Giá : 2,5 Triệu/tháng
        price_str = response.css("li.li_100:nth-child(1) > span:nth-child(1)::text").get()
        try:
            item["price"] = float(price_str.split()[0].replace(',', '.'))
        except ValueError:  # Giá thỏa thuận
            item["price"] = 0

        # Diện tích : 20m
        area_str = response.css("li.li_100:nth-child(2) > span:nth-child(1)::text").get()
        item["area"] = int(area_str[:-1]) if area_str else 0

        # Địa chỉ
        address = response.css("p.cl_666::text").get()
        (item["street"], item["ward"], item["district"], *_) = extract_location(address).split(',')
        item["street"] = standardize.standardize_street_name(item["street"])
        item["ward"] = standardize.standardize_ward_name(item["ward"])
        item["district"] = standardize.standardize_district_name(item["district"])

        # Dùng mô tả điền các trường còn lại
        desc_str = response.css(".info-content-body::text").getall()
        fields = extract_description(' '.join(desc_str)).split(',')
        fields_int = []
        for field in fields:
            try:
                fields_int.append(int(field))
            except ValueError:
                fields_int.append(field)
        (item["num_bedroom"], item["num_diningroom"], item["num_kitchen"], item["num_toilet"], item["num_floor"],
         item["current_floor"], item["direction"], item["street_width"], *_) = fields_int

        yield item
