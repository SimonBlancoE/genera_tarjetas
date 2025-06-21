# generador_tarjetas.py
# Copyright (C) 2023 Simón Blanco Estévez
#
# Este programa es software libre: usted puede redistribuirlo y/o modificarlo
# bajo los términos de la Licencia Pública General GNU publicada por
# la Free Software Foundation, ya sea la versión 3 de la Licencia,
# o (a su elección) cualquier versión posterior.
#
# Este programa se distribuye con la esperanza de que sea útil, pero
# SIN GARANTÍA ALGUNA; ni siquiera la garantía implícita de
# MERCANTIBILIDAD o IDONEIDAD PARA UN PROPÓSITO PARTICULAR. Consulte la
# Licencia Pública General GNU para más detalles.
#
# Usted debería haber recibido una copia de la Licencia Pública General GNU
# junto con este programa. Si noবীর, consulte <https://www.gnu.org/licenses/>.


from PIL import Image, ImageDraw, ImageFont
import os
import re
import argparse
import sys # Necesario para resource_path

# --- Función para obtener la ruta de recursos (para PyInstaller) ---
def resource_path(relative_path):
    """ Obtiene la ruta absoluta al recurso, funciona para desarrollo y para PyInstaller """
    try:
        # PyInstaller crea una carpeta temporal y guarda la ruta en _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # sys._MEIPASS no está definido, así que estamos en desarrollo
        base_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)

# --- Función para Añadir Saltos de Línea (Word Wrap) ---
def wrap_text(text, font, max_width):
    """
    Añade saltos de línea ('\n') a un string para que no exceda max_width.
    Funciona palabra por palabra.
    """
    lines = []
    if text is None or not text.strip():
        return ""
    words = text.split()
    if not words:
        return ""
    current_line = words[0]
    for word in words[1:]:
        test_line = f"{current_line} {word}"
        bbox = font.getbbox(test_line)
        width = bbox[2] - bbox[0]
        if width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)
    return "\n".join(lines)

# --- Función para Crear una Tarjeta de Texto (Modificada con Sombra) ---
def create_text_card(text, output_path, font_path_param, font_size, text_color, width, height,
                     text_anchor, text_alignment, margin=100, line_spacing=10,
                     shadow_color=(0, 0, 0, 128), shadow_offset=(3, 3)):
    """Genera una imagen PNG con texto auto-ajustado y sombreado sobre fondo transparente."""
    image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype(font_path_param, font_size)
    except IOError:
        print(f"Error: No se pudo cargar la fuente en '{font_path_param}'. Usando predeterminada.")
        try:
            font = ImageFont.load_default()
        except IOError:
            print("Error: Tampoco se pudo cargar la fuente predeterminada. Saliendo.")
            return False

    max_text_width = width - (2 * margin)
    wrapped_text = wrap_text(text, font, max_text_width)

    base_position_x = width / 2
    base_position_y = height / 2

    if shadow_color and shadow_offset and (shadow_offset[0] != 0 or shadow_offset[1] != 0):
        shadow_pos_x = base_position_x + shadow_offset[0]
        shadow_pos_y = base_position_y + shadow_offset[1]
        draw.text(
            (shadow_pos_x, shadow_pos_y), wrapped_text, fill=shadow_color, font=font,
            anchor=text_anchor, align=text_alignment, spacing=line_spacing
        )

    draw.text(
        (base_position_x, base_position_y), wrapped_text, fill=text_color, font=font,
        anchor=text_anchor, align=text_alignment, spacing=line_spacing
    )

    try:
        image.save(output_path, "PNG")
        print(f"Tarjeta guardada como '{output_path}'")
        return True
    except Exception as e:
        print(f"Error al guardar la imagen '{output_path}': {e}")
        return False

# --- Función para parsear color RGBA desde string ---
def parse_color(color_string):
    try:
        r, g, b, a = map(int, color_string.split(','))
        if not all(0 <= val <= 255 for val in (r, g, b, a)):
            raise ValueError("Los valores de color deben estar entre 0 y 255.")
        return (r, g, b, a)
    except ValueError as e:
        raise argparse.ArgumentTypeError(f"El color '{color_string}' debe tener el formato R,G,B,A con valores 0-255 (ej: 0,0,0,128). Error: {e}")

# --- Función Principal (Modificada para argumentos de sombra y mejor ayuda) ---
def main():
    # --- Configuración de Argumentos con Ayuda Mejorada ---
    parser = argparse.ArgumentParser(
        description="Genera tarjetas de texto (imágenes PNG) para cada frase de un archivo de texto, con auto-ajuste de línea y sombra opcional.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter, # Muestra los valores por defecto
        epilog="""Ejemplos de uso:
  %(prog)s mi_archivo.txt
  %(prog)s entrada.txt -o ./salida_custom -fs 80 --shadow_color "255,0,0,150"
  %(prog)s texto_largo.txt -m 50 --no_shadow

Notas:
  Asegúrate de tener la fuente 'Merriweather-Regular.ttf' en el mismo directorio que el script/ejecutable,
  o que esté instalada en el sistema si la ruta por defecto se utiliza y la empaquetada no se encuentra.
  PyInstaller: Si empaquetas, usa '--add-data "Merriweather-Regular.ttf:."' para incluir la fuente.
"""
    )
    parser.add_argument("input_file", help="Ruta al archivo de texto de entrada (.txt)")
    parser.add_argument("-o", "--output_dir", default="tarjetas_generadas", help="Directorio donde se guardarán las imágenes.")
    parser.add_argument("-m", "--margin", type=int, default=100, help="Margen lateral en píxeles para el texto.")
    parser.add_argument("-fs", "--fontsize", type=int, default=70, help="Tamaño de la fuente base.")
    parser.add_argument("-ls", "--linespacing", type=int, default=10, help="Espacio extra entre líneas en píxeles.")

    shadow_group = parser.add_argument_group('Opciones de Sombra')
    shadow_group.add_argument("--shadow_color", type=parse_color, default="0,0,0,128", help="Color de la sombra en formato R,G,B,A (ej: '0,0,0,128').")
    shadow_group.add_argument("--shadow_offset_x", type=int, default=3, help="Desplazamiento horizontal de la sombra en píxeles.")
    shadow_group.add_argument("--shadow_offset_y", type=int, default=3, help="Desplazamiento vertical de la sombra en píxeles.")
    shadow_group.add_argument("--no_shadow", action="store_true", help="Desactiva la sombra del texto.")

    font_group = parser.add_argument_group('Opciones de Fuente (Avanzado)')
    font_group.add_argument("--font_path", default=None, help="Ruta personalizada al archivo de fuente .ttf. Si no se especifica, se busca 'Merriweather-Regular.ttf' junto al script/ejecutable, luego en rutas del sistema, y finalmente se usa la fuente por defecto de Pillow.")
    font_group.add_argument("--font_name_bundled", default="Merriweather_VariableFont_opsz,wdth,wght.ttf", help="Nombre del archivo de fuente que se espera esté empaquetado o junto al script.")


    args = parser.parse_args()

    # --- Parámetros de Imagen y Texto ---
    width = 1920
    height = 1080
    text_color = (0, 0, 0, 255)
    text_anchor = "mm"
    text_alignment = "center"

    # --- Configuración de la Fuente ---
    font_to_use = args.font_path # Prioridad 1: ruta especificada por el usuario

    if font_to_use is None: # Si el usuario no especificó una ruta
        font_to_use = resource_path(args.font_name_bundled) # Prioridad 2: fuente junto al script/empaquetada
        if not os.path.exists(font_to_use):
            print(f"Advertencia: Fuente '{args.font_name_bundled}' no encontrada junto al script/ejecutable en '{font_to_use}'.")
            # Prioridad 3: Ruta de sistema (puedes añadir más si es necesario)
            system_font_path_linux = "/usr/share/fonts/truetype/merriweather/Merriweather-Regular.ttf"
            # Añade aquí otras rutas comunes para Windows/macOS si quieres
            # system_font_path_windows = "C:\\Windows\\Fonts\\Merriw.ttf" # Ejemplo
            if os.path.exists(system_font_path_linux):
                print(f"Intentando usar fuente del sistema: {system_font_path_linux}")
                font_to_use = system_font_path_linux
            # else if os.path.exists(system_font_path_windows):
            #    font_to_use = system_font_path_windows
            else:
                print("No se encontró una fuente especificada ni en el sistema. Se intentará usar la fuente por defecto de Pillow.")
                font_to_use = None # Se pasará None a create_text_card, que usará la default
    else:
        if not os.path.exists(font_to_use):
            print(f"Advertencia: La ruta de fuente especificada '{font_to_use}' no existe. Se intentará usar la fuente por defecto de Pillow.")
            font_to_use = None # Se pasará None a create_text_card, que usará la default


    shadow_color_val = args.shadow_color
    shadow_offset_val = (args.shadow_offset_x, args.shadow_offset_y)
    if args.no_shadow:
        shadow_color_val = None
        shadow_offset_val = (0, 0)

    try:
        with open(args.input_file, 'r', encoding='utf-8') as f:
            full_text = f.read()
    except FileNotFoundError:
        print(f"Error: El archivo de entrada '{args.input_file}' no fue encontrado.")
        return
    except Exception as e:
        print(f"Error al leer el archivo '{args.input_file}': {e}")
        return

    text_cleaned = ' '.join(full_text.split())
    sentences = re.split(r'([.?!])\s*', text_cleaned)
    phrases = []
    current_phrase = ""
    for i in range(0, len(sentences)):
        part = sentences[i]
        if not part: continue
        current_phrase += part
        if part in ".?!": # Si es un delimitador
            phrases.append(current_phrase.strip())
            current_phrase = ""
        elif i == len(sentences) -1 and current_phrase.strip(): # Última parte sin delimitador
             phrases.append(current_phrase.strip())

    if not phrases and current_phrase.strip(): # Caso de texto sin delimitadores
        phrases.append(current_phrase.strip())


    if not phrases:
        print("No se encontraron frases en el texto.")
        return
    print(f"Se encontraron {len(phrases)} frases.")

    output_dir = args.output_dir
    os.makedirs(output_dir, exist_ok=True)

    for i, phrase in enumerate(phrases):
        if not phrase.strip(): # Omitir frases vacías que puedan surgir
            continue
        output_filename = f"tarjeta_{i+1:03d}.png"
        output_filepath = os.path.join(output_dir, output_filename)
        print(f"\nGenerando tarjeta {i+1}/{len(phrases)} para la frase:")
        print(f"'{phrase}'")
        create_text_card(
            text=phrase,
            output_path=output_filepath,
            font_path_param=font_to_use, # Pasar la ruta de fuente determinada
            font_size=args.fontsize,
            text_color=text_color,
            width=width,
            height=height,
            text_anchor=text_anchor,
            text_alignment=text_alignment,
            margin=args.margin,
            line_spacing=args.linespacing,
            shadow_color=shadow_color_val,
            shadow_offset=shadow_offset_val
        )
    print(f"\n¡Proceso completado! Imágenes guardadas en '{output_dir}'")

if __name__ == "__main__":
    main()
