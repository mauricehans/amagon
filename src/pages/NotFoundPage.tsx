import React from 'react';
import { Link } from 'react-router-dom';

const NotFoundPage: React.FC = () => {
  return (
    <div className="container-custom py-12 text-center">
      <h1 className="text-2xl font-bold mb-4">Looking for something?</h1>
      <p className="mb-6">We're sorry. The Web address you entered is not a functioning page on our site.</p>
      
      <div className="max-w-md mx-auto bg-white p-6 rounded shadow-sm">
        <h2 className="font-bold mb-4">Here are some helpful links instead:</h2>
        <ul className="space-y-2 mb-6">
          <li>
            <Link to="/" className="text-amazon-teal hover:underline">Home Page</Link>
          </li>
          <li>
            <Link to="/deals" className="text-amazon-teal hover:underline">Today's Deals</Link>
          </li>
          <li>
            <Link to="/account" className="text-amazon-teal hover:underline">Your Account</Link>
          </li>
          <li>
            <Link to="/help" className="text-amazon-teal hover:underline">Customer Service</Link>
          </li>
        </ul>
        
        <Link to="/" className="btn btn-primary">
          Go to Amazon.com Home Page
        </Link>
      </div>
    </div>
  );
};

export default NotFoundPage;