# Automating building virtual environment

.ONESHELL:
DEFAULT_GOAL: help
.PHONY: help venv run clean

VIRTUAL_ENV = venv
VIRTUAL_ENV_SUB = Scripts		# if using Windows
# VIRTUAL_ENV_SUB = bin 		# if using Mac/Linux

PYTHON = ./$(VIRTUAL_ENV)/Scripts/python
PIP = ./$(VIRTUAL_ENV)/Scripts/pip

# Colors for echos (from https://gist.github.com/genyrosk/50196ad03231093b604cdd205f7e5e0d)
ccend = $(shell tput sgr0)
ccso = $(shell tput smso)

$(VIRTUAL_ENV)/Scripts/activate: requirements.txt ## >> build the virtual environment and activate it in the oneshell
	@echo ''
	@echo '$(ccso)--> Building virtual environment $(ccend)'
	python -m venv $(VIRTUAL_ENV)
	chmod +x $(VIRTUAL_ENV)/Scripts/activate
	. ./$(VIRTUAL_ENV)/Scripts/activate
	$(PIP) install -r requirements.txt

$(VIRTUAL_ENV): $(VIRTUAL_ENV)/Scripts/activate ## >> install virtualenv and setup the virtual environment
	. ./$(VIRTUAL_ENV)/Scripts/activate

run: $(VIRTUAL_ENV) ## >> Run the API
	@echo ''
	@echo '$(ccso)--> Generating your API key $(ccend)'
	> .env
	printf 'API_KEY=' >> .env
	gpg --gen-random --armor 1 18 >> .env
	cat .env
	@echo ''
	@echo '$(ccso)--> Running the API $(ccend)'
	$(PYTHON) -m src.main

clean:  ## >> Remove all environment and build files
	@echo ''
	@echo '$(ccso)--> Removing virtual environment $(ccend)'
	rm -rf $(VIRTUAL_ENV)

# And add help text after each target name starting with '\#\#'
# A category can be added with @category
HELP_FUN = \
	%help; \
	while(<>) { push @{$$help{$$2 // 'options'}}, [$$1, $$3] if /^([a-zA-Z\-\$\(]+)\s*:.*\#\#(?:@([a-zA-Z\-\)]+))?\s(.*)$$/ }; \
	print 'usage: make [target]\n\n'; \
	for (sort keys %help) { \
	print '${WHITE}$$_:${RESET}\n'; \
	for (@{$$help{$$_}}) { \
	$$sep = ' ' x (32 - length $$_->[0]); \
	print '  ${YELLOW}$$_->[0]${RESET}$$sep${GREEN}$$_->[1]${RESET}\n'; \
	}; \
	print '\n'; }

help: ##@other >> Show this help.
	@perl -e '$(HELP_FUN)' $(MAKEFILE_LIST)
	@echo ''
	@echo 'Note: to activate the environment in your local shell type:'
	@echo '   $$ source $(VIRTUAL_ENV)/Script/activate for Windows or source $(VIRTUAL_ENV)/bin/activate for Mac/Linux'