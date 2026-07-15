

export function OrdersPage({ orders }) {
  return (
    <section className="card">
      <h2>All orders</h2>
      {orders.length === 0 ? (
        <p>No orders yet.</p>
      ) : (
        <div className="orders-list">
          {orders.map((order) => (
            <article key={order.id} className="order-card">
              <div className="order-header">
                <strong>#{order.id}</strong>
                <span>{order.customerName}</span>
              </div>
              <p>{order.deliveryAddress?.addressLine1}, {order.deliveryAddress?.city}</p>
              <p>Delivery date: {order.deliveryDate}</p>
              <ul>
                {order.items?.map((item, index) => (
                  <li key={`${order.id}-${index}`}>
                    {item.productName} × {item.quantity}
                  </li>
                ))}
              </ul>
              <p className="order-total">Total: £{Number(order.total || 0).toFixed(2)}</p>
            </article>
          ))}
        </div>
      )}
    </section>
  );
}
