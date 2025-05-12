import cv2
import numpy as np


# video_path = "./day3_chicken_heartbeat.mp4"

# cap = cv2.VideoCapture(video_path)

img_test = "./embryo_snapshot.png"
debug = True


def image_to_HSV(image):

    img = cv2.imread(image)
    cv2.imshow('Contours', img)

    cv2.waitKey(0)
    hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    cv2.imshow('Contours', hsv_image)

    cv2.waitKey(0)


    # closing all open windows
    cv2.destroyAllWindows()

    return hsv_image

def show_sat_hue_image(hsv_image):
    hue, saturation, value = cv2.split(hsv_image)
    cv2.imshow('Hue Channel', hue)
    cv2.imshow('saturation Channel', saturation)


    cv2.imshow('Value Channel', value)

    cv2.waitKey(0)
    cv2.destroyAllWindows()




def morphologies(hsv_image):
     # Plage de couleur definie pour seuillage
    lower_red = np.array([0, 50, 50])  # Valeurs minimales de teinte, saturation et valeur
    upper_red = np.array([10, 255, 255])  # Valeurs maximales de teinte, saturation et valeur

    # Seuiller l'image pour isoler la couleur du cœur
    mask = cv2.inRange(hsv_image, lower_red, upper_red)

    # Elimination du bruit via des opérations de morphologies
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)

    if debug:

            cv2.imshow('Masque Seuillé', mask)
            cv2.imshow('Après Morphologie (Opening)', opening)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    # cv2.imwrite('Mask.jpg', opening)
    # cv2.imwrite('opening_morph.jpg', opening)
    return opening

def cdraw(img, morph):
     # Countour sur image avec seuille
    contours, _ = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


    # Recherche du plus grand contour parmi tous les contours détectés
    contour_plus_grand = max(contours, key=cv2.contourArea)

    # Creation d'une liste contenant uniquement le plus grand contour
    contours_filtres = [contour_plus_grand]

    # Dessiner les contours détectés sur l'image originale
    cv2.drawContours(img, contours_filtres, -1, (0, 255, 0), 2)



hsv_image = image_to_HSV(img_test)
#show_sat_hue_image(hsv_image)
morph = morphologies(hsv_image)

contour = cdraw(hsv_image, morph)

   
# def detect_beat(signal, threshold):
#     beat = 0
#     curr_sig = signal[1]
#     max_sig = signal[0]
#     saved_sig = signal[0]
#     index = 1
#     while index < len(signal):
#         while curr_sig > max_sig and index < len(signal):
#             max_sig = curr_sig
#             index += 1
#             if (index < len(signal)):
#                 curr_sig = signal[index]
        
#         if (max_sig - saved_sig) > threshold:
#             beat += 1
        
#         saved_sig = curr_sig
#         max_sig = curr_sig
#         index += 1
#         if (index < len(signal)):
#             curr_sig = signal[index]
#     return beat

# # Variables initial
# frame_count = 0
# contour_area_variations = []

# # Boucle de traitement des images de la vidéo
# while cap.isOpened():
#     # Lire la prochaine image
#     ret, frame = cap.read()
    
#     # Verif
#     if not ret:
#         break

#     # Passage au HSV
#     hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
#     cv2.imshow('Contours', hsv_image)


#     # Plage de couleur definie pour seuillage
#     lower_red = np.array([0, 50, 50])  # Valeurs minimales de teinte, saturation et valeur
#     upper_red = np.array([10, 255, 255])  # Valeurs maximales de teinte, saturation et valeur

#     # Seuiller l'image pour isoler la couleur du cœur
#     mask = cv2.inRange(hsv_image, lower_red, upper_red)

#     # Elimination du bruit via des opérations de morphologies
#     kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
#     opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)

#     # Countour sur image avec seuille
#     contours, _ = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


#     # Recherche du plus grand contour parmi tous les contours détectés
#     contour_plus_grand = max(contours, key=cv2.contourArea)

#     # Creation d'une liste contenant uniquement le plus grand contour
#     contours_filtres = [contour_plus_grand]

#     # Dessiner les contours détectés sur l'image originale
#     cv2.drawContours(frame, contours_filtres, -1, (0, 255, 0), 2)

#     cv2.imshow('Contours', frame)
#     cv2.waitKey(100)
    
#     # q pour quitter
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
    
#     # Application  algo / extraction signal
#     contour_area = cv2.contourArea(contour_plus_grand)
#     contour_area_variations.append(contour_area)
#     frame_count += 1
#     # debug tool
#     #print(contour_area)    
#     #print("Frame:", frame_count)

# # Fermer la capture vidéo
# cap.release()
# cv2.destroyAllWindows()

# # Seuil de détection des pics
# threshold = 1000  

# # Détection des pics dans les variations d'aire
# heart_beats = detect_beat(contour_area_variations, threshold)
# duration = frame_count / 30 
# heart_rate = (heart_beats / duration) * 60
# print("Estimation du rythme cardiaque:", heart_rate, "bpm")