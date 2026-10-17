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


## 2026-10-12 — Ejecución confirmada del proyecto v10: el solver requiere SolveInside

### Evidencia del artefacto adjunto por el usuario
- El archivo y JSON aportados corresponden a `M18_H1_Campo_v10_20261012_161140`, no a una ejecución v11.
- En v10 se logró crear la región (padding 300 %), asignar los potenciales 1 V / 0 V y crear Setup1; la geometría reporta gap de 4.0 mm.
- El Message Manager devuelve el error exacto: “At least one material assignment should have solve inside set!” y luego el análisis se detiene. `solved=false`; aún no existen resultados de campo o plots válidos.
- Causa identificada en la plantilla v10: todos los cuerpos de cobre tenían `SolveInside=False` y la región de vacío también se creó con `SolveInside=False`, por lo que no hay volumen habilitado para resolver el potencial en el dieléctrico.
- La plantilla v11 suministrada corrige la región de vacío a `SolveInside=True`, manteniendo los cuerpos conductores como `SolveInside=False`. Esa versión sigue pendiente de ejecución; no considerar el error v10 como fallo de v11.
- Próxima acción: ejecutar la plantilla/PS1 v11 del paquete `M18_ANSYS_H1_Campo_v11_SolveInsideFix.zip` y revisar su nuevo JSON. No volver a ejecutar la versión v10.
- Criterio de salida: solver complete sin el error SolveInside; validar la convergencia antes de aceptar cualquier gráfica de campo.

## 2026-10-16 — H1 v11 ejecutó el solver y creó visualizaciones; convergencia pendiente de auditar

### Evidencia aportada por el usuario
- Se recibió el JSON `M18_H1_Campo_v11_20261016_214333.json` y la captura de AEDT.
- El JSON registra `status=H1_SOLVED_FIELD_VISUALIZATION_CREATED`, `solved=true`, `solver_call_completed=true`, `region_created=true`, `region_solve_inside=true`, fronteras de potencial creadas y `Setup1` creado. El error previo de `SolveInside` ya no aparece en el estado resumido.
- Se crearon los tres tipos de visualización: `Mag_E`, `E_Vector` y `QuantityName_FieldLineTrace`; `plot_errors=[]`.
- No se asignó una frontera Balloon: el JSON conserva la condición Neumann por defecto en las seis caras de la región con padding del 300 %. Esta elección es una aproximación y requiere sensibilidad al tamaño de región.
- La geometría reportada conserva la separación sensor–objetivo de 4.0 mm y tres sólidos importados; los tres se idealizaron como cobre. La región usa vacío como aproximación inicial de aire.
- La captura compartida muestra una visualización muy saturada de vectores/líneas sobre un dominio grande. El indicador de escala visible llega a 200 mm; esto parece deberse en gran parte a que se muestran simultáneamente trazas y vectores en un volumen exterior amplio. Una región de aire no necesita ser cúbica por principio; lo importante es que las fronteras lejanas no alteren materialmente la métrica calculada.
- La leyenda visible en la captura indica máximos y mínimos de campo, pero no se registran como resultados científicos todavía: hay capas de visualización superpuestas y no se ha aportado evidencia de convergencia/adaptación del solver, estadística de malla ni sensibilidad de frontera.

### Interpretación y limitaciones
- Esta ejecución confirma el avance de preparación a una llamada de solver completada y a plots creados; no equivale por sí sola a una solución científicamente aceptada.
- El campo electrostático es estático, no una onda electromagnética propagante. Tampoco se han calculado todavía capacitancia frente a distancia, influencia térmica, EMI dinámica ni vibración.
- La excitación de 1 V sigue siendo una normalización matemática, no una afirmación acerca de la tensión interna del producto comercial.

### Próximo paso obligatorio
1. Abrir el proyecto existente `M18_H1_Campo_v11_20261016_214333.aedt`; no regenerar el proyecto ni volver a ejecutar el script de momento.
2. Revisar en AEDT el estado de convergencia/adaptive passes de `Setup1` y el Message Manager; guardar evidencia visual de ese estado.
3. Para despejar la figura, ocultar temporalmente los plots `E_Vector` y `Field Lines H1`, dejando visible solo `MagE_H1`. Crear después un corte central longitudinal (plano XZ o XY, según el sistema de coordenadas) y acercar la zona sensor–objetivo para visualizar `|E|` con leyenda en V/m.
4. Si el caso es convergente, conservar la corrida de 300 % como referencia y estudiar posteriormente sensibilidad del dominio exterior (por ejemplo, 200/300/400 %) y de malla usando una métrica cuantitativa común, preferentemente capacitancia extraída de forma documentada.
5. Solo tras verificar convergencia y sensibilidad, aceptar las figuras A3–A4 y continuar con extracción de capacitancia y barrido de `d_target`.

### Estado para el artículo
- Estado: **solver ejecutado y visualizaciones creadas; convergencia aún no verificada documentalmente**.
- No reportar todavía el campo máximo de la leyenda como hallazgo, ni afirmar validación de H1, hasta auditar los mensajes/convergencia y clarificar la visualización.

## 2026-10-16 — Automatización v12 preparada para mapa longitudinal de |E| en plano XZ

### Motivo
- En las capturas de v11 el overlay de líneas/vectores densos dificultaba ver el campo en la brecha frontal.
- El usuario ocultó esos overlays siguiendo la indicación anterior; por eso las líneas dejan de verse. Ocultarlas no borra los plots de v11.
- Las capturas compartidas de `Solve Setup` muestran configuración de convergencia (12 pasadas máximas, error porcentual 1 %, refinamiento por pasada 30 %, mínimo 2 pasadas y mínimo 1 pasada convergida), pero no constituyen evidencia de que esas condiciones se hayan alcanzado.

### Paquete v12
- Artefacto local: `M18_ANSYS_H1_CorteLongitudinal_v12.zip`.
- Se prepara un proyecto independiente H1 (no sobrescribe v11), con una hoja diagnóstica de espesor nulo en el plano XZ, `y=0 mm`, que cubre `x=-25..0 mm` y `z=-20..20 mm`.
- La hoja es exclusivamente de visualización; no representa un componente físico, no se le asigna excitación o frontera eléctrica. Se crea después de la región exterior, con el fin de que no cambie el cálculo inicial del tamaño de la región.
- El gráfico principal es `Mag_E` sobre la cara de la hoja, mediante `CreateFieldPlot` con `PlotGeomInfo=[1,"Surface","FacesList",1,face_id]`, tomando como base la documentación de Maxwell Scripting Guide 2025 R2: https://ansyshelp.ansys.com/public/Views/Secured/Electronics/v252/en/Subsystems/Maxwell/Subsystems/Maxwell%20Scripting/Content/CreateFieldPlot.htm
- v12 omite los overlays volumétricos de flechas y trazas 3D para no saturar la vista, y ejecuta un análisis H1 nuevo. El automatizador conserva el proyecto v11 sin modificar.
- El script y la estructura del paquete se revisaron sintácticamente fuera de AEDT. **v12 aún no ha sido ejecutada en el equipo del usuario**; la creación de la hoja y el plot deben verificarse con el JSON de salida y la interfaz.
- Ruta esperada de salidas: `%USERPROFILE%\ANSYS_M18\Maxwell_Proyectos\M18_H1_CorteLongitudinal_v12_*`.

### Próximo criterio de aceptación
1. El JSON debe informar `solved=true`, `longitudinal_cut_created=true` y `longitudinal_cut_field_plot_created=true`.
2. Revisar convergencia/adaptive passes y Message Manager. La finalización de `Analyze` no acredita por sí misma convergencia física.
3. Confirmar que el mapa de `|E|` es visible sobre el corte XZ, con unidades V/m y brecha nominal de 4 mm reconocible.
4. Si falla el plot sobre hoja, conservar el JSON/error; no atribuir un resultado físico al mapa no generado.

