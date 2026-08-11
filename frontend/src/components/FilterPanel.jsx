import React from 'react';
import { Calendar, User, Shield } from 'lucide-react';
import './FilterPanel.css';

const FilterPanel = ({
  seasons = [],
  roles = [],
  teams = [],
  selectedSeason,
  selectedRole,
  selectedTeam,
  onSeasonChange,
  onRoleChange,
  onTeamChange
}) => {
  return (
    <div className="filter-panel">
      <div className="filter-group">
        <Calendar className="filter-icon" size={18} />
        <select value={selectedSeason} onChange={onSeasonChange} className="filter-select">
          <option value="">All Seasons</option>
          {seasons.map(season => (
            <option key={season} value={season}>{season}</option>
          ))}
        </select>
      </div>
      
      <div className="filter-group">
        <User className="filter-icon" size={18} />
        <select value={selectedRole} onChange={onRoleChange} className="filter-select">
          <option value="">All Roles</option>
          {roles.map(role => (
            <option key={role} value={role}>{role}</option>
          ))}
        </select>
      </div>

      <div className="filter-group">
        <Shield className="filter-icon" size={18} />
        <select value={selectedTeam} onChange={onTeamChange} className="filter-select">
          <option value="">All Teams</option>
          {teams.map(team => (
            <option key={team} value={team}>{team}</option>
          ))}
        </select>
      </div>
    </div>
  );
};

export default FilterPanel;
