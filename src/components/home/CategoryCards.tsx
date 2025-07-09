import React from 'react';
import { Link } from 'react-router-dom';

interface Category {
  id: string;
  title: string;
  image: string;
  link: string;
}

const categories: Category[] = [
  {
    id: 'electronics',
    title: 'Electronics',
    image: 'https://images.pexels.com/photos/1841841/pexels-photo-1841841.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2',
    link: '/category/electronics'
  },
  {
    id: 'fashion',
    title: 'Fashion',
    image: 'https://images.pexels.com/photos/934070/pexels-photo-934070.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2',
    link: '/category/fashion'
  },
  {
    id: 'home',
    title: 'Home & Kitchen',
    image: 'https://images.pexels.com/photos/1358900/pexels-photo-1358900.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2',
    link: '/category/home'
  },
  {
    id: 'books',
    title: 'Books',
    image: 'https://images.pexels.com/photos/159711/books-bookstore-book-reading-159711.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2',
    link: '/category/books'
  }
];

const CategoryCards: React.FC = () => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 my-6">
      {categories.map((category) => (
        <div key={category.id} className="bg-white p-4 rounded shadow-product">
          <h3 className="font-bold text-lg mb-3">{category.title}</h3>
          
          <Link to={category.link} className="block">
            <div className="relative pb-[60%] overflow-hidden mb-3">
              <img 
                src={category.image} 
                alt={category.title} 
                className="absolute top-0 left-0 w-full h-full object-cover transition-transform hover:scale-105"
              />
            </div>
            
            <span className="text-amazon-teal text-sm hover:underline cursor-pointer">
              Shop now
            </span>
          </Link>
        </div>
      ))}
    </div>
  );
};

export default CategoryCards;