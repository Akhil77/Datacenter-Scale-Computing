VERSION=v5
DOCKERUSER=akhilsm

build:
	docker buildx build -f Dockerfile -t sentiment-rest . --platform=linux/amd64

push:
	docker tag sentiment-rest $(DOCKERUSER)/sentiment-rest:$(VERSION)
	docker push $(DOCKERUSER)/sentiment-rest:$(VERSION)
	
#docker tag sentiment-rest $(DOCKERUSER)/sentiment-rest:latest
#docker push $(DOCKERUSER)/sentiment-rest:latest
