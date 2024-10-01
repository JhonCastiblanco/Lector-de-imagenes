import easyocr
from PIL import Image
import os

# Inicializar el lector de OCR
easyocr_reader = easyocr.Reader(['es'])  # Cambié a 'es' para el español

# Función para recortar y ajustar la imagen
def draw_boxes(image_path, model):
    image = Image.open(image_path)
    res = model.readtext(image)

    found_keyword = False  # Variable para detectar si se encuentra la palabra clave
    cropped_image = None  # Variable para almacenar la imagen recortada

    for bound in res:
        p0, p1, p2, p3 = bound[0]
        text = bound[1]

        # Verificar si el texto contiene "ficha predial"
        if "ficha predial" in text.lower():
            found_keyword = True
            print(f'Palabra encontrada en: "{image_path}"')

            # Calcular dimensiones para el recorte
            min_x = int(min(p0[0], p1[0], p2[0], p3[0]))  # Comenzar desde el punto más a la izquierda
            min_y = int(min(p0[1], p1[1], p2[1], p3[1])) - 60  # 10 píxeles arriba
            max_x = image.width  # Extender hasta el borde derecho
            max_y = int(max(p0[1], p1[1], p2[1], p3[1])) + 60  # 10 píxeles abajo

            # Asegurarse de que los límites no excedan las dimensiones de la imagen
            min_y = max(min_y, 0)
            max_y = min(max_y, image.height)

            # Recortar la imagen
            cropped_image = image.crop((min_x, min_y, max_x, max_y))

    return cropped_image, found_keyword

# Ruta de entrada y salida
input_folder = r'C:\Users\57320\Desktop\Carpetas documentos'
output_folder = r'C:\Users\57320\Desktop\imgs'

# Asegurarse de que la carpeta de salida existe
os.makedirs(output_folder, exist_ok=True)

# Procesar todas las imágenes en la carpeta y sus subcarpetas
for root, dirs, files in os.walk(input_folder):
    for filename in files:
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):  # Formatos de imagen
            image_path = os.path.join(root, filename)
            output_image, found = draw_boxes(image_path, easyocr_reader)

            # Guardar la imagen recortada si se encontró la palabra
            if found and output_image is not None:
                # Crear la ruta de salida, manteniendo la estructura de carpetas
                relative_path = os.path.relpath(image_path, input_folder)
                output_path = os.path.join(output_folder, relative_path)

                # Asegurarse de que la subcarpeta existe
                os.makedirs(os.path.dirname(output_path), exist_ok=True)

                output_image.save(output_path)
                print(f'Imagen guardada: {output_path}')
            else:
                print(f'La palabra "FICHA PREDIAL" no fue encontrada en: {image_path}')
