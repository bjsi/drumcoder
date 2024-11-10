# DrumCoder

# Notes on how DreamCoder Works

## Training

- init grammar, uniform prob
- call @ecIterator
- start the wake, sleep, compress loop
- wake: @default_wake_generative
  - for i = 0 no trained recognition model yet, so call @multicoreEnumeration with uniform grammar
  - for i > 0, call recognition model @enumerateFrontiers to guess a grammar, then call @multicoreEnumeration with that grammar
  - different solver backends, eg. ocaml, python, pypy
  - (see inference below)
  - return frontier programs
- sleep: @sleep_recognition TODO
- compression @consolidate TODO

# Inference

- eg. @competeOnOneTask
- optionally init recognition model
- if init recognition model, call recognitionModel @enumerateFrontiers which guesses a grammar and then calls @multicoreEnumeration
- if solver == ocaml, dispatch to ocaml
- if solver == python call @enumerateForTasks
- call grammar @enumeration to do iterative deepening search
- store successful programs in an array of "frontiers"
