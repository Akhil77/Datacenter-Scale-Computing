VERSION=v1
DOCKERUSER=akhilsm

#
# You should probably update the docker.io user if you update this
#
build:
	docker buildx build -f Dockerfile -t sentiment-logs . --platform=linux/amd64

push:
	docker tag sentiment-logs $(DOCKERUSER)/sentiment-logs:$(VERSION)
	docker push $(DOCKERUSER)/sentiment-logs:$(VERSION)