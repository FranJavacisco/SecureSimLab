export interface SystemMetrics {
    cpu: number;
    memory: number;
    disk: number;
    network: number;
  }
  
  export interface ChartData {
    time: string;
    cpu: number;
    memory: number;
  }
  
  export type SimulationStatus = 'inactive' | 'active' | 'error';