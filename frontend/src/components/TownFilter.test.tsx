import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { TownFilter } from './TownFilter';

const mockTowns = ['Boston', 'Cambridge', 'Somerville'];

describe('TownFilter', () => {
  it('renders all available towns as checkboxes', () => {
    render(
      <TownFilter
        availableTowns={mockTowns}
        selectedTowns={[]}
        onChange={() => {}}
      />
    );
    expect(screen.getByLabelText('Boston')).toBeInTheDocument();
    expect(screen.getByLabelText('Cambridge')).toBeInTheDocument();
    expect(screen.getByLabelText('Somerville')).toBeInTheDocument();
  });

  it('shows selected towns as checked', () => {
    render(
      <TownFilter
        availableTowns={mockTowns}
        selectedTowns={['Boston', 'Cambridge']}
        onChange={() => {}}
      />
    );
    expect(screen.getByLabelText('Boston')).toBeChecked();
    expect(screen.getByLabelText('Cambridge')).toBeChecked();
    expect(screen.getByLabelText('Somerville')).not.toBeChecked();
  });

  it('calls onChange when checkbox is clicked', async () => {
    const user = userEvent.setup();
    const handleChange = vi.fn();
    render(
      <TownFilter
        availableTowns={mockTowns}
        selectedTowns={[]}
        onChange={handleChange}
      />
    );

    await user.click(screen.getByLabelText('Boston'));
    expect(handleChange).toHaveBeenCalledWith(['Boston']);
  });

  it('removes town from selection when unchecked', async () => {
    const user = userEvent.setup();
    const handleChange = vi.fn();
    render(
      <TownFilter
        availableTowns={mockTowns}
        selectedTowns={['Boston', 'Cambridge']}
        onChange={handleChange}
      />
    );

    await user.click(screen.getByLabelText('Boston'));
    expect(handleChange).toHaveBeenCalledWith(['Cambridge']);
  });
});
