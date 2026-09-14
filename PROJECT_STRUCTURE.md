# Thesis project structure

The current manuscript is a conference-style IEEE paper in methodology stage.

## Research blocks represented

- Analytical model: capacitance, thermal strain, thermal expansion, gap variation, structural dynamics, modal analysis.
- Numerical work: ANSYS finite-element thermomechanical, modal and harmonic analyses.
- Experimental platform: thermal excitation, vibration excitation, reference instrumentation, capacitive measurement, synchronized DAQ and safety.
- Thermomechanical adapter: mechanical interface with SMA element.
- Validation: baseline versus protected configuration, attenuation and experiment-vs-FEA comparison.

## Suggested repository areas

```text
tesis/
  manuscript/
    es/
    en/
  references/
  figures/
    conceptual/
    bench/
    method/
    adapter/
  cad/
    bench/
    adapter/
  ansys/
    geometry/
    materials/
    thermomechanical/
    modal/
    harmonic/
  experiments/
    raw/
    processed/
    metadata/
    protocols/
  analysis/
  docs/
  overleaf/
```

The manuscript itself explicitly reserves four figures for the conceptual integration, bench architecture, methodological sequence, and adapter concept, so those figure groups should be maintained.