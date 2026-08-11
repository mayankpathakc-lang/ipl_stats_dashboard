import { Trophy, AlertCircle, Zap, Target, TrendingUp, Swords } from 'lucide-react'
import './App.css'
import SearchBar from './components/SearchBar'
import FilterPanel from './components/FilterPanel'
import StatCard from './components/StatCard'
import PlayerTable from './components/PlayerTable'
import Pagination from './components/Pagination'
import { usePlayers } from './hooks/usePlayers'

function App() {
  const {
    players,
    totalItems,
    totalPages,
    currentPage,
    loading,
    error,
    filters,
    selectedSeason,
    selectedRole,
    selectedTeam,
    searchQuery,
    sortBy,
    sortOrder,
    summary,
    setSearchQuery,
    setSelectedSeason,
    setSelectedRole,
    setSelectedTeam,
    setCurrentPage,
    handleSort,
  } = usePlayers()

  return (
    <div className="app">
      {/* Header */}
      <header className="app-header">
        <div className="header-content">
          <div className="header-icon">
            <Trophy size={24} />
          </div>
          <div className="header-text">
            <h1>IPL <span>Stats</span> Dashboard</h1>
            <p>Aggregated player performance metrics across seasons</p>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="app-main">
        {/* Controls */}
        <div className="controls-bar">
          <div className="search-wrapper">
            <SearchBar
              value={searchQuery}
              onChange={setSearchQuery}
            />
          </div>
          <FilterPanel
            seasons={filters.seasons}
            roles={filters.roles}
            teams={filters.teams}
            selectedSeason={selectedSeason}
            selectedRole={selectedRole}
            selectedTeam={selectedTeam}
            onSeasonChange={setSelectedSeason}
            onRoleChange={setSelectedRole}
            onTeamChange={setSelectedTeam}
          />
        </div>

        {/* Summary Cards */}
        {summary && (
          <div className="summary-cards">
            <StatCard
              icon={<TrendingUp size={20} />}
              title="Top Scorer"
              value={summary.highest_runs}
              subtitle={summary.highest_runs_player || '—'}
              accentColor="#f5c518"
            />
            <StatCard
              icon={<Target size={20} />}
              title="Top Wicket-Taker"
              value={summary.highest_wickets}
              subtitle={summary.highest_wickets_player || '—'}
              accentColor="#4ade80"
            />
            <StatCard
              icon={<Zap size={20} />}
              title="Best Strike Rate"
              value={summary.best_strike_rate?.toFixed(1)}
              subtitle={summary.best_strike_rate_player || '—'}
              accentColor="#7c3aed"
            />
            <StatCard
              icon={<Swords size={20} />}
              title="Best Death Economy"
              value={summary.best_death_economy?.toFixed(2)}
              subtitle={summary.best_death_economy_player || '—'}
              accentColor="#60a5fa"
            />
          </div>
        )}

        {/* Error Banner */}
        {error && (
          <div className="error-banner">
            <AlertCircle size={18} />
            {error}
          </div>
        )}

        {/* Player Table */}
        <div className="table-section">
          <div className="table-header">
            <h2>Player Statistics</h2>
            <span className="result-count">
              {totalItems} player{totalItems !== 1 ? 's' : ''} found
            </span>
          </div>
          <div className="table-body">
            <PlayerTable
              players={players}
              sortBy={sortBy}
              sortOrder={sortOrder}
              onSort={handleSort}
              loading={loading}
            />
          </div>
          {totalPages > 1 && (
            <div className="pagination-wrapper">
              <Pagination
                currentPage={currentPage}
                totalPages={totalPages}
                onPageChange={setCurrentPage}
              />
            </div>
          )}
        </div>
      </main>

      {/* Footer */}
      <footer className="app-footer">
        <p>IPL Stats Dashboard &mdash; Built with FastAPI &amp; React</p>
      </footer>
    </div>
  )
}

export default App
