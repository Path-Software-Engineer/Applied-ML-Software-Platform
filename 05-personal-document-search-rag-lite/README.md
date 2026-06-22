# 05-personal-document-search-rag-lite

## 🧠 Descripción

Buscador semántico ligero para documentos personales o notas técnicas.

Este proyecto introduce conceptos de RAG de forma pequeña y aplicada: cargar documentos, dividirlos en fragmentos, buscar por significado y mostrar fuentes recuperadas.

No busca crear un agente complejo. Busca una herramienta clara para consultar documentos pequeños con evidencia visible.

---

## 🎯 Objetivo

Crear un buscador semántico pequeño para documentos personales o notas técnicas:

```txt
Documentos → ingesta → chunks → embeddings / búsqueda semántica → resultados con fuentes → UI simple
```

---

## 👤 Usuario objetivo

* Estudiante con apuntes técnicos.
* Persona que quiere buscar dentro de documentos propios.
* Investigador que necesita recuperar fragmentos.
* Reclutador técnico interesado en RAG aplicado de forma ligera.

---

## 🧱 Arquitectura esperada

```txt
Documentos locales
      ↓
Document Ingestion
      ↓
Chunking
      ↓
Semantic Search
      ↓
Source Display
      ↓
UI simple / README visual
```

---

## 🧩 Módulos

### Módulo 1 — Document Ingestion

Cargar documentos.

### Módulo 2 — Chunking

Dividir texto en partes pequeñas.

### Módulo 3 — Semantic Search

Buscar por significado.

### Módulo 4 — Source Display

Mostrar fuentes recuperadas.

---

## 🧪 Labs

### tec-document-ingestion-lab

Cargar documentos locales y preparar texto.

### tec-chunking-basic-lab

Dividir documentos en chunks y analizar tamaño.

### tec-semantic-search-lab

Realizar búsqueda semántica y revisar resultados.

### cloud-documents-to-gcp-cloud-storage-lab

Traducir conceptualmente documentos locales hacia GCP Cloud Storage.

### cloud-documents-to-aws-s3-lab

Traducir conceptualmente documentos locales hacia AWS S3.

### cloud-documents-to-azure-blob-lab

Traducir conceptualmente documentos locales hacia Azure Blob Storage.

---

## 📊 Métricas / Evidencia

* Documentos cargados.
* Número de chunks.
* Consulta de ejemplo.
* Fragmentos recuperados.
* Fuentes visibles.
* Limitaciones del buscador.
* Capturas o evidencia visual.
* README con ejemplo de uso.

---

## 🚀 Estado actual

Pendiente / por iniciar.

---

## 🧭 Ciclo de trabajo

```txt
Día 1 → Exploración
Día 2 → Ejecución 1
Día 3 → Ejecución 2
Día 4 → Ejecución 3
```

---

## 📌 Próximos pasos

* Elegir 3 a 5 documentos.
* Crear ingesta de documentos.
* Crear chunking básico.
* Crear búsqueda semántica.
* Mostrar fuentes recuperadas.
* Crear UI simple o salida visual.
* Documentar limitaciones.
* Cerrar labs.
* Preparar capturas.
* Publicar repo.
