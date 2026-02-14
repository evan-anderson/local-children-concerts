interface TownFilterProps {
  availableTowns: string[];
  selectedTowns: string[];
  onChange: (towns: string[]) => void;
}

export function TownFilter({ availableTowns, selectedTowns, onChange }: TownFilterProps) {
  const handleToggle = (town: string) => {
    if (selectedTowns.includes(town)) {
      onChange(selectedTowns.filter(t => t !== town));
    } else {
      onChange([...selectedTowns, town]);
    }
  };

  return (
    <div className="town-filter">
      <label>Filter by town:</label>
      <div className="town-checkboxes">
        {availableTowns.map(town => (
          <label key={town} className="checkbox-label">
            <input
              type="checkbox"
              checked={selectedTowns.includes(town)}
              onChange={() => handleToggle(town)}
            />
            {town}
          </label>
        ))}
      </div>
    </div>
  );
}
