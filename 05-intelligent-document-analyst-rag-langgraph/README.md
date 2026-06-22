# 05-intelligent-document-analyst-rag-langgraph

## 🧠 Descripción

Asistente inteligente para analizar documentos usando RAG, embeddings, LangGraph, tools y guardrails.

Este proyecto trabaja recuperación de información, respuestas con fuentes, flujos controlados de agentes y evaluación básica de respuestas.

---

## 🎯 Objetivo

Construir un sistema capaz de responder preguntas sobre documentos mostrando fuentes y controlando el flujo del agente.

---

## 👤 Usuario objetivo

* Estudiante.
* Investigador.
* Analista.
* Equipo que trabaja con documentos técnicos.
* Reclutador técnico interesado en RAG y agentes.

---

## 🧱 Arquitectura esperada

```txt
Documents
   ↓
Chunking
   ↓
Embeddings
   ↓
Vector Database
   ↓
Retriever
   ↓
RAG
   ↓
LangGraph Agent
   ↓
Tools / Guardrails
   ↓
Chat UI
```

---

## 🧩 Módulos

### Módulo 1 — Embeddings

Comparar modelos de embeddings.

### Módulo 2 — Chunking

Comparar tamaños de chunk.

### Módulo 3 — Retrieval

Evaluar si recupera fuentes correctas.

### Módulo 4 — LangGraph Workflow

Controlar pasos del agente.

### Módulo 5 — Guardrails

Reducir alucinaciones y prompt injection.

---

## 🧪 Labs

* `tec-semantic-search-lab`
* `tec-rag-evaluation-lab`
* `tec-langgraph-tool-use-lab`
* `cloud-rag-documents-to-aws-s3-lab`
* `cloud-rag-to-aws-bedrock-concept-lab`
* `cloud-rag-to-azure-openai-concept-lab`

---

## 📊 Métricas / Evidencia

* Documentos cargados.
* Chunks generados.
* Embeddings creados.
* Vector database funcional.
* Fuentes visibles.
* RAG funcional.
* LangGraph básico.
* Tools.
* Guardrails.
* Demo de chat.

---

## 🚀 Estado actual

Pendiente.

---

## 🧭 Ciclo de trabajo

```txt
Día 1 → Exploración
Día 2 → Ejecución
Día 3 → Ejecución
Día 4 → Ejecución
```

---

## 📌 Próximos pasos

* Cargar documentos.
* Dividir en chunks.
* Crear embeddings.
* Guardar en FAISS o ChromaDB.
* Crear retrieval.
* Crear RAG.
* Crear chat UI.
* Agregar LangGraph.
* Agregar tools.
* Agregar guardrails.
* Evaluar respuestas.
* Grabar demo.
* Actualizar LinkedIn y CV.

