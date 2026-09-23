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
| 4 | another pipeline, `fleet.py`, same machine | 0 built, it reuses the 500 and Panda, ~0.7s |
| 5 | same pipeline, user B with their own cache store | 2 built, ~4.7s |
| 6 | a helper outside `describe` changes (`LABEL_STYLE=upper`) | output stays lowercase, the cache lies |
| 7 | the cache version is bumped by hand (`DESCRIBE_VERSION=v2`) | output updates, no car rebuilt |
| 8 | `--year "deux-mille"` | rejected as not an integer, the run never starts |
 
Each built car prints `building <model>`, so you can see exactly what ran.

Flyte decides, using a cache key of four parts: task name, an interface hash over the
input and output **types**, the inputs, and the cache version. The typed interface is a
component of the key, not documentation.

With `cache="auto"` the cache version is a hash of the function source, so editing a task
body invalidates its entry. It cannot see helpers, libraries or external data, which is
why `describe` pins its version by hand with `version_override` (steps 6 and 7). In local
mode Flyte only reads the cache when `behavior="auto"`, so the pinned version is set as
`flyte.Cache(behavior="auto", version_override=...)`.
 
The cache key contains neither the pipeline nor the user: what decides sharing is the
cache store (steps 4 and 5).

`Car` is a `@dataclass` so Flyte can serialise it between tasks. A plain class works
too, but Flyte falls back to pickle and warns me about it.

## Tests
 
```bash
pytest -v
```
 
One unit test for `label()`, and integration tests that replay every demo step through
the real `flyte run --local` CLI, each with its own isolated cache. They run on GitHub
Actions after every push, and double as a failsafe if the live demo breaks.
 
Tested on flyte 2.8.1 and 2.10.0.

link to [slides](https://hessoit-my.sharepoint.com/:p:/r/personal/sebastia_morsch_hes-so_ch/Documents/Presentation%208.pptx?d=w9e030e3a56c848c8918f836c6c41f899&csf=1&web=1&e=y79M3S)