.PHONY: install lint test type-check up down migrate upgrade-db send-test-audio simulate-call cleanup

install:
	pip install -r requirements.txt
	pip install -e ".[dev]"

lint:
	ruff check .

type-check:
	mypy app

test:
	pytest tests/ -v

up:
	docker-compose up -d

down:
	docker-compose down

migrate:
	alembic upgrade head

upgrade-db:
	docker-compose exec api alembic upgrade head

send-test-audio:
	python scripts/send_test_audio.py

simulate-call:
	python scripts/simulate_call.py

cleanup:
	python scripts/cleanup_old_calls.py

dev:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
