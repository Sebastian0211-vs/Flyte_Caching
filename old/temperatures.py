# temperatures.py
import time
import flyte

# A TaskEnvironment groups configuration for the tasks defined within it:
# the container image, resources, and so on. This one keeps the defaults.
env = flyte.TaskEnvironment(name="temperatures", cache="auto")

# The @env.task decorator turns a Python function into a task.
# Type annotations on the inputs and output are required.
@env.task
def to_fahrenheit(celsius: float) -> float:
    time.sleep(2) # to simulate a long-running task
    return celsius * 9 / 5 + 32

# This is the entrypoint task of the workflow. It calls to_fahrenheit
# once per reading using flyte.map, which is like Python's map but runs
# the calls in parallel, then returns the highest result.
@env.task
def hottest(readings: list[float] = [21.5, 19.0, 24.3, 22.8]) -> float:
    return round(max(flyte.map(to_fahrenheit, readings)), 1)


if __name__ == "__main__":
    flyte.init()
    t0 = time.time()
    r = flyte.run(hottest)
    print(f"Result: {r} (took {time.time() - t0:.2f} seconds)")