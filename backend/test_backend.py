import os
import sys
import time
import unittest

from fastapi.testclient import TestClient

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from backend.main import app


class BackendApiTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_get_orders_returns_valid_orders(self):
        response = self.client.get("/orders")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIsInstance(payload, list)
        self.assertGreaterEqual(len(payload), 1)

    def test_create_order_persists_valid_order(self):
        order = {
            "id": int(time.time() * 1000),
            "customerName": "API Test Customer",
            "deliveryAddress": {
                "addressLine1": "1 API Street",
                "postcode": "SW1A 1AA",
                "city": "London"
            },
            "deliveryDate": "13/07/2026",
            "items": [
                {
                    "productSku": "YR9U90T57MR0",
                    "productName": "Whole Milk 2L",
                    "quantity": 1,
                    "itemTotal": 2.35
                }
            ],
            "total": 2.35
        }

        response = self.client.post("/orders", json=order)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["id"], order["id"])

        get_response = self.client.get("/orders")
        persisted_ids = {item["id"] for item in get_response.json()}
        self.assertIn(order["id"], persisted_ids)

    def test_create_order_rejects_invalid_payload(self):
        invalid_order = {
            "id": 88888,
            "customerName": "Broken Order",
            "deliveryAddress": {
                "addressLine1": "",
                "postcode": "SW1A 1AA",
                "city": "London"
            },
            "deliveryDate": "13/07/2026",
            "items": [],
            "total": 0
        }

        response = self.client.post("/orders", json=invalid_order)
        self.assertEqual(response.status_code, 400)
        self.assertIn("rejected", response.json()["detail"].lower())


if __name__ == "__main__":
    unittest.main()
