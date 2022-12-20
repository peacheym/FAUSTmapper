# FAUSTmapper

This repository hosts FAUSTmapper, a tool for binding popular mapping tools to the [FAUST](https://faust.grame.fr/) ecosystem.

## libmapper Connectivity

The default action for the FAUSTmapper project is establishing a binding to the [libmapper](http://libmapper.org) project. When the script is run, the entire parameter space of an active FAUST project (with HTTP control enabled) will be discovered. Once discovered, a libmapper signal will be created for each of the parameters identified, including appropriate meta data such as min, max & default values.

To run the script, use the following command:

```bash
./faustmapper.py
```

## Wekinator Connectivity

FAUSTmapper also supports establishing a binding to the [Wekinator](http://www.wekinator.org/) project.

<todo: Include Wekinator description>

To run the script, use the following command:

```bash
./faustmapper.py --mapping-target wekinator
```

## Todo List

This is an ongoing project, the following is a todo list of development tasks that would improve the usability of FAUSTmapper.

- Documentation
- `run.sh` type script to make the entire process work via a single command.
  - Run FAUST Synth
  - Connect via `faustmapper.py`
  - Ensure everything is up and running.
- Demos & Examples
