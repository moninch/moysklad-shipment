from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from starlette.responses import JSONResponse
import requests

from app.api.dependencies import get_counterparty_id, get_organization_id, get_products
from app.settings import SETTINGS

router = APIRouter()
BASE_URL = "https://api.moysklad.ru/api/remap/1.3"
HEADERS = {
    "Authorization": f"Bearer {SETTINGS.TOKEN}",
    "Content-Type": "application/json",
}


class Position(BaseModel):
    quantity: float
    price: float
    product_id: str


@router.get("/")
async def root():
    return JSONResponse(content={"message": "Hello World"})


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
    organization_id: str,
    counterparty_id: str,
    positions: list[Position],
    warehouse_id: Optional[str] = None,
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
    if warehouse_id:
        payload["store"] = {
            "meta": {
                "href": f"{BASE_URL}/entity/warehouse/{warehouse_id}",
                "type": "warehouse",
                "mediaType": "application/json",
            },
        }
    response = requests.post(url, json=payload, headers=HEADERS)
    if response.status_code in (200, 201):
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)


@router.post("/create-shipment/")
async def create_shipment(customer_order_id: str, positions: list[Position]):
    organization_data = get_organization_id()
    counterparty_data = get_counterparty_id()

    if not organization_data or not counterparty_data:
        raise HTTPException(
            status_code=400, detail="Organization or Counterparty not found"
        )

    url = f"{BASE_URL}/entity/shipment"

    payload = {
        "organization": {
            "meta": {
                "href": f"{BASE_URL}/entity/organization/{organization_data['id']}",
                "type": "organization",
                "mediaType": "application/json",
            }
        },
        "agent": {
            "meta": {
                "href": f"{BASE_URL}/entity/counterparty/{counterparty_data['id']}",
                "type": "counterparty",
                "mediaType": "application/json",
            }
        },
        "customerOrder": {
            "meta": {
                "href": f"{BASE_URL}/entity/customerorder/{customer_order_id}",
                "type": "customerorder",
                "mediaType": "application/json",
            }
        },
        "positions": [
            {
                "quantity": pos.quantity,
                "price": pos.price,
                "assortment": {
                    "meta": {
                        "href": f"{BASE_URL}/entity/product/{pos.product_id}",
                        "type": "product",
                        "mediaType": "application/json",
                    }
                },
            }
            for pos in positions
        ],
    }

    response = requests.post(url, json=payload, headers=HEADERS)

    if response.status_code in (200, 201):
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)


@router.get("/get-customer-orders/")
async def get_customer_orders():
    response = requests.get(f"{BASE_URL}/entity/customerorder", headers=HEADERS)
    if response.status_code == 200:
        return response.json()["rows"]
    raise HTTPException(status_code=response.status_code, detail=response.text)


@router.get("/get-organizations/")
def get_organizations():
    organization_data = get_organization_id()
    return organization_data


@router.get("/get-counterparties/")
def get_counterparties():
    counterparty_data = get_counterparty_id()
    return counterparty_data


@router.get("/get-products/")
def get_products_endpoint():
    products = get_products()
    return products


# print(get_products())
# print(get_organization_id())
# print(get_counterparty_id())
