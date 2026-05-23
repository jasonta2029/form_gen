/**
 * Sidebar.jsx — Side panel layout skeleton.
 */
import React from 'react';

export const Sidebar = ({ children }) => {
  return (
    <aside className="w-80 bg-[#1a1a24] border-r border-[#23232f] flex flex-col h-full">
      {children}
    </aside>
  );
};

export default Sidebar;
