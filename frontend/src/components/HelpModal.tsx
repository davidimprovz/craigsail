import { FC } from 'react';

interface HelpModalProps {
    isOpen: boolean;
    onClose: () => void;
}

const HelpModal: FC<HelpModalProps> = ({ isOpen, onClose }) => {
    if (!isOpen) return null;

    return (
        <div style={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundColor: 'rgba(0, 0, 0, 0.8)',
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            zIndex: 1000
        }} onClick={onClose}>
            <div style={{
                backgroundColor: '#000',
                border: '2px solid var(--term-fg)',
                padding: '20px',
                minWidth: '400px',
                boxShadow: '0 0 20px var(--term-dim)'
            }} onClick={e => e.stopPropagation()}>
                <div style={{ borderBottom: '1px solid var(--term-dim)', paddingBottom: '10px', marginBottom: '15px' }}>
                    <h2 style={{ margin: 0 }}>SYSTEM COMMANDS</h2>
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: 'auto 1fr', gap: '10px', fontSize: '0.9rem' }}>
                    <div style={{ color: 'var(--term-fg)', fontWeight: 'bold' }}>[S]</div>
                    <div>Focus Search Input</div>

                    <div style={{ color: 'var(--term-fg)', fontWeight: 'bold' }}>[C]</div>
                    <div>Clear Results</div>

                    <div style={{ color: 'var(--term-fg)', fontWeight: 'bold' }}>[H] / [?]</div>
                    <div>Toggle Help</div>

                    <div style={{ color: 'var(--term-fg)', fontWeight: 'bold' }}>[↑] / [↓]</div>
                    <div>Navigate Results</div>

                    <div style={{ color: 'var(--term-fg)', fontWeight: 'bold' }}>[ENTER]</div>
                    <div>Analyze Selected</div>
                </div>

                <div style={{ marginTop: '20px', textAlign: 'right', fontSize: '0.8rem', opacity: 0.7 }}>
                    PRESS [ESC] TO CLOSE
                </div>
            </div>
        </div>
    );
};

export default HelpModal;
