import cv2
import numpy as np


video_path = "./day3_chicken_heartbeat.mp4"

cap = cv2.VideoCapture(video_path)

def detect_beat(signal, threshold):
    beat = 0
    curr_sig = signal[1]
    max_sig = signal[0]
    saved_sig = signal[0]
    index = 1
    while index < len(signal):
        while curr_sig > max_sig and index < len(signal):
            max_sig = curr_sig
            index += 1
            if (index < len(signal)):
                curr_sig = signal[index]
        
        if (max_sig - saved_sig) > threshold:
            beat += 1
        
        saved_sig = curr_sig
        max_sig = curr_sig
        index += 1
        if (index < len(signal)):
            curr_sig = signal[index]
    return beat

# Variables initial
frame_count = 0
contour_area_variations = []

# Boucle de traitement des images de la vidéo
while cap.isOpened():
    # Lire la prochaine image
    ret, frame = cap.read()
    
    # Verif
    if not ret:
        break

    # Passage au HSV
    hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    cv2.imshow('Contours', hsv_image)


    # Plage de couleur definie pour seuillage
    lower_red = np.array([0, 50, 50])  # Valeurs minimales de teinte, saturation et valeur
    upper_red = np.array([10, 255, 255])  # Valeurs maximales de teinte, saturation et valeur

    # Seuiller l'image pour isoler la couleur du cœur
    mask = cv2.inRange(hsv_image, lower_red, upper_red)

    # Elimination du bruit via des opérations de morphologies
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)

    # Countour sur image avec seuille
    contours, _ = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


    # Recherche du plus grand contour parmi tous les contours détectés
    contour_plus_grand = max(contours, key=cv2.contourArea)

    # Creation d'une liste contenant uniquement le plus grand contour
    contours_filtres = [contour_plus_grand]

    # Dessiner les contours détectés sur l'image originale
    cv2.drawContours(frame, contours_filtres, -1, (0, 255, 0), 2)

    cv2.imshow('Contours', frame)
    cv2.waitKey(100)
    
    # q pour quitter
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    # Application  algo / extraction signal
    contour_area = cv2.contourArea(contour_plus_grand)
    contour_area_variations.append(contour_area)
    frame_count += 1
    # debug tool
    #print(contour_area)    
    #print("Frame:", frame_count)

# Fermer la capture vidéo
cap.release()
cv2.destroyAllWindows()

# Seuil de détection des pics
threshold = 1000  

# Détection des pics dans les variations d'aire
heart_beats = detect_beat(contour_area_variations, threshold)
duration = frame_count / 30 
heart_rate = (heart_beats / duration) * 60
print("Estimation du rythme cardiaque:", heart_rate, "bpm")