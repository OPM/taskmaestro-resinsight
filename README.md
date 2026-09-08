# taskmaestro-resinsight

taskmaestro tasks and example workflows for ResInsight.

## Installation

```bash
pip install taskmaestro-resinsight
```

`rips` must match the ResInsight build it talks to. To use the API from a local
ResInsight checkout instead of the released one on PyPI:

```bash
pip install -e /path/to/resinsight/GrpcInterface/Python
```

## Development setup

```bash
git clone https://github.com/OPM/taskmaestro-resinsight ~/src/taskmaestro-resinsight
cd ~/src/taskmaestro-resinsight

# install this repo and its test/lint tools (including Ruff 0.16+)
pip install -e ".[dev]"
```

## Exposing workflows to ResInsight

ResInsight discovers workflows under `~/.taskmaestro/workflows/<name>/workflow.yaml`.
Symlink each workflow directory in once:

```bash
mkdir -p ~/.taskmaestro/workflows
for d in workflows/*/; do
    ln -sfn "$(realpath "$d")" ~/.taskmaestro/workflows/"$(basename "$d")"
done
```

After `pip install -e .` the `taskmaestro_resinsight` package resolves from the
venv, so no `PYTHONPATH` tricks are needed. To verify:

```bash
cd /tmp && python -c "from taskmaestro_resinsight.select_eclipse_case import SelectEclipseCase; print(SelectEclipseCase)"
```

## Running tests

```bash
RESINSIGHT_EXECUTABLE=/path/to/ResInsight pytest tests/ -v
```
