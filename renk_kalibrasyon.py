import cv2
import numpy as np

def bos_fonksiyon(x):
    pass

cap = cv2.VideoCapture(0)


cv2.namedWindow("Ayar Paneli", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Ayar Paneli", 520, 260)


cv2.createTrackbar("H_ALT", "Ayar Paneli", 0, 179, bos_fonksiyon)
cv2.createTrackbar("H_UST", "Ayar Paneli", 10, 179, bos_fonksiyon)
cv2.createTrackbar("S_ALT", "Ayar Paneli", 120, 255, bos_fonksiyon)
cv2.createTrackbar("S_UST", "Ayar Paneli", 255, 255, bos_fonksiyon)
cv2.createTrackbar("V_ALT", "Ayar Paneli", 70, 255, bos_fonksiyon)
cv2.createTrackbar("V_UST", "Ayar Paneli", 255, 255, bos_fonksiyon)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    
    h_alt = cv2.getTrackbarPos("H_ALT", "Ayar Paneli")
    h_ust = cv2.getTrackbarPos("H_UST", "Ayar Paneli")
    s_alt = cv2.getTrackbarPos("S_ALT", "Ayar Paneli")
    s_ust = cv2.getTrackbarPos("S_UST", "Ayar Paneli")
    v_alt = cv2.getTrackbarPos("V_ALT", "Ayar Paneli")
    v_ust = cv2.getTrackbarPos("V_UST", "Ayar Paneli")

    alt_sinir = np.array([h_alt, s_alt, v_alt])
    ust_sinir = np.array([h_ust, s_ust, v_ust])

   
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    maske = cv2.inRange(hsv, alt_sinir, ust_sinir)
    filtrelenmis = cv2.bitwise_and(frame, frame, mask=maske)

   
    panel_ekrani = np.zeros((140, 500, 3), dtype=np.uint8)

    metin_alt = f"ALT:  H={h_alt:<3}  S={s_alt:<3}  V={v_alt:<3}"
    metin_ust = f"UST:  H={h_ust:<3}  S={s_ust:<3}  V={v_ust:<3}"
   

    cv2.putText(panel_ekrani, metin_alt, (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 255), 2)
    cv2.putText(panel_ekrani, metin_ust, (15, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 255), 2)
   
    
    cv2.imshow("Ayar Paneli", panel_ekrani)
    cv2.imshow("Kamera (Orijinal)", frame)
    cv2.imshow("Maske (Siyah/Beyaz)", maske)
    cv2.imshow("Filtrelenmis Goruntu", filtrelenmis)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('p'):
        print("\n--- KOPYALANABILIR KOD ---")
        print(kod_alt)
        print(kod_ust)

cap.release()
cv2.destroyAllWindows()
