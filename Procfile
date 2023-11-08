web: gunicorn -w 4 'backend.app:create_app()'
release: cd backend && flask db upgrade
