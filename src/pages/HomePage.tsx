import React from 'react';
import HeroBanner from '../components/home/HeroBanner';
import CategoryCards from '../components/home/CategoryCards';
import ProductGrid from '../components/home/ProductGrid';

const HomePage: React.FC = () => {
  return (
    <div>
      <HeroBanner />
      
      <div className="container-custom py-4">
        <CategoryCards />
        
        <ProductGrid 
          title="Today's Deals" 
          viewAllLink="/deals" 
          limit={6}
        />
        
        <div className="bg-white rounded-lg shadow-sm p-4 my-6">
          <h2 className="text-xl font-bold mb-4">Top Sellers in Books</h2>
          
          <ProductGrid 
            title="Best Sellers" 
            viewAllLink="/category/books/best-sellers" 
            limit={6}
          />
        </div>
        
        <div className="bg-amazon-blue-light rounded-lg p-6 my-6 text-white">
          <div className="flex flex-col md:flex-row items-center justify-between">
            <div className="mb-4 md:mb-0 md:mr-8">
              <h2 className="text-2xl font-bold mb-2">Become an Amazon Prime Member</h2>
              <p className="text-gray-300 mb-4">Fast, FREE Delivery on over 100 million items</p>
              <button className="bg-amazon-yellow hover:bg-amazon-yellow-hover text-black font-medium py-2 px-6 rounded">
                Try Prime FREE for 30 days
              </button>
            </div>
            <img 
              src="https://images.pexels.com/photos/4391470/pexels-photo-4391470.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2" 
              alt="Amazon Prime" 
              className="w-full md:w-1/3 h-40 object-cover rounded"
            />
          </div>
        </div>
        
        <ProductGrid 
          title="Recommended for You" 
          viewAllLink="/recommendations" 
          limit={12}
        />
      </div>
    </div>
  );
};

export default HomePage;