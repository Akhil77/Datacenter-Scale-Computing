VERSION=v5
DOCKERUSER=akhilsm

build:
	docker buildx build -f Dockerfile -t sentiment-worker . --platform=linux/amd64
push:
	docker tag sentiment-worker $(DOCKERUSER)/sentiment-worker:$(VERSION)
	docker push $(DOCKERUSER)/sentiment-worker:$(VERSION)

#docker tag sentiment-worker $(DOCKERUSER)/sentiment-worker:latest
#docker push $(DOCKERUSER)/sentiment-worker:latest

##
## The dirkcgrunwald/flair:latest container simply includes the FLAIR library
##

DOCKERUSER_FLAIR=dirkcgrunwald
build-base:
	docker build -f Dockerfile-flair -t flair .
push-base:
	docker tag flair $(DOCKERUSER_FLAIR)/flair:latest
	docker push $(DOCKERUSER_FLAIR)/flair:latest