# Solución Ejercicio 2

## Explicación
Va a leer el archivo verilog de entrada linea por linea. En cada linea se va a consultar por una estructura distinta. Inicialmente el objetivo es encontrar una declaración de memoria, una vez se haya reconocido este patron se comenzará a loopear entre las asignaciones. En cada uno de estos búcles se almacenará el valor de memoria que se este guardando.

Finalmente se escribiran los archivos de salida.

## Testing

Para ejecutar los test del script correr el siguiente comando:

```
pytest
```

## Dependencias
El único modulo utilizado para la realización de este ejercicio es nativo de python. No es necesario instalar dependencias.


# Referencias

* [HOWTO regex](https://docs.python.org/3/howto/regex.html)
* [PyTest](https://docs.pytest.org/en/6.2.x/)

# Contacto

* Lucas Liaño: lliano@frba.utn.edu.ar
