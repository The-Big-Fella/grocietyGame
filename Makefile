BACKEND_WC = ./BackEnd/
VENV = $(BACKEND_WC)venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

create_venv:
	python3 -m venv $(VENV)

install_deps: create_venv
	$(PIP) install -r $(BACKEND_WC)requirements.txt

update_deps:
	$(PIP) freeze > $(BACKEND_WC)requirements.txt

start_backend:
	$(PYTHON) $(BACKEND_WC)main.py

test_backend:
	$(PYTHON) -m pytest $(BACKEND_WC)

shell: create_venv
	@bash --rcfile <(echo "source $(VENV)/bin/activate; PS1='(venv) $$PS1'") -i
	
