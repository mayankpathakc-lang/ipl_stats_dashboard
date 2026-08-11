import React from 'react';
import { ChevronUp, ChevronDown, ArrowUpDown } from 'lucide-react';
import './PlayerTable.css';

const PlayerTable = ({ players = [], sortBy, sortOrder, onSort, loading }) => {
  const columns = [
    { key: 'player_name', label: 'Player Name' },
    { key: 'team', label: 'Team' },
    { key: 'role', label: 'Role' },
    { key: 'matches', label: 'Mat' },
    { key: 'runs', label: 'Runs' },
    { key: 'batting_strike_rate', label: 'SR' },
    { key: 'powerplay_strike_rate', label: 'PP SR' },
    { key: 'middle_strike_rate', label: 'Mid SR' },
    { key: 'death_strike_rate', label: 'Death SR' },
    { key: 'wickets', label: 'Wkts' },
    { key: 'bowling_economy', label: 'Econ' },
    { key: 'death_over_economy', label: 'Death Econ' }
  ];

  const renderSortIcon = (key) => {
    if (sortBy !== key) return <ArrowUpDown size={14} className="sort-icon inactive" />;
    return sortOrder === 'asc' ? 
      <ChevronUp size={14} className="sort-icon active" /> : 
      <ChevronDown size={14} className="sort-icon active" />;
  };

  const renderSkeleton = () => {
    return Array(5).fill(0).map((_, idx) => (
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
                  className="sortable-header"
                >
                  <div className="header-content">
                    {col.label}
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
                <td colSpan={columns.length} className="empty-state">
                  No players found
                </td>
              </tr>
            ) : (
              players.map((player, index) => (
                <tr key={player.player_id || index}>
                  <td className="player-name">{player.player_name}</td>
                  <td>{player.team}</td>
                  <td>{player.role}</td>
                  <td>{player.matches}</td>
                  <td className="stat-highlight">{player.runs}</td>
                  <td>{player.batting_strike_rate}</td>
                  <td>{player.powerplay_strike_rate}</td>
                  <td>{player.middle_strike_rate}</td>
                  <td>{player.death_strike_rate}</td>
                  <td className="stat-highlight">{player.wickets}</td>
                  <td>{player.bowling_economy}</td>
                  <td>{player.death_over_economy}</td>
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
