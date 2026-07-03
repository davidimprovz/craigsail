import { FC } from 'react';

export interface Listing {
    title: string;
    price: string;
    location: string;
    url: string;
    image_url?: string;
    description?: string;
    date_posted?: string;
    date_updated?: string;
    raw_location?: string;
}

const ALL_COLUMNS = [
    { key: 'price', label: 'PRICE' },
    { key: 'item', label: 'ITEM' },
    { key: 'posted', label: 'POSTED' },
    { key: 'loc', label: 'LOC' },
    { key: 'action', label: 'ACTION' }
];

interface ListingGridProps {
    results: Listing[];
    isLoading: boolean;
    onAnalyze: (url: string) => void;
    selectedIndex: number;
    onSelect: (index: number) => void;
    visibleColumns: Record<string, boolean>;
    onToggleColumn: (column: string) => void;
}

const ListingGrid: FC<ListingGridProps> = ({
    results,
    isLoading,
    onAnalyze,
    selectedIndex,
    onSelect,
    visibleColumns,
    onToggleColumn
}) => {
    const visibleCount = Object.values(visibleColumns).filter(Boolean).length;
    const hiddenColumns = ALL_COLUMNS.filter(c => !visibleColumns[c.key]);

    if (isLoading) {
        return <div className="blink">SCANNING NETWORK...</div>;
    }

    if (results.length === 0) {
        return <div style={{ opacity: 0.5 }}>NO DATA FOUND. WAITING FOR INPUT.</div>;
    }

    return (
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column', minHeight: 0 }}>
            {/* Column Selector Bar */}
            <div style={{
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                paddingBottom: '10px',
                borderBottom: '1px solid var(--term-dim)',
                marginBottom: '10px',
                flexWrap: 'wrap',
                flexShrink: 0
            }}>
                <span style={{ fontSize: '0.8em', color: 'var(--term-dim)' }}>COLUMNS:</span>

                {ALL_COLUMNS.filter(c => visibleColumns[c.key]).map(col => (
                    <div key={col.key} style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '4px',
                        background: '#1a1a1a',
                        border: '1px solid var(--term-dim)',
                        padding: '2px 8px',
                        fontSize: '0.8em'
                    }}>
                        <span>{col.label}</span>
                        {visibleCount > 1 && (
                            <button
                                onClick={() => onToggleColumn(col.key)}
                                style={{
                                    background: 'transparent',
                                    border: 'none',
                                    color: 'var(--term-dim)',
                                    cursor: 'pointer',
                                    padding: '0 2px',
                                    fontSize: '1em',
                                    lineHeight: 1
                                }}
                            >
                                ×
                            </button>
                        )}
                    </div>
                ))}

                {hiddenColumns.length > 0 && (
                    <select
                        onChange={(e) => {
                            if (e.target.value) onToggleColumn(e.target.value);
                            e.target.value = '';
                        }}
                        value=""
                        style={{
                            background: '#000',
                            border: '1px solid var(--term-dim)',
                            color: 'var(--term-fg)',
                            padding: '2px 5px',
                            fontSize: '0.8em',
                            fontFamily: 'inherit',
                            cursor: 'pointer'
                        }}
                    >
                        <option value="">+ ADD</option>
                        {hiddenColumns.map(col => (
                            <option key={col.key} value={col.key}>{col.label}</option>
                        ))}
                    </select>
                )}
            </div>

            {/* Scrollable Table Container */}
            <div style={{ flex: 1, overflow: 'auto', minHeight: 0 }}>
                <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
                    <thead style={{ position: 'sticky', top: 0, background: 'var(--term-bg)', zIndex: 1 }}>
                        <tr style={{ borderBottom: '1px solid var(--term-dim)' }}>
                            {visibleColumns.price && <th style={{ padding: '10px' }}>PRICE</th>}
                            {visibleColumns.item && <th style={{ padding: '10px' }}>ITEM</th>}
                            {visibleColumns.posted && <th style={{ padding: '10px' }}>POSTED</th>}
                            {visibleColumns.loc && <th style={{ padding: '10px' }}>LOC</th>}
                            {visibleColumns.action && <th style={{ padding: '10px' }}>ACTION</th>}
                        </tr>
                    </thead>
                    <tbody>
                        {results.map((item, i) => {
                            const isSelected = i === selectedIndex;
                            return (
                                <tr
                                    key={i}
                                    style={{
                                        borderBottom: '1px solid #1a800033',
                                        background: isSelected ? 'rgba(0, 255, 255, 0.1)' : 'transparent',
                                        cursor: 'pointer',
                                        color: isSelected ? 'var(--term-cyan)' : 'inherit'
                                    }}
                                    onClick={() => onSelect(i)}
                                >
                                    {visibleColumns.price && <td style={{ padding: '10px', color: isSelected ? 'inherit' : 'var(--term-fg)' }}>{item.price}</td>}
                                    {visibleColumns.item && <td style={{ padding: '10px' }}>
                                        <a
                                            href={item.url}
                                            target="_blank"
                                            rel="noreferrer"
                                            style={{ color: 'inherit', textDecoration: 'none' }}
                                            onClick={e => e.stopPropagation()}
                                        >
                                            {item.title}
                                        </a>
                                    </td>}
                                    {visibleColumns.posted && <td style={{ padding: '10px', fontSize: '0.8em', opacity: 0.8 }}>{item.date_posted || 'N/A'}</td>}
                                    {visibleColumns.loc && <td style={{ padding: '10px', fontSize: '0.8em' }}>{item.location}</td>}
                                    {visibleColumns.action && <td style={{ padding: '10px' }}>
                                        <button
                                            style={{
                                                background: isSelected ? 'var(--term-cyan)' : 'var(--term-dim)',
                                                border: 'none',
                                                color: '#000',
                                                cursor: 'pointer',
                                                fontFamily: 'inherit',
                                                padding: '2px 5px'
                                            }}
                                            onClick={(e) => {
                                                e.stopPropagation();
                                                onAnalyze(item.url);
                                            }}
                                        >
                                            ANALYZE
                                        </button>
                                    </td>}
                                </tr>
                            );
                        })}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default ListingGrid;
