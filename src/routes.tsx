import React from 'react';
import { createBrowserRouter } from 'react-router-dom';
import Layout from './components/layout/Layout';
import HomePage from './pages/HomePage';
import ProductDetailPage from './pages/ProductDetailPage';
import CartPage from './pages/CartPage';
import CheckoutPage from './pages/CheckoutPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import AccountPage from './pages/AccountPage';
import OrdersPage from './pages/OrdersPage';
import NotFoundPage from './pages/NotFoundPage';
import PaymentPage from './pages/PaymentPage';
import AdminLoginPage from './pages/AdminLoginPage';
import AdminDashboardPage from './pages/AdminDashboardPage';
import SellerLoginPage from './pages/seller/SellerLoginPage';
import SellerRegisterPage from './pages/seller/SellerRegisterPage';
import SellerDashboardPage from './pages/seller/SellerDashboardPage';
import SellerProductsPage from './pages/seller/SellerProductsPage';
import SellerProductCreatePage from './pages/seller/SellerProductCreatePage';
import SellerProductDetailPage from './pages/seller/SellerProductDetailPage';
import SellerProductUpdatePage from './pages/seller/SellerProductUpdatePage';
import SellerOrdersPage from './pages/seller/SellerOrdersPage';
import SellerAnalyticsPage from './pages/seller/SellerAnalyticsPage';
import SellerProfilePage from './pages/seller/SellerProfilePage';

export const router = createBrowserRouter([
  {
    path: '/',
    element: <Layout />,
    children: [
      { index: true, element: <HomePage /> },
      { path: 'product/:id', element: <ProductDetailPage /> },
      { path: 'cart', element: <CartPage /> },
      { path: 'checkout', element: <CheckoutPage /> },
      { path: 'payment', element: <PaymentPage /> },
      { path: 'login', element: <LoginPage /> },
      { path: 'register', element: <RegisterPage /> },
      { path: 'account', element: <AccountPage /> },
      { path: 'orders', element: <OrdersPage /> },
      { path: 'admin/login', element: <AdminLoginPage /> },
      { path: 'admin/dashboard', element: <AdminDashboardPage /> },
      { path: 'seller/login', element: <SellerLoginPage /> },
      { path: 'seller/register', element: <SellerRegisterPage /> },
      { path: 'seller/dashboard', element: <SellerDashboardPage /> },
      { path: 'seller/products', element: <SellerProductsPage /> },
      { path: 'seller/products/create', element: <SellerProductCreatePage /> },
      { path: 'seller/products/:id', element: <SellerProductDetailPage /> },
      { path: 'seller/products/:id/edit', element: <SellerProductUpdatePage /> },
      { path: 'seller/orders', element: <SellerOrdersPage /> },
      { path: 'seller/analytics', element: <SellerAnalyticsPage /> },
      { path: 'seller/profile', element: <SellerProfilePage /> },
      { path: '*', element: <NotFoundPage /> },
    ],
  },
]);
