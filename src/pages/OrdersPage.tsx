import React from 'react';

const OrdersPage = () => {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">My Orders</h1>
      <div className="space-y-4">
        {/* Example order - In a real app, this would map over actual orders */}
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-sm text-gray-600">Order #12345</p>
              <p className="text-sm text-gray-600">Placed on March 15, 2024</p>
              <div className="mt-4">
                <h3 className="font-semibold">Items:</h3>
                <ul className="mt-2 space-y-2">
                  <li className="flex items-center">
                    <span className="text-gray-800">Product Name x 1</span>
                    <span className="ml-4 text-gray-600">$99.99</span>
                  </li>
                </ul>
              </div>
            </div>
            <div className="text-right">
              <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800">
                Delivered
              </span>
              <p className="mt-2 text-lg font-semibold">Total: $99.99</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default OrdersPage;