import { useState } from 'react'
import { Dashboard } from './components/Dashboard'
import { SystemMetrics, SimulationStatus } from './types/types'

function App() {
  const [metrics, setMetrics] = useState<SystemMetrics>({
    cpu: 0,
    memory: 0,
    disk: 0,
    network: 0
  });
  const [status, setStatus] = useState<SimulationStatus>('inactive');

  return (
    <Dashboard
      metrics={metrics}
      status={status}
      onStart={() => {/* Implementar */}}
      onStop={() => {/* Implementar */}}
      onGenerateReport={() => {/* Implementar */}}
    />
  )
}

export default App
