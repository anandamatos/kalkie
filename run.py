#!/usr/bin/env python3
"""
🎯 KALKIE - Sistema de Gerenciamento de Perda de Peso
Execução principal do programa migrado do Jupyter para arquivos .py
"""

import sys
import os

# Adicionar o diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def main():
    """Função principal de execução."""
    print("🎯" + "="*60)
    print("🎯 KALKIE - SISTEMA DE GESTÃO DE PERDA DE PESO")
    print("🎯" + "="*60)
    print("📦 Versão: 2.0 (Migração Completa)")
    print("🐍 Python: " + sys.version.split()[0])
    print("📁 Diretório: " + os.getcwd())
    print("🎯" + "="*60)
    
    try:
        from src.main import executar_programa_principal
        
        print("\n🚀 Iniciando programa principal...")
        print("💡 Dica: Use Ctrl+C para sair a qualquer momento")
        print("-" * 50)
        
        executar_programa_principal()
        
    except KeyboardInterrupt:
        print("\n\n👋 Programa interrompido pelo usuário. Até logo!")
        
    except Exception as e:
        print(f"\n❌ Erro não esperado: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        print("\n🎯 Programa finalizado. Obrigado por usar KALKIE!")

if __name__ == "__main__":
    main()