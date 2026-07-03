import React, { useState, useEffect } from 'react';
import SearchableSelector from './SearchableSelector';

interface SearchBuilderProps {
    onSearch: (city: string, category: string, query: string) => void;
    onParse: (model: string) => void;
    debug?: boolean;
}

const CATEGORIES = [
    { label: 'For Sale (All)', value: 'sss' },
    { label: 'Boats', value: 'boo' },
    { label: 'Cars/Trucks', value: 'cto' },
    { label: 'Electronics', value: 'ela' },
    { label: 'Free', value: 'zip' },
    { label: 'Computers', value: 'sys' },
    { label: 'Bicycles', value: 'bia' },
    { label: 'Furniture', value: 'fua' },
    { label: 'Aviation', value: 'ava' },
    { label: 'Motorcycles', value: 'mca' },
    { label: 'RVs', value: 'rva' },
    { label: 'Auto Parts', value: 'pta' },
    { label: 'Materials', value: 'maa' },
    { label: 'Tools', value: 'tla' },
];

const SearchBuilder: React.FC<SearchBuilderProps> = ({ onSearch, onParse, debug = false }) => {
    // V5 Multi-city
    const [selectedCities, setSelectedCities] = useState<string[]>(['sfbay']);
    const [selectedCategories, setSelectedCategories] = useState<string[]>(['sss']);
    const [query, setQuery] = useState('');

    // V5 AI Models
    const [models, setModels] = useState<string[]>([]);
    const [selectedModel, setSelectedModel] = useState('mistral');
    const [modelsLoaded, setModelsLoaded] = useState(false);

    useEffect(() => {
        if (modelsLoaded) return;
        if (debug) console.log("[SearchBuilder] Fetching AI models...");
        fetch('/api/models')
            .then(res => res.json())
            .then(data => {
                if (debug) console.log("[SearchBuilder] Models:", data);
                if (data.models && data.models.length > 0) {
                    setModels(data.models);
                    setSelectedModel(data.models[0]);
                } else {
                    setModels(['ministral-3', 'mistral', 'gemma:2b']);
                }
            })
            .catch((e) => {
                if (debug) console.error("[SearchBuilder] Failed to fetch models", e);
                setModels(['ministral-3', 'mistral', 'gemma:2b']);
            })
            .finally(() => setModelsLoaded(true));
    }, [modelsLoaded, debug]);

    const handleSearch = () => {
        if (debug) console.log(`[SearchBuilder] Executing search: cities=${selectedCities.join(',')}, cat=${selectedCategories[0]}, query=${query}`);
        if (selectedCities.length === 0) return;
        const cityString = selectedCities.join(',');
        // For categories, Craigslist usually only supports one category strictly per search URL structure, 
        // but our backend could loop them. For now, let's take the first one or if we support multi-cat in backend loop.
        // User asked for "selectable as well", implying multi might be nice, but backend `scraper.search` takes one category.
        // Let's force single select behavior UI-wise or loop in frontend? 
        // Best approach for now: Just use the first selected category.
        const categoryString = selectedCategories.length > 0 ? selectedCategories[0] : 'sss';
        onSearch(cityString, categoryString, query);
    };

    return (
        <div style={{
            padding: '15px',
            borderBottom: '1px solid var(--term-line)',
            background: '#0a0a0a',
            display: 'flex',
            flexDirection: 'column',
            gap: '10px'
        }}>
            <div style={{ display: 'flex', gap: '15px', alignItems: 'center', flexWrap: 'wrap' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
                    <span style={{ color: 'var(--term-dim)', fontSize: '0.8em' }}>REGIONS:</span>
                    <SearchableSelector
                        label="SELECT REGIONS"
                        selectedValues={selectedCities}
                        onSelectionChange={setSelectedCities}
                        fetchUrl="/api/cities"
                        multiSelect={true}
                        placeholder="Filter cities..."
                        debug={debug}
                    />
                </div>

                <div style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
                    <span style={{ color: 'var(--term-dim)', fontSize: '0.8em' }}>CATEGORY:</span>
                    <SearchableSelector
                        label="CATEGORY"
                        options={CATEGORIES}
                        selectedValues={selectedCategories}
                        // Force single select for now by taking the last clicked? Or just allow multi but use first?
                        // Let's allow multi in UI but use first in search to avoid backend complexity for now.
                        onSelectionChange={(vals) => {
                            // Enforce single select if we want, or just let them pick and we use [0]
                            // Let's enforce single select behavior for Category to match `scraper` expectation
                            if (vals.length > 0) setSelectedCategories([vals[vals.length - 1]]);
                            else setSelectedCategories([]);
                        }}
                        multiSelect={true} // Set to true to use the generic UI, but we handle it as single above
                        placeholder="Filter categories..."
                        debug={debug}
                    />
                </div>
            </div>

            <div style={{ display: 'flex', gap: '10px', width: '100%' }}>
                <div style={{
                    display: 'flex',
                    flex: 1,
                    position: 'relative',
                    alignItems: 'center',
                    border: '1px solid #333',
                    background: '#111'
                }}>
                    <input
                        type="text"
                        placeholder="Keywords (e.g. 'macbook pro' or 'sailing')"
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
                        style={{
                            flex: 1,
                            background: 'transparent',
                            border: 'none',
                            color: '#fff',
                            padding: '10px',
                            fontSize: '1.2em',
                            fontFamily: 'inherit',
                            outline: 'none',
                            minWidth: 0 // Fix flex overflow
                        }}
                    />
                </div>

                <button
                    type="button"
                    onClick={handleSearch}
                    style={{
                        background: 'var(--term-cyan)',
                        color: '#000',
                        border: 'none',
                        padding: '0 20px',
                        fontSize: '1.2em',
                        fontWeight: 'bold',
                        cursor: 'pointer',
                        whiteSpace: 'nowrap'
                    }}
                >
                    EXECUTE {'>'}
                </button>
            </div>

            <div style={{ display: 'flex', gap: '15px', paddingTop: '5px', alignItems: 'center', borderTop: '1px solid #222' }}>
                <span style={{ color: 'var(--term-dim)', fontSize: '0.8em' }}>AI PARSING:</span>
                <select
                    value={selectedModel}
                    onChange={(e) => setSelectedModel(e.target.value)}
                    style={{
                        background: '#000',
                        color: '#aaa',
                        border: '1px solid #444',
                        padding: '5px',
                        fontFamily: 'monospace'
                    }}
                >
                    {models.map(m => <option key={m} value={m}>{m}</option>)}
                </select>

                <button
                    type="button"
                    onClick={() => onParse(selectedModel)}
                    style={{
                        background: 'transparent',
                        border: '1px solid #444',
                        color: '#ddd',
                        padding: '5px 10px',
                        cursor: 'pointer',
                        fontSize: '0.9em',
                        fontFamily: 'monospace'
                    }}
                >
                    [ RUN BATCH PARSE ]
                </button>
            </div>
        </div>
    );
};

export default SearchBuilder;
