# SecureSimLab - Educational Security Testing Framework
# File: src/__init__.py

"""
SecureSimLab - A framework for educational security testing and system monitoring
"""

from .ransomware_simulator import RansomwareSimulator
from .system_monitor import SystemMonitor
from .simulator_gui import SimulatorGUI

__version__ = '1.0.0'
__author__ = 'Your Name'
__license__ = 'MIT'

# Versión del paquete
VERSION = (1, 0, 0)

def get_version():
    """
    Returns the current version of SecureSimLab
    """
    return '.'.join(str(v) for v in VERSION)

# Exportar las clases principales
__all__ = [
    'RansomwareSimulator',
    'SystemMonitor',
    'SimulatorGUI'
]