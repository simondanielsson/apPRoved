.PHONY:
	install_poetry
	install
	install_dev

install_poetry:
	pip install --upgrade pip
	# Installing poetry if not installed...
	@python -m poetry --version || \
		pip install poetry

install: install_poetry
	poetry install

install_dev: install_poetry
	poetry install --with dev,test
	# Installs the pre-commit hook.
	pre-commit install
