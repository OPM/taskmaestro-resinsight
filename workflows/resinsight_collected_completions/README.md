# Collect and perforate selected and mapped well paths

This example sits beside `resinsight_completions`. Two selected wells receive
explicit MD intervals.

`load_wells` maps over the `paths` dictionary in `input.yaml`: each key becomes
`well_key`, each value becomes `path`, and the result is a dictionary of
`WellPath` objects. `add_full_length_perforations` accepts that dictionary
via its `well_paths` port and applies `AddFullLengthPerforation` to each well.
That single-well task reads `trajectory_properties(resampling_interval=10.0)`
and uses the minimum and maximum measured depths to create an event. A missing,
invalid or zero-length trajectory raises an error. The batch output preserves
the mapping keys.

The exporter has just one `perforations: list[PerforationOutput]` port for all
wells. A single `collect` fills it: `add_perf_1` and `add_perf_2` are added as
items, and the `dict[str, PerforationOutput]` from
`add_full_length_perforations` is flattened into its values in mapping order.

Replace the placeholder `.dev` paths and supply runtime `case` and `well_path`
values (as with `resinsight_completions`) before running with ResInsight.

To use the single-well task with one selected or imported `WellPath`:

```yaml
- task: resinsight.add_full_length_perforation
  depends_on:
    resinsight: resinsight.connect
    well_path: select_well_path_1
  config_fields: [event_date]
```

A mapped task's output is already a dictionary; the workflow therefore uses a
direct dependency from `load_wells` to `well_paths`. Taskmaestro cannot map a
task over an *upstream output* with `map.over` (it maps over per-task config),
so the batch task bridges the two. The legacy `export_completions.perforation_1`
and `.perforation_2` ports remain individual outputs, not collections.
