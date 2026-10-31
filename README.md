# 🍇 Vineyard MLOps

Pipeline MLOps end-to-end para detectar enfermedades en hojas de vid con visión por
computador. Orquestado con Apache Airflow y desplegable con Docker.

![CI](https://github.com/TU_USUARIO/TU_REPO/actions/workflows/ci.yml/badge.svg)

## Estado

- [x] Infraestructura: Airflow, Postgres, RustFS (almacén compatible con S3)
- [x] DAG de ingesta con validación de imágenes (formato, tamaño, duplicados)
- [x] Tests y CI con GitHub Actions
- [ ] Baseline de entrenamiento y tracking con MLflow
- [ ] Evaluación en datos de campo (domain shift)
- [ ] API de inferencia y demo pública

## Arranque

    cp .env.example .env
    docker compose up -d --build

Airflow: http://localhost:8080 · Consola de almacenamiento: http://localhost:9001