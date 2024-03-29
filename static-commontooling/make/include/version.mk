#
# Makefile include file to include standard versioning support for top level
# Included by other .mk files, do not use directly.
#

PBRVERSION_VERSION?=1.4.1
PBRVERSION_CONTAINER?=public.ecr.aws/o4o2s1w1/cloudfit/pbrversion
# Since the version is pinned above, there's no need to pull images every time, especially since this tool runs very
# frequently
PBRVERSION?=$(DOCKER) run --rm -v $(project_root_dir):/data:ro $(PBRVERSION_CONTAINER):$(PBRVERSION_VERSION)

# If VERSION is't already set (because it was exported from a higher-level Makefile, extractit from a top level VERSION
# file if present, otherwise we use PBR to extract the version from git in the right formats
ifndef VERSION
# pbrversion --list gives an output of the form '<full version> <brief version> <dockerised version> <node version> <docker tag> [<docker tag>]'
# which gets split out here into the four variables we need (while only calling pbrversion once).
PBRVERSION_OUTPUT := $(shell $(PBRVERSION) --list)
export VERSION := $(shell [ -f VERSION ] && cat VERSION || echo $(word 1, $(PBRVERSION_OUTPUT)))
export NEXT_VERSION := $(shell [ -f VERSION ] && cat VERSION || echo $(word 2, $(PBRVERSION_OUTPUT)))
export DOCKERISED_VERSION := $(shell [ -f VERSION ] && cat VERSION || echo $(word 3, $(PBRVERSION_OUTPUT)))
export NODEIFIED_VERSION := $(shell [ -f VERSION ] && cat VERSION || echo $(word 4, $(PBRVERSION_OUTPUT)))
export DOCKER_TAGS := $(wordlist 5, $(words $(PBRVERSION_OUTPUT)), $(PBRVERSION_OUTPUT))

endif

all: help-version

# Versioning support
version:
	@echo $(VERSION)

next-version:
	@echo $(NEXT_VERSION)

help-version:
	@echo "$(PROJECT)-$(VERSION)"
	@echo "make version                     - Print the current version of the code in the repo, including pre-release indicators"
	@echo "make next-version                - Print the version the code should have if it is released as it currently is"

.PHONY: version next-version help-version
