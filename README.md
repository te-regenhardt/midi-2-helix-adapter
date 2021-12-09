# midi-2-helix-adapter
A software adapter to translate MIDI keyboard notes to a format that can be accepted from the Line6 Helix 3-Note-Generator as input.

## Connect your MIDI keyboard to the Helix Floor / LT / Rack / HX Stomp (XL) / HX Effects

Considering the versatile guitar effects and amp modeling devices from the Line 6 Helix family, two facts are quite apparent:

* The Line 6 Helix Family has a build in synthesizer/oscillators.
* The Helix devices can receive MIDI input.

The problem in this constellation is:
* The synths are not controllable by MIDI note values, so keyboards are not able to control them!

This adapter script connects MIDI keyboards (and the NOTE ON and NOTE OFF signals send by them) to the Helix's built-in oscillator.


### The oscillator situation:
Taking a look at the *3 Note Generator* (3NG) block in the Helix, the behaviour and controllability are as follows:
* The 3NG can be switched on as a whole, or be bypassed.
* The 3NG can be switched via a CC control change message
    * Control Change with value 0 switches the 3NG off.
    * Control Change with value 127 switches the 3NG on.
* Every parameter of the 3NG can be controlled with a CC command each. For each of the 3 oscillators of one 3NG-block the possibilities are:
    * Oscillator shape (Saw Up, Saw Down, Square, Sine, Triangle)
    * Oscillator note (C, C#, ..., A#, B)
    * Oscillator octave (0 to 8)
    * Oscillator glide (time to glide from one note value to another)
    * Oscillator volume
* None of the five parameters above are mapped as MIDI notes 1:1 are (0 to 127) except for volume and glide.


### The (usual) MIDI keyboard situation:

### How the adapter fixes this (in a way)

## How to use the adapter

### Dependencies

### The functions and their parameters

### Ports

### Stopping the adapter

### Known bugs


## Run the adapter on your computer

## Run the adapter on a rasperry pi (and possibly headless)

