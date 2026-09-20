step() { echo; echo "== $1"; read -r _; }

flyte delete local-cache

step "1. Run it: 5 actions execute"
time flyte run --local temperatures.py hottest

step "2. Again, unchanged: 0 execute"
time flyte run --local temperatures.py hottest

step "3. One reading changed: exactly 1 executes"
time flyte run --local temperatures.py hottest --readings '[21.5, 19.0, 26.1, 22.8]'

step "4. Broken type: 0 execute, the run never starts"
time flyte run --local temperatures.py hottest --readings '[21.5, "cold"]'