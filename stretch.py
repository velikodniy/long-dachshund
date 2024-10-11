import argparse
import dataclasses
import functools
import json
import pathlib
import sys

SCRIPT_DIR = pathlib.Path(__file__).parent
MODEL_CONFIG_FILE = "dachshund.json"
MODEL_FILE = "dachshund.obj"


@dataclasses.dataclass
class ModelConfig:
    body_x_min: float
    body_x_max: float
    axis: int


@functools.cache
def get_coeffs(x_min: float, x_max: float, factor: float) -> list[float]:
    delta = x_max - x_min
    delta_sqr = delta**2
    a = -2 * (factor - 1)
    b = 3 * (factor - 1) * (x_max + x_min)
    c = x_max**2 + (4 - 6 * factor) * x_min * x_max + x_min**2
    d = (factor - 1) * (3 * x_max - x_min) * x_min**2
    return [a / delta_sqr, b / delta_sqr, c / delta_sqr, d / delta_sqr]


def poly(coeffs: list[float], x: float) -> float:
    y = coeffs[0]
    for c in coeffs[1:]:
        y = y * x + c
    return y


def map_x(x: float, config: ModelConfig, stretch_factor: float) -> float:
    x_min = config.body_x_min
    x_max = config.body_x_max
    delta = x_max - x_min
    if x <= x_min:
        return x
    if x > x_max:
        return x + delta * (stretch_factor - 1)
    coeffs = get_coeffs(x_min, x_max, stretch_factor)
    return poly(coeffs, x)


def is_vertex(line: str) -> bool:
    return line.startswith("v ")


def vertex_to_coords(line: str) -> list[float]:
    items = line.split()
    return [float(x) for x in items[1:]]


def coords_to_vertex(coords: list[float]) -> str:
    coords_str = [f"{x:.4}" for x in coords]
    return f"v {' '.join(coords_str)}"


def process_line(line: str, config: ModelConfig, stretch_factor: float) -> str:
    line = line.strip()
    if not is_vertex(line):
        return line
    coords = vertex_to_coords(line)
    coords[config.axis] = map_x(coords[config.axis], config, stretch_factor)
    return coords_to_vertex(coords)


def make_long_model(base_model: str, config: ModelConfig, stretch_factor: float) -> str:
    output = []
    for line in base_model.split("\n"):
        new_line = process_line(line, config, stretch_factor)
        output.append(new_line)
    return "\n".join(output)


def load_config(config_path: pathlib.Path) -> ModelConfig:
    with config_path.open() as fp:
        config_object = json.load(fp)
    return ModelConfig(**config_object)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Make a long dachshund OBJ model")
    parser.add_argument(
        "-s",
        "--stretch",
        type=float,
        default=2.0,
        help="The stretch factor. Default: %(default)s",
    )
    parser.add_argument(
        "-o", "--output", type=pathlib.Path, required=True, help="The output OBJ file"
    )
    return parser.parse_args()


if __name__ == "__main__":
    config = load_config(SCRIPT_DIR / MODEL_CONFIG_FILE)
    args = parse_args()
    stretch_factor: float = args.stretch
    base_model_path = SCRIPT_DIR / MODEL_FILE
    output_path: pathlib.Path = args.output

    if output_path.absolute() == base_model_path.absolute():
        sys.exit("Can't overwrite the base model")

    base_model = base_model_path.read_text()
    output_model = make_long_model(base_model, config, stretch_factor)
    output_path.write_text(output_model)
