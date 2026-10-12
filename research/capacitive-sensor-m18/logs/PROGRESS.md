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


## 2026-10-12 — Fase electrostática v7: fallo al crear región; corrección v8 preparada

### Resultado de ejecución v7 (JSON aportado por el usuario)
- AEDT inició correctamente como Student 2025 R2.4.
- Los cuatro diseños importaron los sólidos esperados y el reporte confirmó una brecha nominal de 4.0 mm entre cara del sensor y placa objetivo.
- Todos los diseños fallaron en `editor.CreateRegion(...)`; por tanto no se completaron frontera Balloon, potenciales ni Setup1, y no se resolvió el solver. Estado global: `FAILED_OR_PARTIAL`.
- La guía oficial Maxwell Scripting Guide v2025 R2 especifica que `Transparency` debe estar entre 0 y 1. La plantilla v7 enviaba `Transparency:=85`, valor fuera del rango documentado. No podemos probar causalidad absoluta sin ejecutar la corrección, pero es la discrepancia más clara identificada.
- Referencia: Ansys, “3D Modeler Editor Script Commands”, https://ansyshelp.ansys.com/public/Views/Secured/Electronics/v252/en/Subsystems/Maxwell/Subsystems/Maxwell%20Scripting/Content/3DModelerEditorScriptCommands.htm
- Referencia: Ansys, “CreateRegion”, https://ansyshelp.ansys.com/public/Views/Secured/Electronics/v252/en/Subsystems/Maxwell/Subsystems/Maxwell%20Scripting/Content/CreateRegion.htm

### Correcciones incluidas en el paquete local v8 (pendiente de probar en el equipo del usuario)
- Cambiar `Transparency` de 85 a 0.85.
- Simplificar `Flags` a `Wireframe`.
- Usar cadena vacía en `ShellElementThickness` porque el dominio no es un shell.
- Reducir el padding inicial de la región de 300% a 100% para evitar un dominio excesivo en la primera prueba.
- Recomendación de ejecución: N (no resolver) y comprobar primero que los cuatro diseños reporten Region, Balloon, voltajes y Setup1 creados.
- Paquete local entregado: `M18_ANSYS_Automatizacion_v8_RegionFix.zip`.
- Estado actual: corrección generada y sintaxis Python validada localmente; **no es aún una verificación en AEDT**.

### Interpretación científica
La importación geométrica sí queda verificada por los bounding boxes, recuento de sólidos y separación de 4 mm registrados en el JSON, pero no equivale a una simulación electrostática. Hasta tener región/fronteras/setup y una ejecución con convergencia documentada, no reportar campo, capacitancia ni umbral de detección como resultados.


## 2026-10-12 — Fase visual H1: v8 no completó región; v9 preparada

### Revisión del script y reporte v8 aportado
- El script ejecutado por el usuario reporta FAILED_OR_PARTIAL en las cuatro arquitecturas; el error ocurre en editor.CreateRegion(...). No hay solver completado ni field plot de v8, por lo que no existe aún resultado de campo que reportar.
- Se inspeccionó la referencia oficial: el ejemplo de CreateRegion en Maxwell Scripting Guide v252 usa Flags = "Wireframe#", Transparency = 0 y ShellElementThickness = "nan ". El script v8 difería en estos atributos (usaba Wireframe, 0.85 y cadena vacía). Se ha preparado un v9 que replica el ejemplo del manual de forma más fiel; aún requiere ejecutar en el AEDT del usuario.
- Referencia oficial CreateRegion: https://ansyshelp.ansys.com/public/Views/Secured/Electronics/v252/en/Subsystems/Maxwell/Subsystems/Maxwell%20Scripting/Content/CreateRegion.htm
- Referencia oficial CreateFieldPlot: https://ansyshelp.ansys.com/public/Views/Secured/Electronics/v252/en/Subsystems/Maxwell/Subsystems/Maxwell%20Scripting/Content/CreateFieldPlot.htm
- Referencia oficial field-line traces: https://ansyshelp.ansys.com/public/Views/Secured/Electronics/v252/en/Subsystems/Maxwell/Content/Maxwell/PlottingFieldLineTraces.htm

### Paquete local v9 — objetivo acotado a H1
- Se ha generado M18_ANSYS_H1_Campo_v9.zip; estado: preparado, no probado todavía en AEDT.
- El flujo actúa solo sobre H1: importa electrodo central, anillo auxiliar y target; asigna material conductor idealizado, región exterior, Balloon, 1 V normalizado a sense y 0 V al auxiliar/target; inserta setup, resuelve H1 y después intenta crear tres overlays independientes: magnitud del campo Mag_E, vector E_Vector y líneas de campo QuantityName_FieldLineTrace.
- Los errores de creación de cada overlay se registran separados del estado del solver para distinguir una solución electrostática de una visualización que falla.
- Se conserva la salvedad física: Maxwell Electrostatic genera un campo estático (líneas, magnitud/vector), no ondas electromagnéticas propagantes. Para ondas/campos variables en el tiempo se requeriría una formulación y solver diferentes.
- No se generalizará el automatizador a H2–H4 hasta comprobar región, solución y visualización de H1.

### Próximo criterio de aceptación
- Reporte JSON de v9 muestra region_created=true, balloon_created=true, voltage_boundaries_created=true, setup_created=true, solved=true y al menos uno de e_magnitude_plot_created, e_vector_plot_created o field_line_plot_created.
- Tras ello, inspeccionar el mensaje de convergencia de AEDT y confirmar visualmente líneas/colores y dirección del campo entre el electrodo a 1 V y los conductores de referencia a 0 V.
- No reportar una curva de capacitancia, umbral de detección ni comportamiento con temperatura/EMI/vibración hasta implementar y validar las fases correspondientes.


## 2026-10-12 — H1 v9: región creada; fallo en AssignBalloon; v10 preparada

### Evidencia de ejecución v9 enviada por el usuario
- La geometría H1 se importó: dos electrodos conceptuales y objetivo metálico; el informe indica unidad mm y separación sensor-objetivo de 4.0 mm.
- La región se creó (`region_created=true`), pero `BoundarySetup.AssignBalloon` falló porque el objeto COM no expone ese método (`ADispatchWrapper has no attribute AssignBalloon`). No se crearon las fronteras de voltaje ni el Setup; el solver no se ejecutó (`solved=false`).
- Resultado documentado: `H1_FAILED_OR_PARTIAL`; no hay campo eléctrico numérico ni plots validables de v9.

### Revisión de la API/documentación
- El scripting de `CreateFieldPlot` en Maxwell 2025 R2 documenta expresamente plots de `Mag_E`, `E_Vector` y `QuantityName_FieldLineTrace` en diseños electrostáticos 3D: https://ansyshelp.ansys.com/public/Views/Secured/Electronics/v252/en/Subsystems/Maxwell/Subsystems/Maxwell%20Scripting/Content/CreateFieldPlot.htm
- La documentación de condiciones de frontera electrostáticas describe las condiciones predeterminadas para 3D: fronteras naturales en interfaces y Neumann en las caras exteriores de la región; dejar una cara por defecto no requiere asignación adicional. https://ansyshelp.ansys.com/public/Views/Secured/Electronics/v261/en/Subsystems/Maxwell/Content/Maxwell/ElectrostaticBoundaries.htm
- En consecuencia, el flujo v10 elimina la llamada a `AssignBalloon` en Maxwell 3D Electrostatic, registra la condición Neumann exterior predeterminada y aumenta el padding de la región a 300 %. Esto es una aproximación inicial: la influencia de la frontera se deberá verificar con una sensibilidad de tamaño de región (por ejemplo 200 %, 300 %, 400 %) y no se debe describir como una frontera infinita exacta.

### Paquete local v10
- `M18_ANSYS_H1_Campo_v10_RegionBoundaryFix.zip`: generado y se comprobó sintaxis Python tras sustituir las variables de plantilla.
- El script solo intenta resolver H1 y generar magnitud de campo, vector y líneas; no relanza H2–H4.
- Estado: preparado, no probado en el equipo del usuario. Se requiere el nuevo JSON para validar si pasó asignación de voltaje, setup, solver y visualizaciones.

### Criterio para aceptar la fase
El JSON debe mostrar que la región está creada, las fronteras 1 V / 0 V están asignadas, Setup1 existe, el solver termina y al menos una visualización de campo se genera. Verificar además convergencia/malla en Message Manager antes de informar resultados científicos.


## 2026-10-12 — H1 v10: solver rechazó SolveInside; v11 preparada

### Evidencia en el JSON v10 aportado por el usuario
- Se verificó que H1 sí importó tres sólidos, comprobó el gap nominal de 4.0 mm, creó la región exterior, asignó las fronteras de tensión y creó Setup1.
- El solve falló con el mensaje de AEDT: “At least one material assignment should have solve inside set!”; los campos `solved`, `e_magnitude_plot_created` y `field_line_plot_created` permanecieron en false. No se obtuvo resultado de campo válido.
- El script v10 asigna `SolveInside=False` a los tres sólidos conductores y también asigna `SolveInside=False` a la región de vacío. Para una región de aire/vacío en la que se quiere calcular el campo, la hipótesis de corrección es mantener los conductores ideales con `SolveInside=False` y cambiar la región a `SolveInside=True`.

### Paquete local v11
- Paquete preparado: `M18_ANSYS_H1_Campo_v11_SolveInsideFix.zip`.
- El cambio de código se limita a la propiedad `SolveInside` de la región vacuum: pasa de false a true. Los sólidos conductores se mantienen con `SolveInside=False`.
- Se añadió un campo `region_solve_inside` al informe JSON. Se conserva el método H1, objetivo conductor a 4 mm, sense a 1 V normalizado y referencias/objetivo a 0 V.
- La sintaxis de la plantilla fue comprobada en Python fuera de AEDT; **el paquete v11 no ha sido aún ejecutado en el Ansys del usuario**, por lo que no debe describirse como solución exitosa hasta recibir el nuevo JSON y revisar convergencia.

### Criterio de aceptación
- El solver debe completar H1 sin el error de SolveInside; revisar el Message Manager y convergencia.
- Después, comprobar si se crean `Mag_E`, `E_Vector` y/o las trazas de campo.
- Solo entonces registrar la primera visualización estática del campo eléctrico. No llamarla onda electromagnética ni extrapolar aún distancia de detección, capacitancia frente a distancia, temperatura, EMI o vibración.
