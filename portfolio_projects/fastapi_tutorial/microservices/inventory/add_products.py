import requests

products = [
    {"name": "Apple iPhone", "price": 999.99, "quantity": 10},
    {"name": "Samsung Galaxy", "price": 899.99, "quantity": 15},
    {"name": "Google Pixel", "price": 799.99, "quantity": 20},
    {"name": "OnePlus 9", "price": 699.99, "quantity": 18},
    {"name": "Sony Xperia", "price": 649.99, "quantity": 12},
    {"name": "Huawei P30", "price": 599.99, "quantity": 17},
    {"name": "Nokia X20", "price": 499.99, "quantity": 25},
    {"name": "Motorola Edge", "price": 549.99, "quantity": 14},
    {"name": "LG Velvet", "price": 579.99, "quantity": 9},
    {"name": "Asus ROG Phone", "price": 899.00, "quantity": 6},
    {"name": "Xiaomi Mi 11", "price": 699.99, "quantity": 19},
    {"name": "Realme GT", "price": 599.99, "quantity": 11},
    {"name": "Vivo V21", "price": 499.99, "quantity": 22},
    {"name": "Oppo Reno6", "price": 649.99, "quantity": 13},
    {"name": "ZTE Axon", "price": 699.00, "quantity": 8},
    {"name": "Infinix Zero", "price": 299.99, "quantity": 30},
    {"name": "Tecno Phantom", "price": 349.99, "quantity": 27},
    {"name": "Lenovo Legion", "price": 999.00, "quantity": 5},
    {"name": "BlackBerry Key2", "price": 599.99, "quantity": 7},
    {"name": "Fairphone 4", "price": 579.00, "quantity": 4},
]

for product in products:
    response = requests.post("http://localhost:8000/products", json=product)
    print(response.json())
