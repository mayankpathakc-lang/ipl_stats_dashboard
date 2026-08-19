import React from 'react';
import { Calendar, User, Shield, RotateCcw } from 'lucide-react';
import './FilterPanel.css';

const FilterPanel = ({
  seasons = [],
  roles = [],
  teams = [],
  selectedSeason = '',
  selectedRole = '',
  selectedTeam = '',
  onSeasonChange,
  onRoleChange,
  onTeamChange,
  onResetFilters
}) => {
  const hasActiveFilters = Boolean(selectedSeason || selectedRole || selectedTeam);

  return (
    <div className="filter-panel">
      <div className="filter-group">
        <Calendar className="filter-icon" size={18} />
        <select 
          value={selectedSeason} 
          onChange={(e) => onSeasonChange(e.target.value)} 
          className="filter-select"
          aria-label="Filter by season"
        >
          <option value="">All Seasons</option>
          {seasons.map(season => (
            <option key={season} value={season}>{season}</option>
          ))}
        </select>
      </div>
      
      <div className="filter-group">
        <User className="filter-icon" size={18} />
        <select 
          value={selectedRole} 
          onChange={(e) => onRoleChange(e.target.value)} 
          className="filter-select"
          aria-label="Filter by role"
        >
          <option value="">All Roles</option>
          {roles.map(role => (
            <option key={role} value={role}>{role}</option>
          ))}
        </select>
      </div>

      <div className="filter-group">
        <Shield className="filter-icon" size={18} />
        <select 
          value={selectedTeam} 
          onChange={(e) => onTeamChange(e.target.value)} 
          className="filter-select"
          aria-label="Filter by team"
        >
          <option value="">All Teams</option>
          {teams.map(team => (
            <option key={team} value={team}>{team}</option>
          ))}
        </select>
      </div>

      {hasActiveFilters && onResetFilters && (
        <button 
          className="reset-filters-btn" 
          onClick={onResetFilters}
          type="button"
          title="Reset active filters"
        >
          <RotateCcw size={15} />
          <span>Reset</span>
        </button>
      )}
    </div>
  );
};

export default FilterPanel;
