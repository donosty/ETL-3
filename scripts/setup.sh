#!/bin/bash
set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

cd "$(dirname "$0")/.."
echo -e "${GREEN}UBICACIÓN ACTUAL: $(pwd)${NC}"
echo -e "${GREEN}VALIDANDO DEPENDENCIAS DEL SISTEMA${NC}"

check_dep(){
    if ! command -v $1 &> /dev/null; then
        echo -e "${RED} Error: $1 no está instalado${NC}"
        exit 1
    fi
}

check_dep "docker"
check_dep "uv"

#Validar docker compose
if ! docker compose version &> /dev/null; then
    echo -e "${RED}Error: Docker Compose (plugin) no disponible${NC}"
    exit 1
fi

# Crear .env si no existe
if [ ! -f .env ]; then
    if [ -f .env.example ]; then
        cp .env.example .env
        echo -e "${GREEN}Archivo .env creado desde el ejemplo${NC}"
    else
        echo -e "${RED}Error: No existe .env.example para copiar${NC}"
        exit 1
    fi
fi

if [ ! -d logs ]; then
    mkdir -p logs/bd-logs logs/etl-logs
fi

START_TIME=$(date +%s)

echo -e "${GREEN}Limpiando residuos${NC}"
docker compose down

echo -e "${GREEN}Levantando infraestructura en segundo plano${NC}"
docker compose up -d --build

echo -e "${BLUE}Esperando a que el proceso ETL termine${NC}"
EXIT_CODE=$(docker wait etl_app || echo "1")

TIMESTAMP=$(date +'%Y%m%d_%H%M%S')
LOG_FILE_BD="logs/bd-logs/bd_run_${TIMESTAMP}.log"
LOG_FILE_ETL="logs/etl-logs/etl_run_${TIMESTAMP}.log"

echo -e "${BLUE}Extrayendo logs a: $LOG_FILE_BD${NC}"
docker logs bd-postgres &> "$LOG_FILE_BD"

echo -e "${BLUE}Extrayendo logs a: $LOG_FILE_ETL${NC}"
docker logs etl_app &> "$LOG_FILE_ETL"


END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))


if [ "$EXIT_CODE" -eq 0 ]; then
    echo -e "${GREEN}Pipeline completado con éxito${NC}"
else
    echo -e "${RED}El Pipeline falló con código $EXIT_CODE${NC}"
    echo -e "${RED}Revisa el log en:${NC}"
    echo -e "${RED}BD: $LOG_FILE_BD"
    echo -e "${RED}ETL: $LOG_FILE_ETL"
fi


echo -e "${BLUE}Duracion del pipeline: ${DURATION}s${NC}"

echo -e "${GREEN}Estado de los contenedores:${NC}"
docker compose ps