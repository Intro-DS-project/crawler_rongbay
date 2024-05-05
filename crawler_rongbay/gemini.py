import os
from dotenv import load_dotenv
from pathlib import Path

import google.generativeai as genai

load_dotenv(dotenv_path=Path('.env'))
GOOGLE_API_KEY = os.getenv('API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro')


def extract_description(description):
    prompt = f"Ta có thông tin rao bán nhà bằng tiếng Việt như sau: \
        {description} \n \
        Hãy trích xuất thông tin trên và trả về 8 trường thông tin dưới đây. \
        Danh sách các trường: num_bedroom, \
        num_diningroom, num_kitchen, num_toilet, num_floor (nếu là nhà trọ thì có mấy tầng), \
        current_floor (phòng trọ ở tầng mấy), direction (hướng nhà, 1 trong 4 giá trị Đông/Tây/Nam/Bắc), \
        street_width (số thực, theo mét). \
        Trường nào không xuất hiện thì để là 0.\
        Các trường thông tin ngăn cách bởi dấu phẩy.\
        Ví dụ: \"0,0,1,1,0,0,Đông,0\", hoặc \"1,0,1,1,0,0,0,0\" nếu không có direction."

    response = model.generate_content(prompt)
    return response.text


def extract_location(location):
    prompt = f"Ta có thông tin địa chỉ bằng tiếng Việt như sau: \
        {location} \n \
        Hãy trích xuất thông tin trên và trả về 3 trường thông tin dưới đây. \
        Danh sách các trường: \
        street (tên đường hoặc phố. Không bao gồm ngõ/ngách. Không bao gồm số nhà ở trước tên đường. Chỉ có tên, không có chữ 'đường' ở trước), \
        ward (là phường, nhưng có thể thay bằng xã. Chỉ gồm tên, không có chữ 'phường'/'xã' ở trước), \
        district (là quận, nhưng có thể thay bằng huyện Chỉ gồm tên, không có chữ 'quận'/'huyện' ở trước). Không bao gồm tên thành phố Hà Nội. \
        Trường nào không xuất hiện thì để là rỗng. \
        Các trường thông tin ngăn cách bởi dấu phẩy.\
        Ví dụ: \"Tân Triều,Thanh Xuân Nam,Thanh Xuân\", hoặc \"Tân Triều,,Thanh Xuân\" nếu có trường trống."

    response = model.generate_content(prompt)
    return response.text