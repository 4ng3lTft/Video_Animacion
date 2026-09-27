#!/bin/bash
# Renderiza todos los fotogramas PNG de una composición en 4 procesos paralelos.
# Uso: NODE_PATH=... herramientas/cuadros.sh <composicion.html> <carpeta> <total_fotogramas>
set -e
html=$1; dir=$2; total=$3; n=4
por=$(( (total + n - 1) / n ))
for i in $(seq 0 $((n-1))); do
  a=$((i*por)); b=$(( (i+1)*por - 1 )); [ $b -ge $total ] && b=$((total-1))
  node "$(dirname "$0")/render.cjs" "$html" "$dir" --cuadros $a-$b 2>&1 | grep -v "^  " &
done
wait
