# Lerchis
Mi version del Parchis con mis reglas.


## Comandos

### Generar UI
```
pyuic5 parchis.ui -o parchis_ui.py
```

### Generar RC
```
pyrcc5 parchis.qrc -o parchis_rc.py
```

### Generar EXE
```
pyinstaller --onefile --windowed --name Lerchis.exe --icon images/icono/icono.ico --add-data "sounds:sounds" parchis.py
```
### Generar EXE: Usando SPEC
```
pyinstaller Lerchis.exe.spec
```


## Reglas

### Generales
- Juegan entre 2 y 4 jugadores por turnos.
- Los turnos son de un máximo de 30 segundos.
- Debes jugar todos tus movimientos posibles rapidamente o perderás el turno.
- En cada casilla solo puede haber dos fichas.
  * Excepto en la casa y la meta en dónde puedeb haber 4 fichas del mismo color.
- Los jugadores no pueden hacer nada hasta que tiran los dados.

### Sacar
- Para sacar una ficha de la casa es necesario tener un 5.
- Puede ser en uno de los dados o la suma de ambos.

### Puentes
- Los jugadores pueden hacer un puente manteniendo dos de sus fichas en su casilla de salida.
- Los puentes no pueden ser cruzados.
- Si a un jugador con un puente le cae una pareja en los dados está obligado a abrir el puente.
  * Excepto cuando las fichas del puente no tienen movimientos disponibles.

### Comer
- Si una ficha cae en la misma casilla que otra de otro color la regresa a su casa.
  * Excepto en las zonas seguras marcadas.
- El jugador que come gana un bono de 20 pasos.
- La recompensa por comer no se acumula.
- La recompensa por comer puede ser caminada con cualquier ficha del jugador excepto las de la casa y meta.
  * Incluso puede caminarlo con la misma ficha que ha comido.

### Llegar
- Para llegar a la meta es necesario que te caiga una cifra exacta.
- El jugador que llega gana un bono de 10 pasos.
- La recompensa por llegar no se acumula.
- La recompensa por llegar puede ser caminada con cualquier ficha del jugador excepto las de la casa y meta.
- Cuando solo tengas una ficha fuera de la meta y esta se encuentre dentro de la recta final, utilizarás un solo dado.

### Nota adicional
- Luego de tirar los dados, el jugador distribuye los pasos que va a caminar como mejor le convenga.
- Puede caminar más de una vez con cada ficha mientras que tenga dado o bono disponible para utilizar.
