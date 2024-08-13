import os
import logging
import numpy as np
import tensorflow as tf
from sklearn.impute import KNNImputer
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import pydot
import graphviz

tf.get_logger().setLevel(logging.ERROR)

# Veri seti okuma
data = pd.read_csv('C:/Users/busra.yaman/Desktop/tubitak/tubitakprojesi/GAN/IOT.csv')

# Display basic information and the first few rows of the dataset
print(data.info())
print(data.head())

# Replace '-' with NaN
data.replace('-', np.nan, inplace=True)

# Check for missing values
missing_values_new = data.isnull().sum()
print(missing_values_new)

data['proto'].fillna(data['proto'].mode()[0], inplace=True)
numeric_columns = ['duration', 'orig_bytes']
data[numeric_columns] = data[numeric_columns].apply(pd.to_numeric, errors='coerce')
for col in numeric_columns:
    data[col].fillna(data[col].median(), inplace=True)

# Categorical columns encoding
from sklearn.preprocessing import LabelEncoder
label_encoders = {}
categorical_columns = ['id.resp_p', 'proto', 'resp_bytes', 'malware status']

for col in categorical_columns:
    le = LabelEncoder()
    data[col] = le.fit_transform(data[col].astype(str))
    label_encoders[col] = le

# 'orig_bytes' için kutu grafiği
sns.boxplot(x=data['orig_bytes'])
plt.title('Original Bytes Box Plot')
plt.show()

plt.scatter(data['duration'], data['orig_bytes'])
plt.title('Duration vs Original Bytes')
plt.xlabel('Duration')
plt.ylabel('Original Bytes')
plt.show()

correlation_matrix = data.corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Matrix')
plt.show()

# Sayısal sütunların listesi
numeric_columns = ['duration', 'orig_bytes', 'history', 'orig_pkts', 'orig_ip_bytes', 'resp_pkts']

# StandardScaler nesnesi oluştur
scaler = StandardScaler()

# Sayısal sütunları normalleştir ve DataFrame içindeki ilgili sütunları güncelle
data[numeric_columns] = scaler.fit_transform(data[numeric_columns])

# Normalleştirilmiş verilerin ilk birkaç satırını göster
print(data[numeric_columns].head())

# 'malware status' sütununu ayrı olarak saklama
malware_status = data['malware status']

# Verileri giriş ve çıkış olarak ayırma (malware status sütunu hariç)
X = data.drop(columns=["malware status"]).values

class Gan():

    def __init__(self, data, latent_dim=100):
        self.data = data
        self.latent_dim = latent_dim
        self.generator = self._generator()
        self.discriminator = self._discriminator()
        self.gan = self._GAN(self.generator, self.discriminator)

        # Model özetlerini yazdırma
        print("Generator Model Summary:")
        self.generator.summary()
        print("\nDiscriminator Model Summary:")
        self.discriminator.summary()
        print("\nGAN Model Summary:")
        self.gan.summary()

        # Model görselleştirme
        plot_model(self.generator, to_file='generator_model.png', show_shapes=True, show_layer_names=True)
        plot_model(self.discriminator, to_file='discriminator_model.png', show_shapes=True, show_layer_names=True)
        plot_model(self.gan, to_file='gan_model.png', show_shapes=True, show_layer_names=True)
    
        
    # Random noise uret...
    def _noise(self, batch_size):
        noise = np.random.normal(0, 1, (batch_size, self.latent_dim))
        return noise

    def _generator(self):
        model = tf.keras.Sequential(name="Generator_model")
        model.add(tf.keras.Input(shape=(self.latent_dim,)))
        model.add(tf.keras.layers.Dense(128, activation='relu', kernel_initializer='he_uniform'))
        model.add(tf.keras.layers.BatchNormalization())
        model.add(tf.keras.layers.Dense(256, activation='relu'))
        model.add(tf.keras.layers.BatchNormalization())
        model.add(tf.keras.layers.Dense(512, activation='relu'))
        model.add(tf.keras.layers.BatchNormalization())
        model.add(tf.keras.layers.Dense(self.data.shape[1], activation='linear'))
        
        
        return model

    def _discriminator(self):
        model = tf.keras.Sequential(name="Discriminator_model")
        model.add(tf.keras.Input(shape=(self.data.shape[1],)))
        model.add(tf.keras.layers.Dense(1024, kernel_initializer='he_uniform'))
        model.add(tf.keras.layers.LeakyReLU(negative_slope=0.2))
        model.add(tf.keras.layers.Dropout(0.3))
        model.add(tf.keras.layers.LayerNormalization())
        model.add(tf.keras.layers.Dense(512))
        model.add(tf.keras.layers.LeakyReLU(negative_slope=0.2))
        model.add(tf.keras.layers.Dropout(0.3))
        model.add(tf.keras.layers.LayerNormalization())
        model.add(tf.keras.layers.Dense(256))
        model.add(tf.keras.layers.LeakyReLU(negative_slope=0.2))
        model.add(tf.keras.layers.Dropout(0.3))
        model.add(tf.keras.layers.LayerNormalization())
        model.add(tf.keras.layers.Dense(1, activation='sigmoid'))

        model.compile(loss='binary_crossentropy', optimizer=tf.keras.optimizers.Adam(learning_rate=0.00001, beta_1=0.5), metrics=['accuracy'])
        
        return model

    def _GAN(self, generator, discriminator):
        discriminator.trainable = False
        generator.trainable = True
        model = tf.keras.Sequential(name="GAN")
        model.add(generator)
        model.add(discriminator)
        model.compile(loss='binary_crossentropy', optimizer=tf.keras.optimizers.Adam(learning_rate=0.00001, beta_1=0.5))
        model.summary()
       
        return model

    def train(self, epochs=300, batch_size=128):
        batch_count = int(self.data.shape[0] / batch_size)
        for epoch in range(epochs):
            d_losses = []
            g_losses = []
            for _ in range(batch_count):
                noise = self._noise(batch_size)
                generated_data = self.generator.predict(noise)
                real_data = self.data[np.random.randint(0, self.data.shape[0], batch_size)]

                X_discriminator = np.concatenate([real_data, generated_data])
                y_discriminator = np.zeros(2 * batch_size)
                y_discriminator[:batch_size] = 0.9  # Label smoothing for real data

                self.discriminator.trainable = True
                d_loss = self.discriminator.train_on_batch(X_discriminator, y_discriminator)
                d_losses.append(d_loss[0])

                noise = self._noise(batch_size)
                y_generator = np.ones(batch_size)

                self.discriminator.trainable = False
                g_loss = self.gan.train_on_batch(noise, y_generator)
                g_losses.append(g_loss)

            # Print average losses per epoch
            print(f"Epoch {epoch+1}/{epochs} [Discriminator Loss: {np.mean(d_losses):.4f}] [Generator Loss: {np.mean(g_losses):.4f}]")

# GAN modelini oluştur ve eğit
gan = Gan(data=X)
gan.train(epochs=300, batch_size=128)  # Increased epochs and reduced batch size

# Yeni veri üretme
noise = gan._noise(250)  # 500 yeni örnek üret
generated_data = gan.generator.predict(noise)

# Normalleştirilmiş verileri geri alma
generated_data_df = pd.DataFrame(generated_data, columns=data.drop(columns=["malware status"]).columns)
generated_data_df[numeric_columns] = scaler.inverse_transform(generated_data_df[numeric_columns])


# Negatif değerleri sıfırdan büyük değerlere dönüştürme
generated_data_df[generated_data_df < 0] = 0

# Orijinal 'malware status' sütununu yeni verilere ekleme
generated_data_df['malware status'] = np.random.choice(malware_status, size=len(generated_data_df))

# Kategorik sütunları orijinal değerlere geri dönüştürme
for col in categorical_columns:
    if col in generated_data_df.columns:
        le = label_encoders[col]
        # Ensure the labels are within the original range
        max_label = len(le.classes_) - 1
        generated_data_df[col] = np.clip(generated_data_df[col].astype(int), 0, max_label)
        generated_data_df[col] = le.inverse_transform(generated_data_df[col])

# Ensuring the original distribution of the 'proto' column
proto_counts = data['proto'].value_counts(normalize=True)
generated_proto = np.random.choice(proto_counts.index, size=len(generated_data_df), p=proto_counts.values)
generated_data_df['proto'] = generated_proto

# Convert the 'proto' column back to its original categorical values
generated_data_df['proto'] = label_encoders['proto'].inverse_transform(generated_data_df['proto'].astype(int))

# Yeni veriyi CSV dosyasına kaydetme
generated_data_df.to_excel("C:/Users/busra.yaman/Desktop/tubitak/tubitakprojesi/GAN/generated_data.xlsx", index=False)
print("Yeni veri Excel dosyasına kaydedildi: generated_data.xlsx")

#Gorseller
#Confusion Matrix
fig, ax = plt.subplots(1, 2, figsize=(20, 6))
sns.heatmap(data.corr(), annot=True, ax=ax[0], cmap="Reds")
sns.heatmap(generated_data_df.select_dtypes(include=[np.number]).corr(), annot=True, ax=ax[1], cmap="Reds")
ax[0].set_title("Orijinal Veri")
ax[1].set_title("Yeni (Sentetik) Veri")

#Veri Dagilimi
fig, ax = plt.subplots(1, 2, figsize=(20, 6))
ax[0].scatter(data.iloc[:, 0], data.iloc[:, 1])
ax[1].scatter(generated_data_df.iloc[:, 0], generated_data_df.iloc[:, 1])
ax[0].set_title("Orijinal Veri")
ax[1].set_title("Yeni (Sentetik) Veri")

plt.show()