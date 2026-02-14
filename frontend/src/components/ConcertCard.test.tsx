import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { ConcertCard } from './ConcertCard';
import type { Concert } from '../types/concert';

const mockConcert: Concert = {
  title: 'Kids Rock Concert',
  venue: 'Symphony Hall',
  town: 'Boston',
  date: '2025-06-15T14:00:00',
  url: 'https://example.com/concert',
  description: 'A fun concert for the whole family',
  scraped_at: '2025-01-01T00:00:00',
};

describe('ConcertCard', () => {
  it('renders concert title', () => {
    render(<ConcertCard concert={mockConcert} />);
    expect(screen.getByText('Kids Rock Concert')).toBeInTheDocument();
  });

  it('renders venue and town', () => {
    render(<ConcertCard concert={mockConcert} />);
    expect(screen.getByText(/Symphony Hall/)).toBeInTheDocument();
    expect(screen.getByText(/Boston/)).toBeInTheDocument();
  });

  it('renders description when provided', () => {
    render(<ConcertCard concert={mockConcert} />);
    expect(screen.getByText('A fun concert for the whole family')).toBeInTheDocument();
  });

  it('renders link when URL is provided', () => {
    render(<ConcertCard concert={mockConcert} />);
    const link = screen.getByRole('link', { name: /more info/i });
    expect(link).toHaveAttribute('href', 'https://example.com/concert');
  });

  it('does not render link when URL is not provided', () => {
    const concertWithoutUrl = { ...mockConcert, url: undefined };
    render(<ConcertCard concert={concertWithoutUrl} />);
    expect(screen.queryByRole('link')).not.toBeInTheDocument();
  });

  it('does not render description when not provided', () => {
    const concertWithoutDesc = { ...mockConcert, description: undefined };
    render(<ConcertCard concert={concertWithoutDesc} />);
    expect(screen.queryByText('A fun concert for the whole family')).not.toBeInTheDocument();
  });
});
