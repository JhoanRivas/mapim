#!/usr/bin/env bash
host="$1"
port="$2"
shift 2
until nc -z "$host" "$port"; do
  >&2 echo "Postgres no está disponible - durmiendo"
  sleep 1
done

>&2 echo "Postgres está activo: ejecutando comando"
exec "$@"
