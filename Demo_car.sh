step() { echo; echo "== $1"; read -r _; }

flyte delete local-cache

step "1. Build three cars: all 3 execute"
time flyte run --local car_factory.py car_factory_workflow

step "2. Again, unchanged: 0 execute"
time flyte run --local car_factory.py car_factory_workflow

step "3. Swap one model, Punto -> Uno: exactly 1 executes"
time flyte run --local car_factory.py car_factory_workflow --models '["500","Panda","Uno"]'

step "4. Broken type: the run never starts"
time flyte run --local car_factory.py car_factory_workflow --year "deux-mille"
