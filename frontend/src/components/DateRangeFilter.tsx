interface DateRangeFilterProps {
  startDate: string | null;
  endDate: string | null;
  onStartDateChange: (date: string | null) => void;
  onEndDateChange: (date: string | null) => void;
}

export function DateRangeFilter({
  startDate,
  endDate,
  onStartDateChange,
  onEndDateChange,
}: DateRangeFilterProps) {
  return (
    <div className="date-filter">
      <label>Filter by date:</label>
      <div className="date-inputs">
        <input
          type="date"
          value={startDate || ''}
          onChange={e => onStartDateChange(e.target.value || null)}
          placeholder="Start date"
        />
        <span>to</span>
        <input
          type="date"
          value={endDate || ''}
          onChange={e => onEndDateChange(e.target.value || null)}
          placeholder="End date"
        />
      </div>
    </div>
  );
}
