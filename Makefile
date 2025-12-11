BACKEND_WC = ./BackEnd/
FRONTEND_WC = ./FrontEnd/
ARDUINO_WC = ./Arduino/

create_venv:
	python -m venv $(BACKEND_WC)venv

activate_venv:
	source $(BACKEND_WC)venv/bin/activate

install_deps:
	pip install -r $(BACKEND_WC)requirments.txt

update_deps:
	pip freeze > $(BACKEND_WC)requirments.txt

start_backend:
	python ${BACKEND_WC}main.py

test_backend:
	pytest $(BACKEND_WC)
	
