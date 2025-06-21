# Generador de Tarjetas de Texto

Este script de Python genera imágenes PNG transparentes con texto extraído de un archivo de entrada.
El texto se divide en frases, se ajusta automáticamente (word wrap) y se le puede aplicar una sombra.

## Características

*   Divide texto de un archivo en frases.
*   Genera una imagen PNG por frase.
*   Fondo transparente.
*   Ajuste automático de línea (word wrap).
*   Sombreado de texto personalizable.
*   Opciones configurables mediante argumentos de línea de comandos.

## Requisitos

*   Python 3.x
*   Pillow (ver `requirements.txt`)

## Instalación

1.  Clona este repositorio:
    ```bash
    git clone https://github.com/TU_USUARIO/NOMBRE_DEL_REPOSITORIO.git
    cd NOMBRE_DEL_REPOSITORIO
    ```
2.  (Recomendado) Crea y activa un entorno virtual:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```
4.  Asegúrate de tener el archivo de fuente `Merriweather_VariableFont_opsz,wdth,wght.ttf` en el mismo directorio que el script.

## Uso

```bash
python generar_tarjetas.py <archivo_de_entrada.txt> [opciones]
```

Ejecuta con -h o --help para ver todas las opciones disponibles:
```bash
python generar_tarjetas.py -h
```

## Ejemplos


Generar tarjetas con configuración por defecto:
```bash
python generar_tarjetas.py mi_texto.txt
```

Personalizar tamaño de fuente y directorio de salida:
```bash
python generar_tarjetas.py mi_texto.txt -o ./mis_tarjetas -fs 80
```

Añadir sombra roja y desactivar la fuente empaquetada (si tienes una específica en el sistema):
```bash
python generar_tarjetas.py mi_texto.txt --shadow_color "255,0,0,128" --font_path "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
```


## Licencia

Este proyecto está licenciado bajo la GNU General Public License v3.0.
Consulta el archivo `LICENSE` para ver el texto completo de la licencia.

En resumen, esto significa que eres libre de:
*   **Compartir** — copiar y redistribuir el material en cualquier medio o formato.
*   **Adaptar** — remezclar, transformar y construir sobre el material para cualquier propósito, incluso comercialmente.

Bajo las siguientes condiciones:
*   **Atribución** — Debes dar crédito de manera adecuada, brindar un enlace a la licencia, e indicar si se han realizado cambios. Puedes hacerlo de cualquier manera razonable, pero no de una manera que sugiera que el licenciante te respalda a ti o al uso que hagas del material.
*   **CompartirIgual (ShareAlike)** — Si remezclas, transformas o construyes sobre el material, debes distribuir tus contribuciones bajo la misma licencia que el original.
*   **Sin restricciones adicionales** — No puedes aplicar términos legales o medidas tecnológicas que restrinjan legalmente a otros de hacer cualquier cosa que la licencia permita.

Para más detalles, visita: [https://www.gnu.org/licenses/gpl-3.0.html](https://www.gnu.org/licenses/gpl-3.0.html)

