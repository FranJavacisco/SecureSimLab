# SecureSimLab - Interfaz Gráfica
# Archivo: simulator_gui.py
# Este código es parte del proyecto SecureSimLab y está diseñado solo para propósitos educativos.

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import threading
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import os
import sys

# Importar nuestros módulos
from ransomware_simulator import RansomwareSimulator
from system_monitor import SystemMonitor

class SimulatorGUI:
    """Interfaz gráfica para el simulador de ransomware y monitor del sistema"""
    
    def __init__(self):
        """Inicializa la interfaz gráfica"""
        self.root = tk.Tk()
        self.root.title("SecureSimLab - Simulador de Análisis de Seguridad")
        self.root.geometry("1200x800")
        
        # Inicializar simulador y monitor
        self.setup_simulation_environment()
        self.setup_gui()
        self.setup_graphs()
        self.update_thread = None
        self.running = False
        
    def setup_simulation_environment(self):
        """Configura el entorno de simulación y monitoreo"""
        # Configurar directorios
        self.target_dir = os.path.join("data", "test_files")
        self.backup_dir = os.path.join("data", "backup_files")
        
        # Crear directorios si no existen
        os.makedirs(self.target_dir, exist_ok=True)
        os.makedirs(self.backup_dir, exist_ok=True)
        
        # Inicializar simulador y monitor
        self.simulator = RansomwareSimulator(self.target_dir, self.backup_dir)
        self.monitor = SystemMonitor()
        
    def setup_gui(self):
        """Configura los elementos de la interfaz gráfica"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Estilo
        style = ttk.Style()
        style.configure('Alert.TLabel', foreground='red')
        
        # Panel de control
        control_frame = ttk.LabelFrame(main_frame, text="Panel de Control", padding="5")
        control_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # Botones de control
        ttk.Button(control_frame, text="Iniciar Simulación", 
                  command=self.start_simulation).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(control_frame, text="Detener Simulación", 
                  command=self.stop_simulation).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(control_frame, text="Generar Reporte", 
                  command=self.generate_report).grid(row=0, column=2, padx=5, pady=5)
        
        # Advertencia de seguridad
        warning_label = ttk.Label(control_frame, 
                                text="⚠️ Usar solo en entorno controlado de laboratorio",
                                style='Alert.TLabel')
        warning_label.grid(row=1, column=0, columnspan=3, pady=5)
        
        # Panel de estado
        status_frame = ttk.LabelFrame(main_frame, text="Estado del Sistema", padding="5")
        status_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        self.status_text = tk.Text(status_frame, height=5, width=70)
        self.status_text.grid(row=0, column=0, padx=5, pady=5)
        
        # Scrollbar para el texto de estado
        scrollbar = ttk.Scrollbar(status_frame, orient=tk.VERTICAL, 
                                command=self.status_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.status_text['yscrollcommand'] = scrollbar.set
        
        # Panel de métricas
        metrics_frame = ttk.LabelFrame(main_frame, text="Métricas del Sistema", padding="5")
        metrics_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # Variables para métricas
        self.cpu_var = tk.StringVar(value="CPU: 0%")
        self.memory_var = tk.StringVar(value="Memoria: 0%")
        self.disk_var = tk.StringVar(value="Disco: 0 MB/s")
        self.network_var = tk.StringVar(value="Red: 0 MB/s")
        
        # Etiquetas de métricas
        ttk.Label(metrics_frame, textvariable=self.cpu_var, width=20).grid(
            row=0, column=0, padx=5, pady=5)
        ttk.Label(metrics_frame, textvariable=self.memory_var, width=20).grid(
            row=0, column=1, padx=5, pady=5)
        ttk.Label(metrics_frame, textvariable=self.disk_var, width=20).grid(
            row=0, column=2, padx=5, pady=5)
        ttk.Label(metrics_frame, textvariable=self.network_var, width=20).grid(
            row=0, column=3, padx=5, pady=5)
        
    def setup_graphs(self):
        """Configura los gráficos de monitoreo"""
        graphs_frame = ttk.LabelFrame(self.root, text="Monitoreo en Tiempo Real", padding="5")
        graphs_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=5)
        
        # Crear figura para gráficos
        self.fig = Figure(figsize=(10, 4), dpi=100)
        self.cpu_ax = self.fig.add_subplot(121)
        self.memory_ax = self.fig.add_subplot(122)
        
        # Inicializar datos
        self.times = []
        self.cpu_values = []
        self.memory_values = []
        
        # Crear canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=graphs_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
    def update_graphs(self, cpu_percent, memory_percent):
        """Actualiza los gráficos con nuevos datos"""
        current_time = datetime.now().strftime('%H:%M:%S')
        self.times.append(current_time)
        self.cpu_values.append(cpu_percent)
        self.memory_values.append(memory_percent)
        
        # Mantener solo los últimos 60 valores
        if len(self.times) > 60:
            self.times.pop(0)
            self.cpu_values.pop(0)
            self.memory_values.pop(0)
            
        # Actualizar gráficos
        self.cpu_ax.clear()
        self.memory_ax.clear()
        
        self.cpu_ax.plot(self.times, self.cpu_values, 'b-')
        self.cpu_ax.set_title('Uso de CPU')
        self.cpu_ax.set_ylabel('Porcentaje')
        self.cpu_ax.tick_params(axis='x', rotation=45)
        
        self.memory_ax.plot(self.times, self.memory_values, 'r-')
        self.memory_ax.set_title('Uso de Memoria')
        self.memory_ax.set_ylabel('Porcentaje')
        self.memory_ax.tick_params(axis='x', rotation=45)
        
        self.fig.tight_layout()
        self.canvas.draw()
        
    def update_metrics(self):
        """Actualiza las métricas mostradas en la interfaz"""
        if not self.running:
            return
            
        try:
            # Obtener métricas actuales
            metrics = self.monitor.collect_metrics()
            
            if metrics:
                # Actualizar etiquetas
                self.cpu_var.set(f"CPU: {metrics['cpu_percent']}%")
                self.memory_var.set(f"Memoria: {metrics['memory_percent']}%")
                
                disk_write_speed = metrics['disk_io'].write_bytes / 1024 / 1024
                self.disk_var.set(f"Disco: {disk_write_speed:.2f} MB/s")
                
                network_speed = (metrics['network'].bytes_sent + 
                               metrics['network'].bytes_recv) / 1024 / 1024
                self.network_var.set(f"Red: {network_speed:.2f} MB/s")
                
                # Actualizar gráficos
                self.update_graphs(metrics['cpu_percent'], metrics['memory_percent'])
                
            # Programar próxima actualización
            self.root.after(1000, self.update_metrics)
            
        except Exception as e:
            self.log_message(f"Error al actualizar métricas: {str(e)}")
            
    def log_message(self, message):
        """Añade un mensaje al panel de estado"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.status_text.insert(tk.END, f"\n[{timestamp}] {message}")
        self.status_text.see(tk.END)
        
    def start_simulation(self):
        """Inicia la simulación y el monitoreo"""
        try:
            if not self.running:
                # Iniciar simulador
                self.simulator.start_simulation()
                
                # Iniciar monitor
                self.monitor.start_monitoring()
                
                self.running = True
                self.update_metrics()
                
                self.log_message("Simulación y monitoreo iniciados")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al iniciar simulación: {str(e)}")
            
    def stop_simulation(self):
        """Detiene la simulación y el monitoreo"""
        try:
            if self.running:
                # Detener simulador
                self.simulator.stop_simulation()
                
                # Detener monitor
                self.monitor.stop_monitoring()
                
                self.running = False
                
                self.log_message("Simulación y monitoreo detenidos")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al detener simulación: {str(e)}")
            
    def generate_report(self):
        """Genera y muestra el reporte de la simulación"""
        try:
            report = self.monitor.generate_report()
            
            if report:
                # Crear ventana para mostrar reporte
                report_window = tk.Toplevel(self.root)
                report_window.title("Reporte de Simulación")
                report_window.geometry("800x600")
                
                report_text = tk.Text(report_window, wrap=tk.WORD)
                report_text.pack(expand=True, fill=tk.BOTH)
                
                # Mostrar reporte formateado
                report_text.insert(tk.END, json.dumps(report, indent=4))
                report_text.config(state=tk.DISABLED)
                
                self.log_message("Reporte generado exitosamente")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reporte: {str(e)}")
            
    def run(self):
        """Inicia la ejecución de la interfaz gráfica"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
        
    def on_closing(self):
        """Maneja el evento de cierre de la ventana"""
        if self.running:
            self.stop_simulation()
        self.root.destroy()

def main():
    """Función principal para ejecutar la interfaz gráfica"""
    gui = SimulatorGUI()
    gui.run()

if __name__ == "__main__":
    main()