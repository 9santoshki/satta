# Makefile for managing Docker commands

# Default target (runs when `make` is called without arguments)
.DEFAULT_GOAL := help

# Services
SERVICE_BACKEND=backend
SERVICE_FRONTEND=frontend
SERVICE_DB=db

# Docker Compose file
DOCKER_COMPOSE=docker-compose

# Build the Docker images for backend and frontend
build: ## Build the Docker containers
	$(DOCKER_COMPOSE) up --build -d

# Start the containers in detached mode
up: ## Start the Docker containers
	$(DOCKER_COMPOSE) up -d

# Stop the containers
down: ## Stop and remove the Docker containers
	$(DOCKER_COMPOSE) down

# Restart the Docker containers
restart: ## Restart the Docker containers
	$(DOCKER_COMPOSE) restart

# View the logs of the backend container
logs-backend: ## Tail the backend logs
	$(DOCKER_COMPOSE) logs -f $(SERVICE_BACKEND)

# View the logs of the frontend container
logs-frontend: ## Tail the frontend logs
	$(DOCKER_COMPOSE) logs -f $(SERVICE_FRONTEND)

# Run database migrations
migrate: ## Apply Django migrations
	$(DOCKER_COMPOSE) exec $(SERVICE_BACKEND) python manage.py migrate

# Create a Django superuser
createsuperuser: ## Create a superuser for Django admin
	$(DOCKER_COMPOSE) exec $(SERVICE_BACKEND) python manage.py createsuperuser

# Show the status of the Docker containers
status: ## Show the status of Docker containers
	$(DOCKER_COMPOSE) ps

# Clean up unused Docker containers, images, and volumes
prune: ## Clean up unused Docker containers and images
	docker system prune -af

# Display help (this is the default target)
help: ## Show this help message
	@echo "Available commands:"
	@echo "  make build             Build the Docker containers"
	@echo "  make up                Start the Docker containers"
	@echo "  make down              Stop and remove the Docker containers"
	@echo "  make restart           Restart the Docker containers"
	@echo "  make logs-backend      Tail the backend logs"
	@echo "  make logs-frontend     Tail the frontend logs"
	@echo "  make migrate           Apply Django migrations"
	@echo "  make createsuperuser   Create a superuser for Django admin"
	@echo "  make status            Show the status of Docker containers"
	@echo "  make prune             Clean up unused Docker containers and images"
