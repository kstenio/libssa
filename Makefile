# Commands for setting up/installing uv 
uv_ver := 0.4

install-uv-linux:
	curl -LsSf https://astral.sh/uv/$(uv_ver)/install.sh | sh

install-uv-windows:
	powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/$(uv_ver)/install.ps1 | iex"

# Commands for setting up the environment
setup:
	uv sync --dev

setup-pc:
	uv run pre-commit install --install-hooks

# Pre-commit commands
pc-run:
	uv run pre-commit run

pc-run-all:
	uv run pre-commit run --all-files

# Commitizen commands (type -> alpha|beta|rc)
bump: setup
	uv run cz bump

bump-prerelease: setup
	uv run cz bump --prerelease $(type)

# Ruff commands
ruff-run:
	uv run ruff check --select I --fix
	uv run ruff format

# Testing commands
test:
	uv run pytest