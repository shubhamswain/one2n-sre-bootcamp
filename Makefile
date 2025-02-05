FLASK = ./.venv/bin/flask

setup: requirements.txt
	python3 -m venv .venv
	./.venv/bin/pip install -r requirements.txt

activate: setup
	./.venv/bin/activate

run: setup activate
	${FLASK} run