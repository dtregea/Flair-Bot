IMAGE_NAME := modbot

.PHONY: build up up-d

build:
	docker build -t $(IMAGE_NAME) .

up:
	docker run --name $(IMAGE_NAME) --rm --env-file .env $(IMAGE_NAME)

up-d:
	docker run -d --name $(IMAGE_NAME) --rm --env-file .env $(IMAGE_NAME)

down:
	docker rm -f $(IMAGE_NAME)