from datetime import datetime


def address_conversion(address_str):
    # Địa chỉ: Nguyễn Chí Thanh, Láng Thượng, Q.Đống Đa, Hà Nội
    # Địa chỉ format khác
    address_str = address_str.split(",")
    try:
        street = ','.join(address_str[:-3]).strip()
    except IndexError:
        street = ""
    try:
        ward = address_str[-3].strip()
    except IndexError:
        ward = ""
    try:
        district = address_str[-2].strip().replace("Q.", "Quận ")
    except IndexError:
        district = ""

    return street, ward, district


def date_conversion(date_str):
    date = datetime.strptime(date_str, "%d/%m/%Y")
    converted_date = date.strftime("%Y-%m-%d %H:%M:%S")
    return converted_date
