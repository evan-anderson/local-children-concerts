import { useState, useEffect, useMemo } from 'react';
import type { Concert, ConcertsResponse, ConcertFilters } from '../types/concert';

export function useConcerts(filters: ConcertFilters) {
  const [concerts, setConcerts] = useState<Concert[]>([]);
  const [lastUpdated, setLastUpdated] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  // Stable serialization of towns array for dependency tracking
  const townsKey = useMemo(() => JSON.stringify(filters.towns), [filters.towns]);

  useEffect(() => {
    setIsLoading(true);

    const params = new URLSearchParams();
    filters.towns.forEach(t => params.append('towns', t));
    if (filters.startDate) params.set('start_date', filters.startDate);
    if (filters.endDate) params.set('end_date', filters.endDate);

    fetch(`/api/concerts?${params}`)
      .then(res => {
        if (!res.ok) throw new Error('Failed to fetch concerts');
        return res.json();
      })
      .then((data: ConcertsResponse) => {
        setConcerts(data.concerts);
        setLastUpdated(data.last_updated);
        setError(null);
      })
      .catch(err => setError(err))
      .finally(() => setIsLoading(false));
  }, [townsKey, filters.startDate, filters.endDate]);

  return { concerts, lastUpdated, isLoading, error };
}

export function useTowns() {
  const [towns, setTowns] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetch('/api/towns')
      .then(res => res.json())
      .then(setTowns)
      .finally(() => setIsLoading(false));
  }, []);

  return { towns, isLoading };
}
