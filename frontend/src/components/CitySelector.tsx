import React, { useState, useEffect, useRef } from 'react';

interface City {
    label: string;
    value: string;
}

interface CitySelectorProps {
    selectedCities: string[];
    onChange: (cities: string[]) => void;
}

const CitySelector: React.FC<CitySelectorProps> = ({ selectedCities, onChange }) => {
    const [cities, setCities] = useState<City[]>([]);
    const [loading, setLoading] = useState(true);
    const [isOpen, setIsOpen] = useState(false);
    const [search, setSearch] = useState('');
    const dropdownRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        const fetchCities = async () => {
            try {
                const res = await fetch('http://localhost:8008/api/cities'); // Direct to backend
                if (res.ok) {
                    const data = await res.json();
                    if (data && data.length > 0) {
                        setCities(data);
                    } else {
                        // Fallback
                        setCities([{ label: 'SF Bay Area', value: 'sfbay' }]);
                    }
                }
            } catch (e) {
                console.error("Failed to fetch cities", e);
                setCities([{ label: 'SF Bay Area', value: 'sfbay' }]);
            } finally {
                setLoading(false);
            }
        };
        fetchCities();

        // Close on click outside
        const handleClickOutside = (event: MouseEvent) => {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
                setIsOpen(false);
            }
        };
        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, []);

    const toggleCity = (value: string) => {
        if (selectedCities.includes(value)) {
            onChange(selectedCities.filter(c => c !== value));
        } else {
            onChange([...selectedCities, value]);
        }
    };

    const filteredCities = cities.filter(c =>
        c.label.toLowerCase().includes(search.toLowerCase()) ||
        c.value.toLowerCase().includes(search.toLowerCase())
    );

    return (
        <div style={{ position: 'relative', width: '200px' }} ref={dropdownRef}>
            <div
                onClick={() => setIsOpen(!isOpen)}
                style={{
                    backgroundColor: '#000',
                    color: 'var(--term-cyan)',
                    border: '1px solid var(--term-cyan)',
                    padding: '8px',
                    cursor: 'pointer',
                    fontSize: '1em',
                    fontFamily: 'Courier New, monospace',
                    whiteSpace: 'nowrap',
                    overflow: 'hidden',
                    textOverflow: 'ellipsis'
                }}
            >
                {selectedCities.length === 0 ? 'SELECT REGIONS' :
                    selectedCities.length === 1 ? cities.find(c => c.value === selectedCities[0])?.label || selectedCities[0] :
                        `${selectedCities.length} REGIONS SELECTED`}
                {' '}{isOpen ? '▲' : '▼'}
            </div>

            {isOpen && (
                <div style={{
                    position: 'absolute',
                    top: '100%',
                    left: 0,
                    width: '300px', // Wider dropdown
                    maxHeight: '400px',
                    overflowY: 'auto',
                    backgroundColor: '#000',
                    border: '1px solid var(--term-cyan)',
                    zIndex: 1000,
                    padding: '5px'
                }}>
                    <input
                        type="text"
                        placeholder="Filter cities..."
                        value={search}
                        onChange={(e) => setSearch(e.target.value)}
                        autoFocus
                        style={{
                            width: '100%',
                            backgroundColor: '#111',
                            color: '#fff',
                            border: '1px solid #444',
                            padding: '5px',
                            marginBottom: '5px',
                            fontFamily: 'inherit'
                        }}
                    />

                    {loading ? <div style={{ padding: '10px' }}>Loading...</div> :
                        filteredCities.map(city => {
                            const isSelected = selectedCities.includes(city.value);
                            return (
                                <div
                                    key={city.value}
                                    onClick={() => toggleCity(city.value)}
                                    style={{
                                        padding: '5px',
                                        cursor: 'pointer',
                                        backgroundColor: isSelected ? 'rgba(0, 255, 255, 0.2)' : 'transparent',
                                        color: isSelected ? '#fff' : '#aaa',
                                        display: 'flex',
                                        justifyContent: 'space-between'
                                    }}
                                >
                                    <span>{city.label}</span>
                                    {isSelected && <span style={{ color: 'var(--term-cyan)' }}>✓</span>}
                                </div>
                            );
                        })}

                    {filteredCities.length === 0 && <div style={{ padding: '10px', color: '#666' }}>No matches</div>}
                </div>
            )}
        </div>
    );
};

export default CitySelector;
