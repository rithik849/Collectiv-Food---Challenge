import { useEffect, useMemo, useState } from 'react';
import { Link, Route, Routes, useNavigate } from 'react-router-dom';
import {CreateOrderPage} from './create_orders.jsx'
import {OrdersPage} from './view_orders.jsx'

export const API_URL = import.meta.env.VITE_API_URL;

function App() {
  const [orders, setOrders] = useState([]);
  const [products, setProducts] = useState([]);
  const [errors, setErrors] = useState('');

  const loadOrders = () => {
    fetch(`${API_URL}/orders`)
      .then((response) => response.json())
      .then(setOrders)
      .catch(() => setErrors('Unable to load orders.'));
  };

  const loadProducts = () => {
    fetch(`${API_URL}/products`)
      .then((response) => response.json())
      .then(setProducts)
      .catch(() => setErrors('Unable to load products.'));
  }

  useEffect(() => {
    loadOrders();
    loadProducts();
  }, []);

  return (
    <div className="app-shell">
      <header>
        <h1>Order Management</h1>
        <p>Use the links below to switch between creating and reviewing orders.</p>
        <nav className="nav-links">
          <Link to="/orders">View orders</Link>
          <Link to="/create">Create order</Link>
        </nav>
      </header>

      {errors ? <p className="error">{errors}</p> : null}

      <main>
        <Routes>
          <Route path="/" element={<OrdersPage orders={orders} />} />
          <Route path="/create" element={<CreateOrderPage products={products} onCreated={loadOrders} />} />
          <Route path="/orders" element={<OrdersPage orders={orders} />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
