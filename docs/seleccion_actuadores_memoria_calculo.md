# Revisión de arquitectura y base de cálculo — actuador vibratorio

**Fecha:** 2026-10-14  
**Estado:** Base de diseño revisada; selección de motor y controlador aún por cerrar.  
**No usar como selección final:** el primer borrador generado con woofer quedó descartado porque no representa la arquitectura acordada.

## 1. Fuentes y decisiones

### Antecedente encontrado
El informe anterior del proyecto propone un **motor con masa excéntrica**, una medición de vibración mediante MPU-6050 y un PLC Siemens S7-1200 como controlador central. Ese documento indica una banda histórica de 10–200 Hz y 0,5–5 g. La documentación histórica además mezcla la expresión “motor DC” con “variador de frecuencia”; esa combinación debe aclararse antes de seleccionar hardware porque el accionamiento depende de si el motor es DC o AC.

### Requisito vigente de diseño
- Frecuencia mecánica de vibración: **10–300 Hz obligatorios**.
- Alimentación nominal de diseño en Perú: **220 V AC, 60 Hz**. El unifilar preliminar representa entrada monofásica L–N–PE porque así está dibujada la toma en EL-04; confirmar físicamente la configuración de la toma antes de seleccionar el VFD, pues también existen suministros de 220 V trifásicos.
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

El dato de diseño de entrada es 220 V AC, 60 Hz. La hoja EL-04 representa una toma monofásica L–N–PE, que se utilizará como hipótesis de diseño del unifilar preliminar. Antes de comprar el VFD debe verificarse la toma real en laboratorio, ya que el valor nominal de 220 V no determina por sí mismo el número de fases. También se requieren los datos de placa del motor para dimensionar el accionamiento.

- Arquitectura candidata: red de 220 V AC → VFD compatible con el suministro y el motor → motor AC con masa excéntrica.
- Si el suministro de laboratorio es monofásico de 220 V y se selecciona un motor trifásico de 220 V, el VFD debe especificar entrada monofásica de 220 V y salida trifásica apropiada; revisar además la posible reducción de capacidad del VFD cuando trabaja con entrada monofásica.
- El PLC entrega la consigna por una interfaz soportada en ambos equipos (p. ej., 0–10 V solo si ambos disponen de ella, o comunicación industrial compatible) y señales digitales de marcha/permiso, parada, reset y estado/fallo. Las salidas de potencia del PLC no alimentan directamente el motor.
- Se dimensionan VFD, protección y cableado a partir de tensión, fases, corriente, potencia, velocidad y par nominales del motor y de la sobrecarga requerida.
- El PLC debe registrar consigna y aceleración real. Para validar vibración hasta 300 Hz, el ancho de banda y la frecuencia de muestreo deben ser adecuados; una actualización de 10 Hz (o un dato cada 100 ms) no puede caracterizar correctamente una vibración de 300 Hz. La interfaz de adquisición del acelerómetro debe ser compatible con el PLC y tener velocidad suficiente.

## 6. Criterios de selección pendientes de resolver

| Decisión/dato | Por qué se necesita |
|---|---|
| Ficha exacta de motor AC y VFD compatible con 220 V AC, 60 Hz | La preferencia de arquitectura es AC + VFD; verificar que el VFD acepta la configuración monofásica representada en el plano y entrega la salida requerida por el motor, además de velocidad mecánica, potencia, corriente y protocolo de control. |
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


## 8. Planos eléctricos preliminares — revisión A (2026-10-14)

Se elaboraron dos hojas A3 separando la distribución de potencia del cableado de campo:

- **EL-04 — Diagrama unifilar del gabinete:** entrada nominal de diseño 220 V AC, 60 Hz; seccionamiento y protección general; ramal de VFD/motor; ramal H-101 de 220 V AC con SSR y termostato independiente; fuente preliminar 24 V DC/15 A; distribución de 24 V de control y de actuadores, con corte de seguridad.
- **EL-05 — Interconexión gabinete–banco:** identifica gabinete CE-01 y banco BE-01 como equipos físicamente independientes, cables C01–C09, terminales de campo y rutas separadas para potencia, 24 V DC, RTD, aceleración, sensores PNP y cadena de seguridad.

Los planos tienen estado **PRELIMINAR PARA REVISIÓN**, no están liberados para fabricar/cablear. Los valores nominales de protecciones y secciones de conductor no se rellenaron porque aún no se dispone de los datos definitivos de placa del motor/VFD ni del cálculo de cortocircuito y condiciones de instalación.

### Decisiones de diseño reflejadas

- Arquitectura candidata de vibración: motor AC con masa excéntrica, VFD en el gabinete y mando desde PLC.
- La hoja EL-04 presupone entrada L–N–PE monofásica de 220 V, 60 Hz como aparece en el esquema de toma de la hoja electrónica existente; verificar físicamente la toma antes de seleccionar el VFD.
- Para un ciclo mecánico por revolución, 300 Hz implican 18 000 rpm. La velocidad máxima autorizada del conjunto motor/rotor y la frecuencia de salida del VFD deben validarse con las fichas del fabricante antes de considerar viable la solución.
- La CPU S7-1200 1214C DC/DC/DC referida en los planos tiene dos entradas analógicas y ninguna salida analógica integrada. Si se usa consigna 0–10 V al VFD, se necesita un módulo AQ; como alternativa, puede estudiarse una interfaz de comunicación compatible con el PLC y el modelo final de VFD.
- El canal de vibración se especifica como medición de aceleración RMS acondicionada con ancho de banda adecuado. Una lectura de tendencia a 10 Hz no sirve por sí sola para muestrear directamente una onda vibratoria de 300 Hz.
- El paro de emergencia debe implementarse mediante una cadena cableada y elementos compatibles con la evaluación de riesgos; el software del PLC no se considera el único medio de parada. La conexión a STO depende de que el VFD seleccionado disponga de esa función y de las instrucciones del fabricante.
- La fuente de 24 V DC/15 A permanece como candidata. El presupuesto anterior incluía el amplificador del woofer ya descartado; debe recalcularse con la nueva instrumentación, la cama caliente y las cargas finales.

### Entregables creados

- EL-04_Unifilar_gabinete_RevA.svg
- EL-05_Interconexion_gabinete_banco_RevA.svg
- Planos_unifilar_interconexion_RevA.pdf

Las fuentes SVG se conservan para editar las figuras vectoriales. Se debe actualizar la revisión del plano después de cerrar: modelo del motor, motor/VFD compatibles con el requisito de 10–300 Hz, módulo de salida PLC o comunicación seleccionada, sensor/acondicionador de aceleración, carga real de 24 V, dispositivos de protección, conductores y conectores de campo.


## 9. Cálculos de diseño — revisión 0.01 (2026-10-14)

La imagen compartida del esquema de conexión de la CPU S7-1200 se trata como **referencia gráfica preliminar v0.01** para el cableado de bornes; no reemplaza el diagrama unifilar de potencia ni el plano de interconexión gabinete–banco.

### Base actual
- Alimentación de diseño: 220 V AC, 60 Hz.
- Arquitectura candidata: motor AC con masa excéntrica y VFD ubicado en el gabinete; PLC/HMI envían consigna y órdenes por una interfaz compatible.
- Banda de vibración mecánica obligatoria: 10–300 Hz.
- La aceleración 0,5–5 g se mantiene solo como antecedente histórico, porque la versión anterior del informe la indicaba para 10–200 Hz y no definía si era pico o RMS. Los cálculos cinemáticos de esta revisión suponen valor pico únicamente como escenario de referencia.
- Hipótesis cinemática: una oscilación fundamental por revolución.

### Tabla de relación cinemática
`n = 60 f_v`, `ω = 2π f_v`, `x_pk = a_pk/ω²`.

| f_v (Hz) | n equivalente (rpm) | ω (rad/s) | x_pk a 0,5 g pico (mm) | x_pk a 5 g pico (mm) |
|---:|---:|---:|---:|---:|
| 10 | 600 | 62.83 | 1.2420 | 12.4203 |
| 50 | 3 000 | 314.16 | 0.0497 | 0.4968 |
| 100 | 6 000 | 628.32 | 0.0124 | 0.1242 |
| 200 | 12 000 | 1 256.64 | 0.0031 | 0.0311 |
| 300 | 18 000 | 1 884.96 | 0.0014 | 0.0138 |

El límite de 300 Hz corresponde a 18 000 rpm con excitación 1× por revolución. Debe validarse por ficha del fabricante para motor, rotor/excentricidad, rodamientos, equilibrado y operación a frecuencia elevada; no se asume que un VFD que permita configurar 300 Hz garantice la seguridad mecánica.

### DCL y modelo dinámico
Para un modelo equivalente de un grado de libertad, midiendo x desde el equilibrio estático:

`M x¨ + c x˙ + k x = F_{e,pk} sin(ωt)`

`F_{e,pk} = m_e e ω²`

`X = F_{e,pk} / sqrt[(k − Mω²)² + (cω)²]`; `a_pk = ω² X`.

Donde M es la masa móvil total, m_e la masa excéntrica, e la excentricidad, k la rigidez y c el amortiguamiento equivalente. Estos cuatro parámetros todavía no están definidos. No se debe proponer una masa excéntrica ni potencia de motor a partir de una aceleración sin resolver el DCL y validar la respuesta de la plataforma.

Para un momento de desequilibrio fijo U = m_e e, la fuerza ideal de desequilibrio aumenta con ω², por lo que se multiplica por (300/10)² = 900 entre los extremos de la banda. Esto no significa que la aceleración de la plataforma se multiplique exactamente por 900, porque depende de M, k, c, resonancias y montaje; sí evidencia que debe verificarse el rango de aceleración punto a punto y considerar si el desequilibrio debe ser ajustable.

### Selección eléctrica y control
La corriente de entrada no se calcula todavía porque falta potencia nominal del motor, rendimiento, factor de potencia y datos del VFD. Como estimación:

`P_in ≈ P_2/(η_motor η_VFD)`; `I_in ≈ P_2/(V_in η_motor η_VFD PF_in)`

Para el diseño final, priorizar la corriente de entrada indicada por el fabricante del VFD y su tabla de coordinación de protecciones; la ecuación es una comprobación energética, no una sustitución de la ficha técnica.

La CPU 1214C DC/DC/DC especificada tiene 14 DI, 10 DO de 24 VDC y 2 AI de 0–10 V, sin AO integrada. Para la consigna analógica 0–10 V se necesitaría un módulo AQ compatible; alternativamente, se puede elegir una comunicación industrial soportada tanto por el PLC como por el VFD.

### Entregables de cálculo
- `Memoria_calculo_motor_AC_VFD_Rev001.docx`: base de diseño, DCL, relación de frecuencia/velocidad, cálculos de desplazamiento, modelo dinámico y lista de decisiones pendientes.
- `Calculos_motor_AC_VFD_banco_Rev001.xlsx`: hojas `Base_diseno`, `Rango_10_300`, `DCL_dinamica` y `Calculo_electrico`. La hoja DCL queda paramétrica hasta ingresar M, m_e, e, k y c; la hoja eléctrica queda paramétrica hasta ingresar datos nominales del motor y VFD.

### Fuentes técnicas
- Siemens, ficha CPU 1214C DC/DC/DC: https://support.industry.siemens.com/teddatasheet/?caller=SIOS&format=pdf&language=en&mlfbs=6ES7214-1AG40-0XB0
- WEG, manual de instalación/operación/mantenimiento de motores: consultar velocidad máxima mecánica y frecuencia máxima de placa: https://static.weg.net/medias/downloadcenter/h0c/hfd/WEG-WMO-iom-installation-operation-and-maintenance-manual-of-electric-motors-50033244-manual-pt-en-es-web.pdf
- ISO/TR 230-8:2010, sección de vibraciones: fuerza de desequilibrio proporcional al momento de desequilibrio y a ω².
