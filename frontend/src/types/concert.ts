export interface Concert {
  title: string;
  venue: string;
  town: string;
  date: string;
  url?: string;
  description?: string;
  address?: string;
  source?: string;
  scraped_at: string;
}

export interface ConcertsResponse {
  concerts: Concert[];
  total: number;
}

export interface ConcertFilters {
  towns: string[];
  startDate: string | null;
  endDate: string | null;
}
