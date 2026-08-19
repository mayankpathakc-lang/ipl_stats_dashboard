import { useState, useEffect, useCallback, useRef } from 'react';
import { fetchPlayers, fetchFilters, fetchSummary } from '../utils/api';

export const usePlayers = () => {
  const [players, setPlayers] = useState([]);
  const [totalItems, setTotalItems] = useState(0);
  const [totalPages, setTotalPages] = useState(0);
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize] = useState(10);
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  const [filters, setFilters] = useState({ seasons: [], roles: [], teams: [] });
  const [selectedSeason, setSelectedSeason] = useState('');
  const [selectedRole, setSelectedRole] = useState('');
  const [selectedTeam, setSelectedTeam] = useState('');
  
  const [searchQuery, setSearchQuery] = useState('');
  const [debouncedSearchQuery, setDebouncedSearchQuery] = useState('');
  
  const [sortBy, setSortBy] = useState('runs');
  const [sortOrder, setSortOrder] = useState('desc');
  
  const [summary, setSummary] = useState(null);

  const debounceTimer = useRef(null);

  useEffect(() => {
    if (debounceTimer.current) {
      clearTimeout(debounceTimer.current);
    }
    debounceTimer.current = setTimeout(() => {
      setDebouncedSearchQuery(searchQuery);
    }, 300);
    return () => clearTimeout(debounceTimer.current);
  }, [searchQuery]);

  useEffect(() => {
    const loadFilters = async () => {
      try {
        const data = await fetchFilters();
        setFilters(data);
      } catch (err) {
        console.error("Failed to load filters", err);
      }
    };
    loadFilters();
  }, []);

  useEffect(() => {
    const loadSummary = async () => {
      try {
        const data = await fetchSummary({
          season: selectedSeason ? parseInt(selectedSeason, 10) : undefined,
          role: selectedRole || undefined,
          team: selectedTeam || undefined,
        });
        setSummary(data);
      } catch (err) {
        console.error("Failed to load summary", err);
      }
    };
    loadSummary();
  }, [selectedSeason, selectedRole, selectedTeam]);

  useEffect(() => {
    const loadPlayers = async () => {
      setLoading(true);
      setError(null);
      try {
        const data = await fetchPlayers({
          search: debouncedSearchQuery || undefined,
          season: selectedSeason ? parseInt(selectedSeason, 10) : undefined,
          role: selectedRole || undefined,
          team: selectedTeam || undefined,
          sort_by: sortBy,
          sort_order: sortOrder,
          page: currentPage,
          page_size: pageSize,
        });
        
        if (Array.isArray(data)) {
          setPlayers(data);
        } else {
          setPlayers(data.data || data.players || []);
          setTotalItems(data.total || data.total_items || 0);
          setTotalPages(data.total_pages || 1);
        }
      } catch (err) {
        console.error("Failed to load players", err);
        setError("Unable to load player statistics. Please check connection and try again.");
      } finally {
        setLoading(false);
      }
    };
    loadPlayers();
  }, [debouncedSearchQuery, selectedSeason, selectedRole, selectedTeam, sortBy, sortOrder, currentPage, pageSize]);

  const handleSort = useCallback((column) => {
    if (sortBy === column) {
      setSortOrder(prev => (prev === 'asc' ? 'desc' : 'asc'));
    } else {
      setSortBy(column);
      setSortOrder('desc');
    }
  }, [sortBy]);

  const resetFilters = useCallback(() => {
    setSelectedSeason('');
    setSelectedRole('');
    setSelectedTeam('');
    setSearchQuery('');
    setSortBy('runs');
    setSortOrder('desc');
    setCurrentPage(1);
  }, []);

  // Reset to first page on filter changes (excluding page changes themselves)
  useEffect(() => {
    setCurrentPage(1);
  }, [debouncedSearchQuery, selectedSeason, selectedRole, selectedTeam, sortBy, sortOrder]);

  return {
    players,
    totalItems,
    totalPages,
    currentPage,
    pageSize,
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
    setSortBy,
    setSortOrder,
    setCurrentPage,
    handleSort,
    resetFilters,
  };
};

export default usePlayers;
