import requests
from app.settings import SETTINGS

BASE_URL = "https://api.moysklad.ru/api/remap/1.2"
HEADERS = {
    "Authorization": f"Bearer {SETTINGS.TOKEN}",
    "Content-Type": "application/json",
}


def get_organization_id(name=None):
    url = f"{BASE_URL}/entity/organization"
    params = {}
    if name:
        params["filter"] = f"name={name}"
    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code == 200:
        organizations = response.json().get("rows", [])
        if organizations:
            org = organizations[0]
            return {"id": org.get("id"), "name": org.get("name")}
        else:
            return None
    else:
        response.raise_for_status()


def get_counterparty_id(name=None):
    url = f"{BASE_URL}/entity/counterparty"
    params = {}
    if name:
        params["filter"] = f"name={name}"
    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code == 200:
        counterparties = response.json().get("rows", [])
        if counterparties:
            counterparty = counterparties[0]
            return {"id": counterparty.get("id"), "name": counterparty.get("name")}
        else:
            return None
    else:
        response.raise_for_status()


def get_products():
    url = f"{BASE_URL}/entity/product"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        products = response.json().get("rows", [])
        product_list = [
            {
                "id": product.get("id"),
                "name": product.get("name"),
                "price": product.get("price"),
            }
            for product in products
        ]
        return product_list
    else:
        response.raise_for_status()


print("Organizations:")
org = get_organization_id(name="Test Organization")
print(org)

print("\nCounterparties:")
counterparty = get_counterparty_id(name="Test Counterparty")
print(counterparty)

print("\nProducts:")
products = get_products()
print(products)
