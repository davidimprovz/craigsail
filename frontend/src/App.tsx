import { useState, useEffect, useRef, useMemo } from 'react';
import Terminal from './components/Terminal';
import ListingGrid, { Listing } from './components/ListingGrid';
import HelpModal from './components/HelpModal';
import CommandPalette, { Command } from './components/CommandPalette';

interface SearchResponse {
    results: Listing[];
}

function App() {
    const [logs, setLogs] = useState<string[]>(['> SYSTEM INITIALIZED...', '> WAITING FOR COMMAND...']);
    const [results, setResults] = useState<Listing[]>([]);
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [debugMode, setDebugMode] = useState(false);

    // V2 State
    const [showHelp, setShowHelp] = useState(false);
    const [filterText, setFilterText] = useState('');
    const [selectedIndex, setSelectedIndex] = useState<number>(-1);
    const [globalNotes, setGlobalNotes] = useState(() => localStorage.getItem('craigsail_global_notes') || '');
    const [listingNotes, setListingNotes] = useState<Record<string, string>>(() =>
        JSON.parse(localStorage.getItem('craigsail_listing_notes') || '{}')
    );

    // V3 State
    const [showPalette, setShowPalette] = useState(false);
    const [visibleColumns, setVisibleColumns] = useState<Record<string, boolean>>({
        price: true,
        item: true,
        posted: true,
        loc: true,
        action: true
    });

    const searchInputRef = useRef<HTMLInputElement>(null);

    // Persistence effects
    useEffect(() => {
        localStorage.setItem('craigsail_global_notes', globalNotes);
    }, [globalNotes]);

    useEffect(() => {
        localStorage.setItem('craigsail_listing_notes', JSON.stringify(listingNotes));
    }, [listingNotes]);

    const addLog = (msg: string) => setLogs(prev => [...prev, `> ${msg}`]);

    const performSearch = async (city: string, category: string, query: string) => {
        setIsLoading(true);
        addLog(`SEARCHING ${city} [${category}] FOR "${query}"...`);
        if (debugMode) console.log(`[App] Performing search: city=${city}, category=${category}, query=${query}`);
        try {
            const response = await fetch('/api/search', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ city, category, query })
            });
            const data: SearchResponse = await response.json();
            setResults(data.results);
            setSelectedIndex(-1);
            addLog(`FOUND ${data.results.length} RESULTS.`);
        } catch (err) {
            addLog(`ERROR: ${err instanceof Error ? err.message : String(err)}`);
        } finally {
            setIsLoading(false);
        }
    };

    const handleCommand = async (cmd: string) => {
        addLog(`EXECUTING: ${cmd}`);
        const [action, ...args] = cmd.split(' ');

        if (action === 'search') {
            // Format: search <city> <category> <query>
            // If only 2 args, assume category is 'sss'
            let city = args[0] || 'sfbay';
            let category = 'sss';
            let query = '';

            if (args.length >= 3) {
                category = args[1];
                query = args.slice(2).join(' ');
            } else {
                // Fallback for manual typing "search sfbay query"
                query = args.slice(1).join(' ') || 'boats';
            }

            await performSearch(city, category, query);
        } else if (action === 'clear') {
            setResults([]);
            setSelectedIndex(-1);
            setLogs(['> CLEARED.']);
        } else if (action === 'help') {
            setShowHelp(true);
        } else {
            addLog(`UNKNOWN COMMAND: ${action}`);
        }
    };

    const handleAnalyze = async (url: string) => {
        if (!url) return;
        addLog(`ANALYZING LISTING: ${url}...`);
        addLog(`> CONNECTING TO AI AGENT...`);
        try {
            const response = await fetch('/api/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ listing_url: url, user_query: "Is this a good deal? What are the red flags?" })
            });
            const data = await response.json();
            addLog(`AI REPORT:`);
            addLog(data.analysis);
            addLog(`----------------------------------------`);
        } catch (err) {
            addLog(`ERROR: ${err instanceof Error ? err.message : String(err)}`);
        }
    };

    // Filtered results
    const filteredResults = useMemo(() => {
        if (!filterText) return results;
        return results.filter(r =>
            r.title.toLowerCase().includes(filterText.toLowerCase()) ||
            r.price.toLowerCase().includes(filterText.toLowerCase())
        );
    }, [results, filterText]);

    // Command Palette Commands
    const commands: Command[] = [
        { id: 'search', label: 'Search Craigslist', action: () => document.querySelector<HTMLInputElement>('input[type="text"]')?.focus(), group: 'General' },
        { id: 'clear', label: 'Clear Results', action: () => { setResults([]); setSelectedIndex(-1); addLog('> CLEARED.'); }, group: 'General' },
        { id: 'help', label: 'View Help', action: () => setShowHelp(true), group: 'General' },
        { id: 'toggle-posted', label: 'Toggle Column: Posted', action: () => setVisibleColumns(prev => ({ ...prev, posted: !prev.posted })), group: 'View' },
        { id: 'toggle-loc', label: 'Toggle Column: Location', action: () => setVisibleColumns(prev => ({ ...prev, loc: !prev.loc })), group: 'View' },
        { id: 'toggle-price', label: 'Toggle Column: Price', action: () => setVisibleColumns(prev => ({ ...prev, price: !prev.price })), group: 'View' },
    ];

    // Hotkey Handler
    useEffect(() => {
        const handleKeyDown = (e: KeyboardEvent) => {
            // Allow Command Palette (Cmd+K or P) anywhere
            if ((e.metaKey && e.key === 'k') || (e.ctrlKey && e.key === 'k') || (e.key.toLowerCase() === 'p' && !['INPUT', 'TEXTAREA'].includes((e.target as HTMLElement).tagName))) {
                e.preventDefault();
                setShowPalette(true);
                return;
            }

            // Close modal/palette on Escape
            if (e.key === 'Escape') {
                setShowHelp(false);
                setShowPalette(false);
                if (['INPUT', 'TEXTAREA'].includes((e.target as HTMLElement).tagName)) {
                    (e.target as HTMLElement).blur();
                }
                return;
            }

            // If typing in an input/textarea, ignore other hotkeys
            const target = e.target as HTMLElement;
            const isInput = target.tagName === 'INPUT' || target.tagName === 'TEXTAREA';
            if (isInput) return;

            switch (e.key.toLowerCase()) {
                case 's':
                    e.preventDefault();
                    document.querySelector<HTMLInputElement>('input[type="text"]')?.focus();
                    break;
                case 'arrowup':
                    e.preventDefault();
                    setSelectedIndex(prev => Math.max(0, prev - 1));
                    break;
                case 'arrowdown':
                    e.preventDefault();
                    setSelectedIndex(prev => Math.min(filteredResults.length - 1, prev + 1));
                    break;
                case 'enter':
                    if (selectedIndex >= 0 && selectedIndex < filteredResults.length) {
                        handleAnalyze(filteredResults[selectedIndex].url);
                    }
                    break;
            }
        };

        window.addEventListener('keydown', handleKeyDown);
        return () => window.removeEventListener('keydown', handleKeyDown);
    }, [filteredResults, selectedIndex]);

    // Status Polling
    const [backendReady, setBackendReady] = useState(false);
    const [ollamaReady, setOllamaReady] = useState(false);

    useEffect(() => {
        const checkStatus = () => {
            // Check Backend - use relative path to go through proxy
            fetch('/health')
                .then(r => setBackendReady(r.ok))
                .catch(() => setBackendReady(false));

            // Check Ollama
            fetch('/api/models')
                .then(r => r.json())
                .then(d => setOllamaReady(d.models && d.models.length > 0))
                .catch(() => setOllamaReady(false));
        };

        checkStatus();
        const interval = setInterval(checkStatus, 10000); // 10s poll
        return () => clearInterval(interval);
    }, []);

    const StatusDot = ({ label, active }: { label: string, active: boolean }) => (
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.65em', fontFamily: 'monospace' }}>
            <div style={{
                width: '8px',
                height: '8px',
                borderRadius: '50%',
                backgroundColor: active ? '#0f0' : '#333',
                boxShadow: active ? '0 0 8px #0f0' : 'none',
                transition: 'all 0.3s ease'
            }} />
            <span style={{ color: active ? '#0f0' : '#555', transition: 'color 0.3s ease' }}>{label}</span>
        </div>
    );

    const activeListing = selectedIndex >= 0 ? filteredResults[selectedIndex] : null;

    const handleToggleColumn = (column: string) => {
        setVisibleColumns(prev => ({ ...prev, [column]: !prev[column] }));
    };

    const handleParse = async (model: string) => {
        if (results.length === 0) {
            addLog('NO DATA TO PARSE. RUN A SEARCH FIRST.');
            return;
        }
        setIsLoading(true);
        addLog(`PARSING ${results.length} ITEMS WITH MODEL: ${model.toUpperCase()}...`);
        try {
            const response = await fetch('/api/parse', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ listings: results, model })
            });
            const data: SearchResponse = await response.json();
            setResults(data.results);

            // eslint-disable-next-line @typescript-eslint/no-explicit-any
            const cleanedCount = data.results.filter((r: any) => r.location !== r.raw_location).length;
            addLog(`PARSE COMPLETE. ${data.results.length} ITEMS PROCESSED.`);
            if (cleanedCount > 0) {
                addLog(`CLEANED ${cleanedCount} LOCATION RECORDS.`);
            } else {
                addLog(`NO LOCATION CHANGES (data already clean or parse returned same values).`);
            }
        } catch (err) {
            addLog(`ERROR PARSING: ${err instanceof Error ? err.message : String(err)}`);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="crt app-container" style={{ padding: '20px', height: '100%', display: 'flex', flexDirection: 'column' }}>
            <div className="scanline"></div>
            <HelpModal isOpen={showHelp} onClose={() => setShowHelp(false)} />
            <CommandPalette isOpen={showPalette} onClose={() => setShowPalette(false)} commands={commands} />

            <header style={{ borderBottom: '2px solid var(--term-fg)', marginBottom: '20px', paddingBottom: '10px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexShrink: 0 }}>
                <div>
                    <h1 style={{ margin: 0 }}>CRAIGSAIL // V5.1</h1>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
                        <span style={{ fontSize: '0.8rem', opacity: 0.8 }}>Funds Intelligence Platform</span>
                        <div style={{ display: 'flex', gap: '12px', paddingLeft: '15px', borderLeft: '1px solid #333' }}>
                            <StatusDot label="API" active={backendReady} />
                            <StatusDot label="OLLAMA" active={ollamaReady} />
                        </div>
                        <button
                            onClick={() => setDebugMode(!debugMode)}
                            style={{
                                background: debugMode ? 'var(--term-cyan)' : 'transparent',
                                color: debugMode ? '#000' : 'var(--term-dim)',
                                border: '1px solid var(--term-dim)',
                                fontSize: '0.8em',
                                fontWeight: 'bold',
                                cursor: 'pointer',
                                padding: '2px 8px',
                                marginLeft: '10px'
                            }}
                        >
                            {debugMode ? 'DEBUG: ON' : 'DEBUG: OFF'}
                        </button>
                    </div>
                </div>
                <div style={{ display: 'flex', gap: '20px', alignItems: 'center' }}>
                    <div style={{ display: 'flex', flexDirection: 'column' }}>
                        <label style={{ fontSize: '0.7rem', opacity: 0.7 }}>FILTER</label>
                        <input
                            type="text"
                            value={filterText}
                            onChange={e => setFilterText(e.target.value)}
                            style={{ background: 'transparent', border: '1px solid var(--term-dim)', color: 'var(--term-cyan)', padding: '5px', outline: 'none' }}
                            placeholder="Type to filter..."
                        />
                    </div>
                    <button onClick={() => setShowPalette(true)} style={{ background: 'transparent', border: '1px solid var(--term-fg)', color: 'var(--term-fg)', cursor: 'pointer', fontFamily: 'inherit' }}>[CMD]</button>
                    <button onClick={() => setShowHelp(true)} style={{ background: 'transparent', border: '1px solid var(--term-fg)', color: 'var(--term-fg)', cursor: 'pointer', fontFamily: 'inherit' }}>[?] HELP</button>
                </div>
            </header >

            <div style={{ flex: 1, minHeight: 0, display: 'flex', gap: '20px' }}>
                {/* Main Grid Area */}
                <div style={{ flex: 2, border: '1px solid var(--term-dim)', padding: '10px', display: 'flex', flexDirection: 'column', minHeight: 0, overflow: 'hidden' }}>
                    <ListingGrid
                        results={filteredResults}
                        isLoading={isLoading}
                        onAnalyze={handleAnalyze}
                        selectedIndex={selectedIndex}
                        onSelect={setSelectedIndex}
                        visibleColumns={visibleColumns}
                        onToggleColumn={handleToggleColumn}
                    />
                </div>

                {/* Sidebar (Logs + Notes) */}
                <div style={{ flex: 1, minWidth: '350px', display: 'flex', flexDirection: 'column', gap: '20px', overflowY: 'auto' }}>

                    {/* Terminal / Logs */}
                    <div style={{ flex: '0 0 auto', maxHeight: '400px', border: '1px solid var(--term-dim)', display: 'flex', flexDirection: 'column' }}>
                        <div style={{ borderBottom: '1px solid var(--term-dim)', padding: '5px', fontSize: '0.8rem', fontWeight: 'bold', background: '#001100' }}>SYSTEM LOG</div>
                        <div style={{ height: '150px', padding: '10px', overflowY: 'auto', fontSize: '0.9rem' }}>
                            {logs.map((log, i) => <div key={i}>{log}</div>)}
                        </div>
                        <Terminal onCommand={handleCommand} onParse={handleParse} ref={searchInputRef} debug={debugMode} />
                    </div>

                    {/* Notepads */}
                    <div style={{ flex: 1, minHeight: '300px', display: 'flex', flexDirection: 'column', gap: '10px' }}>
                        {/* Global Notes */}
                        <div style={{ flex: 1, border: '1px solid var(--term-dim)', display: 'flex', flexDirection: 'column', minHeight: '150px' }}>
                            <div style={{ borderBottom: '1px solid var(--term-dim)', padding: '5px', fontSize: '0.8rem', fontWeight: 'bold', background: '#001100' }}>GLOBAL MISSION NOTES</div>
                            <textarea
                                value={globalNotes}
                                onChange={(e) => setGlobalNotes(e.target.value)}
                                style={{ flex: 1, background: 'transparent', border: 'none', color: 'var(--term-cyan)', padding: '10px', resize: 'none', outline: 'none', fontFamily: 'inherit' }}
                                placeholder="// ENTER MISSION NOTES HERE..."
                            />
                        </div>

                        {/* Listing Notes */}
                        <div style={{ flex: 1, border: '1px solid var(--term-dim)', display: 'flex', flexDirection: 'column', minHeight: '150px', opacity: activeListing ? 1 : 0.5 }}>
                            <div style={{ borderBottom: '1px solid var(--term-dim)', padding: '5px', fontSize: '0.8rem', fontWeight: 'bold', background: '#001100' }}>
                                TARGET NOTES {activeListing ? `[${activeListing.title.substring(0, 15)}...]` : '(SELECT LISTING)'}
                            </div>
                            <textarea
                                disabled={!activeListing}
                                value={activeListing ? (listingNotes[activeListing.url] || '') : ''}
                                onChange={(e) => {
                                    if (activeListing) {
                                        setListingNotes(prev => ({ ...prev, [activeListing.url]: e.target.value }));
                                    }
                                }}
                                style={{ flex: 1, background: 'transparent', border: 'none', color: 'var(--term-cyan)', padding: '10px', resize: 'none', outline: 'none', fontFamily: 'inherit' }}
                                placeholder={activeListing ? "// ENTER TARGET INTEL..." : "// SELECT A TARGET TO ANNOTATE"}
                            />
                        </div>
                    </div>
                </div>
            </div>
        </div >
    );
};

export default App;
