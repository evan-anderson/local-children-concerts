import type { Concert } from '../types/concert';

interface ConcertCardProps {
  concert: Concert;
}

export function ConcertCard({ concert }: ConcertCardProps) {
  const formattedDate = new Date(concert.date).toLocaleDateString('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
  });

  return (
    <div className="concert-card">
      <h3>{concert.title}</h3>
      <p className="date">{formattedDate}</p>
      <p className="venue">
        {concert.venue} &bull; {concert.town}
      </p>
      {concert.description && (
        <p className="description">{concert.description}</p>
      )}
      {concert.url && (
        <a href={concert.url} target="_blank" rel="noopener noreferrer" className="link">
          More Info &rarr;
        </a>
      )}
    </div>
  );
}
