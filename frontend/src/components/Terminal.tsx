import { useState, FormEvent, forwardRef, useImperativeHandle, useRef } from 'react';

interface TerminalProps {
    onCommand: (cmd: string) => void;
    onParse: (model: string) => void;
    debug?: boolean;
}

import SearchBuilder from './SearchBuilder';

const Terminal = forwardRef<HTMLInputElement, TerminalProps>(({ onCommand, onParse, debug = false }, ref) => {
    const [input, setInput] = useState<string>('');
    const internalInputRef = useRef<HTMLInputElement>(null);

    useImperativeHandle(ref, () => internalInputRef.current as HTMLInputElement);

    const handleSubmit = (e: FormEvent) => {
        e.preventDefault();
        if (!input.trim()) return;
        onCommand(input);
        setInput('');
    };

    const handleSearchBuild = (city: string, category: string, query: string) => {
        // Construct the command string
        const cmd = `search ${city} ${category} ${query}`;
        onCommand(cmd);
    };

    return (
        <div style={{ borderTop: '1px solid var(--term-dim)', display: 'flex', flexDirection: 'column' }}>
            <SearchBuilder onSearch={handleSearchBuild} onParse={onParse} debug={debug} />
            <form onSubmit={handleSubmit} style={{ padding: '10px' }}>
                <div style={{ display: 'flex' }}>
                    <span style={{ marginRight: '10px' }}>$</span>
                    <input
                        ref={internalInputRef}
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        autoFocus
                        style={{
                            background: 'transparent',
                            border: 'none',
                            color: 'var(--term-fg)',
                            fontFamily: 'inherit',
                            flex: 1,
                            outline: 'none'
                        }}
                    />
                </div>
            </form>
        </div>
    );
});

export default Terminal;
