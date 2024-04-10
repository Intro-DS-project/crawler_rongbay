from datetime import datetime


def address_conversion(address_str):
    # Địa chỉ: Nguyễn Chí Thanh, Láng Thượng, Q.Đống Đa, Hà Nội
    # Địa chỉ format khác
    address_part = address_str.split(",")
    if len(address_part) == 1:
        address_part = address_str.split("-")

    length = len(address_part)
    if length == 1:
        street, ward, district = "", "", ""
    elif length == 2:
        street, ward, district = "", "", address_part[-2]
    elif length == 3:
        street, ward, district = address_part[-3], "", address_part[-2]
    else:
        street, ward, district = address_part[-4], address_part[-3], address_part[-2]

    def clean(str, pat):
        res = str
        for p in pat:
            if p in str:
                res = str.split(p)[-1]
                break
        return res.lstrip('0123456789/ ')

    street = clean(street.replace("Q.", "Quận "), ["Phố", "Đường", "phố", "đường", "Ngõ", "ngõ", "Ngách", "ngách"])
    ward = clean(ward, ["Phường", "Xã", "phường", "xã",])
    district = clean(district, ["Quận", "Huyện", "quận", "huyện"])

    return street, ward, district


def date_conversion(date_str):
    date = datetime.strptime(date_str, "%d/%m/%Y")
    converted_date = date.strftime("%Y-%m-%d %H:%M:%S")
    return converted_date
