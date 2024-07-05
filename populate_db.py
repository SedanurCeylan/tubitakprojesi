import pandas as pd
from website import create_app, db
from website.models import BeignDataset, GeneratedDataDataset, MaliciousDataset

app = create_app()

# Veritabanını temizleme (isteğe bağlı)
with app.app_context():
    db.drop_all()
    db.create_all()

# Veritabanına veri ekleme fonksiyonu
def add_data(file_path, model):
    data = pd.read_excel(file_path)
    # Sütun adlarını yeniden adlandırma
    data.columns = data.columns.str.strip().str.replace('.', '_').str.replace(' ', '_').str.lower()
    with app.app_context():
        for index, row in data.iterrows():
            print(f"Adding row: {row.to_dict()}")  # Her satırı yazdırarak kontrol edin
            record = model(
                id_orig_h=row['id_orig_h'],
                id_resp_h=row['id_resp_h'],
                id_resp_p=row['id_resp_p'],
                proto=row['proto'],
                duration=row['duration'],
                orig_bytes=row['orig_bytes'],
                resp_bytes=row['resp_bytes'],
                history=row['history'],
                orig_pkts=row['orig_pkts'],
                orig_ip_bytes=row['orig_ip_bytes'],
                resp_pkts=row['resp_pkts'],
                malware_status=row['malware_status']
            )
            db.session.add(record)
        db.session.commit()

# Dosya yolları ve modeller
file_paths_and_models = [
    ('website/static/dataset/beign.xlsx', BeignDataset),
    ('website/static/dataset/generated_data.xlsx', GeneratedDataDataset),
    ('website/static/dataset/malicious.xlsx', MaliciousDataset)
]

# Her bir dosyayı ve modeli işleyin
for file_path, model in file_paths_and_models:
    add_data(file_path, model)

print("Veriler başarıyla eklendi!")
