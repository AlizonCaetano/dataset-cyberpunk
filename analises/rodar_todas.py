"""Roda todas as análises em ordem. Uso, a partir da raiz do projeto: python3 analises/rodar_todas.py"""
import glob
import os
import subprocess
import sys

pasta = os.path.dirname(os.path.abspath(__file__))
for script in sorted(glob.glob(os.path.join(pasta, "[0-9][0-9]_*.py"))):
    print(f"\n===== {os.path.basename(script)} =====")
    subprocess.run([sys.executable, script], check=True)
