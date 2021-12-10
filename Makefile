USE_VERSION_FILE:=TRUE

# Needed here due to gitignore being generated in standalone.mk but Dockerfile.multi being added in docker.mk
EXTRA_GITIGNORE_LINES+=Dockerfile.multi

include ./static-commontooling/make/lib_static_commontooling.mk
include ./static-commontooling/make/standalone.mk
include ./static-commontooling/make/pythonic.mk
include ./static-commontooling/make/docker.mk
