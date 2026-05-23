/**
 * Layout.jsx — Standard Layout wrapper containing page headers.
 */
import React from 'react';

export const Layout = ({ children }) => {
  return (
    <div className="min-h-screen bg-[#121214] text-white flex flex-col font-sans select-none">
      {/* Content wrapper */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {children}
      </div>
    </div>
  );
};

export default Layout;
