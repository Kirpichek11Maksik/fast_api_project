.PHONY: run alembic upgrade

run:
	uvicorn main:app --reload

migrate-create:
	alembic revision --autogenerate -m $(MIGRATION)

upgrade:
	alembic upgrade head