from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from starlette.responses import JSONResponse
import requests
from app.settings import SETTINGS

router = APIRouter()
BASE_URL = "https://api.moysklad.ru/api/remap/1.2"
HEADERS = {
    "Authorization": f"Bearer {SETTINGS.TOKEN}",
    "Content-Type": "application/json",
}


class Position(BaseModel):
    quantity: float
    price: float
    product_id: str = "ee1d75c8-ad8e-11ef-0a80-07b6008509e3"


@router.post("/create-shipment-without-customer_order/")
def create_shipment_without_order(
    organization_id: str = "a0a7a2fc-ad8e-11ef-0a80-04290083f6e2",
    counterparty_id: str = "a0aa6181-ad8e-11ef-0a80-04290083f6e8",
    positions: list[Position] = None,
    store_id: str = "a0aa0f41-ad8e-11ef-0a80-04290083f6e5",
):
    url = f"{BASE_URL}/entity/demand"
    payload = {
        "organization": {
            "meta": {
                "href": f"{BASE_URL}/entity/organization/{organization_id}",
                "type": "organization",
                "mediaType": "application/json",
            },
        },
        "agent": {
            "meta": {
                "href": f"{BASE_URL}/entity/counterparty/{counterparty_id}",
                "type": "counterparty",
                "mediaType": "application/json",
            },
        },
        "store": {
            "meta": {
                "href": f"{BASE_URL}/entity/store/{store_id}",
                "type": "store",
                "mediaType": "application/json",
            },
        },
        "positions": [
            {
                "quantity": pos.quantity,
                "assortment": {
                    "meta": {
                        "href": f"{BASE_URL}/entity/product/{pos.product_id}",
                        "type": "product",
                        "mediaType": "application/json",
                    },
                },
                "price": pos.price,
            }
            for pos in positions
        ],
        "applicable": True,
    }
    response = requests.post(url, json=payload, headers=HEADERS)
    if response.status_code in (200, 201):
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)


@router.get("/get-organizations/")
def get_organizations():
    url = f"https://api.moysklad.ru/api/remap/1.3/entity/organization"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        organizations = response.json()["rows"]  # Список всех организаций
        # return [{"id": org["id"], "name": org["name"]} for org in organizations]
        return organizations
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)


@router.get("/get-counterparties/")
def get_counterparties():
    url = f"{BASE_URL}/entity/counterparty"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        counterparties = response.json()["rows"]  # Список всех контрагентов
        return [{"id": cp["id"], "name": cp["name"]} for cp in counterparties]
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)


@router.get("/get-products/")
def get_products_endpoint():
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


@router.get("/get-stores/")
def get_warehouses():
    url = f"{BASE_URL}/entity/store"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()["rows"]
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")
