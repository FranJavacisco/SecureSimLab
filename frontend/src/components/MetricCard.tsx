import React from 'react';

interface MetricCardProps {
  title: string;
  value: string | number;
  unit?: string;
}

export const MetricCard: React.FC<MetricCardProps> = ({ title, value, unit }) => (
  <div className="bg-white overflow-hidden shadow rounded-lg">
    <div className="px-4 py-5 sm:p-6">
      <dt className="text-sm font-medium text-gray-500 truncate">{title}</dt>
      <dd className="mt-1 text-3xl font-semibold text-gray-900">
        {value}{unit && <span className="text-xl ml-1">{unit}</span>}
      </dd>
    </div>
  </div>
);