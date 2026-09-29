![NORA logo](https://i.ibb.co/0VJCC9Gf/IMG-20260114-WA0008.jpg)
 
# Geochemical Geothermometer
 
*For geothermal geologists and geochemists: enter concentrations of key ions or silica in geothermal fluids to instantly estimate reservoir temperature using standard geothermometers.*
 
[![GitHub](https://img.shields.io/badge/GitHub-Nora--Research--Lab-181717?logo=github)](https://github.com/Nora-Research-Lab) [![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-NoraResearchLab-yellow)](https://huggingface.co/NoraResearchLab) [![LinkedIn](https://img.shields.io/badge/LinkedIn-NORA%20Research%20Lab-0A66C2?logo=linkedin)](https://www.linkedin.com/company/nora-research-lab) [![X](https://img.shields.io/badge/X-@noraresearchlab-000000?logo=x)](https://x.com/noraresearchlab) [![NORA Research Lab](https://img.shields.io/badge/Website-noraresearchlab.site-2ea44f)](https://noraresearchlab.site) [![NORA Earth Intelligence](https://img.shields.io/badge/Platform-noraearth.xyz-2ea44f)](https://noraearth.xyz)
 

## Overview
 
**Industry:** Geothermal Energy
 
Inputs:
- Select a geothermometer method from a dropdown: Na-K (Fournier, 1979), Na-K (Giggenbach, 1988), Na-K-Ca (Fournier & Truesdell, 1973), Quartz (no steam loss), Quartz (adiabatic cooling).
- Depending on method, enter ion concentrations in mg/L: for Na-K methods: Na and K; for Na-K-Ca: Na, K, Ca; for Quartz methods: SiO2.
- Optional: for Na-K-Ca, a correction factor for Ca (usually 1/3 or 4/3) selectable.
- Temperature units default to °C, output also in °C.

Core calculation logic:
Na-K (Fournier): T = (1217.0 / (log10(Na/K) + 1.483)) - 273.15
Na-K (Giggenbach): T = (1390.0 / (log10(Na/K) + 1.750)) - 273.15
Na-K-Ca: T = {1647.0 / [log10(Na/K) + β*log10(sqrt(Ca)/Na) + 2.24]} - 273.15, with β = 1/3 if T<100°C else 4/3 (iterative).
Quartz (no steam loss): T = [72.5 * (log10(SiO2))^2 - 36.0 * log10(SiO2) + 42.4] for SiO2 in mg/L, valid 0-250°C.
Quartz (adiabatic): T = [42.2 * (log10(SiO2))^2 - 22.0 * log10(SiO2) + 24.4].

Classification: If T < 100°C → low enthalpy, 100-200°C → medium, >200°C → high.
If any required input is zero or negative, show error.

UI layout:
- Top: dropdown for method.
- Below: dynamic input fields (labels with units).
- 'Calculate' button.
- Output area: computed temperature in °C, enthalpy class, and the formula used.
- Optionally, a small info box with brief explanation of assumptions.

No AI/ML component. Purely deterministic geothermometer equations. Output is a single temperature value and classification.
 
## Run it
 
```bash
docker build -t geochemical-geothermometer .
docker run -p 7860:7860 geochemical-geothermometer
```
 
Then open http://localhost:7860 in your browser.
 
## About
 
This tool was generated and published automatically by the **NORA Earth Intelligence**
tool factory, an autonomous pipeline maintained by **NORA Research Lab** that turns
one idea per run into a small, working geoscience tool — end to end, with an
LLM writing and Docker-testing the code, and another model generating the
banner above.
 
- Platform: [https://noraearth.xyz](https://noraearth.xyz)
- Parent lab: [https://noraresearchlab.site](https://noraresearchlab.site)
 
Built 2026-09-29.
 
---
 
### Maintainer
 
**NORA Research Lab**
[![GitHub](https://img.shields.io/badge/GitHub-Nora--Research--Lab-181717?logo=github)](https://github.com/Nora-Research-Lab) [![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-NoraResearchLab-yellow)](https://huggingface.co/NoraResearchLab) [![LinkedIn](https://img.shields.io/badge/LinkedIn-NORA%20Research%20Lab-0A66C2?logo=linkedin)](https://www.linkedin.com/company/nora-research-lab) [![X](https://img.shields.io/badge/X-@noraresearchlab-000000?logo=x)](https://x.com/noraresearchlab) [![NORA Research Lab](https://img.shields.io/badge/Website-noraresearchlab.site-2ea44f)](https://noraresearchlab.site) [![NORA Earth Intelligence](https://img.shields.io/badge/Platform-noraearth.xyz-2ea44f)](https://noraearth.xyz)
