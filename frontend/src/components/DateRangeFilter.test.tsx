import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { DateRangeFilter } from './DateRangeFilter';

describe('DateRangeFilter', () => {
  it('renders start and end date inputs', () => {
    render(
      <DateRangeFilter
        startDate={null}
        endDate={null}
        onStartDateChange={() => {}}
        onEndDateChange={() => {}}
      />
    );
    expect(screen.getByPlaceholderText('Start date')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('End date')).toBeInTheDocument();
  });

  it('displays provided date values', () => {
    render(
      <DateRangeFilter
        startDate="2025-06-01"
        endDate="2025-06-30"
        onStartDateChange={() => {}}
        onEndDateChange={() => {}}
      />
    );
    expect(screen.getByDisplayValue('2025-06-01')).toBeInTheDocument();
    expect(screen.getByDisplayValue('2025-06-30')).toBeInTheDocument();
  });

  it('calls onStartDateChange when start date changes', () => {
    const handleStartChange = vi.fn();
    render(
      <DateRangeFilter
        startDate={null}
        endDate={null}
        onStartDateChange={handleStartChange}
        onEndDateChange={() => {}}
      />
    );

    const startInput = screen.getByPlaceholderText('Start date');
    fireEvent.change(startInput, { target: { value: '2025-06-01' } });
    expect(handleStartChange).toHaveBeenCalledWith('2025-06-01');
  });

  it('calls onEndDateChange when end date changes', () => {
    const handleEndChange = vi.fn();
    render(
      <DateRangeFilter
        startDate={null}
        endDate={null}
        onStartDateChange={() => {}}
        onEndDateChange={handleEndChange}
      />
    );

    const endInput = screen.getByPlaceholderText('End date');
    fireEvent.change(endInput, { target: { value: '2025-06-30' } });
    expect(handleEndChange).toHaveBeenCalledWith('2025-06-30');
  });

  it('calls onChange with null when date is cleared', () => {
    const handleStartChange = vi.fn();
    render(
      <DateRangeFilter
        startDate="2025-06-01"
        endDate={null}
        onStartDateChange={handleStartChange}
        onEndDateChange={() => {}}
      />
    );

    const startInput = screen.getByPlaceholderText('Start date');
    fireEvent.change(startInput, { target: { value: '' } });
    expect(handleStartChange).toHaveBeenCalledWith(null);
  });
});
