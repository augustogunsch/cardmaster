```
cp ./hooks/* ./.git/hooks
cp config.py.template config.py
(edit config.py)
python -m venv venv
. ./venv/bin/activate
pip install -r ./requirements.txt
flask --app run.py db upgrade
flask --app run.py run
```
