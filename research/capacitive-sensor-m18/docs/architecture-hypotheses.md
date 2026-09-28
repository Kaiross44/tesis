# Hipótesis de arquitectura interna

## Estado actual
La envolvente externa considerada es M18 × 69 mm. La arquitectura interna del dispositivo comercial no está disponible directamente.

## H1 — electrodo central + electrodo auxiliar anular
Se modelará una cabeza capacitiva con electrodo central circular y electrodo auxiliar anular, separados por un entrehierro radial `g`.

### Variables
- `D_sensor`: diámetro exterior nominal.
- `L_sensor`: longitud total.
- `r_core`: radio del electrodo central.
- `r_aux_inner`: radio interior del electrodo auxiliar.
- `r_aux_outer`: radio exterior del electrodo auxiliar.
- `g = r_aux_inner - r_core`.
- `d_target`: distancia objetivo-cara activa.
- `V_exc`: excitación.
- `epsilon_r`: permitividad relativa.

## Pregunta inicial
¿Cómo modifica `g` la distribución tridimensional del campo eléctrico y la capacitancia equivalente?

## Otras hipótesis
- H2: electrodo central + guarda/blindaje.
- H3: electrodo interno + shield + electrodo externo/carcasa.
- H4: electrodos cilíndricos con separación axial.

Estas configuraciones son hipótesis comparativas, no descripciones confirmadas del sensor comercial.
