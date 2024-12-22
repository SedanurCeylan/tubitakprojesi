# VyroWeb
Bu proje, TUBİTAK 2209-A için geliştirilmiştir.  
*IoT Sızma Testleri İçin Üretici Yapay Zeka Destekli Web Platformu Geliştirilmesi*

## Başlangıç
Projeyi başlatmak için aşağıdaki komutu kullanabilirsiniz:

bash

```
python main.py runserver
```


## Kullanılan Teknolojiler
1. *Python Flask Framework*  
2. *HTML, CSS, JavaScript*
3. *MySQL*

## İçindekiler
- [Proje Hakkında](#proje-hakkında)
- [Kurulum](#kurulum)
  - [Gereksinimler](#gereksinimler)
  - [Kurulum Adımları](#kurulum-adımları)
- [Kullanım](#kullanım)
- [Ekran Görüntüleri](#ekran-görüntüleri)
- [Video](#video)
- [Veri Setleri](#veri-setleri)
- [Yayın Makale](#yayın-makale)

## Proje Hakkında
*IoT Sızma Testleri İçin Üretici Yapay Zeka Destekli Web Platformu Geliştirilmesi*  
Bu proje, IoT cihazlarının güvenliğini test etmek amacıyla yapay zeka teknolojilerini kullanarak, sızma testlerini daha verimli hale getiren bir web platformu geliştirmeyi hedeflemektedir. Platform, IoT sızma testlerinin otomatikleştirilmesine yönelik çözümler sunar ve Generatif Yapay Sinir Ağları (GAN) kullanarak tehdit algılama ve güvenlik analizi süreçlerini iyileştirir.

## Kurulum

### Gereksinimler
Bu projeyi çalıştırabilmek için aşağıdaki yazılımların yüklü olması gerekmektedir:
- Python 3.x  
- Flask Framework (Yazılımın ana framework'ü)
- Diğer gerekli kütüphaneler, requirements.txt dosyasında belirtilmiştir.

### Kurulum Adımları
Projenin kurulumu için aşağıdaki adımları takip edebilirsiniz:

1. Projeyi klonlayın:

    bash
   ```
    git clone https://github.com/SedanurCeylan/tubitakprojesi.git
    cd tubitakprojesi
   ``` 

    

3. Gerekli Python kütüphanelerini yükleyin:

    bash
   ```
    pip install -r requirements.txt
   ```

    

4.  Veritabanı oalrak MySQL Kullanılmıştır. Şablonu repo içinde bulunan veritabanı.sql dosyasında bulunmaktadır.


5. Uygulamayı başlatın:

    bash
   ```
    python main.py
   ```

    

7. Local sunucunuzda uygulamaya erişim:

    [http://127.0.0.1:5000](http://127.0.0.1:5000)



## Kullanım


### Ekran Görüntüleri:

![image](https://github.com/user-attachments/assets/c14c2271-148b-4d39-8ffb-c684a40ec99a)
Bu sayfa, siteye kaydolup giriş yaptıktan sonra sizi karşılayan ekrandır. Bu ekrandan Senaryo sayfasına ve Test sayfasına ulaşabilirsiniz. Ayrıca, profil düzenleme sayfasına ve Hakkımda sayfasına da erişim sağlayabilirsiniz.



![image](https://github.com/user-attachments/assets/137c45c5-8dbf-428d-8378-3ea08802a268)
Ana sayfa ekranından 'Start Test' butonuna tıkladıktan sonra sizi karşılayan sayfa burasıdır. Burada zararlı ve zararsız (malware) çıktıları ve diğer ilgili sonuçları inceleyebilir, açıklamalarını okuyabilirsiniz. Ardından, kendinizi test etmek için oluşturulan testi çözebilirsiniz.



![image](https://github.com/user-attachments/assets/f75bcbfa-a388-46a9-b725-307715d059f4)
Sayfada bulunan 'Continue' butonuna tıkladıktan sonra, burada öğrendiklerinizi test etmeniz için bir alıştırma bulunmaktadır. Burada aldığınız puanlar, profil sayfasında bulunan sıralamanızı (rank) etkileyecektir.



![image](https://github.com/user-attachments/assets/8475ba2e-13f3-4b31-af48-46817189577a)
 Ana sayfada bulunan 'Go to Scenarios' butonuna tıkladıktan sonra senaryo ekranına geçiş yapacaksınız. Burada hazırlanan senaryoları tamamlayabilir ve tamamladıkça puan kazanabilirsiniz. Kazandığınız puanlar, profil sayfasındaki sıralamanızı (rank) etkileyecektir.
 

![image](https://github.com/user-attachments/assets/c0d0341f-27f0-43f6-a343-480e11add02e)
Bu sayfa, ana sayfa üzerinden ulaşabileceğiniz 'profile' sayfasıdır. Bu sayfada, çözdüğünüz senaryolardan ve testlerden elde ettiğiniz puanlarla siteye kaydolan diğer kullanıcılarla rekabet edebilirsiniz. Ayrıca, senaryolardan elde ettiğiniz kazanımları İstatistikler bölümünde görüntüleyebilir ve kullanıcı adınızı ile profil resminizi düzenleyebilirsiniz


![image](https://github.com/user-attachments/assets/b0c868d2-bcf3-4937-a3cb-c0babab066fc)
Bu sayfa, ana sayfa üzerinden ulaşabileceğiniz 'About Us' sayfasıdır. Bu sayfada, proje hakkında bilgi edinebilir ve proje ekibimiz hakkında detaylara ulaşabilirsiniz. Ayrıca, bizimle iletişime geçebilirsiniz.


---

## Video

Projenin detaylı tanıtım videosunu [linkten](https://youtu.be/t84r9F5Eb9k) izleyebilirsiniz.

---

## Veri Setleri

Bu projede kullanılan verisetlerine [buradan](https://www.stratosphereips.org/datasets-iot23) ulaşabilirsiniz.

---

## Yayın Makale

"IoT Siber Tehdit Senaryoları Kullanılarak Generatif Yapay Zeka Destekli Web Platformu ile Siber Güvenlik Eğitimi" başlıklı makalemiz [IEEE Xplore](https://ieeexplore.ieee.org/document/10778718)’da yayımlandı!



