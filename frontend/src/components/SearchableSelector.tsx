import React, { useState, useEffect, useRef } from 'react';

export interface Option {
    label: string;
    value: string;
}

interface SearchableSelectorProps {
    label: string;
    options?: Option[];
    selectedValues: string[];
    onSelectionChange: (values: string[]) => void;
    fetchUrl?: string; // Optional: URL to fetch options from
    multiSelect?: boolean;
    placeholder?: string;
    debug?: boolean; // New debug prop
}

const SearchableSelector: React.FC<SearchableSelectorProps> = ({
    label,
    options = [],
    selectedValues,
    onSelectionChange,
    fetchUrl,
    multiSelect = true,
    placeholder = "Filter...",
    debug = false
}) => {
    const [localOptions, setLocalOptions] = useState<Option[]>(options);
    const [loading, setLoading] = useState(false);
    const [isOpen, setIsOpen] = useState(false);
    const [search, setSearch] = useState('');
    const dropdownRef = useRef<HTMLDivElement>(null);

    // Load data if fetchUrl is provided
    useEffect(() => {
        if (fetchUrl) {
            if (debug) console.log(`[Selector:${label}] Fetching options from ${fetchUrl}`);
            setLoading(true);
            fetch(fetchUrl)
                .then(res => res.json())
                .then(data => {
                    if (Array.isArray(data)) {
                        setLocalOptions(data);
                        if (debug) console.log(`[Selector:${label}] Loaded ${data.length} options.`);
                    } else {
                        if (debug) console.warn(`[Selector:${label}] Invalid data format:`, data);
                        // Fallback to empty if invalid
                        setLocalOptions([]);
                    }
                })
                .catch(err => {
                    console.error("Failed to fetch options for " + label, err);
                    setLocalOptions([]);
                })
                .finally(() => setLoading(false));
        }
    }, [fetchUrl, label, debug]);

    // Update local options if props change AND we are not fetching
    useEffect(() => {
        if (!fetchUrl) {
            setLocalOptions(options);
        }
    }, [options, fetchUrl]);

    // Close on click outside - use MOUSEDOWN to match early events
    useEffect(() => {
        const handleClickOutside = (event: MouseEvent) => {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
                if (isOpen) {
                    if (debug) console.log(`[Selector:${label}] Clicked outside, closing.`);
                    setIsOpen(false);
                }
            }
        };
        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, [isOpen, label, debug]);

    const handleToggle = (e: React.MouseEvent) => {
        // Stop bubbling so the document mousedown listener doesn't immediately fire if we used click there? 
        // Or just to be safe.
        e.stopPropagation();

        if (debug) console.log(`[Selector:${label}] Toggle clicked. Current state: ${isOpen} -> ${!isOpen}`);
        setIsOpen(!isOpen);
    };

    const toggleOption = (value: string) => {
        if (debug) console.log(`[Selector:${label}] Option toggled: ${value}`);
        if (multiSelect) {
            if (selectedValues.includes(value)) {
                onSelectionChange(selectedValues.filter(v => v !== value));
            } else {
                onSelectionChange([...selectedValues, value]);
            }
        } else {
            // Single select: just set it and close
            onSelectionChange([value]);
            setIsOpen(false);
        }
    };

    const filteredOptions = localOptions.filter(opt =>
        opt.label.toLowerCase().includes(search.toLowerCase()) ||
        opt.value.toLowerCase().includes(search.toLowerCase())
    );

    // Display text logic
    let displayText = label;
    if (selectedValues.length > 0) {
        if (selectedValues.length === 1) {
            const found = localOptions.find(o => o.value === selectedValues[0]);
            displayText = found ? found.label : selectedValues[0];
            // Truncate if too long
            if (displayText.length > 25) displayText = displayText.substring(0, 22) + '...';
        } else {
            displayText = `${selectedValues.length} SELECTED`;
        }
    }

    return (
        <div style={{ position: 'relative', minWidth: '150px' }} ref={dropdownRef}>
            <div
                onClick={handleToggle}
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
                    textOverflow: 'ellipsis',
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    gap: '10px'
                }}
            >
                <span>{displayText}</span>
                <span style={{ fontSize: '0.8em' }}>{isOpen ? '▲' : '▼'}</span>
            </div>

            {isOpen && (
                <div style={{
                    position: 'absolute',
                    top: '100%',
                    left: 0,
                    width: '300px',
                    maxHeight: '400px',
                    overflowY: 'auto',
                    backgroundColor: '#000',
                    border: '1px solid var(--term-cyan)',
                    zIndex: 1000,
                    padding: '5px'
                }}>
                    <input
                        type="text"
                        placeholder={placeholder}
                        value={search}
                        onChange={(e) => setSearch(e.target.value)}
                        autoFocus
                        onClick={(e) => e.stopPropagation()} // Prevent closing when interacting with search
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

                    {loading && <div style={{ padding: '10px' }}>Loading...</div>}

                    {!loading && filteredOptions.map(opt => {
                        const isSelected = selectedValues.includes(opt.value);
                        return (
                            <div
                                key={opt.value}
                                onClick={(e) => {
                                    e.stopPropagation();
                                    toggleOption(opt.value);
                                }}
                                style={{
                                    padding: '5px',
                                    cursor: 'pointer',
                                    backgroundColor: isSelected ? 'rgba(0, 255, 255, 0.2)' : 'transparent',
                                    color: isSelected ? '#fff' : '#aaa',
                                    display: 'flex',
                                    justifyContent: 'space-between',
                                    borderBottom: '1px solid #111'
                                }}
                            >
                                <span style={{ marginRight: '10px' }}>{opt.label}</span>
                                {isSelected && <span style={{ color: 'var(--term-cyan)' }}>✓</span>}
                            </div>
                        );
                    })}

                    {!loading && filteredOptions.length === 0 && (
                        <div style={{ padding: '10px', color: '#666' }}>No matches</div>
                    )}
                </div>
            )}
        </div>
    );
};

export default SearchableSelector;
