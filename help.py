import re


def get_orders_ids(data):
    yearly_ids = {}
    orders = {}
    for index, (order, date) in enumerate(sorted(data, key=lambda x: x[1]), start=1):
        year = date[:4]  # Extract the year from the date string
        if year not in yearly_ids:
            yearly_ids[year] = 1
        else:
            yearly_ids[year] += 1
        orders[order] = f"{year}/{yearly_ids[year]:02d}"
    return orders


def is_arabic(text):
    # Remove extra white spaces
    cleaned_text = re.sub(r'\s+', ' ', text.strip())
    # Check if the cleaned text contains only Arabic letters
    return bool(re.match(r"^[\u0600-\u06FF\s]+$", cleaned_text))


def is_phone_number(text):
    # Remove extra white spaces
    cleaned_text = re.sub(r'\s+', '', text.strip())
    # Check if the cleaned text matches the phone number pattern
    return bool(re.match(r"^(05|06|07)\d{8}$", cleaned_text)) if cleaned_text != '' else True


def is_float(text):
    # Remove extra white spaces
    cleaned_text = re.sub(r'\s+', '', text.strip())
    # Check if the cleaned text contains only digits, and optional .2d
    return bool(re.match(r"^\d+(\.\d{0,2})?$", cleaned_text))


def is_number(text):
    # Remove extra white spaces
    cleaned_text = re.sub(r'\s+', '', text.strip())
    # Check if the cleaned text contains only digits
    return bool(re.match(r"^\d+$", cleaned_text))


def is_reg_id(text):
    # Remove non-alphanumeric characters except "/" and "-"
    cleaned_text = re.sub(r'\s+', '', text)
    # Check if the cleaned text contains only English letters, digits, "/", and "-"
    return bool(re.match(r'^[A-Za-z0-9/-]+$', cleaned_text))