import datetime
import json
import math

from typing import Any, Dict, List

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path

try:
    from .validation.process_orders import validate, BASE_DIR
except ImportError:  # pragma: no cover - allows running main.py directly
    from validation.process_orders import validate, BASE_DIR

PRODUCTS_FILE = BASE_DIR / "products.json"
ORDERS_FILE = BASE_DIR / "orders.json"
VALIDATED_ORDERS_FILE = BASE_DIR / "validated_orders.json"
REJECTION_FILE = BASE_DIR / "rejection_list.json"

app = FastAPI(title="Order Management API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://127.0.0.1:8080"
    ],
    allow_credentials=True,
    allow_methods=["GET","POST"],
    allow_headers=["*"],
)


class AddressModel(BaseModel):
    addressLine1: str
    postcode: str
    city: str


class ItemModel(BaseModel):
    productSku: str
    productName: str
    quantity: int
    itemTotal: float


class OrderModel(BaseModel):
    id: int
    customerName: str
    deliveryAddress: AddressModel
    deliveryDate: str
    items: List[ItemModel]
    total: float


PRODUCTS = []
PERSISTED_ORDERS: List[Dict[str, Any]] = []
REJECTED_ORDERS: Dict[int, Dict[str, Any]] = {}


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _write_json(path: Path, payload: Any) -> None:
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)

def bootstrap_orders() -> None:
    global PRODUCTS, PERSISTED_ORDERS, REJECTED_ORDERS

    PRODUCTS = _load_json(PRODUCTS_FILE)
    if VALIDATED_ORDERS_FILE.exists():
        PERSISTED_ORDERS = _load_json(VALIDATED_ORDERS_FILE)
        return

    source_orders = _load_json(ORDERS_FILE)
    REJECTED_ORDERS = {}
    seen_ids = set()
    valid_orders = []
    for order in source_orders:
        if validate(order, PRODUCTS, REJECTED_ORDERS, seen_ids):
            valid_orders.append(order)

    PERSISTED_ORDERS = valid_orders
    _write_json(REJECTION_FILE, REJECTED_ORDERS)
    _write_json(VALIDATED_ORDERS_FILE, PERSISTED_ORDERS)


bootstrap_orders()


@app.get("/health")
def healthcheck() -> Dict[str, str]:
    return {"status": "ok"}

@app.get("/products", response_model=List[Dict[str,Any]])
def list_products() -> List[Dict[str,Any]]:
    return _load_json(PRODUCTS_FILE)
    


@app.get("/orders", response_model=List[Dict[str, Any]])
def list_orders() -> List[Dict[str, Any]]:
    return _load_json(VALIDATED_ORDERS_FILE)


@app.post("/orders", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
def create_order(order: OrderModel) -> Dict[str, Any]:
    payload = order.model_dump()
    print("HERE")
    print(payload)
    existing_ids = {order_entry["id"] for order_entry in PERSISTED_ORDERS}
    local_rejections: Dict[int, Dict[str, Any]] = {}

    validate([payload], PRODUCTS, local_rejections, existing_ids)
    if local_rejections != {}:
        reason = local_rejections.get(payload["id"], {}).get("reason", "Order rejected")
        _write_json(REJECTION_FILE, {**REJECTED_ORDERS, payload["id"]: local_rejections[payload["id"]]})
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Order rejected: {reason}")

    PERSISTED_ORDERS.append(payload)
    _write_json(VALIDATED_ORDERS_FILE, PERSISTED_ORDERS)
    return payload

if __name__ == "__main__":
    bootstrap_orders()
