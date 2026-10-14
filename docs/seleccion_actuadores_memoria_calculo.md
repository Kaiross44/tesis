# Memoria preliminar de cálculo — selección de actuadores del banco

**Fecha:** 2026-10-14  
**Estado:** Revisión 0 — preliminar, no liberada para compra ni como validación de desempeño.  
**Base:** lista de materiales, planos PID y control (12/10/2026), manuscrito español y registro del subproyecto CPS M18.

## 1. Alcance

Dimensionar de manera trazable los subsistemas térmico y vibratorio. Se separan los valores documentados de las hipótesis ilustrativas y de los datos pendientes. El objetivo es definir una selección verificable, no declarar el cumplimiento sin pruebas.

## 2. Datos documentados

| Tag / equipo | Datos en los documentos | Observación de selección |
|---|---|---|
| H-101, calefactor de aire | PTC, 220 VAC, 200 W; aire de cámara 25–80 °C | Se puede estimar la corriente nominal. La suficiencia térmica requiere volumen, aislamiento, masa térmica, pérdidas y tiempo objetivo. |
| FN-101, ventilador | 80 mm, 24 VDC | No se indica curva caudal–presión ni temperatura admisible del motor/rodamiento; solicitar ficha técnica. |
| H-102, superficie caliente | Cama MK2a, 214 × 214 mm, 24 VDC, MOSFET | La opción ideal de la lista señala una placa de silicona de 150 W, pero se debe confirmar el SKU/potencia de la opción elegida. No trasladar automáticamente ese dato. |
| Protección térmica | Dos KSD301 NC de 85 °C; alarma alta de aire a 82 °C | Verificar ubicación y que los termostatos interrumpan físicamente la potencia del calefactor correspondiente. |
| X-201, excitador | Woofer de auto 6,5 in, 4 Ω | Propuesta económica de prototipo. No consta Xmax, fuerza/BL, potencia RMS real ni curva de respuesta. |
| SY-201, amplificador | Módulo TPA3116 anunciado como 2 × 50 W, 12–24 V | Confirmar ficha del módulo, potencia continua a 4 Ω, fuente y disipación. La cifra publicitaria no certifica fuerza vibratoria. |
| P-201, placa | Aluminio ~220 × 160 × 3 mm y cuatro resortes | Se estima solo la masa de la placa. La masa móvil completa y la rigidez de los resortes quedan pendientes. |
| Ensayo vibratorio | Barrido propuesto de 10–300 Hz; aceleración a_rms registrada con ADXL345 + ESP32 | El plano actual describe mando y monitoreo; no da una aceleración objetivo ni demuestra que se alcance el barrido completo. |

## 3. Cálculos térmicos preliminares

### 3.1 H-101 — corriente y resistencia equivalentes

Datos de lista: P = 200 W, V = 220 V AC.

```
I ≈ P/V = 200/220 = 0.91 A
R_eq ≈ V²/P = 220²/200 = 242 Ω
```

Estos son valores de primer orden. Un calentador PTC no debe tratarse como una resistencia constante en todo su rango; revisar la ficha y medir la corriente real. No utilizar estos resultados por sí solos para seleccionar conductores, protección o relé.

El balance térmico preliminar es:

```
Q̇_requerida ≈ [(m_aire c_p,aire) + Σ(m_i c_i)] · ΔT/t + Q̇_pérdidas
```

No se puede demostrar que 200 W sea suficiente hasta definir volumen/altura de CT-100, materiales y espesor de aislamiento, masas internas, fugas/renovación de aire y tiempo máximo para alcanzar consigna. El plano propone estabilidad de ±1 °C, que debe verificarse experimentalmente.

### 3.2 H-102 — área y corriente condicional

```
A = 0.214 × 0.214 = 0.0458 m²
```

Si —y solo si— se confirma una cama de 150 W a 24 V:

```
I = 150/24 = 6.25 A
R_eq ≈ 24²/150 = 3.84 Ω
```

La potencia debe confirmarse antes de cerrar el MOSFET, fusible, sección de cable y fuente. Documentar la referencia exacta y potencia nominal de la opción económica elegida.

## 4. Cálculos preliminares de vibración

### 4.1 Masa de placa sin accesorios

Para placa idealizada de aluminio L = 0.220 m, W = 0.160 m, t = 0.003 m, con densidad típica de cálculo ρ = 2700 kg/m³:

```
V = L·W·t = 1.056 × 10⁻⁴ m³
m_placa = ρ·V ≈ 0.285 kg
```

La masa de 0.285 kg no incluye sensor, adaptador, objetivo, tornillos ni la parte móvil efectiva del transductor. Se debe pesar la configuración montada.

### 4.2 Desplazamiento sinusoidal asociado a aceleración

Para movimiento sinusoidal:

```
a_pk = (2πf)² · x_pk
x_pk = a_pk / (2πf)²
```

Si se ilustra a_pk = 1 g = 9.81 m/s², el desplazamiento pico cinemático requerido es:

| Frecuencia | Desplazamiento pico para 1 g pico |
|---:|---:|
| 10 Hz | 2.49 mm |
| 50 Hz | 0.099 mm |
| 100 Hz | 0.0248 mm |
| 300 Hz | 0.00276 mm |

Esta tabla es una conversión cinemática ilustrativa, no un requisito aprobado ni una predicción del woofer. Para una señal sinusoidal, a_pk = √2 · a_rms. A 10 Hz el recorrido podría ser una restricción importante; a frecuencias altas deben revisarse respuesta dinámica, resonancias, instrumentación y montaje.

### 4.3 Fuerza inercial y frecuencia natural

```
F_inercial,pk = m_móvil · a_pk
```

Ejemplo estrictamente ilustrativo: para masa móvil total de 0.40 kg y 1 g pico, F_inercial,pk = 3.92 N. El cálculo no contempla reacción de resortes, amortiguamiento, pérdidas, resonancia ni límites del transductor; tampoco demuestra que el woofer proporcione esa fuerza a todas las frecuencias.

Para n resortes iguales en paralelo:

```
k_eq = n·k_s
f_n = (1/2π) · √(k_eq/m_móvil)
```

Con cuatro resortes, k_eq = 4 k_s. Obtener la rigidez real de ficha o prueba carga–deflexión; contrastar la frecuencia natural calculada con una prueba modal/barrido de baja amplitud.

## 5. Criterios para cerrar la selección

| Prioridad | Parámetro pendiente | Evidencia para cerrar |
|---|---|---|
| Crítica | Perfil objetivo de a_rms frente a frecuencia y tolerancia | Definir puntos/intervalo, amplitud, permanencia y tolerancia de aceptación. |
| Crítica | Masa móvil total | Pesar la placa con todos los componentes montados y estimar masa efectiva móvil del excitador. |
| Crítica | Xmax y rango útil del woofer | Ficha técnica del transductor; comparar recorrido requerido con recorrido lineal permitido. |
| Crítica | Potencia RMS y respuesta del amplificador a 4 Ω | Ficha del módulo, fuente, disipación y prueba de temperatura/saturación. |
| Alta | Rigidez/amortiguamiento de resortes | Ficha técnica o ensayo de carga–deflexión; verificar frecuencia natural. |
| Alta | Potencia real de H-102 | Referencia exacta de la cama y corriente nominal. |
| Alta | Volumen/aislamiento y pérdidas de CT-100 | Dimensiones internas, espesores/materiales y prueba escalón térmico. |
| Alta | Caudal útil de FN-101 | Curva caudal–presión y mapa de uniformidad térmica. |
| Crítica | Límites térmicos de sensor, adaptador y cables | Fichas de componentes y máxima temperatura admisible. |
| Alta | Rango/ancho de banda de ADXL345 | Configurar tasa de muestreo y verificar con referencia calibrada. |

## 6. Plan mínimo de verificación

1. **Térmico:** prueba escalón por consignas progresivas, registrando T_aire, T_superficie, tiempo de subida, sobreimpulso y error estacionario. No declarar ±1 °C hasta medirlo.
2. **Vibración:** comenzar a baja amplitud, medir a_rms y desplazamiento, inspeccionar fijaciones y temperatura de amplificador/excitador; detener ante golpes o saturación.
3. **Identificación dinámica:** efectuar barrido de bajo nivel para localizar resonancias y comparar con el modelo masa–resorte.
4. **Trazabilidad:** guardar ID de ensayo, configuración B1/B2, temperatura, frecuencia, aceleración, porcentaje de mando, duración, alarmas y archivos brutos. Separar datos medidos de los calculados.

## 7. Conclusión preliminar

La corriente ideal estimada para H-101 es 0.91 A y la masa geométrica de la placa propuesta es aproximadamente 0.285 kg. La selección del woofer, amplificador, resortes y cama caliente aún no puede considerarse cerrada: falta fijar aceleración objetivo, masa móvil real, recorrido permitido, rigidez y fichas técnicas. El conjunto woofer + TPA3116 debe presentarse como prototipo económico pendiente de validación, no como excitador que ya garantiza 10–300 Hz.

**Control de integridad:** los cuatro modelos internos del sensor M18 en el subproyecto FEM son hipótesis geométricas, no reconstrucciones confirmadas del fabricante. El registro actual del subproyecto no demuestra todavía una solución FEM validada; no se usa como prueba de capacidad del actuador.
