/**
 * Header.jsx — Workspace top navigation bar skeleton.
 */
import React from 'react';

export const Header = () => {
  return (
    <header className="bg-[#1a1a24] border-b border-[#23232f] px-6 py-4 flex items-center justify-between">
      <h1 className="text-xl font-black">Form<span className="text-[#ff2a7f]">Flow</span></h1>
    </header>
  );
};

export default Header;
