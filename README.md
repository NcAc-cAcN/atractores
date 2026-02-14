# Generador de Atractores Caóticos

Generador y visualizador de atractores caóticos utilizando el exponente de Lyapunov.

## Instalación

```sh
git clone https://github.com/NcAc-cAcN/atractores.git
cd atractores
pip install -r requirements.txt
```

## Uso

```sh
python main.py
```

### Ejemplos

```sh
# Con semilla personalizada
python main.py --seed "mi_semilla"

# Alta resolución
python main.py --width 3840 --height 2160

# Coloreado por densidad
python main.py --density-color

# Cargar desde metadatos
python main.py --load-metadata outputs/atractor_metadata.json
```

### Parámetros principales

- `-o, --output`: Nombre base para archivos de salida (default: "atractor")
- `-s, --seed`: Semilla para reproducibilidad
- `-w, --width`: Ancho de imagen (default: 1920)
- `--height`: Alto de imagen (default: 1080)
- `-i, --iterations`: Máximo de iteraciones (default: 10000)
- `--density-color`: Colorear por densidad local
- `--load-metadata`: Cargar desde archivo de metadatos

## Salida

- `outputs/[nombre].png`: Imagen del atractor
- `outputs/[nombre]_metadata.json`: Metadatos para reproducir el atractor


