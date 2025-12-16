## Alkalmazás indítása Windows rendszeren

Az alkalmazás Windows környezetben egy kattintással indítható a `start.bat`
fájl segítségével.

### A `start.bat` tartalma

```bat
@echo off
python -m streamlit run gui.py
pause