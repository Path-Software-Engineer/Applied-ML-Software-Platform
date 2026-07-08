# Architecture — Retail Intelligence Platform

## Objetivo

Definir la estructura base del proyecto `01-retail-intelligence-platform`.

Este proyecto se organiza como una plataforma aplicada de IA para retail, separando responsabilidades entre frontend, backend, servicios de IA, datos, reportes, documentación, labs y despliegue.

## Capas principales

### frontend/

Responsable de mostrar el dashboard visual y permitir que el usuario vea resultados de ventas, métricas, modelos e inventario.

### backend/

Responsable de exponer endpoints, coordinar servicios y servir datos procesados al frontend.

### ai-services/

Responsable de contener la lógica de análisis, feature engineering, baseline, métricas, modelos e insights.

### data/

Responsable de guardar datos raw y processed.

### models/

Responsable de guardar artefactos de modelos y metadatos.

### reports/

Responsable de guardar summaries, métricas, gráficos y reportes generados.

### docs/

Responsable de guardar arquitectura, decisiones, user stories, technical stories y documentación de sprints.

### labs/

Responsable de guardar experimentos técnicos, cloud, producto y documentación.

### tests/

Responsable de guardar pruebas mínimas por capa.

### scripts/

Responsable de guardar comandos repetibles.

### deployment/

Responsable de guardar notas y archivos relacionados con despliegue.