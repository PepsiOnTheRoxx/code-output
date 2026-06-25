import os
import sqlite3
from flask import Flask
from src.app_exceptions import AppSetupException
from boekapi.routes import boekapi_blueprint
from jinja2 import FileSystemLoader

class App:
    def __init__(self, db_path='database.db', templates_dir='templates'):
        self.db_path = db_path
        self.templates_dir = templates_dir
        self.app = None

    def initialize_app(self):
        try:
            self.app = Flask(__name__, template_folder=self.templates_dir)
            self._register_blueprints()
            self._ensure_templates()
            self._create_requirements_txt()
            self._initialize_db()
            self._seed_db()
        except Exception as e:
            raise AppSetupException(f"App setup failed: {e}")

    def _register_blueprints(self):
        self.app.register_blueprint(boekapi_blueprint)

    def _ensure_templates(self):
        if not os.path.isdir(self.templates_dir):
            os.makedirs(self.templates_dir, exist_ok=True)
        if not os.path.exists(os.path.join(self.templates_dir, 'index.html')):
            with open(os.path.join(self.templates_dir, 'index.html'), 'w') as f:
                f.write('<html><body><h1>Welkom bij de BoekAPI</h1></body></html>')

    def _create_requirements_txt(self):
        requirements = ['Flask', 'jinja2']
        req_path = 'requirements.txt'
        with open(req_path, 'w') as f:
            for req in requirements:
                f.write(f"{req}\n")

    def _initialize_db(self):
        if not os.path.exists(self.db_path):
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS boeken (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titel TEXT NOT NULL,
                    auteur TEXT NOT NULL,
                    jaar INTEGER
                )''')
            conn.commit()
            conn.close()

    def _seed_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM boeken")
        count = cursor.fetchone()[0]
        if count == 0:
            boeken = [
                ('De ontdekking van de hemel', 'Harry Mulisch', 1992),
                ('Het diner', 'Herman Koch', 2009),
                ('Publieke werken', 'Thomas Rosenboom', 1999)
            ]
            cursor.executemany('INSERT INTO boeken (titel, auteur, jaar) VALUES (?, ?, ?)', boeken)
            conn.commit()
        conn.close()

    def run(self, *args, **kwargs):
        if self.app:
            self.app.run(*args, **kwargs)
        else:
            raise AppSetupException("App is not initialized. Call initialize_app() first.")