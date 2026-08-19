# taskmaestro-resinsight

taskmaestro tasks and example workflows for ResInsight.

## Setup

```bash
git clone https://github.com/kriben/taskmaestro-resinsight ~/src/taskmaestro-resinsight
cd ~/src/taskmaestro-resinsight

# rips is not on PyPI; install from a local ResInsight checkout
pip install -e /path/to/resinsight/GrpcInterface/Python

# install this repo and its test/lint tools (including Ruff 0.16+)
pip install -e ".[dev]"
```

## Discovering tasks and workflows

Installing the package registers its tasks and completions workflow through the
`taskmaestro.tasks` and `taskmaestro.workflows` entry-point groups. No source-tree scan,
`PYTHONPATH` change, or workflow-directory symlink is needed:

```python
from taskmaestro import (
    get_registered_workflow,
    registered_task_names,
    registered_workflow_names,
)

print(
    sorted(name for name in registered_task_names() if name.startswith("resinsight."))
)
# ['resinsight.add_perforation', 'resinsight.connect', ...]

print(registered_workflow_names())
# {'resinsight.completions'}

workflow = get_registered_workflow("resinsight.completions")
print(workflow.to_mermaid())
```

The example in `workflows/resinsight_completions/workflow.yaml` also uses entry-point
identifiers such as `resinsight.connect` in its `task:` and `depends_on:` fields. It can
be loaded normally after installation:

```python
from taskmaestro import load_workflow_from_yaml

loaded = load_workflow_from_yaml(
    "workflows/resinsight_completions/workflow.yaml",
    "workflows/resinsight_completions/input.yaml",
)
```

Applications can use `registered_workflows()` as their workflow catalogue and avoid the
old convention of scanning `~/.taskmaestro/workflows`.

## Running tests

```bash
RESINSIGHT_EXECUTABLE=/path/to/ResInsight pytest tests/ -v
```
