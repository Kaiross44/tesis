# Bibliografía maestra — CPS industriales y módulo de adaptación multifísico

## Enfoque del paper

Título de trabajo:

> Diseño y evaluación de un módulo de adaptación termovibratoria y electromagnética para sensores capacitivos de proximidad industrial mediante simulación numérica.

El objeto principal es el **módulo de adaptación**. El banco/plataforma de pruebas se considera un medio posterior de caracterización y validación. La introducción de Semana 4 se concentra en antecedentes, propuestas de solución y secuencia del planteamiento; las ecuaciones, modelos FEM y matriz experimental se desarrollarán en Metodología.

## Criterio de uso de las fuentes

Cada referencia se evalúa por:
- pertinencia directa con sensores capacitivos de proximidad (CPS);
- problema y variables;
- aplicación;
- método;
- ventajas;
- limitaciones;
- relación con el módulo;
- posibilidad de complementar otras fuentes;
- sección prevista del paper.

Una fuente antigua no se elimina solo por su año. Se conserva cuando aporta un fundamento físico o metodológico que sigue siendo transferible. Para el requisito de Semana 4 se priorizan fuentes de medios con indexación Scopus vigente; el estado de indexación debe volver a verificarse en el Portal de Recursos/Scopus de la UPC antes de una entrega formal.

---

## A. Núcleo directo: sensores capacitivos de proximidad

### 1. Ye et al., 2020
**Y. Ye, C. Zhang, C. He, X. Wang, J. Huang, J. Deng. “A Review on Applications of Capacitive Displacement Sensing for Capacitive Proximity Sensor.” IEEE Access, 8, 45325–45342. DOI: 10.1109/ACCESS.2020.2977716.**

- Problema: estado del arte del sensado capacitivo de proximidad y desplazamiento; relación entre capacitancia, distancia y objeto.
- Variables: distancia, rango de detección, exactitud, sensibilidad, geometría/estructura del electrodo, modalidades de sensado.
- Aplicaciones: medición de distancia, mediciones indirectas, ambientes inteligentes, robótica y clasificación de objetos.
- Método: revisión de literatura y clasificación de modalidades/aplicaciones.
- Ventajas: es directamente específica de CPS; explica ventajas como bajo costo, bajo consumo y flexibilidad estructural.
- Limitaciones: es una revisión; no entrega por sí sola una validación experimental de nuestro módulo y no está centrada en encapsulados industriales M18/M30.
- Base para nosotros: definición del objeto de estudio y variables fundamentales.
- Complementa: Xia, Kirchner, Haque, Liu y Ye 2025.
- Sección: **Introducción — núcleo**.
- Estado: **Scopus vigente verificado a nivel de revista (IEEE Access)**.

La revisión distingue tres modalidades de sensado y señala que el sensado por desplazamiento permite mediciones de distancia y otras magnitudes; también advierte que la relación capacitancia-distancia puede ser no lineal y que rango/precisión pueden mejorarse mediante distintas estrategias. 

### 2. Kirchner et al., 2008
**N. Kirchner, D. Hordern, D. Liu, G. Dissanayake. “Capacitive sensor for object ranging and material type identification.” Sensors and Actuators A: Physical, 148(1), 96–104. DOI: 10.1016/j.sna.2008.07.027.**

- Problema: estimación de distancia e identificación del tipo de material en ambientes exigentes.
- Variables: distancia, frecuencia de excitación, respuesta capacitiva, material, variación entre lecturas.
- Aplicación: mantenimiento de puentes mediante robótica autónoma, incluyendo un ambiente de granallado.
- Método: sensor multifrecuencia, procesamiento de señal, clasificación supervisada y ensayos con brazo robótico.
- Ventajas: demuestra robustez frente a un entorno real y muestra que la información capacitiva puede discriminar materiales.
- Limitaciones: no es un sensor cilíndrico industrial M18/M30; la estrategia depende de multifrecuencia y procesamiento.
- Base para nosotros: material/entorno/distancia como factores que deben controlarse.
- Complementa: Xia 2019, que cuantifica el efecto de la geometría; Moheimani 2022, que amplía el panorama.
- Sección: **Introducción/antecedentes de desempeño** y luego Metodología.
- Estado: **Scopus por pertenecer a Sensors and Actuators A: Physical, revista activa**.

El estudio reporta que la variación de lecturas a diferentes frecuencias permite identificar grupos de materiales y que el sistema se diseñó para entornos de mantenimiento con granallado. 

### 3. Xia et al., 2019
**F. Xia, U. Zakia, C. Menon, B. Bahreyni. “Improved Capacitive Proximity Detection for Conductive Objects through Target Profile Estimation.” Journal of Sensors, 2019, Article 3891350. DOI: 10.1155/2019/3891350.**

- Problema: el error de estimación de distancia depende de la geometría y composición del objeto cercano.
- Variables: capacitancia, distancia, geometría/perfil del objetivo, error absoluto y relativo.
- Aplicación: detección de objetos metálicos, robótica.
- Método: matriz de electrodos, patrones de conexión, clasificación de perfil, regresión exponencial y ensayos con robot industrial.
- Resultado cuantitativo útil: reconocer la geometría redujo el error de medición a corta distancia por un factor de cinco; con el modelo adecuado la incertidumbre relativa se limitó en las condiciones reportadas.
- Ventajas: convierte el problema de proximidad en métricas cuantitativas de desempeño.
- Limitaciones: se centra en el objetivo y en el algoritmo, no en una interfaz protectora; usa una arquitectura de electrodos distinta del sensor cilíndrico.
- Base para nosotros: **error de detección, distancia, sensibilidad y geometría** como variables.
- Complementa: Liu para adaptabilidad, Haque para FEM y Ye 2025 para blindaje.
- Sección: **Introducción — núcleo** y posteriormente Resultados.
- Estado: **Scopus vigente verificado para Journal of Sensors**.

### 4. Haque et al., 2022
**R. I. Haque, M. Lubej, D. Briand. “Design and printing of a coplanar capacitive proximity sensor to detect the gap between dielectric foils edges.” Sensors and Actuators A: Physical, 337, 113424. DOI: 10.1016/j.sna.2022.113424.**

- Problema: diseño de un CPS para detectar una separación entre bordes dieléctricos.
- Variables: geometría de electrodos, parámetros físicos/externos, capacitancia y respuesta de proximidad.
- Aplicación: detección sin contacto de bordes de láminas dieléctricas.
- Método: FEM, optimización geométrica, fabricación por inkjet printing y caracterización experimental.
- Ventajas: conecta directamente **geometría → simulación numérica → experimento**.
- Limitaciones: sensor coplanar flexible, no cuerpo cilíndrico industrial.
- Base para nosotros: estrategia de simulación y validación de parámetros geométricos.
- Complementa: Keshyagol y Li 2022 para diseño geométrico.
- Sección: **Introducción — núcleo**, después Metodología.
- Estado: **Scopus vigente por revista activa**.

### 5. Liu et al., 2024
**Z. Liu, D. Chen, J. Ma, T. Wang, D. Jia, Y. Liu. “Multimodal capacitive proximity sensing array with programmable spatial resolution and dynamic detection range.” Sensors and Actuators A: Physical, 370, 115279. DOI: 10.1016/j.sna.2024.115279.**

- Problema: compromiso entre resolución espacial y rango de detección.
- Variables: área efectiva del electrodo, resolución espacial, rango de detección, clasificación de forma.
- Aplicación: mano robótica y tareas de percepción.
- Método: modificación física del área efectiva de una matriz CPS.
- Resultado cuantitativo: la arquitectura reporta 800 % de ajustabilidad en resolución y 300 % en rango; la clasificación superó 95 % en el escenario experimental reportado.
- Ventajas: evidencia fuerte para el concepto de **adaptabilidad física configurable**.
- Limitaciones: matriz flexible multielemento, no sensor industrial cilíndrico.
- Base para nosotros: justificar que una arquitectura física adaptable puede modificar el desempeño.
- Complementa: Ye 2025 y Okuno 2026.
- Sección: **Introducción — propuesta/adaptabilidad** y Metodología.
- Estado: **Scopus vigente por Sensors and Actuators A: Physical**.

### 6. Ye et al., 2025
**Y. Ye, X. Li, Q. Zhang, Y. Liu, H. Qian, J. Deng. “A Near-Ground Shielding Structure for Grounded Capacitive Proximity Sensors to Mitigate Performance Discrepancies Between Flush and Non-Flush Mounting.” Electronics, 14(11), 2166. DOI: 10.3390/electronics14112166.**

- Problema: superficies metálicas de trabajo provocan diferencias de desempeño entre montaje flush y non-flush.
- Variables: diferencia de capacitancia C_d, distancia del objetivo, condición de montaje, tipo de blindaje.
- Aplicación: sensores capacitivos de proximidad en aplicaciones industriales.
- Método: FEM + experimentación.
- Resultado cuantitativo: la estructura near-ground obtuvo un desempeño comparable al blindaje activo con C_d de 17 fF, siendo pasiva.
- Ventajas: muy próxima a nuestro problema; arquitectura simple, pasiva y de menor complejidad que un active shield.
- Limitaciones: se centra en la perturbación electromagnética y el montaje; no aborda simultáneamente temperatura y vibración.
- Base para nosotros: **módulo electromagnético externo**, geometría de guarda y control de acoplamientos.
- Complementa: Li/Risos/Bai para teoría de shield/guard y Okuno para compensación.
- Sección: **Introducción — núcleo** y luego Metodología.
- Estado: **Scopus vigente verificado en Electronics**.

### 7. Okuno & Yamamoto, 2026
**A. Okuno, A. Yamamoto. “Capacitive proximity sensor with an integrated drift compensation electrode.” Sensors and Actuators A: Physical, 398, 117314. DOI: 10.1016/j.sna.2025.117314.**

- Problema: deriva de salida causada por cambios atmosféricos y aumento de temperatura del circuito, especialmente en mediciones de largo alcance.
- Variables: deriva, temperatura, separación entre electrodo de sensado y electrodo de calibración, respuesta de proximidad.
- Aplicación: detección de proximidad de largo alcance.
- Método: electrodo de calibración dedicado, cambio entre modo sensado/calibración y compensación por resta de la deriva.
- Resultado cuantitativo: tras la compensación se reporta detección estable más allá de 30 cm durante un ensayo de 6 h; el ancho del gap influye en desempeño.
- Ventajas: conecta directamente temperatura/deriva + geometría + electrodo adicional.
- Limitaciones: integra el electrodo en el sensor, mientras que nuestro concepto busca una interfaz predominantemente externa.
- Base para nosotros: concepto de **adaptación/compensación sin cambiar la variable física objetivo**.
- Complementa: Ye 2025 para shield y nuestra arquitectura externa para trasladar parte de la función fuera del sensor.
- Sección: **Introducción — núcleo** y Metodología.
- Estado: **Scopus vigente por Sensors and Actuators A: Physical**.

### 8. Moheimani et al., 2022
**R. Moheimani, P. Hosseini, S. Mohammadi, H. Dalir. “Recent Advances on Capacitive Proximity Sensors: From Design and Materials to Creative Applications.” C, 8(2), 26. DOI: 10.3390/c8020026.**

- Problema: panorama de tecnologías, materiales, diseños y aplicaciones CPS.
- Variables: rango, señal, sensibilidad, relación señal/ruido, geometría y materiales.
- Aplicaciones: IoT, robótica, interfaces hombre-máquina, detección de materiales y otras.
- Método: mini-review.
- Ventajas: reúne diseño, materiales y aplicaciones en un solo documento.
- Limitaciones: revisión con fuerte énfasis en sensores flexibles/nanocompuestos y no específicamente en sensores industriales M18/M30.
- Base para nosotros: contextualización y lenguaje de diseño/material.
- Complementa: Ye 2020 para CPS y las fuentes experimentales directas.
- Sección: **Introducción — estado del arte**.
- Estado: **Scopus vigente verificado para C — Journal of Carbon Research**.

---

## B. Geometría, blindaje y campo eléctrico

### 9. Bai et al., 2016
**Y. Bai, Y. Lu, P. Hu, G. Wang, J. Xu, T. Zeng, Z. Li, Z. Zhang, J. Tan. “Absolute Position Sensing Based on a Robust Differential Capacitive Sensor with a Grounded Shield Window.” Sensors, 16(5), 680. DOI: 10.3390/s16050680.**

- Problema: sensibilidad a movimientos/vibraciones no deseados y no linealidad de un sensor diferencial.
- Variables: diferencial de capacitancia, desplazamiento, resolución, linealidad, vibración en otros grados de libertad.
- Aplicación: metrología de posición.
- Método: shield window, puente de capacitancia AC y validación experimental.
- Resultado cuantitativo: sensibilidad 2 × 10^-4 pF/μm, resolución 0.08 μm, rango 6 mm y error de linealidad <0.01 % en la condición reportada.
- Ventajas: muestra que un elemento de shield puede modificar positivamente la selectividad espacial y la respuesta frente a vibración.
- Limitaciones: arquitectura diferencial de metrología, no CPS industrial.
- Base para nosotros: relación entre **shield, campo y rechazo de perturbaciones mecánicas**.
- Complementa: Ye 2025 y Risos 2017.
- Sección: Metodología/antecedentes técnicos.
- Estado: **Scopus vigente por Sensors**.

### 10. Risos et al., 2017
**A. Risos, N. Long, A. Hunze, G. Gouws. “A 3D Faraday Shield for Interdigitated Dielectrometry Sensors and Its Effect on Capacitance.” Sensors, 17(1), 77. DOI: 10.3390/s17010077.**

- Problema: ruido producido por campos eléctricos externos.
- Variables: capacitancia, distancia al shield, campo eléctrico, respuesta del sensor.
- Aplicación: dielectrometría de aceites en sistemas de potencia.
- Método: jaula de Faraday 3D, análisis teórico, Green's function, FEM y experimentación.
- Ventajas: estudia explícitamente el efecto del shield sobre la señal y la distribución espacial del campo.
- Limitaciones: sensor de dielectrometría, no CPS industrial; el shield puede alterar la propiedad que se intenta medir.
- Base para nosotros: fundamento electromagnético de la **separación entre blindaje y elemento sensor**.
- Complementa: Ye 2025 y Li 2022.
- Sección: Metodología.
- Estado: **Scopus vigente por Sensors**.

### 11. Li et al. / Abdollahi-Mamoudan et al., 2022
**F. Abdollahi-Mamoudan, S. Savard, C. Ibarra-Castanedo, T. Filleter, X. Maldague. “Influence of different design parameters on a coplanar capacitive sensor performance.” NDT & E International, 126, 102588. DOI: 10.1016/j.ndteint.2021.102588.**

- Problema: cómo forma, tamaño, separación, frecuencia, lift-off, shielding plate y guard electrode afectan la respuesta.
- Variables: geometría, frecuencia, lift-off, intensidad/profundidad del campo, shield, guard.
- Aplicación: NDT e inspección de materiales.
- Método: FEM 3D en COMSOL + fabricación + experimentación.
- Resultado: se observa que geometría, tamaño, separación, shield y guard cambian la penetración y fuerza de campo; simulación y experimentos presentan buen acuerdo cualitativo.
- Ventajas: excelente para parametrizar el módulo y justificar un análisis de sensibilidad geométrica.
- Limitaciones: sonda coplanar de NDT, no sensor cilíndrico M18/M30.
- Base para nosotros: matriz de parámetros del módulo electromagnético.
- Complementa: Haque, Ye 2025, Risos.
- Sección: Metodología y parte de discusión.
- Estado: **Scopus vigente verificado para NDT & E International**.

---

## C. Térmico y termo-mecánico

### 12. Blasquez et al., 2000
**G. Blasquez, X. Chauffleur, P. Pons, C. Douziech, P. Favaro, Ph. Menini. “Intrinsic thermal behaviour of capacitive pressure sensors: mechanisms and minimisation.” Sensors and Actuators A: Physical, 85(1–3), 65–69. DOI: 10.1016/S0924-4247(00)00369-1.**

- Problema: variación térmica intrínseca de la capacitancia.
- Variables: temperatura, deformación termo-mecánica, espesor del wafer, área de unión.
- Método: modelado numérico 3D + observación de una familia de sensores.
- Resultado: identifica la **deformación estructural** como principal mecanismo de variación térmica de capacitancia en el sensor estudiado.
- Ventajas: fundamento físico claro para conectar temperatura con geometría y capacitancia.
- Limitaciones: sensor de presión de silicio/Pyrex, estudio de 2000.
- Base para nosotros: mecanismo transferible **temperatura → deformación → capacitancia**.
- Complementa: Hao 2012 y Ghanam 2023.
- Sección: Metodología; puede aparecer brevemente en antecedentes.
- Estado: **Scopus vigente por Sensors and Actuators A: Physical**.

### 13. Hao et al., 2012
**X. Hao, Y. Jiang, H. Takao, K. Maenaka, K. Higuchi. “An Annular Mechanical Temperature Compensation Structure for Gas-Sealed Capacitive Pressure Sensor.” Sensors, 12(6), 8026–8038. DOI: 10.3390/s120608026.**

- Problema: expansión térmica que produce deriva de un sensor capacitivo.
- Variables: temperatura, deflexión de diafragma, capacitancia-temperatura, radio de la estructura de compensación.
- Método: modelo analítico/numérico, ANSYS, fabricación y medición.
- Resultado: una estructura anular reduce fuertemente el coeficiente térmico manteniendo una sensibilidad de presión similar.
- Ventajas: ejemplo directo de **compensación mecánica mediante geometría**.
- Limitaciones: sensor de presión sellado; la arquitectura se implementa internamente.
- Base para nosotros: desacoplamiento/compensación termo-mecánica mediante geometría.
- Complementa: Blasquez y Ghanam.
- Sección: Metodología y antecedente técnico.
- Estado: **Scopus vigente por Sensors**.

### 14. Ghanam et al., 2023
**M. Ghanam, F. Goldschmidtboeing, T. Bilger, A. Bucherer, P. Woias. “MEMS Shielded Capacitive Pressure and Force Sensors with Excellent Thermal Stability and High Operating Temperature.” Sensors, 23(9), 4248. DOI: 10.3390/s23094248.**

- Problema: obtener sensores capacitivos estables a alta temperatura.
- Variables: temperatura, deriva, linealidad, rango de medición, arquitectura de shield.
- Aplicación: medición de presión/fuerza en alta temperatura.
- Método: fabricación, encapsulado y caracterización.
- Resultados reportados: operación hasta 500 °C; a 350 °C se reporta linealidad de 99.992 % FS y deriva térmica de −0.001 % FS/K; a 500 °C, deriva −0.0027 % FS/K y no linealidad 0.035 % FS.
- Ventajas: combina estabilidad térmica, blindaje y fabricación de sensores de distintos tamaños.
- Limitaciones: MEMS de presión/fuerza; valores no transferibles directamente a proximity.
- Base para nosotros: argumento de que **arquitectura/material/encapsulado pueden mejorar estabilidad térmica**.
- Complementa: Blasquez, Hao y futuras fuentes de materiales.
- Sección: Introducción/Metodología.
- Estado: **Scopus vigente por Sensors**.

---

## D. Vibración y caracterización

### 15. Zaitsev et al., 2022
**I. Zaitsev et al. “Calculation of Capacitive-Based Sensors of Rotating Shaft Vibration for Fault Diagnostic Systems of Powerful Generators.” Sensors, 22(4), 1634. DOI: 10.3390/s22041634.**

- Problema: medición capacitiva de vibración de ejes rotatorios.
- Variables: distancia electrodo-eje, geometría de electrodos, respuesta de capacitancia, frecuencia/condición vibratoria, fringe effects.
- Aplicación: diagnóstico de generadores y turbinas.
- Método: ecuaciones analíticas + simulación computacional + 3D FEM.
- Ventajas: muy útil para conectar **sensor capacitivo + vibración + guard electrode + FEM 3D**.
- Limitaciones: diseño dedicado a ejes rotativos, no CPS de proximidad general.
- Base para nosotros: modelado del efecto vibratorio y dimensionamiento de regiones activas/de guarda.
- Complementa: Zhang 2024 y Li 2022.
- Sección: Metodología.

### 16. Zhang et al., 2024
**S. Zhang et al. “Analysis of the Frequency-Dependent Vibration Rectification Error in Area-Variation-Based Capacitive MEMS Accelerometers.” Micromachines, 15(1), 65. DOI: 10.3390/mi15010065.**

- Problema: error de rectificación por vibración y dependencia con frecuencia.
- Variables: frecuencia, amplitud de desplazamiento, resonancia, no linealidad, fringe effect, offset mecánico.
- Aplicación: navegación inercial, inclinación y sistemas donde las vibraciones ambientales degradan una señal capacitiva.
- Método: análisis experimental con acelerómetro capacitivo MEMS.
- Resultado: identifica el acoplamiento entre amplificación cerca de resonancia, no linealidad capacitancia-desplazamiento y fringing; la optimización de transductor y damping redujo fuertemente el coeficiente de no linealidad de segundo orden.
- Ventajas: fundamenta por qué el módulo debe estudiarse en frecuencia y no solo en una carga estática.
- Limitaciones: acelerómetro MEMS, no proximity.
- Base para nosotros: **frecuencia natural, respuesta armónica, amplitud y desplazamiento**.
- Complementa: Zaitsev.
- Sección: Metodología/Resultados.
- Estado: **Scopus vigente por Micromachines**.

### 17. Schwenck et al., 2021
**A. Schwenck, T. Guenther, A. Zimmermann. “Characterization and Benchmark of a Novel Capacitive and Fluidic Inclination Sensor.” Sensors, 21(23), 8030. DOI: 10.3390/s21238030.**

- Problema: caracterizar y comparar sensores capacitivos mediante métricas de calidad.
- Variables: Allan deviation, no repetibilidad, histéresis, estabilidad de offset con temperatura, ruido y curva característica.
- Aplicación: medición de inclinación.
- Método: construcción de variantes y benchmark frente a MEMS comerciales.
- Ventajas: aporta una batería de **métricas de caracterización cuantitativa** que podemos adaptar.
- Limitaciones: variable medida distinta de proximidad y arquitectura fluídica.
- Base para nosotros: definir criterios de repetibilidad, estabilidad, histéresis y ruido.
- Complementa: Xia para error de distancia y nuestras métricas capacitivas.
- Sección: Metodología/Resultados.
- Estado: **Scopus vigente por Sensors**.

---

## E. Diseño computacional / optimización

### 18. Keshyagol et al., 2024
**K. Keshyagol, S. Hiremath, H. M. Vishwanatha, A. U. Kini, N. Naik, P. Hiremath. “Optimizing Capacitive Pressure Sensor Geometry: A Design of Experiments Approach with a Computer-Generated Model.” Sensors, 24(11), 3504. DOI: 10.3390/s24113504.**

- Problema: optimización de geometría de un sensor capacitivo.
- Variables: geometría del electrodo/dieléctrico, espesor, capacitancia, sensibilidad, desplazamiento, esfuerzo, densidad de malla.
- Método: FEM + Design of Experiments + análisis estadístico.
- Resultado: identifica configuraciones geométricas óptimas y muestra cómo la geometría modifica sensibilidad y respuesta.
- Ventajas: muy útil para convertir nuestro diseño en un problema parametrizado/optimizable.
- Limitaciones: sensor de presión/touch, no proximity industrial.
- Base para nosotros: **DoE, parametrización y selección de geometría**.
- Complementa: Haque y Li 2022.
- Sección: Metodología.
- Estado: **Scopus vigente por Sensors**.

---

## F. Materiales funcionales y amortiguamiento

### 19. Saedi et al., 2023
**S. Saedi, E. Acar, H. Raji, S. E. Saghaian, M. Mirsayar. “Energy Damping in Shape Memory Alloys: A Review.” Journal of Alloys and Compounds, 956, 170286. DOI: 10.1016/j.jallcom.2023.170286.**

- Problema: disipación de energía mediante SMA.
- Variables: frecuencia/tasa de carga, amplitud de deformación, temperatura de operación, ciclos, histeresis y capacidad de damping.
- Aplicaciones: amortiguamiento estructural, aislamiento sísmico, control de vibraciones y otras.
- Método: revisión de mecanismos y métodos experimentales.
- Ventajas: fundamenta técnicamente por qué una SMA puede considerarse como elemento disipativo.
- Limitaciones: no es específica de sensores; la efectividad depende fuertemente del estado termomecánico.
- Base para nosotros: SMA como **opción**, no como solución obligatoria.
- Complementa: Zhang/Zaitsev para necesidades vibratorias y Hossain/Davarnia para selección del material.
- Sección: Metodología/Materiales, no núcleo de Semana 4.
- Estado: **Scopus vigente verificado para Journal of Alloys and Compounds**.

### 20. Hossain et al., 2025
**M. I. Hossain, M. S. Rabbi, M. T. Ali. “Shape Memory Alloys in Modern Engineering: Progress, Problems, and Prospects.” RSC Advances, 15(40), 33046–33100. DOI: 10.1039/D5RA04560F.**

- Problema: panorama de SMA, capacidades, aplicaciones y barreras para adopción.
- Variables/properties: capacidad de recuperación, densidad de energía, respuesta termomecánica, problemas de implementación.
- Aplicaciones: múltiples sectores de ingeniería.
- Método: revisión.
- Ventajas: actualiza el estado del arte y, sobre todo, las **limitaciones** de SMA.
- Limitaciones: generalista, no sensor/proximity.
- Base para nosotros: criterio para decidir si SMA realmente tiene sentido.
- Complementa: Saedi y Davarnia.
- Sección: Metodología/selección de materiales.
- Estado: **Scopus vigente por RSC Advances**.

### 21. Davarnia et al., 2025
**D. Davarnia, S. Cheng, N. van Engelen. “Mechanical Behavior of NiTi Shape Memory Alloy Under Cyclic Loading: A State-of-the-Art Review.” Frontiers of Structural and Civil Engineering, 19(7), 1041–1060. DOI: 10.1007/s11709-025-1195-2.**

- Problema: comportamiento cíclico de NiTi bajo cargas repetidas.
- Variables: número de ciclos, amplitud de deformación, frecuencia, temperatura, predeformación, tamaño de probeta, fatiga funcional/estructural.
- Aplicación: amortiguamiento/control pasivo de vibraciones.
- Ventajas: muy útil si se introduce SMA en una etapa posterior.
- Limitación crítica para cumplimiento Scopus: el medio aparece actualmente como **inactivo/descontinuado en Scopus, con cobertura histórica 2012–2025**, por lo que no debe contarse como referencia Scopus vigente para el requisito formal.
- Base para nosotros: comportamiento cíclico de NiTi y criterios de fatiga.
- Complementa: Saedi y Hossain.
- Sección: reserva para Metodología/selección de materiales.
- Estado: **fuente técnica conservada; no usar para cumplir las 5 referencias Scopus actuales**.

### 22. Bongkarn et al., 2026
**T. Bongkarn et al. “Integration of CCTAO/PDMS Composite Films into Proximity Capacitive Sensor Devices.” Radiation Physics and Chemistry, 249, 114229. DOI: 10.1016/j.radphyschem.2026.114229.**

- Problema: mejorar la respuesta de proximidad mediante materiales dieléctricos funcionales.
- Variables: permitividad, dispersión de partículas, microestructura, carga de relleno, distancia, cambio de capacitancia y sensibilidad.
- Aplicación: sensores capacitivos flexibles de proximidad.
- Método: síntesis de cerámicas CCTAO, incorporación en PDMS, caracterización microestructural/dieléctrica y ensayo de proximidad.
- Resultado cuantitativo: la formulación 10 wt.% CCTNdO/PDMS alcanzó un cambio normalizado máximo de −8.70 %, sensibilidad ~0.42 %/mm y rango efectivo ~20 mm.
- Ventajas: demuestra que **material + microestructura + permitividad + campo de fringing** pueden cambiar el desempeño de proximidad.
- Limitaciones: sensor interdigitado flexible, no cuerpo industrial cilíndrico; aún no demuestra aplicabilidad directa a nuestro módulo.
- Base para nosotros: abre la línea de **cerámico/composite como material funcional**, alternativa a SMA.
- Complementa: Moheimani para materiales, Keshyagol para optimización, Haque para geometría.
- Sección: Metodología/selección de materiales.
- Estado: **Scopus y WoS verificados para Radiation Physics and Chemistry**.

---

## G. Documentación técnica y normativa

### 23. Texas Instruments
**Texas Instruments, “Capacitive Sensing: Ins and Outs of Active Shielding,” Application Report SNOA926, 2014.**

- Tipo: documentación técnica, no artículo científico.
- Aporte: explicación práctica de active shielding, guard electrode, acoplamientos y reducción de ruido.
- Ventaja: fuente útil para implementación electrónica.
- Limitación: **no contar como una de las 5 referencias científicas Scopus**.
- Uso: diseño electrónico/Metodología y apoyo técnico.
- Complementa: Ye 2025 y Risos.

### 24. IEC 60947-5-2:2019
**Low-voltage switchgear and controlgear — Part 5-2: Control circuit devices and switching elements — Proximity switches.**

- Tipo: norma internacional.
- Alcance: incluye interruptores/sensores de proximidad inductivos y capacitivos, entre otros.
- Uso para nosotros: definir lenguaje técnico, condiciones de montaje y parámetros/formatos del componente industrial.
- Importante: una norma no sustituye un artículo científico y no debe contarse dentro de las 5 referencias científicas.
- Verificación: edición 2019 aparece como vigente en la fuente normativa consultada.

### 25. Referencia industrial de formato — OMRON E2K-X
**OMRON E2K-X — General-purpose Threaded Capacitive Sensor.**

- Tipo: catálogo/datasheet de fabricante.
- Evidencia relevante: modelos cilíndricos capacitivos en **M12, M18 y M30**.
- Datos publicados: por ejemplo, M12 4 mm, M18 8 mm y M30 15 mm de distancia de detección en la familia E2K-X.
- Uso para nosotros: justificar que M12/M18/M30 son formatos comerciales reales y construir una arquitectura paramétrica.
- Limitación: catálogo comercial, no evidencia científica.
- Complementa: IEC + literatura científica de CPS.

---

# Síntesis transversal de la literatura

## Problema

La literatura permite separar el problema en cuatro mecanismos:

1. **Geométrico:** distancia, forma y dimensiones alteran la relación entre campo y capacitancia.
2. **Térmico:** temperatura puede producir deriva y deformación estructural.
3. **Vibratorio:** excitación, resonancia, desplazamiento y frecuencia modifican la respuesta.
4. **Electromagnético:** conductores, superficies y blindajes cambian el campo y generan capacitancias parásitas.

## Soluciones encontradas

La literatura muestra alternativas distintas:

- compensación geométrica;
- modificación de área;
- guard electrode;
- shield pasivo;
- active shield;
- electrodo de compensación;
- materiales dieléctricos funcionales;
- modificación de masa/rigidez/damping;
- SMA como elemento disipativo.

## Lo que nosotros NO debemos afirmar

No afirmar que:
- SMA es necesariamente la mejor solución;
- cerámica es necesariamente la mejor solución;
- el módulo es universal;
- la protección siempre mejora la sensibilidad;
- una solución de un MEMS es equivalente automáticamente a un CPS industrial.

## Lo que sí podemos plantear

> Estudiar una arquitectura modular externa y parametrizable capaz de incorporar diferentes mecanismos de adaptación térmica, vibratoria y electromagnética, y evaluar cuantitativamente su efecto sobre la respuesta de un sensor capacitivo de proximidad.

---

# Arquitectura bibliográfica del paper

## Semana 4 — Introducción
Prioridad:
1. Ye 2020
2. Xia 2019
3. Haque 2022
4. Ye 2025
5. Okuno 2026

Alternativa de reemplazo/contexto:
- Kirchner 2008
- Moheimani 2022

## Metodología
- Li 2022
- Bai 2016
- Risos 2017
- Blasquez 2000
- Hao 2012
- Ghanam 2023
- Zaitsev 2022
- Zhang 2024
- Schwenck 2021
- Keshyagol 2024
- Saedi 2023
- Hossain 2025
- Bongkarn 2026

## Resultados/discusión
Se incorporarán según las variables realmente medidas:
- error de detección;
- sensibilidad;
- capacitancia;
- capacitancia parásita;
- desplazamiento;
- temperatura;
- aceleración;
- frecuencia;
- estabilidad;
- repetibilidad;
- histéresis;
- falsos positivos/falsas detecciones, solo si se define una métrica experimental reproducible.

---

# Idea de figura para la Introducción

Debe existir **una única figura conceptual del módulo**, no del banco de pruebas.

Contenido recomendado:

Sensor capacitivo cilíndrico
→ interfaz/módulo externo
→ adaptación termomecánica
→ protección electromagnética
→ interfaz de montaje

Con parámetros:
- diámetro/formato M12–M18–M30;
- abertura frontal;
- separación del shield/guard;
- material/intercambiable;
- elementos de desacoplamiento.

La figura debe hacer evidente al lector qué significa “módulo de adaptación” antes de entrar en la metodología.

---

# Estado conceptual

La investigación queda organizada como:

**CPS industrial**
→ **perturbación**
→ **variable física afectada**
→ **error/desviación de respuesta**
→ **mecanismo de adaptación**
→ **módulo modular**
→ **simulación numérica**
→ **comparación**
→ **validación experimental**

El banco de pruebas aparece al final como infraestructura de validación, no como objeto principal.


---

## H. Patentes y arquitectura interna del CPS M18

> **Uso:** estas patentes se conservan como fuentes de **arquitecturas candidatas y principios de diseño**, no como evidencia de que un sensor M18 comercial específico utilice exactamente dicha arquitectura.

### P1. DE102011121583A1 — Capacitive proximity sensor
**Balluff GmbH.** Arquitectura cilíndrica con electrodo interno y electrodo exterior; incluye realizaciones con electrodo central y elemento de blindaje/guard alrededor, así como variantes integradas en una carcasa roscada.

- Uso en esta investigación: base principal para las arquitecturas **coaxiales M18** y variantes con shield.
- Fuente: https://patents.google.com/patent/DE102011121583A1/en

### P2. DE3221223A1 — Capacitive Proximity Initiator
Arquitectura tubular con electrodo sensor, electrodo de protección/guard y electrodo de blindaje; contempla una carcasa exterior aislante y un shield conectado eléctricamente al circuito.

- Uso: comparar **guard/shield** y separar el concepto de shield de la carcasa metálica.
- Fuente: https://patents.google.com/patent/DE3221223A1/en

### P3. EP2598848A1 / EP2598848B1 — Capacitive probe / flush mounting
Describe configuraciones cilíndricas concéntricas para sensores capacitivos, incluyendo realizaciones **flush** con carcasa conectada a tierra y elementos de guard/shield.

- Uso: base para el eje experimental **flush vs non-flush**, housing metálico y shield.
- Fuentes:
  - https://patents.google.com/patent/EP2598848A1/en
  - https://patents.google.com/patent/EP2598848B1/en

### P4. CN222865950U — Capacitive proximity sensor and electronic device
Incluye electrodo principal, electrodo auxiliar, electrodos de tierra/guard y un electrodo anular exterior. La arquitectura permite comparar capacitancias de medición y referencia y estudiar la influencia del entorno metálico.

- Uso: base para arquitectura **diferencial con referencia + guard/shield**.
- Fuente: https://patents.google.com/patent/CN222865950U/en

### P5. JP2010223794A — Capacitive proximity sensor, detection method and electrode structure
Describe múltiples electrodos, electrodos de referencia/blindaje y estrategias de selección/ajuste de la detección mediante comparación de capacitancias.

- Uso: sustento para estudiar **rango de detección, referencia y umbral electrónico**.
- Fuente: https://patents.google.com/patent/JP2010223794A/en

### P6. US5512836 — Solid-state micro proximity sensor
Patente histórica de sensores capacitivos de proximidad basados en campo de fuga/fringing field y diferentes patrones de electrodos.

- Uso: **benchmark non-shielded** y antecedentes de geometrías de electrodos.
- Fuente: https://patents.justia.com/patent/5512836

### P7. US20120013354A1 — Concentric coplanar capacitive sensor
Arquitectura de electrodo central y anillo concéntrico con separación entre ambos.

- Uso: base de la arquitectura **A — concéntrica non-shielded** y referencia para el estudio de geometría/gap.
- Fuente: https://patents.google.com/patent/US20120013354A1/en

### P8. US20050264304A1 / US7138809B2 — Electrical capacitance proximity sensor
Familia de patentes con configuraciones de electrodos auxiliares/guard y comparación entre señales capacitivas para obtener información espacial.

- Uso: sustento adicional para **arquitecturas diferenciales y multielectrodo**.
- Fuente de familia: https://patents.google.com/patent/HK1083555A1/en

### Matriz preliminar patente → candidato

| Candidato | Arquitectura | Patentes de apoyo |
|---|---|---|
| **A** | Concéntrica 2-electrodo, non-shielded | P6, P7 |
| **B** | Coaxial central + exterior, shield/guard | P1 |
| **C** | Sensor + guard + shield + carcasa | P2, P3 |
| **D** | Sensor + referencia auxiliar + guard/shield | P4, P5, P8 |

### Hipótesis de modelado asociadas

1. **Non-shielded:** la carcasa se modelará como parte del entorno o como conductor no conectado a tierra, según el caso de estudio; se evaluará su influencia como condición de contorno.
2. **Shielded:** se compararán al menos dos configuraciones distintas, porque **shield conectado a GND**, **guard conducido** y **carcasa metálica a GND** no son eléctricamente equivalentes.
3. **Flush/non-flush:** se considerará como condición experimental separada cuando la geometría lo permita.
4. **Referencia/diferencial:** cuando haya dos canales capacitivos, se analizará la diferencia o relación entre capacitancias en vez de asumir que el potenciómetro cambia directamente la capacitancia física.
5. **M18:** la envolvente de trabajo se documentará como Ø18 mm, con longitud nominal aproximada de 69 mm; las dimensiones internas y espesores de carcasa deberán marcarse como **supuestos de modelado** hasta contar con evidencia directa.

