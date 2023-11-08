```
cp .env.template .env
(edit .env)
python -m venv venv
. ./venv/bin/activate
pip install -r ./requirements.txt
flask --app run.py db upgrade
flask --app run.py run
```
