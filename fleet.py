from car_factory import env, build


@env.task(cache="disable")
def fleet_workflow(models: list[str] = ["500", "Panda"]) -> list[str]:
    return [build(m, "Fiat", 2020).model for m in models]
