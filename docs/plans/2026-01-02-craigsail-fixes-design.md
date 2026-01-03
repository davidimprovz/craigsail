# Craigsail App Fixes & Improvements Design

**Date:** 2026-01-02
**Status:** Ready for Implementation

## Overview

This design addresses multiple issues reported in the Craigsail app and adds a requested column selector feature.

## Issues Identified

| Issue | Root Cause | Priority |
|-------|------------|----------|
| Batch parse shows no results | Parse succeeds (200 OK) but no visual feedback when 0 records change; Ollama may be failing silently | P1 |
| Results pane overflow | Table grows unbounded; missing height constraints and scroll containment | P2 |
| Hardcoded localhost URLs | `SearchBuilder.tsx` uses `http://localhost:8008/api/...` bypassing nginx proxy | P2 |
| No column selector UI | Column toggles only in command palette; user wants visual chips above table | P3 |
| Excessive /api/models polling | Fetched on every render + every 10s status poll | P3 |
| /health false positive | Nginx returns index.html for /health (200 OK) instead of actual health endpoint | P3 |

## Solution Design

### 1. Backend: Parser Debugging

**File: `backend/app/parser.py`**

Add logging to trace Ollama calls:
```python
async def parse_listing_fragment(self, raw_location: str, raw_date_text: str) -> dict:
    print(f"[Parser] Input: raw_location='{raw_location}', raw_date='{raw_date_text}'")

    if not self.llm:
        print("[Parser] LLM not initialized, returning raw data")
        return {"location": raw_location, "date_posted": None, "date_updated": None}

    # ... existing chain logic ...

    try:
        response = await chain.ainvoke({...})
        print(f"[Parser] Success: {response}")
        return response
    except Exception as e:
        print(f"[Parser] Failed: {e}")
        return {"location": raw_location, "date_posted": None, "date_updated": None}
```

**File: `backend/app/main.py`**

Add parse statistics:
```python
@app.post("/api/parse", response_model=SearchResponse)
async def parse_data(request: ParseRequest):
    log_debug(f"Parse request: {len(request.listings)} items, model={request.model}")

    parsed_count = 0
    changed_count = 0

    for item in request.listings:
        if item.raw_location:
            parsed_count += 1
            original_location = item.location
            p_data = await parser.parse_listing_fragment(item.raw_location, item.date_posted or "")
            item.location = p_data.get("location", item.location)
            if item.location != original_location:
                changed_count += 1
            # ... rest of updates ...

    log_debug(f"Parse complete: {parsed_count} processed, {changed_count} changed")
    return SearchResponse(results=parsed_listings)
```

### 2. Frontend: URL Fixes

**File: `frontend/src/components/SearchBuilder.tsx`**

Change hardcoded URLs to relative paths:
```typescript
// Line 40 & 86 - Change:
fetch('http://localhost:8008/api/models')
fetch('http://localhost:8008/api/cities')

// To:
fetch('/api/models')
fetch('/api/cities')
```

Prevent excessive model fetching:
```typescript
const [modelsLoaded, setModelsLoaded] = useState(false);

useEffect(() => {
    if (modelsLoaded) return;
    fetch('/api/models')
        .then(res => res.json())
        .then(data => {
            if (data.models?.length > 0) {
                setModels(data.models);
                setSelectedModel(data.models[0]);
            }
        })
        .finally(() => setModelsLoaded(true));
}, [modelsLoaded]);
```

### 3. Frontend: Better Parse Feedback

**File: `frontend/src/App.tsx`**

Update `handleParse` function:
```typescript
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

        const cleanedCount = data.results.filter((r: any) =>
            r.location !== r.raw_location
        ).length;

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
```

### 4. Nginx: Health Proxy

**File: `frontend/nginx.conf`**

Add health endpoint proxy:
```nginx
server {
    listen 80;
    server_name localhost;

    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # Health check proxy
    location /health {
        proxy_pass http://backend:8000/health;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # API proxy
    location /api/ {
        proxy_pass http://backend:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 5. Frontend: Results Pane Overflow Fix

**File: `frontend/src/App.tsx`**

Update main grid container (around line 301):
```tsx
<div style={{
    flex: 2,
    border: '1px solid var(--term-dim)',
    padding: '10px',
    display: 'flex',
    flexDirection: 'column',
    minHeight: 0,
    overflow: 'hidden'
}}>
    <ListingGrid ... />
</div>
```

**File: `frontend/src/components/ListingGrid.tsx`**

Wrap table in scrollable container with sticky header:
```tsx
return (
    <div style={{ flex: 1, display: 'flex', flexDirection: 'column', minHeight: 0 }}>
        {/* Column selector bar - see section 6 */}

        <div style={{ flex: 1, overflow: 'auto', minHeight: 0 }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
                <thead style={{ position: 'sticky', top: 0, background: 'var(--term-bg)', zIndex: 1 }}>
                    {/* ... existing header ... */}
                </thead>
                <tbody>
                    {/* ... existing rows ... */}
                </tbody>
            </table>
        </div>
    </div>
);
```

### 6. Frontend: Column Selector UI

**File: `frontend/src/components/ListingGrid.tsx`**

Add column definitions and selector component:
```tsx
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
    onToggleColumn: (column: string) => void;  // NEW
}
```

Column selector bar:
```tsx
const visibleCount = Object.values(visibleColumns).filter(Boolean).length;
const hiddenColumns = ALL_COLUMNS.filter(c => !visibleColumns[c.key]);

// Render above table:
<div style={{
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    paddingBottom: '10px',
    borderBottom: '1px solid var(--term-dim)',
    marginBottom: '10px',
    flexWrap: 'wrap'
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
                        fontSize: '1em'
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
            style={{
                background: '#000',
                border: '1px solid var(--term-dim)',
                color: 'var(--term-fg)',
                padding: '2px 5px',
                fontSize: '0.8em'
            }}
        >
            <option value="">+ ADD</option>
            {hiddenColumns.map(col => (
                <option key={col.key} value={col.key}>{col.label}</option>
            ))}
        </select>
    )}
</div>
```

**File: `frontend/src/App.tsx`**

Add toggle handler:
```tsx
const handleToggleColumn = (column: string) => {
    setVisibleColumns(prev => ({ ...prev, [column]: !prev[column] }));
};

// Pass to ListingGrid:
<ListingGrid
    ...
    visibleColumns={visibleColumns}
    onToggleColumn={handleToggleColumn}
/>
```

## Implementation Order

1. Backend logging (diagnose parse issue)
2. Frontend URL fixes (quick win)
3. Nginx health proxy (quick fix)
4. Parse feedback improvements
5. Overflow fixes
6. Column selector UI

## Testing Plan

- [ ] Run search, verify results display without overflow
- [ ] Click batch parse, check backend logs for parser output
- [ ] Verify OLLAMA status dot reflects actual connectivity
- [ ] Test column add/remove functionality
- [ ] Verify no excessive /api/models requests in network tab
