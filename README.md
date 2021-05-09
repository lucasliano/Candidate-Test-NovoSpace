# Solución

## Dependencias

**Nota:** En mi caso decidí no utilizar venv.

```
pip install bitstring
```

## Planificación

### Primera parte (Actualmente 4 días)

* [x] Leer la consigna del ejercicio 1 detalladamente
	* [x] Consultar las dudas al respecto.
* [x] Instalar las dependencias para correr el código de ejemplo
	* [x] nMigen
	* [x] cocotb
	* [x] GTKWave
	* [x] iverilog
* [x] Investigar sobre las herramientas a desarrollar (¿Pára que sirven? ¿Cómo se utilizan? ¿Buenas prácticas?)
	* [x] nMigen
	* [x] cocotb
* [x] Ejecutar scripts de ejemplo y sacar conclusiones.
* [x] Replanificar el desarrollo de la solución del primer ejercicio
* [ ] Solución ejercicio 1:
	* [x] Plantear el circuito digital correspondiente
	* [x] Verificar que no haya problemas con la instanciación
	* [x] Simular el comportamiento
	* [ ] Hacer tests!
		* [x] Reset
		* [x] Sumas, Restas
			* [x] Hacer función toCA2()
		* [x] Desbordamiento
		* [x] Burst tests
		* [x] Entradas a destiempo
		* [ ] No r_ready en la salida
		* [x] Evaluar el comportamiento para adders con distinta cantidad de bits
	* [x] Documentar!
		* [x] Consultar herramienta y idioma de preferencia!
		* [x] Comentar el código correspondiente a módulo
		* [x] Comentar el código correspondiente a los tests.
	* [x] Debuggear (Por el momento sin bugs)



### Segunda parte (2 días máximo)
* [x] Leer la consigna del ejercicio 2 detalladamente
	* [x] Consultar las dudas al respecto.
* [x] Investigar sobre las herramientas
	* [x] Sintaxis de Verilog
	* [x] Correcto uso de regular expresions
* [x] Solución ejercicio 2:
	* [x] Generar un regex para cada linea a analizar
	* [x] Crear lógica de funcionamiento
	* [x] Gestión de archivos
		* [x] Verificar buenas practicas
	* [x] Debuggear
	* [x] Documentar código
	* [x] Testear
		* [x] Investigar sobre PyTest
		* [x] Generar dos tests
			* [x] Para archivo Verilog
			* [x] Para archivo de mapa de memoria

# Contacto

* Lucas Liaño: lliano@frba.utn.edu.ar
