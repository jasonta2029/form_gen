/**
 * AddDancerForm.jsx — Side editor component supporting fast adding of dancers.
 */
import React, { useState } from 'react';
import { getDancerColor } from '../../utils/colorPalette';

export const AddDancerForm = ({ onSubmit }) => {
  const [name, setName] = useState('');
  const [group, setGroup] = useState('ensemble');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!name.trim()) return;
    
    // Choose random color offset deterministically
    const randomColor = getDancerColor(Math.floor(Math.random() * 10));

    onSubmit({
      name: name.trim(),
      group: group,
      color: randomColor
    });

    setName('');
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-3">
      <div>
        <label className="block text-[10px] uppercase text-[#b3b3cb] tracking-wider mb-1 font-semibold">
          Dancer Name
        </label>
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="e.g. Patty"
          className="w-full bg-[#171721] border border-[#2d2d3d] text-white px-3 py-2 rounded-lg text-xs focus:outline-none focus:border-[#ff2a7f]"
          required
        />
      </div>

      <div>
        <label className="block text-[10px] uppercase text-[#b3b3cb] tracking-wider mb-1 font-semibold">
          Dancer Role/Group
        </label>
        <select
          value={group}
          onChange={(e) => setGroup(e.target.value)}
          className="w-full bg-[#171721] border border-[#2d2d3d] text-white px-3 py-2 rounded-lg text-xs focus:outline-none focus:border-[#ff2a7f]"
        >
          <option value="leads">Leads</option>
          <option value="ensemble">Ensemble</option>
          <option value="backups">Backups</option>
        </select>
      </div>

      <button
        type="submit"
        className="w-full bg-[#ff2a7f] hover:bg-[#e0206f] text-white text-xs font-bold py-2 rounded-lg transition-colors"
      >
        Add Dancer
      </button>
    </form>
  );
};

export default AddDancerForm;
