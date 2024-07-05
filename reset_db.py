from website import create_app, db

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()
    print("Veritabanı temizlendi ve yeniden oluşturuldu.")
