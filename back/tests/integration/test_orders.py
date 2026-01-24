import pytest
import uuid
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


@pytest.mark.integration
def test_POST_order_1_successful_register(client):
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    payload = {
        "customer_id": str(uuid.uuid4()),
        "order_status": "delivered",
        "order_purchase_timestamp": -46.41607223296136,
        "order_approved_at": now_str,
        "order_delivered_carrier_date": now_str,
        "order_delivered_customer_date": now_str,
        "order_estimated_delivery_date": now_str
    }

    response = client.post("/order/", json=payload)

    assert response.status_code == 201

    data = response.json()

    assert "order_id" in data