import base64
import hashlib
import json
import math
import random
from pathlib import Path
from typing import List, Tuple


def encode_seed(seed: str) -> str:
    md5_hash = hashlib.md5(seed.encode()).hexdigest()
    return base64.b64encode(md5_hash.encode()).decode()


def decode_seed(encoded_seed: str) -> str:
    return base64.b64decode(encoded_seed.encode()).decode()


def set_seed_from_encoded(encoded_seed: str) -> None:
    decoded = decode_seed(encoded_seed)
    seed_int = int(decoded, 16) % (2**32)
    random.seed(seed_int)


def buscar_atractores(
    n: int = 1,
    seed: str = None,
    encoded_seed: str = None,
    max_iterations: int = 10000,
    min_lyapunov: float = 10.0,
    burn_in: int = 100,
    max_attempts: int = 1000
) -> Tuple[List[Tuple[List[float], List[float]]], Tuple[float, float, List[float]], str]:
    """Genera atractores caóticos usando el exponente de Lyapunov.
    
    Raises RuntimeError si no se encuentra ningún atractor válido.
    """
    if encoded_seed is not None:
        set_seed_from_encoded(encoded_seed)
    elif seed is None:
        seed = str(random.random())
        encoded_seed = encode_seed(seed)
        set_seed_from_encoded(encoded_seed)
    else:
        encoded_seed = encode_seed(seed)
        set_seed_from_encoded(encoded_seed)

    atractores = []
    encontrados = 0
    intentos = 0
    ultimos_parametros = None

    while encontrados < n and intentos < max_attempts:
        intentos += 1
        x = random.uniform(-0.5, 0.5)
        y = random.uniform(-0.5, 0.5)

        xe = x + random.uniform(-0.5, 0.5) / 1000
        ye = y + random.uniform(-0.5, 0.5) / 1000

        dx = xe - x
        dy = ye - y
        d0 = math.sqrt(dx * dx + dy * dy)

        a = [random.uniform(-2, 2) for _ in range(12)]

        x_lista = [x]
        y_lista = [y]

        convergiendo = False
        lyapunov = 0.0

        for i in range(max_iterations):
            xnew = (a[0] + a[1] * x + a[2] * x * x + a[3] * y +
                    a[4] * y * y + a[5] * x * y)
            ynew = (a[6] + a[7] * x + a[8] * x * x + a[9] * y +
                    a[10] * y * y + a[11] * x * y)

            if (xnew > 1e10 or ynew > 1e10 or
                    xnew < -1e10 or ynew < -1e10):
                convergiendo = True
                break

            if abs(x - xnew) < 1e-10 and abs(y - ynew) < 1e-10:
                convergiendo = True
                break

            if i > 1000:
                xenew = (a[0] + a[1] * xe + a[2] * xe * xe +
                         a[3] * ye + a[4] * ye * ye + a[5] * xe * ye)
                yenew = (a[6] + a[7] * xe + a[8] * xe * xe +
                         a[9] * ye + a[10] * ye * ye + a[11] * xe * ye)

                dx = xenew - xnew
                dy = yenew - ynew
                d = math.sqrt(dx * dx + dy * dy)

                if d > 0 and d0 > 0:
                    lyapunov += math.log(abs(d / d0))

                    xe = xnew + d0 * dx / d
                    ye = ynew + d0 * dy / d

            x = xnew
            y = ynew

            x_lista.append(x)
            y_lista.append(y)

        if not convergiendo and lyapunov >= min_lyapunov:
            encontrados += 1
            atractores.append((x_lista[burn_in:], y_lista[burn_in:]))
            ultimos_parametros = (x_lista[0], y_lista[0], a)

    if not atractores:
        raise RuntimeError(
            f"No se encontró ningún atractor válido después de {intentos} intentos"
        )

    if ultimos_parametros is None:
        ultimos_parametros = (x_lista[0], y_lista[0], a)

    return atractores, ultimos_parametros, encoded_seed


def save_metadata(
    filepath: Path,
    parametros: Tuple[float, float, List[float]],
    encoded_seed: str,
    num_points: int
) -> None:
    metadata = {
        "seed": encoded_seed,
        "initial_x": parametros[0],
        "initial_y": parametros[1],
        "coefficients": parametros[2],
        "num_points": num_points
    }

    with open(filepath, "w") as f:
        json.dump(metadata, f, indent=2)


def load_metadata(filepath: Path) -> dict:
    with open(filepath, "r") as f:
        return json.load(f)
