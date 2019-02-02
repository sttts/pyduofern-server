all: build

IMAGE_ORG ?= docker.io/sttts
ARCHS ?= amd64 arm32v6 arm64v8
SHELL := /bin/bash -e
REPO ?= $(IMAGE_ORG)/pyduofern-server

.PHONY: build
build:
		# nothing to build for python

# all the multi-arch logic below follows https://lobradov.github.io/Building-docker-multiarch-images/

.PHONY: experimental-docker-cli
experimental-docker-cli:
		@if ! docker manifest &>/dev/null; then \
				echo "Enable experimental docker CLI manifest command: set .experimental to \"enabled\" in ~/.docker/config.json."; \
				false; \
		fi

.PHONY: deps
deps:
		pip install -r requirements

.PHONY: images
images: experimental-docker-cli
		for arch in $(ARCHS); do \
			docker build -f <(sed "s/__BASEIMAGE_ARCH__/$${arch}/" Dockerfile) -t $(REPO):$${arch}-latest .; \
		done

.PHONY: push
push: experimental-docker-cli
		for arch in $(ARCHS); do \
			docker push $(REPO):$${arch}-latest; \
		done
		docker manifest create -a $(REPO):latest $(REPO):amd64-latest $(REPO):arm32v6-latest $(REPO):arm64v8-latest
		docker manifest annotate $(REPO):latest $(REPO):arm32v6-latest --os linux --arch arm
		docker manifest annotate $(REPO):latest $(REPO):arm64v8-latest --os linux --arch arm64 --variant armv8
		docker manifest push $(REPO):latest