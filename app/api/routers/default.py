from fastapi import APIRouter, HTTPException

from starlette.responses import JSONResponse
import requests

from app.settings import SETTINGS

router = APIRouter()
BASE_URL = "https://online.moysklad.ru/api/remap/1.2"
HEADERS = {
    "Authorization": f"Bearer {SETTINGS.TOKEN}",
    "Content-Type": "application/json",
}


@router.get("/")
async def root():
    return JSONResponse(content={"message": "Hello World"})


@router.post("/create-shipment/")
async def create_shipment(customer_order_id: str, positions: list[dict]):
    """
    Создать отгрузку для заказа покупателя
    :param customer_order_id: ID заказа покупателя (customerorder)
    :param positions: Список позиций для отгрузки (товары, количество)
    """
    # URL для создания отгрузки (demand)
    url = f"{BASE_URL}/entity/demand"

    # Формируем тело запроса
    payload = {
        "organization": {
            "meta": {
                "href": f"{BASE_URL}/entity/organization/your-organization-id",
                "type": "organization",
                "mediaType": "application/json",
            }
        },
        "agent": {
            "meta": {
                "href": f"{BASE_URL}/entity/counterparty/your-counterparty-id",
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
                "quantity": pos["quantity"],
                "price": pos["price"],
                "assortment": {
                    "meta": {
                        "href": f"{BASE_URL}/entity/product/{pos['product_id']}",
                        "type": "product",
                        "mediaType": "application/json",
                    }
                },
            }
            for pos in positions
        ],
    }

    response = requests.post(url, json=payload, headers=HEADERS)

    if response.status_code == 200 or response.status_code == 201:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)
