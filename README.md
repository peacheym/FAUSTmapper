# FAUSTmapper

This repository hosts FAUSTmapper, a tool for binding popular Digital Musical Intrument (DMI) mapping tools to the [FAUST](https://faust.grame.fr/) ecosystem.

## libmapper Connectivity

The default action for the FAUSTmapper project is establishing a binding to the [libmapper](http://libmapper.org) project. When the script is run, the entire parameter space of an active FAUST project (with HTTP control enabled) will be discovered. Once discovered, a libmapper signal will be created for each of the parameters identified, including appropriate meta data such as min, max & default values.

To run the script, use the following command:

```bash
./faustmapper.py
```

## Wekinator Connectivity

FAUSTmapper also supports establishing a binding to the [Wekinator](http://www.wekinator.org/) project.

To run the script, use the following command:

```bash
./faustmapper.py --mapping-target wekinator
```

## Compiling FAUST projects

The FAUSTmapper project requires that a FAUST synthesizer or other DSP project is running locally on your machine with HTTP control.

### Faust2...

FAUST has made tooling avaliable to compile `.dsp` files to various platforms. For instance, to compile for use with JACK Audio, use the [faust2jack](https://faustdoc.grame.fr/manual/tools/#faust2jack) tool, as follows:

```bash
faust2jack -httpd -midi -nvoices 8 simplesynth.dsp
```

Which will compile the `simplesynth` project, with both HTTP and MIDI control with 8 voices of polyphony. For more FAUST compilation options, see the [faust2... tools documentation](https://faustdoc.grame.fr/manual/tools/).

## Todo List

This is an ongoing project, the following is a todo list of development tasks that would improve the usability of FAUSTmapper.

- Documentation
- `run.sh` type script to make the entire process work via a single command.
  - Run FAUST Synth
  - Connect via `faustmapper.py`
  - Ensure everything is up and running.
- Demos & Examples


## Poster

The following poster was presented at the [4th Annual International Symposium on the Internet of Sounds](https://internetofsounds.net/is2_2023/) and was awarded the **Best Poster Award**, thank you to the selection committee for this acknowledgement.

![FaustMapperPoster_Final](https://github.com/peacheym/FAUSTmapper/assets/15327742/e86308bb-b2bf-40fc-98fc-fed3c01692d7)
