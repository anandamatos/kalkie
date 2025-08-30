# bridge.py
import sys
import os

# Adiciona o diretório src ao path do Python
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

print("Bridge carregado - Módulos disponíveis:")
print("- src.main")
print("- src.calculator") 
print("- src.data_manager")
print("- src.activity_planner")