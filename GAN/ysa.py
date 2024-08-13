import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from keras.models import Sequential
from keras.layers import Dense
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# Dosyayı okuyun
data = pd.read_csv('veri_seti.csv', header=0 )
print(data.columns)

# Kategorik verileri işleyin
encoder = OneHotEncoder()
data[['proto', 'service', 'conn_state']] = encoder.fit_transform(data[['proto', 'service', 'conn_state']])

# Sayısal verileri işleyin
scaler = StandardScaler()
data[['duration', 'orig_bytes', 'resp_bytes']] = scaler.fit_transform(data[['duration', 'orig_bytes', 'resp_bytes']])

# Etiketleri dönüştürün
le = LabelEncoder()
data['label'] = le.fit_transform(data['label'])
data['detailed-label'] = le.fit_transform(data['detailed-label'])

# Model eğitimi için veri hazırlama
X = data.drop(['label', 'detailed-label'], axis=1)
y = data[['label', 'detailed-label']]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# YSA modelini oluşturun
model = Sequential() #Gizli katman modulü
model.add(Dense(units=16, activation='relu', input_dim=X_train.shape[1])) #Girdi katmanı dinamik alınır
model.add(Dense(units=2, activation='sigmoid'))  # Çıktı katmanında iki birim var çünkü iki etiketimiz var

# Modeli derleyin ve eğitin
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
history = model.fit(X_train, y_train, batch_size=32, epochs=100, validation_data=(X_test, y_test))

# Eğitim ve doğrulama kayıplarını çizin
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model Kaybı')
plt.ylabel('Kayıp')
plt.xlabel('Epok')
plt.legend(['Eğitim', 'Doğrulama'], loc='upper left')
plt.show()

# Tahminleri yapın
y_pred = model.predict(X_test)
y_pred_label = (y_pred[:, 0] > 0.5)
y_pred_detailed_label = y_pred[:, 1].argmax(axis=1)

# Karışıklık matrisini hesaplayın
cm_label = confusion_matrix(y_test['label'], y_pred_label)
cm_detailed_label = confusion_matrix(y_test['detailed-label'], y_pred_detailed_label)

# Karışıklık matrisini çizin
fig, ax = plt.subplots(1, 2, figsize=(12, 6))

sns.heatmap(cm_label, annot=True, ax=ax[0])
ax[0].set_title('Label Karışıklık Matrisi')
ax[0].set_xlabel('Tahmin Edilen Etiket')
ax[0].set_ylabel('Gerçek Etiket')

sns.heatmap(cm_detailed_label, annot=True, ax=ax[1])
ax[1].set_title('Detailed-Label Karışıklık Matrisi')
ax[1].set_xlabel('Tahmin Edilen Etiket')
ax[1].set_ylabel('Gerçek Etiket')

plt.show()


