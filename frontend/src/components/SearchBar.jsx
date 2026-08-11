import React from 'react';
import { Search } from 'lucide-react';
import './SearchBar.css';

const SearchBar = ({ value, onChange }) => {
  return (
    <div className="search-container">
      <Search className="search-icon" size={20} />
      <input
        type="text"
        className="search-input"
        placeholder="Search players..."
        value={value}
        onChange={onChange}
      />
    </div>
  );
};

export default SearchBar;
