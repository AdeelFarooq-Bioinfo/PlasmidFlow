---
title: 'PlasmidFlow: A Web-based Platform for Interactive Visualization of Plasmid-Driven Traits'
tags:
  - Python
  - Dash
  - Flask
  - Plasmid
  - Genomics
  - Visualization
  - Microbiology
  - Bioinformatics
authors:
  - name: Adeel Farooq
    affiliation: 1
  - name: Asma Rafique
    affiliation: 2
affiliations:
  - name: Department of Food Science, University of Guelph, Canada
    index: 1
  - name: Department of Human Health and Nutritional Sciences, University of Guelph, Canada
    index: 2
date: 19 August 2025
bibliography: paper.bib
---

# Summary

Plasmids are central drivers of microbial evolution, antimicrobial resistance dissemination, and functional adaptation. Despite their importance, interactive and user-friendly visualization platforms for plasmid-driven traits remain limited. **PlasmidFlow** is a web-based platform developed in Python using Flask and Dash that enables researchers to upload plasmid datasets and explore their traits in an intuitive, customizable, and interactive interface.

PlasmidFlow provides dynamic visualization of plasmid size, content, and annotated traits. Users can filter, color, and resize visual elements to explore relationships between plasmids and associated functions. The tool is designed for both microbiologists with minimal programming expertise and computational researchers who require modular visualization components for downstream integration.

# Statement of need

The ability to explore plasmid traits interactively is critical for advancing microbial genomics, antimicrobial resistance surveillance, and biocontrol applications. Current pipelines often require heavy command-line expertise and lack accessible web-based visualization tailored to plasmid biology.

**PlasmidFlow** fills this gap by:
- Providing an **interactive web interface** where plasmid data can be explored dynamically.
- Allowing **customization of visualizations** (colors, node sizes, trait labels).
- Enabling **integration with plasmid trait databases** for functional annotation.
- Supporting **modular deployment** for local research or online hosting.

PlasmidFlow complements annotation pipelines by serving as a visualization endpoint, facilitating hypothesis generation and communication of results to both scientific and applied audiences. It is particularly suited for microbiology, biotechnology, and clinical research groups studying plasmid functions.

# Functionality

PlasmidFlow provides:
- Upload of plasmid files in supported formats.
- Interactive network and matrix visualization of plasmid traits.
- Trait filtering and highlighting (e.g., antimicrobial resistance, mobilization, virulence).
- Export of results and figures for downstream analysis or publication.
- Modular backend structure (Flask) with a responsive frontend (Dash/Plotly).

# Example use case

Researchers investigating the distribution of antimicrobial resistance plasmids can upload annotated plasmid datasets into PlasmidFlow. The tool immediately generates trait matrices and interactive networks where resistance determinants can be filtered, resized by frequency, and visualized alongside other plasmid-encoded traits. The user can export publication-quality figures or download summary tables for further statistical analysis.

# Related work

Existing plasmid visualization efforts are typically static or embedded within larger genome browsers. Tools like Bandage and Artemis are powerful but not specialized for **trait-focused plasmid visualization**. PlasmidFlow provides a lightweight, web-based, trait-centric alternative that integrates seamlessly into genomics workflows.

# Acknowledgements

We thank LaPointe’s Research Group for feedback during interface development. Development was supported by postdoctoral funding at the University of Guelph.

# References

