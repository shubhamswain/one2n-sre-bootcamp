FLASK = ./.venv/bin/flask

setup: requirements.txt
	python3 -m venv .venv
	./.venv/bin/pip install -r requirements.txt

activate: setup
	. ./.venv/bin/activate

db_create: setup activate
	${FLASK} db upgrade

run: db_create
	${FLASK} run

clean:
	rm -r .venv/
	rm -r instance/