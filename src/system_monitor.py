# SecureSimLab - Sistema de Monitoreo
# Archivo: system_monitor.py
# Este código es parte del proyecto SecureSimLab y está diseñado solo para propósitos educativos.

import psutil
import platform
import time
import json
import logging
from pathlib import Path
from datetime import datetime
from threading import Thread, Event
from queue import Queue
import sqlite3
import os

class SystemMonitor:
    """
    Sistema de monitoreo y análisis para el simulador de ransomware.
    Registra y analiza el comportamiento del sistema durante la simulación.
    """
    
    def __init__(self, db_path: str = 'data/monitor.db'):
        """
        Inicializa el sistema de monitoreo.
        
        Args:
            db_path (str): Ruta para la base de datos de monitoreo
        """
        self.db_path = db_path
        self.monitoring = False
        self.data_queue = Queue()
        self.stop_event = Event()
        self.setup_logging()
        self.setup_database()
        
    def setup_logging(self):
        """Configura el sistema de registro para el monitor"""
        # Asegurar que existe el directorio de logs
        if not os.path.exists('logs'):
            os.makedirs('logs')
            
        self.logger = logging.getLogger('SystemMonitor')
        self.logger.setLevel(logging.INFO)
        
        handler = logging.FileHandler('logs/system_monitor.log')
        handler.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        
    def setup_database(self):
        """Inicializa la base de datos para almacenar métricas"""
        try:
            # Asegurar que existe el directorio para la base de datos
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Tabla para métricas del sistema
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS system_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME,
                    cpu_percent REAL,
                    memory_percent REAL,
                    disk_io_read REAL,
                    disk_io_write REAL,
                    network_sent REAL,
                    network_recv REAL
                )
            ''')
            
            # Tabla para eventos detectados
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS security_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME,
                    event_type TEXT,
                    description TEXT,
                    severity TEXT
                )
            ''')
            
            conn.commit()
            conn.close()
            self.logger.info("Base de datos inicializada correctamente")
            
        except Exception as e:
            self.logger.error(f"Error al configurar la base de datos: {str(e)}")
            raise
            
    def collect_metrics(self):
        """Recolecta métricas del sistema"""
        try:
            metrics = {
                'timestamp': datetime.now().isoformat(),
                'cpu_percent': psutil.cpu_percent(interval=1),
                'memory_percent': psutil.virtual_memory().percent,
                'disk_io': psutil.disk_io_counters(),
                'network': psutil.net_io_counters()
            }
            return metrics
            
        except Exception as e:
            self.logger.error(f"Error al recolectar métricas: {str(e)}")
            return None
            
    def analyze_behavior(self, metrics):
        """
        Analiza el comportamiento del sistema basado en las métricas recolectadas
        
        Args:
            metrics (dict): Métricas del sistema recolectadas
        """
        try:
            # Analizar uso de CPU
            if metrics['cpu_percent'] > 80:
                self.log_security_event(
                    'HIGH_CPU_USAGE',
                    f"Uso de CPU elevado: {metrics['cpu_percent']}%",
                    'WARNING'
                )
                
            # Analizar uso de memoria
            if metrics['memory_percent'] > 90:
                self.log_security_event(
                    'HIGH_MEMORY_USAGE',
                    f"Uso de memoria elevado: {metrics['memory_percent']}%",
                    'WARNING'
                )
                
            # Analizar actividad de disco
            disk_write_speed = metrics['disk_io'].write_bytes / 1024 / 1024  # MB/s
            if disk_write_speed > 100:  # Más de 100 MB/s
                self.log_security_event(
                    'HIGH_DISK_ACTIVITY',
                    f"Actividad de disco elevada: {disk_write_speed:.2f} MB/s",
                    'WARNING'
                )
                
        except Exception as e:
            self.logger.error(f"Error en análisis de comportamiento: {str(e)}")
            
    def log_security_event(self, event_type: str, description: str, severity: str):
        """
        Registra un evento de seguridad en la base de datos
        
        Args:
            event_type (str): Tipo de evento
            description (str): Descripción detallada
            severity (str): Nivel de severidad
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO security_events 
                (timestamp, event_type, description, severity)
                VALUES (?, ?, ?, ?)
            ''', (datetime.now().isoformat(), event_type, description, severity))
            
            conn.commit()
            conn.close()
            
            self.logger.info(f"Evento de seguridad registrado: {event_type}")
            
        except Exception as e:
            self.logger.error(f"Error al registrar evento: {str(e)}")
            
    def monitor_thread(self):
        """Hilo principal de monitoreo"""
        while not self.stop_event.is_set():
            try:
                metrics = self.collect_metrics()
                if metrics:
                    self.analyze_behavior(metrics)
                    self.data_queue.put(metrics)
                time.sleep(1)  # Intervalo de monitoreo
                
            except Exception as e:
                self.logger.error(f"Error en hilo de monitoreo: {str(e)}")
                
    def start_monitoring(self):
        """Inicia el monitoreo del sistema"""
        if self.monitoring:
            self.logger.warning("El monitoreo ya está activo")
            return
            
        self.monitoring = True
        self.stop_event.clear()
        self.monitor_thread = Thread(target=self.monitor_thread)
        self.monitor_thread.daemon = True  # El hilo se detendrá cuando el programa principal termine
        self.monitor_thread.start()
        self.logger.info("Monitoreo iniciado")
        
    def stop_monitoring(self):
        """Detiene el monitoreo del sistema"""
        if not self.monitoring:
            return
            
        self.stop_event.set()
        self.monitor_thread.join()
        self.monitoring = False
        self.logger.info("Monitoreo detenido")
        
    def generate_report(self, output_file: str = 'data/reports/security_report.json'):
        """
        Genera un reporte de seguridad basado en los datos recolectados
        
        Args:
            output_file (str): Archivo de salida para el reporte
        """
        try:
            # Asegurar que existe el directorio para reportes
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Obtener métricas del sistema
            cursor.execute('''
                SELECT * FROM system_metrics 
                ORDER BY timestamp DESC 
                LIMIT 100
            ''')
            metrics = cursor.fetchall()
            
            # Obtener eventos de seguridad
            cursor.execute('''
                SELECT * FROM security_events 
                ORDER BY timestamp DESC
            ''')
            events = cursor.fetchall()
            
            conn.close()
            
            # Crear reporte
            report = {
                'timestamp': datetime.now().isoformat(),
                'system_info': {
                    'platform': platform.platform(),
                    'processor': platform.processor(),
                    'memory': psutil.virtual_memory().total
                },
                'metrics_summary': {
                    'total_records': len(metrics),
                    'avg_cpu': sum(m[2] for m in metrics) / len(metrics) if metrics else 0,
                    'avg_memory': sum(m[3] for m in metrics) / len(metrics) if metrics else 0
                },
                'security_events': [
                    {
                        'timestamp': e[1],
                        'type': e[2],
                        'description': e[3],
                        'severity': e[4]
                    }
                    for e in events
                ]
            }
            
            # Guardar reporte
            with open(output_file, 'w') as f:
                json.dump(report, f, indent=4)
                
            self.logger.info(f"Reporte generado: {output_file}")
            return report
            
        except Exception as e:
            self.logger.error(f"Error al generar reporte: {str(e)}")
            return None

if __name__ == "__main__":
    # Prueba básica del monitor
    monitor = SystemMonitor()
    
    try:
        print("Iniciando monitoreo del sistema...")
        monitor.start_monitoring()
        
        # Ejecutar monitoreo por 30 segundos
        time.sleep(30)
        
        print("Generando reporte...")
        monitor.generate_report()
        
    finally:
        monitor.stop_monitoring()
        print("Monitoreo finalizado")