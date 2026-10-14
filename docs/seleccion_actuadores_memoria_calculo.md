# Revisión de arquitectura y base de cálculo — actuador vibratorio

**Fecha:** 2026-10-14  
**Estado:** Base de diseño revisada; selección de motor y controlador aún por cerrar.  
**No usar como selección final:** el primer borrador generado con woofer quedó descartado porque no representa la arquitectura acordada.

## 1. Fuentes y decisiones

### Antecedente encontrado
El informe anterior del proyecto propone un **motor con masa excéntrica**, una medición de vibración mediante MPU-6050 y un PLC Siemens S7-1200 como controlador central. Ese documento indica una banda histórica de 10–200 Hz y 0,5–5 g. La documentación histórica además mezcla la expresión “motor DC” con “variador de frecuencia”; esa combinación debe aclararse antes de seleccionar hardware porque el accionamiento depende de si el motor es DC o AC.

### Requisito vigente de diseño
- Frecuencia mecánica de vibración: **10–300 Hz obligatorios**.
- Alimentación disponible del sistema: **220 V AC**.
- El motor y su etapa de potencia/control deben integrarse al PLC (consigna, marcha/permiso, parada, alarma/estado y realimentación).
- La aceleración de ensayo se debe derivar de los requisitos de caracterización y de la capacidad demostrada del conjunto; el antiguo rango 0,5–5 g se conserva como antecedente de diseño, no como decisión final automática.
- La propuesta económica de la lista de materiales de octubre que utiliza woofer/TPA3116/ESP32 queda descartada para la selección actual.

## 2. Relación entre frecuencia mecánica y velocidad del motor

Para un actuador rotativo con una excitación por revolución:

```
f_v = n/60
n = 60 f_v
```

| Frecuencia mecánica | Velocidad de giro equivalente |
|---:|---:|
| 10 Hz | 600 rpm |
| 50 Hz | 3000 rpm |
| 100 Hz | 6000 rpm |
| 200 Hz | 12000 rpm |
| 300 Hz | 18000 rpm |

Por ello, 300 Hz no significa simplemente configurar 300 Hz en un PLC o en un variador. Si la plataforma recibe un ciclo vibratorio por revolución, el motor debe alcanzar 18 000 rpm mecánicas y estar certificado por el fabricante para esa velocidad, rodamientos y carga excéntrica. Un motor industrial estándar no se debe llevar a esa velocidad por asumir que el variador lo permite. La relación se documenta en manuales de motores vibratorios industriales y la fuerza depende del desequilibrio y del cuadrado de la velocidad.

## 3. Diagrama de cuerpo libre (DCL) de la plataforma

Modelo unidimensional simplificado en el eje de ensayo. La coordenada (x(t)) se mide respecto de la posición de equilibrio estático, por lo que el peso queda compensado por la precarga/reacción estática:

- (M): masa móvil total (placa + sensor + adaptador + fijaciones + parte móvil asociada).
- (F_e(t)): componente de fuerza de excitación transmitida por la masa excéntrica.
- (k): rigidez equivalente de la suspensión/guías.
- (c): amortiguamiento equivalente.
- (x,dot{x},ddot{x}): desplazamiento, velocidad y aceleración de la plataforma.

```
             F_e(t) = U·ω²·sin(ωt)
                         ↑
                  ┌───────────┐
                  │ plataforma│    x(t)
                  │     M     │
                  └───────────┘
                    ↓  k·x       reacción elástica
                    ↓  c·ẋ      reacción amortiguadora
              (peso Mg equilibrado en x = 0 estático)
```

La masa excéntrica produce una fuerza centrífuga de amplitud:

```
U = m_e·e
ω = 2π f_v
F_e,pk = m_e·e·ω² = U·(2π f_v)²
```

donde (m_e) es la masa excéntrica y (e) es su excentricidad.

El DCL lleva a la ecuación dinámica linealizada:

```
M·ẍ + c·ẋ + k·x = F_e,pk·sin(ωt)
```

Para una excitación sinusoidal, la amplitud estacionaria del modelo masa–resorte–amortiguador es:

```
X = F_e,pk / √[(k − M·ω²)² + (c·ω)²]
a_pk = ω²·X
```

La aproximación de fuerza inercial (F_{req,pk}=M a_{target,pk}) sirve como primera comprobación, pero no sustituye el cálculo de la respuesta dinámica cerca de resonancia ni la verificación de rigidez, amortiguamiento y límites de desplazamiento.

## 4. Consecuencia de conservar el rango histórico de aceleración

La banda anterior de 0,5–5 g no especificaba claramente si se trataba de valor pico o RMS. Antes de dimensionar se debe definir la convención. Si se usa como ejemplo una aceleración pico de 0,5–5 g, la relación cinemática es:

```
x_pk = a_pk / (2π f_v)²
```

| Frecuencia | Desplazamiento pico a 0,5 g pico | Desplazamiento pico a 5 g pico |
|---:|---:|---:|
| 10 Hz | 1,24 mm | 12,4 mm |
| 50 Hz | 0,0497 mm | 0,497 mm |
| 100 Hz | 0,0124 mm | 0,124 mm |
| 200 Hz | 0,00311 mm | 0,0311 mm |
| 300 Hz | 0,00138 mm | 0,0138 mm |

Son implicaciones cinemáticas del requisito histórico, no resultados de un motor seleccionado. Si los valores solicitados fueran RMS sinusoidal, (a_{pk}=\sqrt{2}\,a_{rms}). Esta tabla muestra por qué deben verificarse tanto el recorrido disponible en el extremo bajo como las fuerzas, el equilibrado y los límites mecánicos en el extremo alto.

Con masa excéntrica fija, la fuerza generada escala como (f_v^2). Por tanto, la aceleración no será independiente de la frecuencia sin ajustes de desequilibrio, modificación de la masa efectiva/estructura o una estrategia de amplitud con realimentación y autoridad suficiente. El acelerómetro mide la respuesta real; no garantiza por sí mismo que el actuador pueda alcanzarla.

## 5. Alimentación de 220 V y cadena de mando PLC

El dato de 220 V AC debe ser una entrada explícita para la selección del controlador/accionamiento, pero no basta para determinar su tamaño. Hay que conocer la tensión, corriente, potencia, velocidad y par nominales del motor.

- **Si es motor AC:** 220 V AC alimentan el variador compatible; el variador entrega la salida adecuada al motor. El PLC entrega la consigna por una interfaz realmente soportada (por ejemplo, 0–10 V/4–20 mA o bus industrial) y señales digitales de permiso/estado.
- **Si es motor DC:** 220 V AC alimentan un accionamiento DC apropiado, que genera la tensión/corriente DC variable para el motor. Un variador AC convencional no se conecta directamente a un motor DC.
- En ambas arquitecturas, las salidas de potencia del PLC no alimentan el motor directamente. Se dimensionan accionamiento, protección y cableado a partir de los datos de placa y las condiciones de carga; se especifican parada de emergencia, inhibición segura y reporte de fallo.
- El PLC debe registrar el setpoint solicitado y la aceleración real. Para evaluar vibración hasta 300 Hz, el canal de adquisición debe tener una frecuencia de muestreo y ancho de banda adecuados; la actualización de una variable cada 100 ms no equivale a muestrear una señal vibratoria a esa tasa.

## 6. Criterios de selección pendientes de resolver

| Decisión/dato | Por qué se necesita |
|---|---|
| Tipo de motor acordado: AC con variador o DC con accionamiento DC | Cambia la etapa de potencia, señal PLC, cálculos eléctricos y gama de motores posibles. |
| Modelo o clase de motor capaz de 18 000 rpm si la excitación es 1× por revolución | Es requisito cinemático para 300 Hz; confirmar certificación de velocidad y montaje de excentricidad. |
| Masa móvil total medida | Convierte aceleración requerida en fuerza dinámica necesaria. |
| Perfil de aceleración deseado frente a frecuencia y convención pico/RMS | Evita confundir capacidad del actuador con requisito de ensayo. |
| Masa excéntrica (m_e) y excentricidad (e), fija o regulable | Define el momento de desequilibrio y la fuerza excitadora. |
| Rigidez (k), amortiguamiento (c), recorrido admisible y geometría de guías | Define la respuesta de la plataforma y previene interferencias mecánicas. |
| Tensión/fases, potencia, corriente, velocidad y par nominales | Permite escoger accionamiento compatible con 220 V AC y dimensionar protecciones. |
| Interface de referencia y feedback soportada por PLC/accionamiento | Permite controlar frecuencia y registrar estados desde PLC/HMI. |

## 7. Criterio para cumplir la rúbrica

La memoria final deberá mostrar el DCL etiquetado, la conversión de frecuencia a rpm, el cálculo de fuerza por desequilibrio, la dinámica masa–resorte–amortiguador, la selección del motor y accionamiento según la alimentación de 220 V, la interfaz PLC, y una tabla de verificación que demuestre el cumplimiento de 10, 50, 100, 200 y 300 Hz en condiciones especificadas. El análisis modal puede servir para validar resonancias, pero no se utiliza para reducir el requisito de frecuencia.

**Límite actual:** no declarar seleccionado ningún modelo de motor/driver ni afirmar cumplimiento de 10–300 Hz hasta resolver el tipo de motor, los datos eléctricos/mecánicos y la fuerza/aceleración de diseño.
