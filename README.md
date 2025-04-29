# Microstorm 🚀

**Microstorm** es un micro-framework para construir microservicios modernos en **Python** usando **FastAPI**, enfocado en:

- Simplicidad
- Auto-registro dinámico de servicios
- Comunicación segura entre microservicios
- Métricas Prometheus integradas
- Registro Discovery Server opcional
- Control de acceso a métodos (público, privado, protegido)

Ideal para arquitecturas basadas en microservicios pequeños, escalables y seguros.

---

## ✨ Características principales

- 🔒 Control de acceso con decoradores (@private, @public, @protected)
- 📦 Auto-registro de servicios (archivo local o Discovery Server)
- 📡 Comunicación HTTP segura usando JWT
- 📊 Métricas listas para Prometheus
- 🔄 Reintentos automáticos con backoff exponencial
- 📚 Fácil integración en cualquier proyecto FastAPI

---

## ⚙️ Instalación

```bash
pip install fastapi uvicorn httpx prometheus_client python-dotenv
