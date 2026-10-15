# Memoria de cálculo y selección de componentes

**Proyecto:** Banco de pruebas para caracterización de sensores capacitivos industriales bajo vibración y temperatura  
**Alimentación nominal de diseño:** 220 V AC, 60 Hz  
**Control central propuesto:** Siemens SIMATIC S7-1200 G2 con módulo analógico  
**Rango mecánico requerido:** 10–300 Hz

## 1. Arquitectura y límites de diseño

El banco y el gabinete eléctrico son equipos físicos independientes. El gabinete contiene seccionamiento y protecciones, VFD, fuente auxiliar de 24 V DC, PLC, módulo analógico y bornes. El banco contiene el motor/excitador, plataforma, cámara térmica, calefactores y sensores.

El rango de vibración mecánica de 10–300 Hz es un requisito funcional y no se reducirá por los resultados de un análisis modal. La aceleración de 0,5–5 g aparece en los antecedentes de diseño, pero debe confirmarse si sigue siendo requisito y si se expresa en pico o RMS. No debe asumirse que 5 g tienen que lograrse en cada punto de frecuencia sin definir el perfil de ensayo.

## 2. Selección del actuador vibratorio

Para un excitador que genera un ciclo mecánico por revolución:

```
n = 60 f_v
ω = 2π f_v
x_pk = a_pk / ω²
F_e,pk = m_e e ω²
```

| Frecuencia mecánica | Velocidad equivalente | Desplazamiento pico a 0,5 g | Desplazamiento pico a 5 g |
|---:|---:|---:|---:|
| 10 Hz | 600 rpm | 1,242 mm | 12,420 mm |
| 50 Hz | 3 000 rpm | 0,0497 mm | 0,4968 mm |
| 100 Hz | 6 000 rpm | 0,0124 mm | 0,1242 mm |
| 200 Hz | 12 000 rpm | 0,00311 mm | 0,0311 mm |
| 300 Hz | 18 000 rpm | 0,00138 mm | 0,0138 mm |

El modelo de un grado de libertad para la plataforma, midiendo el desplazamiento respecto al equilibrio estático, es:

```
M·ẍ + c·ẋ + k·x = F_e,pk·sin(ωt)
X = F_e,pk / √[(k − M·ω²)² + (c·ω)²]
a_pk = ω²·X
```

Los parámetros M (masa móvil), k (rigidez equivalente), c (amortiguamiento), m_e (masa excéntrica) y e (excentricidad) deben fijarse a partir de la geometría CAD, masa pesada y requisitos de ensayo. Para una masa móvil ilustrativa de 0,50 kg, la fuerza inercial ideal requerida es 2,45 N a 0,5 g pico y 24,5 N a 5 g pico. Ese valor de masa es un ejemplo de cálculo, no un dato medido.

Un desequilibrio fijo no garantiza por sí solo un nivel de aceleración constante entre 10 y 300 Hz: la fuerza ideal de desequilibrio escala con el cuadrado de la velocidad angular. Debe especificarse el perfil de aceleración frente a frecuencia y validar la respuesta real de la plataforma.

### Candidato económico para desarrollar el excitador

| Componente | Oferta publicada | Importe | Condiciones |
|---|---|---:|---|
| Husillo AC CNC enfriado por agua, 1,5 kW, ER11, 220 V, 400 Hz, hasta 24 000 rpm | CNC.PE | S/ 1 350 | No incluye bomba ni circuito de refrigeración. Confirmar por escrito corriente, velocidad mínima, operación continua y compatibilidad con carga excéntrica. |
| VFD BEST FC300, 1,5 kW, entrada 220 V AC monofásica, salida 220 V AC trifásica, 7 A | CNC.PE | S/ 839 | Verificar corriente de placa, referencia de velocidad externa, entrada 0–10 V o comunicación, y parámetros para el motor exacto. |
| Subtotal husillo + VFD | Precio publicado combinado | **S/ 2 189** | No incluye refrigeración, rotor, rodamientos, contención, montaje, protección eléctrica ni pruebas. |

Fuentes:
- Husillos CNC enfriados por agua: https://cnc.pe/categoria-de-productos/motores-y-electronica-de-potencia/motore-spindle-enfriado-por-agua/
- VFD BEST FC300 de 1,5 kW: https://cnc.pe/producto/variador-de-frecuencia-best-e300-1-5kw-220v-vfd-para-cnc/
- VFD BEST FC300 de 2,2 kW: https://cnc.pe/producto/variador-de-frecuencia-best-fc300-2-2kw-220v-para-cnc/

**Condición de compra:** se trata de un accionamiento candidato para desarrollar un excitador propio, no de una mesa vibratoria lista para instalar ni de un conjunto ya certificado para 10–300 Hz y 0,5–5 g. Antes de comprar se debe confirmar el régimen mecánico continuo de 600–18 000 rpm y el torque disponible. El rotor excéntrico debe diseñarse y apoyarse en rodamientos propios, con equilibrado y carcasa de contención. No montar una masa desbalanceada directamente en la pinza ER del husillo. Si el proveedor no confirma el régimen de velocidad y carga requerido, no se debe construir el excitador con esa alternativa.

Como alternativa comercial de ensayo, los shakers electrodinámicos tienen bandas superiores a 300 Hz, pero los equipos publicados de laboratorio resultan mucho más caros (referencias de importación en decenas de miles de dólares). Los vibradores económicos de concreto consultados no alcanzan 300 Hz por ficha, por lo que no son sustitutos válidos.

## 3. Calefactor de aire H-101

Base del plano EL-01: calefactor aletado PTC de 220 V AC y 200 W, SSR, transmisor PT100 de 0–10 V y termostato KSD301 NC de 85 °C como límite independiente.

```
I_nom ≈ P/V = 200/220 = 0,91 A
R_eq ≈ V²/P = 220²/200 = 242 Ω
```

La resistencia equivalente corresponde al punto nominal; no implica que un PTC conserve una resistencia constante al variar la temperatura.

Para calentar únicamente el aire de 25 a 75 °C (ΔT = 50 K), con ρ_air = 1,18 kg/m³ y c_p = 1005 J/(kg·K):

```
Q_air = ρ_air·V_c·c_p·ΔT
Q_air ≈ 59,3 kJ por m³ de aire
t_ideal ≈ 4,94 min por m³, con 200 W
```

Es un límite ideal que excluye chasis, aislamiento, útiles, infiltraciones, aperturas, puentes térmicos y pérdidas de calor. No demuestra que 200 W sean suficientes para la cámara real.

**Compra:** no se encontró disponibilidad pública fiable del elemento PTC aletado de 220 V/200 W con la geometría exacta. Resister Perú fabrica resistencias industriales a medida y sensores de temperatura; solicitar cotización de una resistencia aletada para aire forzado, 220 V AC, 200 W, con terminales protegidos y datos de temperatura admisible: https://www.resisterperu.com.pe/. El SSR debe seleccionarse para carga resistiva de 220 V AC, entrada compatible con la señal de control de 24 V DC y corriente efectiva con disipador. El termostato de seguridad debe abrir de forma independiente.

## 4. Superficie caliente H-102

El plano indica una cama MK2A de 214 × 214 mm a 24 V DC y una resistencia equivalente anotada de aproximadamente 3,4 Ω; confirmar la referencia exacta antes de comprar.

```
I_nom = 24/3,4 = 7,06 A
P_nom = 24²/3,4 = 169,4 W
A = 0,214 × 0,214 = 0,0458 m²
P/A ≈ 3,70 kW/m²
```

El anuncio de cama caliente MK2B consultado en Mercado Libre cuesta S/ 70, pero declara 500 W y resistencia entre 0,9 y 1,5 Ω. A 24 V, esos valores implican aproximadamente 16–26,7 A y 384–640 W, por lo que **no debe comprarse como sustituto** del calefactor de 150–170 W previsto.

Fuente de la publicación incompatible: https://www.mercadolibre.com.pe/cama-caliente-mk2b--termistor-impresora-3d-1224v-arduino/up/MPEU2458297157

Solicitar a un fabricante local una placa de 24 V DC, 150–180 W, resistencia nominal cercana a 3,2–3,8 Ω, área activa aproximada de 214 × 214 mm y sensor térmico fijado a la superficie. El MOSFET debe seleccionarse con margen de corriente continua después de considerar temperatura, disipador, terminales y resistencia de conducción; el módulo D4184 de los planos no debe aceptarse únicamente por un valor de corriente publicitado.

## 5. Ventilador y alimentación de 24 V DC

| Componente | Referencia publicada | Precio | Condición |
|---|---|---:|---|
| Ventilador | Commonwealth FP-108D-24VDC, 80 × 80 × 25 mm, 24 V, 0,13 A, 40 CFM | S/ 22 | Verificar temperatura máxima admisible y colocación respecto a la cámara caliente. |
| Fuente auxiliar | PEPTEL PE-360-24V, 24 V DC, 15 A, 360 W | S/ 135,28 | Confirmar hoja técnica y recalcular consumo de PLC/HMI, cama caliente, sensores y ventilador. |

Fuentes:
- Ventilador Bracsan: https://bracsan.pe/producto/ventilador-24vdc-0-13a-80x80x25mm-commonwealth-fp-108d-24vdc/
- Fuente PEPTEL en Mercado Libre: https://www.mercadolibre.com.pe/fuente-de-poder-switching-24v-15a-360w/up/MPEU2457628503

El subtotal publicado de husillo + VFD + ventilador + fuente es S/ 2 346,28. No incluye bomba/depósito/mangueras del husillo, excitador fabricado a medida, calefactores compatibles, PLC/módulo analógico, protecciones, instrumentación, chasis, fabricación, cableado ni transporte.

## 6. Materiales del chasis y cámara

| Elemento | Material candidato | Propiedades típicas de cálculo | Verificación necesaria |
|---|---|---|---|
| Bastidor fijo | Acero S235JR o ASTM A36 | E ≈ 200–210 GPa; ρ ≈ 7850 kg/m³; α ≈ 12 µm/(m·K) | Sección, flecha, tensión, uniones soldadas/pernadas, corrosión, fatiga y respuesta dinámica. |
| Plataforma móvil / placa caliente | Aluminio 6061-T6 | E ≈ 68,3 GPa; ρ ≈ 2710 kg/m³; k ≈ 152 W/(m·K); c_p ≈ 879 J/(kg·K); α ≈ 22,7 µm/(m·K) | Rigidez, planitud, masa móvil, fijaciones, expansión y modos propios. |
| Paredes de cámara | Chapa de acero con acabado anticorrosivo | Espesor y geometría pendientes de CAD | Deformación local, sellos, soportes y accesibilidad de mantenimiento. |
| Aislamiento | Lana mineral con recubrimiento apto | λ ≈ 0,037 W/(m·K) como valor preliminar, sujeto al producto | Temperatura admisible del producto completo, cara, adhesivo, juntas y puentes térmicos. |
| Gabinete eléctrico | Envolvente metálica puesta a tierra | Separado del volumen caliente y de la parte móvil | PE, ventilación/derating del VFD, grado IP y separación potencia/señal. |

La dilatación térmica se calcula mediante:

```
ΔL = α·L·ΔT
```

Para ΔT = 50 K:
- Aluminio 6061-T6 de 214 mm: ΔL ≈ 0,243 mm.
- Acero de 214 mm: ΔL ≈ 0,128 mm.
- Acero por metro: ΔL ≈ 0,600 mm.

Para una viga tubular rectangular simplemente apoyada con carga puntual central F, el filtro estático inicial es:

```
I = [b·h³ − (b−2t)(h−2t)³] / 12
δ_max = F·L³ / (48·E·I)
σ_max = F·L·h / (8·I)
```

Las dimensiones b, h, t y L deben proceder del CAD y la fuerza debe calcularse a partir del DCL. Este cálculo estático no sustituye la verificación de uniones, fatiga ni respuesta modal/harmónica bajo 10–300 Hz. La banda requerida se conserva completa.

## 7. PLC, E/S y control

La rúbrica exige al menos tres canales analógicos de medida, seis entradas digitales y un lazo de control. Si la consigna de velocidad del VFD se envía como señal analógica, se necesita además una salida analógica.

**Hardware candidato para compra nueva:**
- CPU Siemens SIMATIC S7-1200 G2 CPU 1214C DC/DC/DC, referencia 6ES7214-1AH50-0XB0 (14 DI y 10 DQ).
- Módulo SM 1233 de 4 AI/4 AQ, referencia 6ES7233-4HF50-0XB0.
- Capacidad resultante: 4 AI para 3 mediciones requeridas; 4 AQ para 1 consigna analógica y reserva; 14 DI para 6 señales; 10 DQ para unas 5 órdenes de control.
- Asignación: AI0 aire; AI1 superficie; AI2 aceleración RMS acondicionada; AQ0 consigna del VFD. Un PID_Compact principal regula el aire. La superficie puede iniciar con control ON/OFF con histéresis y termostato independiente, sujeto a validación.
- La CPU G2 requiere TIA Portal V20 o posterior. Confirmar licencia de software antes de compra.
- El acelerómetro RMS acondicionado permite supervisión de amplitud, pero no captura directamente la forma de onda a 300 Hz. La adquisición de forma de onda requiere DAQ/acondicionador con ancho de banda y frecuencia de muestreo suficientes.
- El paro de emergencia debe actuar por una cadena cableada adecuada a la evaluación de riesgos; una entrada normal al PLC solo informa el estado. Utilizar STO del VFD únicamente si el modelo lo incorpora y el diseño de seguridad lo valida.

Fuentes:
- CPU 1214C G2: https://mall.industry.siemens.com/mall/en/hr/Catalog/Product/6ES7214-1AH50-0XB0
- SM 1233 4 AI/4 AQ: https://support.industry.siemens.com/cs/attachments/109972011/s71200_system_manual_es-ES_es-ES.pdf
- CPU G2 listada en Ubuy Perú, sin envío/importación: https://www.ubuy.pe/sp/product/U4XCD2U16-new-6es7214-1ah50-0xb0-siemens-simatic-s7-1200-g2-plc-module-simatic-s7
- SM 1233 en PLC-City, precio fuera de Perú y sin importación: https://www.plc-city.com/shop/es/industry-automation-plc-analogue-i-o-module/siemens-6es7233-4hf50-0xb0-nfs.html

## 8. Presupuesto y decisiones pendientes

Los precios son referencias públicas consultadas el 14 de octubre de 2026; deben confirmarse con los proveedores antes de comprar.

| Componente | Precio público |
|---|---:|
| Husillo enfriado por agua, 1,5 kW | S/ 1 350 |
| VFD BEST FC300, 1,5 kW | S/ 839 |
| Ventilador de 24 V | S/ 22 |
| Fuente de 24 V, 15 A | S/ 135,28 |
| **Subtotal parcial** | **S/ 2 346,28** |

El subtotal no es el costo total del banco; excluye el circuito de refrigeración del husillo, rotor y soporte de excitación, montaje/contención, calefactores definitivos, PLC y módulo analógico, protecciones, DAQ/acondicionador, cableado y fabricación.

Antes de autorizar compras deben cerrarse: (1) ficha y velocidad mínima/continua del husillo, (2) diseño seguro del excitador para cubrir 10–300 Hz, (3) aceleración y convención pico/RMS, (4) masa y rigidez de la plataforma, (5) resistencia final de H-102, (6) geometría/aislamiento de la cámara para verificar H-101, y (7) compatibilidad TIA Portal–PLC–VFD.
