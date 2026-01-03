BACKEND_WC = ./BackEnd/
VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

MOCK_WC = ./Mock/
MOCK_SCRIPT = $(MOCK_WC)main.py

TTY_BACKEND = /dev/ttyV0
TTY_MOCK = /dev/ttyV1

create_venv:
	python3 -m venv $(VENV)

install_deps: create_venv
	$(PIP) install -r requirements.txt

update_deps:
	$(PIP) freeze > requirements.txt

start_backend:
	$(PYTHON) $(BACKEND_WC)main.py

test_backend:
	$(PYTHON) -m pytest $(BACKEND_WC)

shell: create_venv
	@bash --rcfile <(echo "source $(VENV)/bin/activate; PS1='(venv) $$PS1'") -i

start_mock_backend: create_venv
	@echo "Starting socat + mock backend..."
	@bash -c " \
		set -e; \
		trap 'echo Shutting down...; kill 0' SIGINT SIGTERM; \
		socat -d -d \
			PTY,link=$(TTY_BACKEND),raw,echo=0 \
			PTY,link=$(TTY_MOCK),raw,echo=0 & \
		sleep 0.5; \
		sudo chmod a+rw $(TTY_BACKEND); \
		sudo chmod a+rw $(TTY_MOCK); \
		$(PYTHON) $(MOCK_SCRIPT) & \
		$(PYTHON) $(BACKEND_WC)main.py; \
	"

