import { useState } from 'react';
import { useConcerts, useTowns } from './hooks/useConcerts';
import { ConcertList } from './components/ConcertList';
import { TownFilter } from './components/TownFilter';
import { DateRangeFilter } from './components/DateRangeFilter';
import './App.css';

function formatRelativeTime(dateString: string | null): string {
  if (!dateString) return '';
  const date = new Date(dateString);
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
  const diffDays = Math.floor(diffHours / 24);

  if (diffDays > 0) {
    return `${diffDays} day${diffDays !== 1 ? 's' : ''} ago`;
  } else if (diffHours > 0) {
    return `${diffHours} hour${diffHours !== 1 ? 's' : ''} ago`;
  } else {
    return 'just now';
  }
}

function App() {
  const [selectedTowns, setSelectedTowns] = useState<string[]>([]);
  const [startDate, setStartDate] = useState<string | null>(null);
  const [endDate, setEndDate] = useState<string | null>(null);

  const { towns } = useTowns();
  const { concerts, lastUpdated, isLoading, error } = useConcerts({
    towns: selectedTowns,
    startDate,
    endDate,
  });

  return (
    <div className="app">
      <header>
        <h1>Kids Concert Finder</h1>
        <p>Discover child-friendly concerts in the Boston metro area</p>
        {lastUpdated && (
          <p className="last-updated">Data updated {formatRelativeTime(lastUpdated)}</p>
        )}
      </header>

      <div className="filters">
        <TownFilter
          availableTowns={towns}
          selectedTowns={selectedTowns}
          onChange={setSelectedTowns}
        />
        <DateRangeFilter
          startDate={startDate}
          endDate={endDate}
          onStartDateChange={setStartDate}
          onEndDateChange={setEndDate}
        />
      </div>

      <main>
        <p className="results-count">
          {!isLoading && `Showing ${concerts.length} concert${concerts.length !== 1 ? 's' : ''}`}
        </p>
        <ConcertList concerts={concerts} isLoading={isLoading} error={error} />
      </main>
    </div>
  );
}

export default App;
