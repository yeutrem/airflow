#!/bin/bash

docker compose -f docker-compose.yaml --env-file=prod.env --profile flower up -d
