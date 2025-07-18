# .PHONY: production_build production_up production_down \
#         staging_build staging_up staging_down \
#         dev_build dev_up dev_down

.PHONY: dev_build dev_up dev_down

# production_build: Dockerfile docker-compose-production.yml
# 	sudo docker compose -p production -f docker-compose-production.yml --env-file env/production.env up --build -d

# production_up: Dockerfile docker-compose-production.yml
# 	sudo docker compose -p production -f docker-compose-production.yml --env-file env/production.env up -d

# production_down: Dockerfile docker-compose-production.yml
# 	sudo docker compose -p production -f docker-compose-production.yml --env-file env/production.env down

# staging_build: Dockerfile docker-compose-staging.yml
# 	sudo docker compose -p staging -f docker-compose-staging.yml --env-file env/staging.env up --build -d

# staging_up: Dockerfile docker-compose-staging.yml
# 	sudo docker compose -p staging -f docker-compose-staging.yml --env-file env/staging.env up -d

# staging_down: Dockerfile docker-compose-staging.yml
# 	sudo docker compose -p staging -f docker-compose-staging.yml --env-file env/staging.env down

dev_build: Dockerfile docker-compose-dev.yml
	sudo docker compose -p dev -f docker-compose-dev.yml --env-file env/development.env up --build -d

dev_up: Dockerfile docker-compose-dev.yml
	sudo docker compose -p dev -f docker-compose-dev.yml --env-file env/development.env up -d

dev_down: Dockerfile docker-compose-dev.yml
	sudo docker compose -p dev -f docker-compose-dev.yml --env-file env/development.env down
