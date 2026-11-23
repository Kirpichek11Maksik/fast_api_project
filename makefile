.PHONY: run migrate-create upgrade

run:
	python -m uvicorn main:app --reload

migrate-create:
	python -m alembic revision --autogenerate -m "$(MIGRATION)"

upgrade:
	python -m alembic upgrade head