import React from 'react';
import './StatCard.css';

const StatCard = ({ icon, title, value, subtitle, accentColor = '#f5c518' }) => {
  return (
    <div className="stat-card" style={{ '--accent-color': accentColor }}>
      <div className="stat-icon-wrapper">
        {icon}
      </div>
      <h3 className="stat-title">{title}</h3>
      <div className="stat-value">{value}</div>
      {subtitle && <p className="stat-subtitle">{subtitle}</p>}
    </div>
  );
};

export default StatCard;
