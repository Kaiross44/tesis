# Registro de progreso — estudio paramétrico CPS M18

> Registro acumulativo para poder sintetizar una metodología de tesis reproducible. Este archivo documenta hechos confirmados, decisiones provisionales y tareas pendientes; no sustituye el registro de fuentes ni los informes por ejecución.

## 2026-10-12 — CAD de referencia e importación inicial en AEDT

### Estado comprobado
- Producto de referencia: Telemecanique Sensors / OsiSense XT1M18PA372, familia de sensor capacitivo cilíndrico M18, montaje flush, carcasa metálica. Los metadatos TraceParts compartidos reportan (S_n=4\,\mathrm{mm}), salida DC PNP NO y cable de 2 m. La arquitectura interna del producto no está identificada en los archivos CAD.
- El STEP compartido contiene la envolvente/carcasa y tuercas de montaje; no aporta sólidos B-rep de los electrodos internos.
- La interfaz del usuario confirma Ansys Electronics Desktop Student 2025 R2.4.
- El script nativo v5 produjo `IMPORTS_COMPLETED` y mostró los cuatro diseños Maxwell 3D H1–H4. En las capturas, los sólidos todavía aparecían bajo `Not Assigned`; por tanto, esa fase solo comprobó importación de geometría, no una simulación física.
- Se preparó una nueva automatización local v7 para agregar materiales, potenciales normalizados, región abierta, condición Balloon y Setup electrostático. **La v7 aún debe ejecutarse y verificarse en el equipo del usuario**; no debe citarse como resultado de simulación.

### Hipótesis geométricas (no reconstrucciones del fabricante)
- H1: electrodo central + anular auxiliar.
- H2: electrodo central + guarda anular.
- H3: electrodo central + blindaje + anillo exterior.
- H4: electrodos con separación axial.
- H1–H4 son escenarios académicos comparativos. No se conoce la conexión real de electrodos auxiliares/guarda/blindaje.

### Configuración base propuesta para el primer solve
- Maxwell 3D / Electrostatic, con el objetivo metálico de referencia a 4 mm de la cara activa.
- Electrodo de sensado a **1 V normalizado**, conductores de referencia y objetivo a 0 V.
- Material de partida `copper` para los conductores idealizados y `vacuum` como fondo inicial.
- No asignar directamente 24 V a los electrodos internos: 24 VDC corresponde a la alimentación industrial del sensor/sistema; la amplitud y arquitectura de excitación interna no están documentadas. El potencial de 1 V es una condición normalizada para resolver el problema lineal, no una afirmación sobre la electrónica real.
- Las asignaciones a 0 V de los electrodos auxiliares/guarda/blindaje son un supuesto de la primera campaña que deberá variarse cuando se estudien alternativas de conexión.
- La distancia nominal (S_n) de la ficha de producto no equivale automáticamente a un umbral FEM; el circuito de oscilación, acondicionamiento y comparador no está modelado.

### Ecuaciones de referencia para el cuaderno de metodología
- Electroestática en medio lineal: (\mathbf{E}=-\nabla V), (\nabla\cdot(\epsilon\nabla V)=-\rho_f).
- Definición de capacitancia: (C=Q/V\) para una configuración de potencial definida; se deberá obtener (C) por matriz, carga o energía almacenada y verificar la convención del solver.
- Placas paralelas como comprobación de orden de magnitud, no sustituto del FEM con campos de borde: (C\approx \epsilon_0\epsilon_r A/d), y (|dC/dd|\approx \epsilon_0\epsilon_r A/d^2).
- Expansión térmica lineal como aproximación: (\Delta L\approx \alpha L_0\Delta T). El sentido y magnitud del cambio en el campo/capacitancia dependen también de la permitividad, deformación relativa y distancia al objetivo; no se asume que (E) necesariamente disminuya al calentarse.

### Fuentes técnicas prioritarias consultadas
- Ansys, Maxwell Scripting Guide 2025 R2, `CreateRegion`: https://ansyshelp.ansys.com/public/Views/Secured/Electronics/v252/en/Subsystems/Maxwell/Subsystems/Maxwell%20Scripting/Content/CreateRegion.htm
- Ansys, Maxwell Scripting Guide 2025 R2, `InsertSetup`: https://ansyshelp.ansys.com/public/Views/Secured/Electronics/v252/en/Subsystems/Maxwell/Subsystems/Maxwell%20Scripting/Content/InsertSetupMaxwell.htm
- Ansys, Maxwell Scripting Guide 2025 R2, `AssignMaterial`: https://ansyshelp.ansys.com/public/Views/Secured/Electronics/v252/en/Subsystems/Maxwell/Subsystems/Maxwell%20Scripting/Content/AssignMaterial.htm
- Ansys, Maxwell Scripting Guide 2025 R2, `AssignVoltage`: https://ansyshelp.ansys.com/public/Views/Secured/Electronics/v252/en/Subsystems/Maxwell/Subsystems/Maxwell%20Scripting/Content/AssignVoltageMaxwell.htm
- Ansys, descripción de frontera Balloon en electrostática: https://ansyshelp.ansys.com/public/Views/Secured/Electronics/v261/en/Subsystems/Maxwell/Content/Maxwell/Balloon.htm

### Fuentes académicas que ya figuran en `references/references.bib` y deben auditarse para este subproyecto
- Keshyagol et al. (2024), “Optimizing Capacitive Pressure Sensor Geometry: A Design of Experiments Approach with a Computer-Generated Model”, *Sensors*, 24(11), 3504. DOI: https://doi.org/10.3390/s24113504. Método FEM y DoE confirmados en el artículo; es un sensor de presión capacitivo, no un proximímetro industrial M18. El solver comercial concreto debe comprobarse en el texto íntegro antes de afirmar que usaron ANSYS.
- Ye et al. (2025), “A Near-Ground Shielding Structure for Grounded Capacitive Proximity Sensors to Mitigate Performance Discrepancies Between Flush and Non-Flush Mounting”, *Electronics*, 14(11), 2166. DOI: https://doi.org/10.3390/electronics14112166. Pertinencia directa: blindaje, montaje flush/no-flush, capacitancia frente a distancia y validación experimental; comprobar el apartado de método para identificar el software exacto antes de atribuir ANSYS.
- Ghanam et al. (2023), “MEMS Shielded Capacitive Pressure and Force Sensors with Excellent Thermal Stability and High Operating Temperature”, *Sensors*, 23(9), 4248. DOI: https://doi.org/10.3390/s23094248. Útil para mecanismos de estabilidad térmica/blindaje; la geometría y escala MEMS limitan la transferencia directa.
- Zhang et al. (2024), “Analysis of the Frequency-Dependent Vibration Rectification Error in Area-Variation-Based Capacitive MEMS Accelerometers”, *Micromachines*, 15(1), 65. DOI: https://doi.org/10.3390/mi15010065. Útil para la fase dinámica/rectificación en un sistema capacitivo MEMS, no como modelo directo del proximímetro industrial.
- La bibliografía maestra también contiene fuentes sobre sensores capacitivos de vibración, estructuras de guarda y estabilidad térmica; se verificarán relevancia, acceso al artículo completo, software realmente usado, geometría, condiciones y validación antes de incorporarlas a la metodología final.

## Próximas tareas
1. Ejecutar la automatización v7 y auditar el JSON: número de sólidos, rol asignado a cada sólido, brecha objetivo, materiales, potenciales, región y condiciones de frontera.
2. Verificar manualmente el árbol `Boundaries`, `Excitations` y `Analysis Setup` en AEDT antes de resolver.
3. Resolver primero H1 y revisar convergencia, campo (E), potencial (V), carga/energía y extracción de (C).
4. Verificar el método de capacitancia con una referencia analítica de orden de magnitud y una comprobación de tamaño de región/malla.
5. Barrer distancia del objetivo (manteniendo tamaño y material constantes), después material/permitividad y dimensiones; no deducir distancia de disparo del sensor físico sin el umbral electrónico.
6. Acoplar térmico de forma secuencial mediante propiedades dependientes de temperatura y deformaciones actualizadas; después vibración y EMI con formulaciones/solver pertinentes.
7. Por ejecución, registrar fecha, versión AEDT/PyAEDT o scripting nativo, hash/script, geometría, unidades, material, excitaciones, malla, convergencia, métricas, archivos CSV y desviaciones.
8. Revisar y etiquetar las fuentes académicas en `references.bib`: una referencia solo podrá citarse como “simulación ANSYS” si el apartado de método lo confirma explícitamente.

## Criterio de reporte
Hasta que se complete el solver y su validación, describir el trabajo como **geometría importada/configuración preparada**, no como una simulación validada. Mantener separados los hechos de fabricante, las hipótesis H1–H4, las decisiones de modelado y los resultados calculados.
