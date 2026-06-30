import { useState, useEffect, useRef, useMemo } from 'react';

export interface Command {
    id: string;
    label: string;
    action: () => void;
    group?: string;
}

interface CommandPaletteProps {
    isOpen: boolean;
    onClose: () => void;
    commands: Command[];
}

const CommandPalette: React.FC<CommandPaletteProps> = ({ isOpen, onClose, commands }) => {
    const [query, setQuery] = useState('');
    const [selectedIndex, setSelectedIndex] = useState(0);
    const inputRef = useRef<HTMLInputElement>(null);

    // Filter commands based on query
    const filteredCommands = useMemo(() => {
        if (!query) return commands;
        return commands.filter(cmd =>
            cmd.label.toLowerCase().includes(query.toLowerCase())
        );
    }, [query, commands]);

    // Reset selection when query or visibility changes
    useEffect(() => {
        setSelectedIndex(0);
    }, [query, isOpen]);

    // Focus input when opened
    useEffect(() => {
        if (isOpen) {
            setTimeout(() => inputRef.current?.focus(), 50);
        } else {
            setQuery(''); // Clear query on close
        }
    }, [isOpen]);

    // Keyboard navigation
    useEffect(() => {
        if (!isOpen) return;

        const handleKeyDown = (e: KeyboardEvent) => {
            if (e.key === 'ArrowDown') {
                e.preventDefault();
                setSelectedIndex(prev => Math.min(prev + 1, filteredCommands.length - 1));
            } else if (e.key === 'ArrowUp') {
                e.preventDefault();
                setSelectedIndex(prev => Math.max(prev - 1, 0));
            } else if (e.key === 'Enter') {
                e.preventDefault();
                if (filteredCommands[selectedIndex]) {
                    filteredCommands[selectedIndex].action();
                    onClose();
                }
            } else if (e.key === 'Escape') {
                e.preventDefault();
                onClose();
            }
        };

        window.addEventListener('keydown', handleKeyDown);
        return () => window.removeEventListener('keydown', handleKeyDown);
    }, [isOpen, filteredCommands, selectedIndex, onClose]);

    if (!isOpen) return null;

    return (
        <div style={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundColor: 'rgba(0, 0, 0, 0.8)',
            zIndex: 1000,
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'flex-start',
            paddingTop: '100px'
        }} onClick={onClose}>
            <div style={{
                width: '600px',
                maxWidth: '90%',
                backgroundColor: 'var(--term-bg)',
                border: '1px solid var(--term-cyan)',
                boxShadow: '0 0 20px rgba(0, 255, 255, 0.2)',
                display: 'flex',
                flexDirection: 'column',
                maxHeight: '400px',
            }} onClick={e => e.stopPropagation()}>
                <div style={{
                    padding: '10px',
                    borderBottom: '1px solid var(--term-dim)',
                    display: 'flex',
                    alignItems: 'center'
                }}>
                    <span style={{ color: 'var(--term-cyan)', marginRight: '10px' }}>&gt;</span>
                    <input
                        ref={inputRef}
                        type="text"
                        value={query}
                        onChange={e => setQuery(e.target.value)}
                        placeholder="Type a command..."
                        style={{
                            background: 'transparent',
                            border: 'none',
                            color: 'var(--term-fg)',
                            fontSize: '1.2rem',
                            fontFamily: 'inherit',
                            flex: 1,
                            outline: 'none'
                        }}
                    />
                </div>
                <div style={{ overflowY: 'auto' }}>
                    {filteredCommands.map((cmd, index) => (
                        <div
                            key={cmd.id}
                            style={{
                                padding: '10px 15px',
                                cursor: 'pointer',
                                backgroundColor: index === selectedIndex ? 'rgba(0, 255, 255, 0.1)' : 'transparent',
                                color: index === selectedIndex ? 'var(--term-cyan)' : 'var(--term-fg)',
                                display: 'flex',
                                justifyContent: 'space-between'
                            }}
                            onMouseEnter={() => setSelectedIndex(index)}
                            onClick={() => {
                                cmd.action();
                                onClose();
                            }}
                        >
                            <span>{cmd.label}</span>
                            {cmd.group && <span style={{ opacity: 0.5, fontSize: '0.8em' }}>{cmd.group}</span>}
                        </div>
                    ))}
                    {filteredCommands.length === 0 && (
                        <div style={{ padding: '20px', textAlign: 'center', opacity: 0.5 }}>
                            No commands found.
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default CommandPalette;
