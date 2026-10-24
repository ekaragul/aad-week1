# Bilgisayarlı Görü & Hedef Takip Atölyesi

Bu kılavuz, insansız hava araçlarında (İHA) kullanılan temel görüntü işleme ve hedef tespit algoritmalarını adım adım inşa etmeniz için hazırlanmıştır. Kılavuzda hazır kod blokları verilmemiştir; amaç, verilen gereksinimleri analiz edip ilgili fonksiyonları dokümantasyonlardan araştırarak kendi çözümünüzü üretmenizdir. Bu yüzden süreç boyunca bilinçsiz LLM kullanımından kaçınmanız şiddetle tavsiye edilir.

## Kurulum

* İndirdiğiniz klasörün dosya yolunda terminali açın ve aşağıdaki kodları çalıştırın. 
 
 
```
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt

```


###  Görev 0: OpenCV Kamera Kullanımı

###  Görev Tanımı
* Bilgisayarın dahili kamerasını veya harici bir USB kamerayı canlı olarak açın.
* Sonsuz bir döngü kurarak kameradan her an bir kare (frame) okuyun; okuma başarısız olursa döngüyü güvenli bir şekilde sonlandırın.
* Görüntü penceresini ekranda gösterin ve klavyeden belirlenen bir tuşa (`q` veya `0`) basıldığında döngüden çıkıp donanım kaynaklarını serbest bırakın.

###  Önerilen Fonksiyonlar 
* `cv2.VideoCapture()`
* `cap.read()`
* `cv2.imshow()`
* `cv2.waitKey()`
* `cap.release()`
* `cv2.destroyAllWindows()`

--------------------------------------------------

### GÖREV 1: İHA Kokpit Ekranı (HUD & Nişangah)

###  Amaç
Kameradan gelen görüntünün merkezine bir nişangah (crosshair) yerleştirmek ve ekranın belirli köşelerine simüle edilmiş telemetri verilerini (irtifa, mod, batarya) dinamik olarak yazdırmak.

###  Görev Tanımı
1. **Ekran Merkezi:** Alınan karenin çözünürlüğünü (yükseklik, genişlik) dinamik olarak öğrenin ve merkez koordinatlarını (x,y) hesaplayın.
2. **Nişangah Tasarımı:** 
   * Merkeze yatay ve dikey iki kesişen çizgi çizerek artı işareti (`+`) oluşturun.
   * Çizgilerin kesiştiği orta noktaya küçük bir hedef çemberi ekleyin.
3. **Telemetri Göstergesi:** 
   * Ekranın sol üst köşesine uçuş modunu (ör. `MOD: OTONOM UÇUŞ`).
   * Ekranın sol alt köşesine dinamik koordinatları kullanarak irtifa ve batarya seviyesini yazdırın.
   * Yazıların ve çizgilerin İHA standartlarına uygun (ör. neon yeşil) tonda olmasını sağlayın.

###  Önerilen Fonksiyonlar & İpuçları
* `frame.shape` *(Dizi boyutlarını ve çözünürlüğü okumak için)*
* `cv2.line()` *(Hedef çizgileri için)*
* `cv2.circle()` *(Merkez çemberi için)*
* `cv2.putText()` *(Yazı ve telemetri verileri için)*
* *Renk Düzeni Notu:* OpenCV'nin varsayılan olarak **BGR** (Mavi, Yeşil, Kırmızı) renk uzayını kullandığını unutmayın. Koordinat parametrelerinin tam sayı (`int`) olması gerektiğini göz önünde bulundurun.

---

## GÖREV 2: Renk Tabanlı Hedef Tespiti & Yönlendirme Algoritması

### Amaç
Görüntüdeki belirli bir rengi **(Kırmızı renk tavsiye edilir.)** arka plandan ayırmak, nesnenin koordinatlarını bulup etrafını sınırlayıcı kutu içine almak ve hedefin merkeze göre konumuna göre İHA yönlendirme komutları üretmek.

### Görev Tanımı
1. **Renk Uzayı Dönüşümü:** Işık değişimlerinden etkilenmemek için kareyi BGR (default) uzayından HSV uzayına dönüştürün.
2. **Maskeleme:** Hedef rengin  alt ve üst HSV eşik değerlerini belirleyerek sadece hedef nesneyi beyaz, diğer tüm alanları siyah yapan bir ikili (binary) maske oluşturun. 
   * Eşik değerleri belirlemek için size verilen 'renk_kalibrasyon.py' uygulamasını kullanabilirsiniz. 
   * Uygulama kodlarını kopyalamanız önerilmez.
			dipnot: Kırmızı renk en dip ve en üst hue aralıklarında bulunduğu için iki ayrı maskenin birleştirilmesi gerekmektedir. 
3. **Sınır ve Kontur Tespiti:** Maskedeki beyaz piksellerin sınırlarını (konturlarını) tespit edin.
4. **Filtreleme & Takip:**
   * Sahnedeki küçük parazit pikselleri görmezden gelmek için belirli bir alan eşiğinin altındaki konturları eleyin.
   * En büyük konturu hedef nesne seçip etrafına dikdörtgen bir sınır kutusu çizin.
5. **İHA Karar Mekanizması:**
   * Tespit edilen nesnenin merkez koordinatını, ekranın merkez koordinatıyla karşılaştırın.
   * Hedef merkezden soldaysa ekrana `"KOMUT: SOLA DÖN"`, sağdaysa `"KOMUT: SAĞA DÖN"`, yaklaşık olarak merkezdeyse `"KİLİTLENDİ!"` uyarısı basın.

###  Önerilen Fonksiyonlar & İpuçları
* `cv2.cvtColor()` *(Renk uzayı değişimi için)*
* `numpy.array()` *(Alt ve üst sınır değerlerini matris olarak tanımlamak için)*
* `cv2.inRange()` *(Renk filtreleme / maskeleme için)*
* `cv2.findContours()` *(Beyaz piksel sınırlarını çıkarmak için)*
* `cv2.contourArea()` *(Alan büyüklüğünü hesaplayıp parazitleri ayıklamak için)*
* `cv2.boundingRect()` *(Konturu saran en küçük kutu koordinatlarını almak için)*
* `cv2.rectangle()` *(Kutuyu çizmek için)*
* `cv2.bitwise_or()` *(Maske birleştirme için, opsiyonel)*


---

## GÖREV 3: Derin Öğrenme Tabanlı Canlı Nesne Tespiti (YOLO)

### Amaç
Geleneksel renk filtrelemenin yetersiz kaldığı karmaşık ortamlarda, önceden eğitilmiş bir derin öğrenme modeli (YOLO) kullanarak karedeki spesifik nesneleri (ör. insan veya araç) tespit etmek ve sınıflandırmak.

### Görev Tanımı
1. **Model Yükleme:** Hafif ve gerçek zamanlı çalışabilen önceden eğitilmiş bir nesne tespit modelini (ör. `yolov8n.pt`) kodun başlangıcında, **döngü dışarısında** belleğe yükleyin.
2. **Çıkarım (Inference):** Her döngüde kameradan gelen kareyi modele girdi olarak verin. 
3. **Filtreleme:**
   * Modelin tespit ettiği kutuları, sınıf kimliklerini (class ID) ve sınıf etiketlerini okuyun.
   * Yalnızca ilgilendiğiniz sınıfı (örneğin `"person"`) seçin; diğer sınıfları filtreleyip ekrana çizmeyin.
4. **Görselleştirme:** Hedef sınıf tespit edildiğinde nesnenin etrafına sınırlayıcı kutu çizin ve üst kısmına sınıf adını veya alarm mesajını yazdırın.

### 🔍 Önerilen Fonksiyonlar & Kütüphaneler
* `from ultralytics import YOLO`
* `YOLO("model_adi.pt")`
* `model(frame)` *(Kare üzerinde çıkarım çalıştırma)*  // **model(frame, stream=True, verbose=False)** *(Verimli kullanım için önerilen ayarlar)*
* `.boxes` *(Kutu oluşturma)*
* `boxes.xyxy` veya `boxes.xywh` *(Kutu koordinat formatları)*
* `boxes.cls` *(Sınıf indeksini okuma)*
* `model.names` *(Sınıf ID'sini insan tarafından okunabilir ada dönüştürme)*
* `cv2.rectangle()` & `cv2.putText()`

---


