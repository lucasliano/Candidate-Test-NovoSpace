# Solución Ejercicio 1

## Explicación
Se va a describir un sumador de N bits de entrada, con reset asincrónico. La salida deberá ser de N+1 bits para poder almacenar el resultado de la suma.

Para esto lo único que debemos tener en consideración es que la llegada de los datos A y B puede no ser simultanea. Esto quiere decir que vamos a tener que esperar a que ambos datos esten disponibles (es decir que si ambas señales de _ready = 0, ya tenemos los dos datos disponibles) para que, en el próximo ciclo de clk, se encuentre en la salida el entero correspondiente a la suma.

Se ejecutaran los tests correspondientes para poder corroborar el correcto funcionamiento. Entre las cosas a evaluar encontramos:
  - Funcionamiento del rst
  - Funcionamiento del adder, debe computar correctamente las operaciones
  - Prueba bajo estrés (Muchas sumas con valores aleatorios)
  - Evaluación de overflow (La suma de dos valores, que superen el valor máximo representable en N bits, debe de poder computarse con N+1 bits)
  - Evaluación de entradas a destiempo (Verificar que aunque A y B no llegen al mismo tiempo se pueda computar la suma correctamente)
  - Evaluación de salidas a destiempo (Verificar que aunque r_ready no se active, el dispositivo no se cuelgue)

## Dependencias
Para poder ejecutar el script hace falta instalar el módulo `bitstring`, esto es posible mediante el comando:

```
pip install bitstring
```

## Testing

Para ejecutar los test correr el siguiente comando:

```
python3 main.py
```

**Nota:** Los tests se encuentran en el mismo archivo que la declaración del módulo.

# Referencias

* [nMigen Docs](https://nmigen.info/nmigen/latest/lang.html)


# Contacto

* Lucas Liaño: lliano@frba.utn.edu.ar
