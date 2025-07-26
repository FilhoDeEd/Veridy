# .PHONY: production_build production_up production_down \
#         staging_build staging_up staging_down \
#         dev_build dev_up dev_down

.PHONY: dev_build dev_up dev_down

# production_build: Dockerfile docker-compose-production.yml
# 	docker compose -p veridy_production -f docker-compose-production.yml --env-file .secrets/production.env up --build -d

# production_up: Dockerfile docker-compose-production.yml
# 	docker compose -p veridy_production -f docker-compose-production.yml --env-file .secrets/production.env up -d

# production_down: Dockerfile docker-compose-production.yml
# 	docker compose -p veridy_production -f docker-compose-production.yml --env-file .secrets/production.env down

# staging_build: Dockerfile docker-compose-staging.yml
# 	docker compose -p veridy_staging -f docker-compose-staging.yml --env-file .secrets/staging.env up --build -d

# staging_up: Dockerfile docker-compose-staging.yml
# 	docker compose -p veridy_staging -f docker-compose-staging.yml --env-file .secrets/staging.env up -d

# staging_down: Dockerfile docker-compose-staging.yml
# 	docker compose -p veridy_staging -f docker-compose-staging.yml --env-file .secrets/staging.env down

dev_build: Dockerfile docker-compose-dev.yml
	docker compose -p veridy_dev -f docker-compose-dev.yml --env-file .secrets/development.env up --build -d

dev_up: Dockerfile docker-compose-dev.yml
	docker compose -p veridy_dev -f docker-compose-dev.yml --env-file .secrets/development.env up -d

dev_down: Dockerfile docker-compose-dev.yml
	docker compose -p veridy_dev -f docker-compose-dev.yml --env-file .secrets/development.env down
