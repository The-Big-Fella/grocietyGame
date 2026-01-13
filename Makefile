SHELL := /bin/bash
BACKEND_WC = ./BackEnd/
VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

MOCK_WC = ./Mock/
MOCK_SCRIPT = $(MOCK_WC)main.py

ARDUINO_WC = ./Arduino/Main

TTY_BACKEND = /tmp/ttyV0
TTY_MOCK = /tmp/ttyV1

CONTROLLER = /dev/ttyACM0

create_venv:
	python3 -m venv $(VENV)

install_deps: create_venv
	$(PIP) install -r requirements.txt

update_deps:
	$(PIP) freeze > requirements.txt

start_backend:
	CONTROLLER_PATH="$(CONTROLLER)" $(PYTHON) $(BACKEND_WC)main.py

test_backend:
	$(PYTHON) -m pytest $(BACKEND_WC)

shell: create_venv
	@bash --rcfile <(echo "source $(VENV)/bin/activate; PS1='(venv) $$PS1'") -i

start_mock_backend: create_venv
	@echo "Starting socat + mock backend..."
	@CONTROLLER_PATH="$(TTY_BACKEND)" bash -c '\
		set -e; \
		socat -d -d \
			PTY,link=$(TTY_BACKEND),raw,echo=0,mode=666 \
			PTY,link=$(TTY_MOCK),raw,echo=0,mode=666 & \
		SOCAT_PID=$$!; \
		while [ ! -e $(TTY_BACKEND) ] || [ ! -e $(TTY_MOCK) ]; do sleep 0.1; done; \
		$(PYTHON) $(MOCK_SCRIPT) & \
		MOCK_PID=$$!; \
		$(PYTHON) $(BACKEND_WC)main.py; \
		kill $$MOCK_PID $$SOCAT_PID; \
	'

setup_arduino:
	@echo "Updating Arduino core index..."
	arduino-cli core update-index

	@echo "Ensuring Arduino AVR core is installed..."
	arduino-cli core list | grep -q "arduino:avr" || \
		arduino-cli core install arduino:avr

upload_arduino:
	@echo "Compiling main.ino..."
	arduino-cli compile --fqbn arduino:avr:mega $(ARDUINO_WC)

	@echo "Giving device proper permissions"

	@echo "uploading sketch"
	arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:mega $(ARDUINO_WC)

