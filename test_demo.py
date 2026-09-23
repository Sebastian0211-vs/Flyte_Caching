import os
import re
import subprocess

from car_factory import Car, label


def run(tmp_path, *args, user="A", **env):
    home = tmp_path / user
    home.mkdir(exist_ok=True)
    p = subprocess.run(
        ["flyte", "run", "--local", *args],
        env={**os.environ, "HOME": str(home), "COLUMNS": "250", **env},
        capture_output=True, text=True,
    )
    built = re.findall(r"building (\w+)", p.stdout)
    return p.returncode, built, p.stdout + p.stderr


WF = ["car_factory.py", "car_factory_workflow"]


# Unit tests

def test_label():
    assert label(Car("Fiat", "500", 2020)) == "2020 Fiat 500"


# Integration tests: one per demo step

def test_cache(tmp_path):
    assert run(tmp_path, *WF)[1] == ["500", "Panda", "Punto"]
    assert run(tmp_path, *WF)[1] == []
    assert run(tmp_path, *WF, "--models", '["500","Panda","Uno"]')[1] == ["Uno"]


def test_shared_cache(tmp_path):
    run(tmp_path, *WF)
    assert run(tmp_path, "fleet.py", "fleet_workflow")[1] == []
    assert run(tmp_path, "fleet.py", "fleet_workflow", user="B")[1] == ["500", "Panda"]


def test_cache_version(tmp_path):
    run(tmp_path, *WF)
    assert "FIAT" not in run(tmp_path, *WF, LABEL_STYLE="upper")[2]
    assert "FIAT" in run(tmp_path, *WF, LABEL_STYLE="upper", DESCRIBE_VERSION="v2")[2]


def test_bad_type(tmp_path):
    code, built, out = run(tmp_path, *WF, "--year", "deux-mille")
    assert code != 0 and built == [] and "not a valid integer" in out