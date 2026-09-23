from dataclasses import dataclass

import time
import flyte
import os

env = flyte.TaskEnvironment(name="car_factory", cache="auto")

DESCRIBE_VERSION = os.environ.get("DESCRIBE_VERSION", "v1")

@dataclass
class Car:
    make: str
    model: str
    year: int

def label(car: Car) -> str:
    text = f"{car.year} {car.make} {car.model}"
    return text.upper() if os.environ.get("LABEL_STYLE") == "upper" else text

@env.task
def build(model: str, make: str, year: int) -> Car:
    print(f"building {model}")
    time.sleep(2)
    return Car(make, model, year)


@env.task(cache=flyte.Cache(behavior="auto", version_override=DESCRIBE_VERSION))
def describe(car: Car) -> str:
    return label(car)


@env.task(cache="disable")
def car_factory_workflow(models: list[str] = ["500", "Panda", "Punto"],
                         make: str = "Fiat", year: int = 2020) -> list[str]:
    return [describe(build(model, make, year)) for model in models]