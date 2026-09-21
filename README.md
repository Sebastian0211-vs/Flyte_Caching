# Caching and typed interfaces in Flyte

Flipped class, 302 Data infrastructures, topic 9.

**You changed one task and re-ran the workflow. What has to run again, and who decides?**

## Run

```bash
uv add -r requirements.txt

bash ./Demo_car.sh
```

Press enter between steps.

## What it shows

`car_factory_workflow` builds three Fiats, a 500, a Panda and a Punto, and describes
each one. That is one **run** made of several **actions**: the entrypoint, plus one
`build` and one `describe` per car. Flyte caches actions, not runs.

| step | what changes | result |
|------|---|---|
| 1 | nothing, cold cache | 3 cars built, ~6.7s |
| 2 | nothing | 0 built, every action a cache hit, ~0.7s |
| 3 | one model, Punto to Uno | 1 car built, the other two from cache, ~2.7s |
| 4 | `--year "deux-mille"` | rejected as not an integer, the run never starts |

Flyte decides, using a cache key of four parts: task name, an interface hash over the
input and output **types**, the inputs, and the cache version. The typed interface is a
component of the key, not documentation.

With `cache="auto"` the cache version is a hash of the function source, so editing a task
body invalidates its entry.

`Car` is a `@dataclass` so Flyte can serialise it between tasks. A plain class works
too, but Flyte falls back to pickle and warns me about it.

Tested on flyte 2.8.1.