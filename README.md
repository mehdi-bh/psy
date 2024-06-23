# psy-core
### How to install
- create venv in python 3.11
- `pip install -r requirements.txt`

### How to run locally
- `serverless offline`

OR you can also do this:
- `uvicorn app.main:app --reload`
- Swagger : http://127.0.0.1:8000/docs

### How to deploy
- `serverless deploy`

### How to run tests
- `pytest`
