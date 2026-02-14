import type { Concert } from '../types/concert';
import { ConcertCard } from './ConcertCard';

interface ConcertListProps {
  concerts: Concert[];
  isLoading: boolean;
  error: Error | null;
}

export function ConcertList({ concerts, isLoading, error }: ConcertListProps) {
  if (isLoading) {
    return <div className="loading">Loading concerts...</div>;
  }

  if (error) {
    return <div className="error">Error: {error.message}</div>;
  }

  if (concerts.length === 0) {
    return <div className="empty">No concerts found. Try adjusting your filters.</div>;
  }

  return (
    <div className="concert-list">
      {concerts.map((concert, index) => (
        <ConcertCard key={`${concert.title}-${concert.date}-${index}`} concert={concert} />
      ))}
    </div>
  );
}
