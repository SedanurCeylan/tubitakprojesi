from flask import Flask
from flask_migrate import Migrate, upgrade, current
from website import create_app, db  # Flask uygulamanızı oluşturan fonksiyon ve db nesnesini içe aktarın

app = create_app()
migrate = Migrate(app, db)

@app.cli.command("db_upgrade")
def db_upgrade():
    """Alembic upgrade head komutunu çalıştırır."""
    with app.app_context():
        upgrade()

@app.cli.command("db_current")
def db_current():
    """Alembic current komutunu çalıştırır."""
    with app.app_context():
        current()

if __name__ == "__main__":
    app.run()
