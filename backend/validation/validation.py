import datetime
import math

def _reject(rejected_orders, order, reason):
    order_id = order.get("id", "unknown")
    if order_id in rejected_orders:
        existing_reason = rejected_orders[order_id]["reason"]
        rejected_orders[order_id]["reason"] = f"{existing_reason}; {reason}"
    else:
        rejected_orders[order_id] = {"order": order, "reason": reason}

def validate_address(order, rejected_orders):
    try:
        address = order.get("deliveryAddress") or {}
        address_line1 = (address.get("addressLine1") or "").strip()
        postcode = (address.get("postcode") or "").strip()
        city = (address.get("city") or "").strip()
        messages = []

        if address_line1 == "":
            messages.append("Address line 1 left blank.")
        if city == "":
            messages.append("City left blank.")
        if postcode == "":
            messages.append("Postcode left blank.")
        elif len(postcode.split()) != 2:
            messages.append("Postcode must be of a valid format.")

        if messages:
            raise Exception("; ".join(messages))
    except Exception as e:
        _reject(rejected_orders, order, str(e))


def validate_date(order, rejected_orders):
    try:
        delivery_date = order.get("deliveryDate")
        if not delivery_date:
            raise ValueError("Delivery date missing.")
        datetime.datetime.strptime(delivery_date, "%d/%m/%Y")
    except Exception as e:
        _reject(rejected_orders, order, str(e))


def validate_items(order, rejected_orders, products):
    
    sku_to_product = {product["sku"]: product for product in products}
    normalized_sku_to_product = {product["sku"].lower(): product for product in products}
    
    if not order.get("items"):
        _reject(rejected_orders, order, "Order has no items.")
        return

    errors = []
    for item in order.get("items", []):
        sku = item.get("productSku")
        if not sku:
            errors.append("Invalid product SKU.")
            continue
        

        exact_match = sku_to_product.get(sku)
        product_name = item.get("productName")
        # Check SKU has an exact match that exists.
        if exact_match:
            if exact_match["name"] != product_name:
                errors.append(
                    f"Product Name {product_name} does not match SKU {sku} product reference {exact_match['name']}"
                )
        else:
            
            # Check case mismatch of SKU or if it exists
            normalized_sku = sku.lower()
            if normalized_sku in normalized_sku_to_product:
                expected_sku = normalized_sku_to_product[normalized_sku]["sku"]
                errors.append(f"Case mismatch for product SKU '{sku}'. Expected '{expected_sku}'.")
            else:
                errors.append(f"Invalid product SKU '{sku}'.")
            
            

    if errors:
        _reject(rejected_orders, order, "; ".join(errors))
        

    item_total_sum = sum(float(item.get("itemTotal", 0)) for item in order.get("items", []))
    order_total = order.get("total")
    if order_total is not None:
        try:
            if not math.isclose(float(order_total), item_total_sum, rel_tol=1e-9, abs_tol=1e-9):
                _reject(rejected_orders, order, "Order total does not equal the sum of item totals.")
                
        except (TypeError, ValueError):
            _reject(rejected_orders, order, "Order total is invalid.")
    else:
        _reject(rejected_orders, order, "Order total not specified.")

def validate_orders(order, rejected_orders, products):

    if not order:
        _reject(rejected_orders, order or {}, "Order record is empty.")
        return

    if not isinstance(order, dict):
        _reject(rejected_orders, order or {}, "Order must be a JSON object.")
        return
    
    validate_items(order, rejected_orders, products)


def validate(orders, products, rejected_orders, seen_id):
    for order in orders:
        if order["id"] in seen_id:
            _reject(rejected_orders, order, f"Order {order['id']} has a duplicate entry.")
        seen_id.add(order["id"])
        validate_address(order, rejected_orders)
        validate_date(order, rejected_orders)
        validate_orders(order, rejected_orders, products)