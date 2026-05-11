#!/bin/bash
echo "Deploying Grafana..."
docker-compose -f "$(dirname "$0")/docker-compose.yml" up -d
echo "Grafana is running at http://localhost:3000 (Admin: admin / admin)"
