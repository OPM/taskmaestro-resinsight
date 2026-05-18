# taskmaestro-resinsight

taskmaestro tasks and example workflows for ResInsight.

## Setup

```bash
git clone https://github.com/kriben/taskmaestro-resinsight ~/src/taskmaestro-resinsight
cd ~/src/taskmaestro-resinsight

# rips is not on PyPI; install from a local ResInsight checkout
pip install -e /path/to/resinsight/GrpcInterface/Python

# install this repo (tasks become importable as taskmaestro_resinsight.*)
pip install -e .
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
