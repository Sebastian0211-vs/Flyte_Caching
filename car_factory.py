from dataclasses import dataclass

import time
import flyte

env = flyte.TaskEnvironment(name="car_factory", cache="auto")

@dataclass
class Car:
    make: str
    model: str
    year: int


@env.task
def build(model: str, make: str, year: int) -> Car:
    time.sleep(2)
    return Car(make, model, year)


@env.task
def describe(car: Car) -> str:
    return f"{car.year} {car.make} {car.model}"


@env.task(cache="disable")
def car_factory_workflow(models: list[str] = ["500", "Panda", "Punto"],
                         make: str = "Fiat", year: int = 2020) -> list[str]:
    return [describe(build(model, make, year)) for model in models]