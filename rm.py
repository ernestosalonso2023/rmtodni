from enum import Enum
from PIL import Image, ImageDraw
from rembg import remove
import cv2
import sys
from enum import Enum

class PhotoSize(Enum):
    SIZE4X6 = "4x6"
    SIZE5X7 = "5x7"

class TypePhoto(Enum):
    SPAIN_DNI = "esp@dni"  # Código de país para DNI español
    SPAIN_PASSPORT = "esp@pas"  # Código de país para pasaporte español
    USA_PASSPORT = "usa@pas"  # Código de país para pasaporte estadounidense
    CUBA_CARNET = "cub@car"  # Código de país para carnet de identidad cubano
    CUBA_LICENCE = "cub@lic"  # Código de país para licencia de conducir cubana
    CHINA_VISA="chi@vis"
    CANADA_VISA="can@vis"

def getphoto(path: str, category: TypePhoto, size: PhotoSize, num: int = 1):
 MARGINLEFT = 5
 MARGINTOP = 20
 output_images = []
 original_img = cv2.imread(path)
 gray = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)
 face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
 faces = face_cascade.detectMultiScale(gray, 1.1, 5)
 
 if len(faces) == 0:
    print("❌ Not face detected.")
    sys.exit(1)

# Tomar el primer rostro y ampliar zona alrededor
 
 (x, y, w, h) = faces[0]
 margen = int(h)
 centro_x, centro_y = x + w // 2, y + h // 2
 x_ini = max(centro_x - int(0.9*margen), 0)
 y_ini = max(centro_y - int(0.9*margen), 0)
 x_fin = min(centro_x + int(0.9*margen), original_img.shape[1])
 y_fin = min(centro_y + int(0.9*margen), original_img.shape[0])

 # Set default values for DNI_WIDTH_PX and DNI_HEIGHT_PX
 DNI_WIDTH_PX = 306
 DNI_HEIGHT_PX = 378
 rest = 0

 if TypePhoto.SPAIN_DNI.value == category or TypePhoto.SPAIN_PASSPORT.value == category:
    DNI_WIDTH_PX = 306
    DNI_HEIGHT_PX = 378
    altura = abs(y_fin - y_ini)  
    ancho = int(0.81 * altura)
    rest = (altura - ancho) // 2
    
 elif TypePhoto.USA_PASSPORT.value == category:
    DNI_WIDTH_PX = 591
    DNI_HEIGHT_PX = 591
    rest =0
 
 elif TypePhoto.CUBA_CARNET.value == category:
    DNI_WIDTH_PX = 354
    DNI_HEIGHT_PX = 354    
    rest = 0
 elif TypePhoto.CUBA_LICENCE.value== category:
    DNI_WIDTH_PX = 302
    DNI_HEIGHT_PX = 302 
    rest = 0
 elif TypePhoto.CHINA_VISA.value== category:
    DNI_WIDTH_PX = 390
    DNI_HEIGHT_PX = 567
    altura = abs(y_fin - y_ini)  
    ancho = int(0.69 * altura)
    rest = (altura - ancho) // 2

 elif TypePhoto.CANADA_VISA.value== category:
     DNI_WIDTH_PX = 413
     DNI_HEIGHT_PX = 531
     altura = abs(y_fin - y_ini)  
     ancho = int(0.78 * altura)
     rest = (altura - ancho) // 2

 recorte = original_img[y_ini:y_fin, x_ini+rest:x_fin-rest]

# Convertir recorte a PIL para usar rembg
 recorte_pil = Image.fromarray(cv2.cvtColor(recorte, cv2.COLOR_BGR2RGB))

# --- Quitar fondo con rembg ---
 output_image = remove(recorte_pil)

#--output_image.save("outputyy.png")
#--sys.exit(0)
# --- Crear fondo blanco ---
# Convertimos a RGBA si no lo está (por seguridad)
 if output_image.mode != "RGBA":
    output_image = output_image.convert("RGBA")

 for i in range(num):
      # Crear fondo blanco con mismo tamaño
   final_image = Image.new("RGB", output_image.size, (255, 255, 255))
     # Combinar imagen sin fondo sobre blanco usando canal alfa
   final_image.paste(output_image, mask=output_image.split()[3])  # canal alfa
    # --- Redimensionar a tamaño  ---
   final_image = final_image.resize((DNI_WIDTH_PX,DNI_HEIGHT_PX), Image.LANCZOS, reducing_gap=3.0)
    # --- Guardar imagen final ---
   output_images.append(final_image)
   
 full_image = Image.new("RGB", (1200,1800), (211,211,211)) if (PhotoSize.SIZE4X6.value==size) else Image.new("RGB", (1500,2100), (211,211,211)) 
 #--full_image = output_images[0].resize((ENOUGHT*DNI_WIDTH_PX, DNI_HEIGHT_PX), Image.LANCZOS, reducing_gap=3.0)
 draw = ImageDraw.Draw(full_image)
# Define margins for image placement
 col=0
 row=0
 for i in range(num):
    # Guardar cada imagen generada
    #--full_image.save(f"foto_{i}.jpg", dpi=(300, 300))
    if (PhotoSize.SIZE4X6.value==size):
        if ((col+1) * DNI_WIDTH_PX < 1200):
            full_image.paste(output_images[i], (col * (DNI_WIDTH_PX+5)+MARGINLEFT, MARGINTOP+row*(DNI_HEIGHT_PX+5)))
            col=col+1
        else:
            row=row+1
            col=0
            full_image.paste(output_images[i], (col * (DNI_WIDTH_PX+5)+MARGINLEFT, MARGINTOP+row*(DNI_HEIGHT_PX+5)))
            col=col+1
        #--output_images[i].save(f"foto_{i}.jpg", dpi=(300, 300))
        print(f"✅ Photo {i} generated successfully.")
        # Línea después de la primera imagen
        #-- draw.line([(DNI_WIDTH_PX*col+MARGINLEFT, 0), (DNI_WIDTH_PX*col, DNI_HEIGHT_PX+MARGINTOP)], fill=(0, 0, 0), width=1)
    elif (PhotoSize.SIZE5X7.value==size):
        if ((col+1) * DNI_WIDTH_PX < 1500):
            full_image.paste(output_images[i], (col * (DNI_WIDTH_PX+5)+MARGINLEFT, MARGINTOP+row*(DNI_HEIGHT_PX+5)))
            col=col+1
        else:
            row=row+1
            col=0
            full_image.paste(output_images[i], (col * (DNI_WIDTH_PX+5)+MARGINLEFT, MARGINTOP+row*(DNI_HEIGHT_PX+5)))
            col=col+1
 full_image.save(path+"resut.jpg", dpi=(300,300))   
 return path+"resut.jpg"