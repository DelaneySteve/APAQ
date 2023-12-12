# # define the name of the virtual environment directory
# VENV := venv
# VENV_SUB := Scripts 	# if on Windows
# # VENV_SUB := bin 		# if on Mac/Linux

# # default target, when make executed without arguments
# all: venv

# $(VENV)/Scripts/activate: requirements.txt
# 	python -m venv $(VENV)
# 	./$(VENV)/Scripts/pip install -r requirements.txt

# # venv is a shortcut target
# venv: $(VENV)/Scripts/activate

# run: venv
# 	./$(VENV)/Scripts/python src/main.py

# clean:
# 	rm -rf $(VENV)
# 	find . -type f -name '*.pyc' -delete

# .PHONY: all venv run clean.

# Makefile

# VENV := venv
# VENV_SUB := Scripts		# if running Windows
# # VENV_SUB := bin			# if running Mac/Linux
# PYTHON := ${VENV}/${VENV_SUB}/python 	

# all: install run

# install: venv
# 	: # Activate venv and install something inside
# 	. $(VENV)/$(VENV_SUB)/activate && pip install -r requirements.txt
# 	: # Other commands here

# venv:
# 	: # Create venv if it doesn't exist
# 	: # test -d venv || virtualenv -p python3 --no-site-packages venv
# 	python -m venv $(VENV)

# run:
# 	: # Run your app here, e.g
# 	: # determine if we are in venv,
# 	: # see https://stackoverflow.com/q/1871549
# 	ifeq ($(VENV), )
# 		@echo "virtual env is not activated"
# 	else
# 		@echo "virtual env is activated"
# 	endif

# clean:
# 	rm -rf $(VENV)
# 	find -iname "*.pyc" -delete


VIRTUAL_ENV=venv

.ONESHELL:
DEFAULT_GOAL: help
.PHONY: help run clean build venv ipykernel update jupyter

# Colors for echos 
ccend = $(shell tput sgr0)
ccbold = $(shell tput bold)
ccgreen = $(shell tput setaf 2)
ccso = $(shell tput smso)

venv/Scripts/activate: requirements.txt
	python -m venv venv
	chmod +x venv/Scripts/activate
	. ./venv/Scripts/activate
	pip install -r requirements.txt

venv: venv/Scripts/activate
	. ./venv/Scripts/activate

run: venv
	python src/main.py

# clean: ## >> remove all environment and build files
# 	@echo ""
# 	@echo "$(ccso)--> Removing virtual environment $(ccend)"
# 	rm -rf $(VIRTUAL_ENV)

# build: ##@main >> build the virtual environment with an ipykernel for jupyter and install requirements
# 	@echo ""
# 	@echo "$(ccso)--> Build $(ccend)"
# 	$(MAKE) clean
# 	$(MAKE) install

# venv: $(VIRTUAL_ENV) ## >> install virtualenv and setup the virtual environment

# $(VIRTUAL_ENV):
# 	@echo "$(ccso)--> Install and setup virtualenv $(ccend)"
# 	python3 -m pip install --upgrade pip
# 	python3 -m pip install virtualenv
# 	virtualenv $(VIRTUAL_ENV)

# install: venv requirements.txt ##@main >> update requirements.txt inside the virtual environment
# 	@echo "$(ccso)--> Updating packages $(ccend)"
# 	$(PYTHON) -m pip install -r requirements.txt

help: ##@other >> Show this help.
	@perl -e '$(HELP_FUN)' $(MAKEFILE_LIST)
	@echo ""
	@echo "Note: to activate the environment in your local shell type:"
	@echo "   $$ source $(VIRTUAL_ENV)/bin/activate"