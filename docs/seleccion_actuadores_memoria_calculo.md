# Revisión de arquitectura y base de cálculo — actuador vibratorio

**Fecha:** 2026-10-14  
**Estado:** Base de diseño revisada; selección de motor y controlador aún por cerrar.  
**No usar como selección final:** el primer borrador generado con woofer quedó descartado porque no representa la arquitectura acordada.

## 1. Fuentes y decisiones

### Antecedente encontrado
El informe anterior del proyecto propone un **motor con masa excéntrica**, una medición de vibración mediante MPU-6050 y un PLC Siemens S7-1200 como controlador central. Ese documento indica una banda histórica de 10–200 Hz y 0,5–5 g. La documentación histórica además mezcla la expresión “motor DC” con “variador de frecuencia”; esa combinación debe aclararse antes de seleccionar hardware porque el accionamiento depende de si el motor es DC o AC.

### Requisito vigente de diseño
- Frecuencia mecánica de vibración: **10–300 Hz obligatorios**.
- Alimentación disponible: **220 V AC**; número de fases de la red por confirmar.
- Arquitectura candidata adoptada para los cálculos: **motor AC industrial + VFD**, con mando desde el PLC. Se considera una decisión preliminar de arquitectura, no una selección final de motor/variador.
- La referencia desde PLC podrá ser analógica (p. ej., 0–10 V, si el PLC y el VFD tienen esa interfaz) o mediante comunicación industrial compatible. El PLC realiza mando/monitorización; no alimenta directamente el motor.
- La aceleración de ensayo se debe justificar desde los requisitos de caracterización y validarse contra la capacidad real del conjunto. El antiguo rango 0,5–5 g se conserva como antecedente hasta confirmar si continúa vigente y si la magnitud es pico o RMS.
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

Por ello, 300 Hz no significa simplemente configurar 300 Hz en el PLC o en el VFD. Si la plataforma recibe un ciclo vibratorio por revolución, el motor debe alcanzar 18 000 rpm mecánicas y estar certificado por el fabricante para esa velocidad, rodamientos y carga excéntrica. Como referencia, una guía técnica de WEG para motores estándar accionados por variador da límites de velocidad mecánica según bastidor y número de polos; muchos motores estándar están muy por debajo de 18 000 rpm. Por tanto, la arquitectura motor AC + VFD queda como candidata económica, pero no puede darse por válida hasta encontrar un motor cuyo fabricante autorice esa velocidad o justificar una conversión mecánica de frecuencia diferente. La fuerza de desequilibrio aumenta con el cuadrado de la velocidad.

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

El dato de 220 V AC se incluye explícitamente en la selección, pero por sí solo no determina la potencia o capacidad del accionamiento. Se requieren datos de placa del motor y debe confirmarse si el suministro disponible es monofásico o trifásico.

- Arquitectura candidata: red de 220 V AC → VFD compatible con el suministro y el motor → motor AC con masa excéntrica.
- Si el suministro de laboratorio es monofásico de 220 V y se selecciona un motor trifásico de 220 V, el VFD debe especificar entrada monofásica de 220 V y salida trifásica apropiada; revisar además la posible reducción de capacidad del VFD cuando trabaja con entrada monofásica.
- El PLC entrega la consigna por una interfaz soportada en ambos equipos (p. ej., 0–10 V solo si ambos disponen de ella, o comunicación industrial compatible) y señales digitales de marcha/permiso, parada, reset y estado/fallo. Las salidas de potencia del PLC no alimentan directamente el motor.
- Se dimensionan VFD, protección y cableado a partir de tensión, fases, corriente, potencia, velocidad y par nominales del motor y de la sobrecarga requerida.
- El PLC debe registrar consigna y aceleración real. Para validar vibración hasta 300 Hz, el ancho de banda y la frecuencia de muestreo deben ser adecuados; una actualización de 10 Hz (o un dato cada 100 ms) no puede caracterizar correctamente una vibración de 300 Hz. La interfaz de adquisición del acelerómetro debe ser compatible con el PLC y tener velocidad suficiente.

## 6. Criterios de selección pendientes de resolver

| Decisión/dato | Por qué se necesita |
|---|---|
| Ficha exacta de motor AC y VFD compatible con 220 V AC | La preferencia de arquitectura es AC + VFD; faltan tipo de red, fases, velocidad mecánica segura, potencia, corriente y protocolo de control. |
| Velocidad mecánica segura para generar hasta 300 Hz | Con excitación 1× por revolución, se requieren 18 000 rpm; confirmar por ficha del fabricante o justificar otro mecanismo excitador. |
| Masa móvil total medida | Convierte aceleración requerida en fuerza dinámica necesaria. |
| Perfil de aceleración deseado frente a frecuencia y convención pico/RMS | Evita confundir capacidad del actuador con requisito de ensayo. |
| Masa excéntrica (m_e) y excentricidad (e), fija o regulable | Define el momento de desequilibrio y la fuerza excitadora. |
| Rigidez (k), amortiguamiento (c), recorrido admisible y geometría de guías | Define la respuesta de la plataforma y previene interferencias mecánicas. |
| Tensión/fases, potencia, corriente, velocidad y par nominales | Permite escoger accionamiento compatible con 220 V AC y dimensionar protecciones. |
| Interfaz de mando VFD–PLC y feedback de aceleración | Permite ajustar velocidad desde PLC/HMI y medir aceleración con ancho de banda suficiente para 300 Hz. |

## 7. Criterio para cumplir la rúbrica

La memoria final deberá mostrar el DCL etiquetado, la conversión de frecuencia a rpm, el cálculo de fuerza por desequilibrio, la dinámica masa–resorte–amortiguador, la selección del motor y accionamiento según la alimentación de 220 V, la interfaz PLC, y una tabla de verificación que demuestre el cumplimiento de 10, 50, 100, 200 y 300 Hz en condiciones especificadas. El análisis modal puede servir para validar resonancias, pero no se utiliza para reducir el requisito de frecuencia.

**Límite actual:** se adopta AC + VFD como arquitectura candidata por preferencia de coste, pero no se afirma todavía que sea la opción final más económica ni que cumpla 10–300 Hz. Faltan número de fases de la red, ficha del motor/VFD, velocidad mecánica segura, masa móvil, masa excéntrica/excentricidad y perfil de aceleración de diseño.
