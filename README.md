# Lerchis
Mi version del Parchis con mis reglas.

## Comandos
### Generar UI
pyuic5 parchis.ui -o parchis_ui.py

### Generar RC
pyrcc5 parchis.qrc -o parchis_rc.py

### Generar EXE
pyinstaller --onefile --windowed --name Lerchis.exe --icon images/icono/icono.ico --add-data "sounds/*.wav:./sounds/" parchis.py
