import React from 'react';
import { Link } from 'react-router-dom';

const Footer: React.FC = () => {
  const scrollToTop = () => {
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  };

  return (
    <footer className="mt-12 bg-amazon-blue-dark text-white">
      {/* Back to top button */}
      <div className="bg-amazon-blue-light text-center py-3 cursor-pointer hover:bg-amazon-blue transition" onClick={scrollToTop}>
        <span className="text-sm">Back to top</span>
      </div>

      {/* Main footer content */}
      <div className="container-custom py-8 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
        <div>
          <h3 className="font-bold mb-3">Get to Know Us</h3>
          <ul className="space-y-2 text-sm text-gray-300">
            <li><Link to="/about" className="hover:text-white hover:underline">About Us</Link></li>
            <li><Link to="/careers" className="hover:text-white hover:underline">Careers</Link></li>
            <li><Link to="/press" className="hover:text-white hover:underline">Press Releases</Link></li>
            <li><Link to="/sustainability" className="hover:text-white hover:underline">Sustainability</Link></li>
          </ul>
        </div>

        <div>
          <h3 className="font-bold mb-3">Make Money with Us</h3>
          <ul className="space-y-2 text-sm text-gray-300">
            <li><Link to="/sell" className="hover:text-white hover:underline">Sell on Amazon</Link></li>
            <li><Link to="/associates" className="hover:text-white hover:underline">Become an Affiliate</Link></li>
            <li><Link to="/fulfillment" className="hover:text-white hover:underline">Fulfillment by Amazon</Link></li>
            <li><Link to="/handmade" className="hover:text-white hover:underline">Handmade</Link></li>
          </ul>
        </div>

        <div>
          <h3 className="font-bold mb-3">Payment Products</h3>
          <ul className="space-y-2 text-sm text-gray-300">
            <li><Link to="/business-card" className="hover:text-white hover:underline">Amazon Business Card</Link></li>
            <li><Link to="/shop-with-points" className="hover:text-white hover:underline">Shop with Points</Link></li>
            <li><Link to="/reload-balance" className="hover:text-white hover:underline">Reload Your Balance</Link></li>
            <li><Link to="/currency-converter" className="hover:text-white hover:underline">Currency Converter</Link></li>
          </ul>
        </div>

        <div>
          <h3 className="font-bold mb-3">Let Us Help You</h3>
          <ul className="space-y-2 text-sm text-gray-300">
            <li><Link to="/help" className="hover:text-white hover:underline">Help Center</Link></li>
            <li><Link to="/shipping" className="hover:text-white hover:underline">Shipping Rates & Policies</Link></li>
            <li><Link to="/returns" className="hover:text-white hover:underline">Returns & Replacements</Link></li>
            <li><Link to="/contact" className="hover:text-white hover:underline">Contact Us</Link></li>
          </ul>
        </div>
      </div>

      {/* Bottom footer */}
      <div className="border-t border-gray-700">
        <div className="container-custom py-6 text-center">
          <Link to="/" className="inline-block mb-4">
            <h2 className="text-2xl font-bold tracking-wide">amazon</h2>
          </Link>
          
          <div className="text-xs text-gray-400 max-w-2xl mx-auto">
            <p className="mb-2">
              This is a demo clone of Amazon for educational purposes only. Not affiliated with Amazon.
            </p>
            <div className="flex flex-wrap justify-center gap-4 mt-4">
              <Link to="/conditions" className="hover:text-white hover:underline">Conditions of Use</Link>
              <Link to="/privacy" className="hover:text-white hover:underline">Privacy Notice</Link>
              <Link to="/cookies" className="hover:text-white hover:underline">Cookies Notice</Link>
              <Link to="/interest-based-ads" className="hover:text-white hover:underline">Interest-Based Ads</Link>
            </div>
            <p className="mt-4">© 2025 Amazon Clone. All rights reserved.</p>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;