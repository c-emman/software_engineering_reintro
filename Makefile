IMAGE_NAME=products_webapp
CONTAINER_NAME=products_webapp_container

docker-build:
	docker build -t $(IMAGE_NAME) .

docker-run:
	docker run -it --env-file ./src/.env products_webapp
