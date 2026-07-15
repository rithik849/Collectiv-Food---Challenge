import { useEffect, useMemo, useState } from 'react';
import { Link, Route, Routes, useNavigate } from 'react-router-dom';
import {API_URL} from './App.jsx'

const emptyItem = () => ({
  productSku: '',
  productName: '',
  quantity: 1,
  itemTotal: 0.01
});


export function CreateOrderPage({ products, onCreated }) {
  const [formData, setFormData] = useState({
    customerName: '',
    addressLine1: '',
    postcode: '',
    city: '',
    deliveryDate: '',
    items: [emptyItem()]
  });
  const [errors, setErrors] = useState('');
  const [success, setSuccess] = useState('');
  const [dateError, setDateError] = useState('');
  const navigate = useNavigate();

  const total = useMemo(() => {
    return formData.items.reduce((sum, item) => sum + Number(item.itemTotal || 0), 0);
  }, [formData.items]);

  const getAvailableProductsForRow = (rowIndex) => {
    const selectedInOtherRows = formData.items
      .filter((_, index) => index !== rowIndex)
      .map((item) => item.productSku)
      .filter(Boolean);

    return products.filter((product) => {
      return !selectedInOtherRows.includes(product.sku) || product.sku === formData.items[rowIndex]?.productSku;
    });
  };

  const updateItem = (index, field, value) => {
    const nextItems = [...formData.items];
    nextItems[index] = { ...nextItems[index], [field]: value };

    if (field === 'productSku') {
      const product = products.find((entry) => entry.sku === value);
      nextItems[index].productName = product?.name || '';
    }

    if (field === 'quantity') {
      const numericValue = Number(value);
      nextItems[index].quantity = numericValue > 0 ? numericValue : 1;
    }

    setFormData({ ...formData, items: nextItems });
  };

  const addItemRow = () => {
    setFormData({ ...formData, items: [...formData.items, emptyItem()] });
  };

  const removeItemRow = (index) => {
    if (formData.items.length === 1) {
      return;
    }
    const nextItems = formData.items.filter((_, itemIndex) => itemIndex !== index);
    setFormData({ ...formData, items: nextItems });
  };

  const formatDateForDisplay = (value) => {
    if (!value) return '';

    const [year, month, day] = value.split('-').map(Number);
    if (!year || !month || !day) return '';

    return `${String(day).padStart(2, '0')}/${String(month).padStart(2, '0')}/${year}`;
  };

  const validateDeliveryDate = (value) => {
    if (!value) {
      return 'Delivery date is required.';
    }

    const [day, month, year] = value.split('/').map(Number);
    const parsedDate = new Date(year, month - 1, day);
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    if (
      Number.isNaN(parsedDate.getTime()) ||
      parsedDate <= today
    ) {
      return 'Delivery date must be in the future.';
    }

    return '';
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setErrors('');
    setSuccess('');
    setDateError('');

    const dateValidationMessage = validateDeliveryDate(formData.deliveryDate);
    if (dateValidationMessage) {
      setDateError(dateValidationMessage);
      return;
    }

    const payload = {
      id: Date.now(),
      customerName: formData.customerName,
      deliveryAddress: {
        addressLine1: formData.addressLine1,
        postcode: formData.postcode,
        city: formData.city
      },
      deliveryDate: formData.deliveryDate,
      items: formData.items.map((item) => ({
        productSku: item.productSku,
        productName: item.productName,
        quantity: Number(item.quantity),
        itemTotal: Number(item.itemTotal)
      })),
      "total" : total
    };

    const response = await fetch(`${API_URL}/orders`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    const data = await response.json();
    if (!response.ok) {
      setErrors(data.detail || 'Order submission failed.');
      return;
    }

    setSuccess('Order created successfully!');
    setFormData({
      customerName: '',
      addressLine1: '',
      postcode: '',
      city: '',
      deliveryDate: '',
      items: [emptyItem()]
    });
    onCreated();
    navigate('/orders');
  };

  return (
    <section className="card">
      <h2>Create order</h2>
      <form onSubmit={handleSubmit} className="form-grid">
        <label>
          Customer name
          <input
            value={formData.customerName}
            onChange={(event) => setFormData({ ...formData, customerName: event.target.value })}
            required
          />
        </label>
        <label>
          Address line 1
          <input
            value={formData.addressLine1}
            onChange={(event) => setFormData({ ...formData, addressLine1: event.target.value })}
            required
          />
        </label>
        <label>
          Postcode
          <input
            value={formData.postcode}
            onChange={(event) => setFormData({ ...formData, postcode: event.target.value })}
            required
          />
        </label>
        <label>
          City
          <input
            value={formData.city}
            onChange={(event) => setFormData({ ...formData, city: event.target.value })}
            required
          />
        </label>
        <label>
          Delivery date
          <input
            type="date"
            value={formData.deliveryDate ? formData.deliveryDate.split('/').reverse().join('-') : ''}
            onChange={(event) => {
              const selectedDate = event.target.value;
              const formattedDate = formatDateForDisplay(selectedDate);
              setFormData({ ...formData, deliveryDate: formattedDate });
              setDateError(validateDeliveryDate(formattedDate));
            }}
            required
          />
          {dateError ? <span className="field-hint error">{dateError}</span> : null}
        </label>

        <div className="items-section">
          <div className="items-header">
            <h3>Items</h3>
            <button type="button" onClick={addItemRow}>Add item</button>
          </div>
          {formData.items.map((item, index) => (
            <div className="item-row" key={`${item.productSku}-${index}`}>
              <label>
                Product
                <select
                  value={item.productSku}
                  onChange={(event) => updateItem(index, 'productSku', event.target.value)}
                  required
                >
                  <option value="">Select a product</option>
                  {getAvailableProductsForRow(index).map((product) => (
                    <option key={product.sku} value={product.sku}>
                      {product.name}
                    </option>
                  ))}
                </select>
              </label>
              <label>
                Quantity
                <input
                  type="number"
                  min="1"
                  value={item.quantity}
                  onChange={(event) => updateItem(index, 'quantity', event.target.value)}
                  required
                />
              </label>
              <label>
                Item total (£)
                <input
                  type="number"
                  min="0.01"
                  step="0.01"
                  value={item.itemTotal}
                  onChange={(event) => updateItem(index, 'itemTotal', event.target.value)}
                  required
                />
              </label>
              {formData.items.length > 1 && (
                <button type="button" className="remove-button" onClick={() => removeItemRow(index)}>
                  Remove
                </button>
              )}
            </div>
          ))}
        </div>

        <div className="summary">
          <strong>Total:</strong> £{Number(total).toFixed(2)}
        </div>

        {errors ? <p className="error">{errors}</p> : null}
        {success ? <p className="success">{success}</p> : null}

        <button type="submit">Create order</button>
      </form>
    </section>
  );
}