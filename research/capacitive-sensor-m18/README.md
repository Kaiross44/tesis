# Estudio paramétrico del sensor capacitivo M18

Estudio computacional complementario de la tesis.

## Objetivo inicial
Analizar mediante modelos geométricos paramétricos y simulación electrostática FEM la influencia del entrehierro entre electrodos sobre la distribución del campo eléctrico y la capacitancia equivalente.

## Alcance
- Envolvente conocida: M18 y longitud total de 69 mm.
- Arquitectura interna real: desconocida.
- Geometrías internas candidatas: sustentadas en literatura y patentes.
- ANSYS/FEM: referencia numérica.
- Python/PyVista: exploración paramétrica y visualización 3D.
- Inductivos: extensión futura, no foco actual.

## Estructura
- `docs/`: hipótesis y metodología.
- `python/`: modelos y visualización interactiva.
- `ansys/`: modelos y documentación FEM.
- `data/`: parámetros y resultados exportados.
