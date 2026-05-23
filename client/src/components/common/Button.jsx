/**
 * Button.jsx — Common UI component supporting diverse options configurations.
 */
import React from 'react';

export const Button = ({
  children,
  onClick,
  type = 'button',
  variant = 'primary', // primary | secondary | danger | outline
  disabled = false,
  className = '',
  ...props
}) => {
  const baseStyles = 'px-4 py-2 rounded-lg font-bold text-xs transition-all focus:outline-none disabled:opacity-50 select-none';
  
  const variants = {
    primary: 'bg-[#ff2a7f] hover:bg-[#e0206f] text-white shadow-[0_0_8px_rgba(255,42,127,0.2)]',
    secondary: 'bg-[#272739] hover:bg-[#34344d] border border-[#3e3e56] text-[#b3b3cb]',
    danger: 'bg-red-600 hover:bg-red-500 text-white',
    outline: 'border border-[#ff2a7f] hover:bg-[#ff2a7f]/10 text-[#ff2a7f]'
  };

  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={`${baseStyles} ${variants[variant] || variants.primary} ${className}`}
      {...props}
    >
      {children}
    </button>
  );
};

export default Button;
