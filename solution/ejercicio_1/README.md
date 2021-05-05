# Solución Ejercicio 1

## Explicación
Se va a describir un sumador de N bits de entrada, con reset asincrónico. La salida deberá ser de N+1 bits para poder almacenar el resultado de la suma.

Para esto lo único que debemos tener en consideración es que la llegada de los datos A y B puede no ser simultanea. Esto quiere decir que vamos a tener que esperar a que ambos datos esten disponibles (es decir que si ambas señales de _ready = 0, ya tenemos los dos datos disponibles) para que, en el próximo ciclo de clk, se encuentre en la salida el entero correspondiente a la suma.



# Referencias

* [nMigen Docs](https://nmigen.info/nmigen/latest/lang.html)


# Contacto

* Lucas Liaño: lliano@frba.utn.edu.ar
