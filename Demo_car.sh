step() { echo; echo "== $1"; read -r _; }

flyte delete local-cache
rm -rf /tmp/userB

step "1. Build three cars: 3 built"
time flyte run --local car_factory.py car_factory_workflow

step "2. Again, unchanged: 0 built"
time flyte run --local car_factory.py car_factory_workflow

step "3. Swap Punto for Uno: only the Uno is built"
time flyte run --local car_factory.py car_factory_workflow --models '["500","Panda","Uno"]'

step "4. Issue #1: another pipeline, same cache store: 0 built"
time flyte run --local Fleet.py fleet_workflow

step "5. Issue #1: user B, own cache store: 2 built"
time HOME=/tmp/userB flyte run --local Fleet.py fleet_workflow

step "6. Issue #2: the cache lies. Helper changed, output does not"
LABEL_STYLE=upper flyte run --local car_factory.py car_factory_workflow

step "7. Issue #2: bump the version by hand, output updates"
LABEL_STYLE=upper DESCRIBE_VERSION=v2 flyte run --local car_factory.py car_factory_workflow

step "8. Broken type: the run never starts"
time flyte run --local car_factory.py car_factory_workflow --year "deux-mille"