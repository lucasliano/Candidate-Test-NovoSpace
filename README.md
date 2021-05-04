# Candidate test!

Bienvenidos a esta etapa de evaluación para formar parte del equipo de Novo Space.
Durante el desarrollo de este test se evaluarán herramientas que posiblemente
nunca hayan utilizado. La idea es que sea lo más ameno posible y que, en caso de no quedar,
también haya sido util para aprender cosas nuevas. La intención de este test es ver
la capacidad de adaptación y de resolución de problemas del postulante, asi como también
la comunicación. Sientase libre de hacernos cualquier tipo de pregunta que posea, que
con gusto intentaremos aclararla.

Aclarado esto, solo me queda decir una cosa: BUENA SUERTE!!

---

# Ejercicio #1

## Introducción

En el diseño de una radio para satélites de comunicación, es necesario realizar
operaciones algebraicas sobre fuentes de datos provenientes de diferentes antenas.
Estas operaciones deben realizarse lo más rápido posible (500 millones de operaciones
por segundo aproximadamente). Es por ello, que se decidió que el procesamiento de estos
datos lo haga una FPGA. La primer operación que se tiene que resolver es la suma.

## Enunciado

Realizar un sumador con lógica de números signados complemento a 2 que cumpla con la siguiente
interfaz:

```
           |--------------|
 a_data -->|              |
a_valid -->|              |
a_ready <--|              |
           |              |-->  r_data
           |    Adder     |--> r_valid
           |              |<--  r_ready
 b_data -->|              |
b_valid -->|              |
b_ready <--|              |
           |--------------|
               ^       ^
               |       |
              rst     clk
```

Tanto las dos entradas como la salida cumplen un protocolo genérico stream con las
siguientes características:

* El dato `_data` es leído por el sumidero cuando `_valid` y `_ready` están en 1
* La señal `_valid` no puede depender depender de la señal `_ready` para ir a 1.

Todas los datos que salgan por el puerto `r` deben ser un resultado valido entre los datos
del puerto `a` y puerto `b`. No se debe realizar corroboración de overflow.

Para realizar este ejercicio, usted debe:
* Cumplir con las especificaciones enunciadas anteriormente
* Realizar un buen batch de test que testee lo mejor posible el diseño
* Utilizar el framework [nMigen](https://nmigen.info/nmigen/latest/) para su desarrollo
* Utilizar el framework [cocotb](https://docs.cocotb.org/en/stable/) para su testeo

Aclaración: Todas las herramientas necesitadas para realizar este ejercicio son opensource
y no se requiere ninguna licencia.

En la carpeta correspondiente a este ejercicio, encontrarás materíal util que puede servír
para resolver este problema. Puede encontrar más material en la documentación de ambos
frameworks o en proyectos opensource en github.

Para ejecutar el ejemplo, dirijase a la carpeta `ej1` y ejecute `python3 exemplo.py` previamente
habiendo instalado todos los paquetes python necesarios (se provee el archivo `requirements.txt`) y
el simulador [iverilog](http://iverilog.icarus.com/). Para visualizar la waveform generada,
es necesario tener instalado el programa [GTKWave](http://gtkwave.sourceforge.net/) y ejecutar
`gtkwave incrementador.vcd`

Ambos SW extras (iverilog y gtkwave) se distribuyen en los repositorios de multiples distribuciones
linux, se instalan con un simple comando apt-get, yum, pacman, etc.


# Ejercicio #2

Muchas veces las herramientas que se utilizan en el dia a dia no son suficientes para lo que se
desea hacer y hay que realizar nuestras propias herramientas o agregar un layer de adaptación
con otra ya existente.

Actualmente, las herramientas de un vendor de FPGA no soportan completamente la sintaxis de
verilog lo cual hace incompatible el output de nMigen. Más puntualmente no soporta la inicialización
inline de memorias:

* **Sintaxis no soportada**
```verilog
  reg [7:0] mem [15:0];
  initial begin
    mem[0] = 8'h3d;
    mem[1] = 8'hc9;
    mem[2] = 8'hbf;
    mem[3] = 8'hd5;
    mem[4] = 8'h52;
    mem[5] = 8'he0;
    mem[6] = 8'h05;
    mem[7] = 8'hc8;
    mem[8] = 8'hbc;
    mem[9] = 8'h6e;
    mem[10] = 8'h98;
    mem[11] = 8'h9f;
    mem[12] = 8'h4b;
    mem[13] = 8'h4c;
    mem[14] = 8'h39;
    mem[15] = 8'h55;
  end
```

* **Sintaxis soportada**
```verilog
  reg [7:0] mem [15:0];
  $readmemh("memdump0.mem", mem);
```
**dump1.mem**:
```
3d
c9
bf
d5
52
e0
05
c8
bc
6e
98
9f
4b`
4c
39
55
```

Se pide desarrollar un script de python que reemplace las estructuras de inicialización inline por
la inicialización soportada por la herramienta y exporte los archivos con los valores de inicialización.
Se otorga un testcase (`testcase.v`) y los resultados esperados (en la carpeta `expected`).

El siguiente regex puede ser de MUCHA utilidad:
```
r'  reg \[(.*)\] (\S*) \[(.*)\];\n  initial begin\n((    \S*\[\S*\] = \S*;\n)*)  end\n'
```


# Que se va a evaluar?

* Capacidad de adaptación: No creemos que mucha gente este trabajando con los frameworks del
ejercicio #1, el desafío principal es su adaptación a este entorno.

* Resolución de problemas: Este es un ejercicio de dificultad baja pero que permite
ver cual es su capacidad para resolver problemas tanto usando la lógica como buscando
material complementario.

* Flujo de trabajo: Viendo los commits en el repositorio git podemos tener una trazabilidad
de como trabajan y de su conocimiento utilizando control de versiones.

* Testeo: Hacer un buen test es igual o más importante que el desarrollo de una solución. Ya
que con esto se evita propagar errores a futuro, mitigarlos lo más cercanamente posible a su
desarrollo y tener confiabilidad en tu diseño.

* Comunicación: La comunicación es un pilar importante en el día a día. Se recomienda siempre
mantener una comunicación con actualizaciones del estado en el que se encuentran y dudas que
posean.


# Entrega

Para realizar la entrega, forkiar este repositorio y trabajar sobre el mismo. Cuando ya lo tengas
creado y subido a alguna plataforma (gitlab o github), danos el acceso para poder verlo.
Cuando esté listo para revisar, enviarnos un e-mail con el url al repositorio y todas las
aclaraciones que tengas.


# Contacto

En cualquier momento, contactarse con nosotros para eliminar cualquier tipo de duda o problema
que posea. Esto no es un periodo de evaluación unicamente, sino que también es de aprendizaje.

* Andres Demski: ademski@novo.space

---

*May the force be with you!*
