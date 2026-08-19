import React from 'react';
import { ChevronUp, ChevronDown, ArrowUpDown, SearchX } from 'lucide-react';
import './PlayerTable.css';

const PlayerTable = ({ 
  players = [], 
  sortBy, 
  sortOrder, 
  onSort, 
  loading,
  onResetFilters 
}) => {
  const columns = [
    { key: 'player_name', label: 'Player' },
    { key: 'team', label: 'Team' },
    { key: 'role', label: 'Role' },
    { key: 'matches', label: 'Mat' },
    { key: 'runs', label: 'Runs' },
    { key: 'batting_strike_rate', label: 'SR', tooltip: 'Overall Strike Rate' },
    { key: 'powerplay_strike_rate', label: 'PP SR', tooltip: 'Powerplay (Overs 1-6) Strike Rate' },
    { key: 'middle_strike_rate', label: 'Mid SR', tooltip: 'Middle Overs (7-15) Strike Rate' },
    { key: 'death_strike_rate', label: 'Death SR', tooltip: 'Death Overs (16-20) Strike Rate' },
    { key: 'wickets', label: 'Wkts' },
    { key: 'bowling_economy', label: 'Econ', tooltip: 'Overall Bowling Economy' },
    { key: 'death_over_economy', label: 'Death Econ', tooltip: 'Death Overs (16-20) Economy' }
  ];

  const renderSortIcon = (key) => {
    if (sortBy !== key) return <ArrowUpDown size={13} className="sort-icon inactive" />;
    return sortOrder === 'asc' ? 
      <ChevronUp size={14} className="sort-icon active" /> : 
      <ChevronDown size={14} className="sort-icon active" />;
  };

  const getRoleBadgeClass = (role) => {
    const r = (role || '').toLowerCase();
    if (r.includes('batsman')) return 'badge-batsman';
    if (r.includes('bowler')) return 'badge-bowler';
    if (r.includes('all-rounder') || r.includes('all rounder')) return 'badge-allrounder';
    if (r.includes('keeper')) return 'badge-keeper';
    return 'badge-default';
  };

  const getTeamBadgeClass = (team) => {
    const t = (team || '').toUpperCase();
    return `badge-team team-${t.toLowerCase()}`;
  };

  const renderSkeleton = () => {
    return Array(8).fill(0).map((_, idx) => (
      <tr key={`skeleton-${idx}`} className="skeleton-row">
        {columns.map((col, colIdx) => (
          <td key={`skel-td-${colIdx}`}>
            <div className="skeleton-cell"></div>
          </td>
        ))}
      </tr>
    ));
  };

  return (
    <div className="table-container">
      <div className="table-scroll-wrapper">
        <table className="player-table">
          <thead>
            <tr>
              {columns.map((col) => (
                <th 
                  key={col.key} 
                  onClick={() => onSort(col.key)}
                  className={`sortable-header ${sortBy === col.key ? 'active-sort-th' : ''}`}
                  title={col.tooltip || `Sort by ${col.label}`}
                >
                  <div className="header-content">
                    <span>{col.label}</span>
                    {renderSortIcon(col.key)}
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {loading ? (
              renderSkeleton()
            ) : players.length === 0 ? (
              <tr>
                <td colSpan={columns.length} className="empty-state-cell">
                  <div className="empty-state-content">
                    <SearchX size={36} className="empty-state-icon" />
                    <h4>No players match your search</h4>
                    <p>Try adjusting your search keywords, season, role, or team filters.</p>
                    {onResetFilters && (
                      <button 
                        type="button" 
                        className="empty-reset-btn" 
                        onClick={onResetFilters}
                      >
                        Clear all filters
                      </button>
                    )}
                  </div>
                </td>
              </tr>
            ) : (
              players.map((player, index) => (
                <tr key={`${player.player_id}-${player.season || index}`}>
                  <td className="player-name-cell">
                    <div className="player-name-wrapper">
                      <span className="player-name-text">{player.player_name}</span>
                      {player.season && <span className="player-season-tag">'{String(player.season).slice(-2)}</span>}
                    </div>
                  </td>
                  <td>
                    <span className={getTeamBadgeClass(player.team)}>{player.team}</span>
                  </td>
                  <td>
                    <span className={`role-badge ${getRoleBadgeClass(player.role)}`}>{player.role}</span>
                  </td>
                  <td>{player.matches}</td>
                  <td className="stat-highlight runs-stat">{player.runs}</td>
                  <td className={`sr-stat ${player.batting_strike_rate >= 160 ? 'high-sr' : ''}`}>
                    {player.batting_strike_rate > 0 ? player.batting_strike_rate.toFixed(1) : '—'}
                  </td>
                  <td>{player.powerplay_strike_rate > 0 ? player.powerplay_strike_rate.toFixed(1) : '—'}</td>
                  <td>{player.middle_strike_rate > 0 ? player.middle_strike_rate.toFixed(1) : '—'}</td>
                  <td className={`death-sr-stat ${player.death_strike_rate >= 190 ? 'elite-sr' : ''}`}>
                    {player.death_strike_rate > 0 ? player.death_strike_rate.toFixed(1) : '—'}
                  </td>
                  <td className="stat-highlight wkts-stat">{player.wickets}</td>
                  <td>{player.bowling_economy > 0 ? player.bowling_economy.toFixed(2) : '—'}</td>
                  <td className={`econ-stat ${player.death_over_economy > 0 && player.death_over_economy <= 8.5 ? 'elite-econ' : ''}`}>
                    {player.death_over_economy > 0 ? player.death_over_economy.toFixed(2) : '—'}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default PlayerTable;
