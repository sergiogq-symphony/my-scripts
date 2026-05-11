#!/bin/bash
echo "Destroying Grafana..."
docker-compose -f "$(dirname "$0")/docker-compose.yml" down -v
echo "Grafana and its volumes have been removed."
