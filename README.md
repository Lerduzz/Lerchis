# Lerchis
Mi version del Parchis con mis reglas.

## Comandos
### Generar UI
pyuic5 parchis.ui -o parchis_ui.py

### Generar RC
pyrcc5 parchis.qrc -o parchis_rc.py

### Generar EXE
pyinstaller --onefile --windowed --name Lerchis.exe --icon images/icono/icono.ico --add-data sounds/dados.mp3:sounds --add-data sounds/llegar.mp3:sounds --add-data sounds/mover.mp3:sounds --add-data sounds/nomover.mp3:sounds --add-data sounds/salir.mp3:sounds --add-data sounds/matar.mp3:sounds --add-data sounds/turno.mp3:sounds --add-data sounds/music1.mp3:sounds --add-data sounds/music2.mp3:sounds parchis.py
