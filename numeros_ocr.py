import easyocr
import os
import re

# Inicializar el lector de OCR
easyocr_reader = easyocr.Reader(['es'])  # Cambié a 'es' para el español

# Ruta de entrada
input_folder = r'C:/Users/57320/Desktop/imgs'

# Procesar todas las imágenes en la carpeta y sus subcarpetas
for root, dirs, files in os.walk(input_folder):
    for filename in files:
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):  # Formatos de imagen
            image_path = os.path.join(root, filename)
            print(f'Procesando: {image_path}')
            
            # Realizar OCR en la imagen
            results = easyocr_reader.readtext(image_path)

            # Generar el nombre del archivo de texto
            txt_filename = os.path.splitext(filename)[0] + '.txt'
            output_txt_path = os.path.join(root, txt_filename)

            # Guardar los resultados en un archivo de texto en la misma subcarpeta
            with open(output_txt_path, 'w', encoding='utf-8') as output_file:
                for bound in results:
                    text = bound[1]

                    # Verificar si el texto contiene números
                    if re.search(r'\d', text):  # Busca cualquier dígito en el texto
                        output_file.write(f'Imagen: {image_path} - Texto: {text}\n')

            print(f'Datos guardados en: {output_txt_path}')

print('Proceso completado.')
