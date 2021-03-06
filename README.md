# Lightning-Counter

A full-screen counter for moderating (lightning-)talks with fully automated
speaker overtime harrassment.

## Installation

    $ virtualenv-2.7 .
    $ bin/pip install -r requirements.txt

## Execution

The talk length is given as the first argument in seconds. For a talk of 5 minutes length, run:

    $ bin/python lighting.py 300

## Keyboard commands

*ESC* or *Q* - quit

*R* or *PAGEDOWN* - restart counter (paused)

*H* or *PAGEUP* - start harrassment

*SPACE* or *B* - toggle pause (silence harrassment music or start/stop counter)

The keys are compatible with typical remote controllers like Kensington #33374
## The counter

The counter starts in pause mode. It displays the remaining minutes and seconds
big and counts down. 

1 minute before the time is over the background will turn yellow.

30 seconds before the time is over the background will turn red.

## Automatic speaker harrassment

If a speaker goes over her time she will automatically be harrassed by playing a sound file (preferably some cheesy entertaining music like the Sesame Street Song) and displaying a picture instead of the counter (like unicorns pooping rainbows, the cookie monster, or a zombie).

Once the music starts playing you can press *R* to restart the counter or just *SPACE* to silence the audio but keep the picture.

You can place files in the following way in the data/ subdirectory:

    $ ls data/
    picture1.jpg    picture2.png    harrassment.wav

As the audio formats are a bit problematic getting AVbin installed for Pyglet I
decided to just rely on you providing an uncompress WAV file.

The images can be named any way, but the audio needs to be named 'harrassment.wav'.

If you have an audio file you need to convert, I recommend using sox for a simple conversion:

    $ sox myfile.mp3 data/harrassment.wav

If you want to start the output file at a certain second (to achieve best effect for the audience with a catchy point in the music) you can use trim:

    $ sox myfile.mp3 data/harrassment.wav trim 28
