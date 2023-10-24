```
cp ./hooks/* ./.git/hooks
python -m venv venv
pip install -r ./requirements.txt
pre-commit install
. ./venv/bin/activate
flask db init
flask run
```
