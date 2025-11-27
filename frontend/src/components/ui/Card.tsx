import React from 'react';
import clsx from 'clsx';

interface CardProps {
    children: React.ReactNode;
    className?: string;
    title?: string;
    action?: React.ReactNode;
    noPadding?: boolean;
}

const Card: React.FC<CardProps> = ({ children, className, title, action, noPadding = false }) => {
    return (
        <div className={clsx("glass-panel rounded-lg overflow-hidden flex flex-col", className)}>
            {title && (
                <div className="px-4 py-3 border-b border-white/5 flex justify-between items-center bg-white/5">
                    <h3 className="text-sm font-mono font-bold text-gray-200 tracking-wider flex items-center gap-2">
                        <span className="w-1 h-4 bg-cyber-neon rounded-sm" />
                        {title}
                    </h3>
                    {action && <div>{action}</div>}
                </div>
            )}
            <div className={clsx("flex-1", !noPadding && "p-4")}>
                {children}
            </div>
        </div>
    );
};

export default Card;
