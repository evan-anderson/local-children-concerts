import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { ConcertList } from './ConcertList';
import type { Concert } from '../types/concert';

const mockConcerts: Concert[] = [
  {
    title: 'Concert One',
    venue: 'Venue A',
    town: 'Boston',
    date: '2025-06-15T14:00:00',
    scraped_at: '2025-01-01T00:00:00',
  },
  {
    title: 'Concert Two',
    venue: 'Venue B',
    town: 'Cambridge',
    date: '2025-06-16T14:00:00',
    scraped_at: '2025-01-01T00:00:00',
  },
];

describe('ConcertList', () => {
  it('renders loading state', () => {
    render(<ConcertList concerts={[]} isLoading={true} error={null} />);
    expect(screen.getByText('Loading concerts...')).toBeInTheDocument();
  });

  it('renders error state', () => {
    const error = new Error('Failed to fetch');
    render(<ConcertList concerts={[]} isLoading={false} error={error} />);
    expect(screen.getByText('Error: Failed to fetch')).toBeInTheDocument();
  });

  it('renders empty state when no concerts', () => {
    render(<ConcertList concerts={[]} isLoading={false} error={null} />);
    expect(screen.getByText('No concerts found. Try adjusting your filters.')).toBeInTheDocument();
  });

  it('renders list of concerts', () => {
    render(<ConcertList concerts={mockConcerts} isLoading={false} error={null} />);
    expect(screen.getByText('Concert One')).toBeInTheDocument();
    expect(screen.getByText('Concert Two')).toBeInTheDocument();
  });

  it('renders correct number of concert cards', () => {
    render(<ConcertList concerts={mockConcerts} isLoading={false} error={null} />);
    const cards = screen.getAllByText(/Venue/);
    expect(cards).toHaveLength(2);
  });
});
