import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Header from './components/layout/Header';
import Footer from './components/layout/Footer';
import HomePage from './pages/HomePage';
import ProductDetailPage from './pages/ProductDetailPage';
import CartPage from './pages/CartPage';
import CheckoutPage from './pages/CheckoutPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import AccountPage from './pages/AccountPage';
import OrdersPage from './pages/OrdersPage';
import NotFoundPage from './pages/NotFoundPage';
import SellerLoginPage from './pages/seller/SellerLoginPage';
import SellerRegisterPage from './pages/seller/SellerRegisterPage';
import SellerDashboardPage from './pages/seller/SellerDashboardPage';
import AdminLoginPage from './pages/AdminLoginPage';
import AdminDashboardPage from './pages/AdminDashboardPage';
import SellerProfilePage from './pages/seller/SellerProfilePage';
import SellerProductsPage from './pages/seller/SellerProductsPage';
import SellerProductCreatePage from './pages/seller/SellerProductCreatePage';
import SellerProductDetailPage from './pages/seller/SellerProductDetailPage';
import SellerProductUpdatePage from './pages/seller/SellerProductUpdatePage';
import SellerOrdersPage from './pages/seller/SellerOrdersPage';
import SellerAnalyticsPage from './pages/seller/SellerAnalyticsPage';

const AppRoutes = () => (
  <Routes>
    {/* Seller routes */}
    <Route path="/seller/login" element={<SellerLoginPage />} />
    <Route path="/seller/register" element={<SellerRegisterPage />} />
    <Route path="/seller/dashboard" element={<SellerDashboardPage />} />
    <Route path="/seller/profile" element={<SellerProfilePage />} />
    <Route path="/seller/products" element={<SellerProductsPage />} />
    <Route path="/seller/products/create" element={<SellerProductCreatePage />} />
    <Route path="/seller/products/:productId" element={<SellerProductDetailPage />} />
    <Route path="/seller/products/:productId/update" element={<SellerProductUpdatePage />} />
    {/* Delete can be handled as a button/action in detail/update page, but route for completeness */}
    <Route path="/seller/products/:productId/delete" element={<SellerProductDetailPage />} />
    <Route path="/seller/orders" element={<SellerOrdersPage />} />
    <Route path="/seller/analytics" element={<SellerAnalyticsPage />} />

    {/* Admin routes */}
    <Route path="/admin/login" element={<AdminLoginPage />} />
    <Route path="/admin/dashboard" element={<AdminDashboardPage />} />

    {/* Main routes with layout */}
    <Route path="/*" element={
      <div className="flex flex-col min-h-screen">
        <Header />
        <main className="flex-grow">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/product/:id" element={<ProductDetailPage />} />
            <Route path="/cart" element={<CartPage />} />
            <Route path="/checkout" element={<CheckoutPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/account" element={<AccountPage />} />
            <Route path="/orders" element={<OrdersPage />} />
            <Route path="*" element={<NotFoundPage />} />
          </Routes>
        </main>
        <Footer />
      </div>
    } />
  </Routes>
);

export default AppRoutes;
