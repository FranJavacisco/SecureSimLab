import React from 'react';
import { MetricCard } from './MetricCard';
import { SystemMetrics, SimulationStatus } from '../types/types';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

interface DashboardProps {
  metrics: SystemMetrics;
  status: SimulationStatus;
  onStart: () => void;
  onStop: () => void;
  onGenerateReport: () => void;
}

export const Dashboard: React.FC<DashboardProps> = ({
  metrics,
  status,
  onStart,
  onStop,
  onGenerateReport,
}) => {
  return (
    <div className="min-h-screen bg-gray-100">
      {/* Contenido del Dashboard */}
    </div>
  );
};