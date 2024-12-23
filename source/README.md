# Building Your Challenge

Steps to "reproduce'':

- Take key and convert to hex (one character 0x<HEX><HEX>)
- The number of characters = number of bars in the song
- A song was created with 25 bars (key is 25 characters long)
- Each bar of 4/4 is split into 16 16th notes. The first 8 notes represent the first hex value, and the second 8 notes represent the second hex value.
- The first four notes of each 8 are ignored (since hex is 4 bits)
- The bass pedal is the instrument encoding this pattern. All others, like snare, hi-hat, and 808 are there to cause confusion and enforce frequency-based analysis as opposed to decibel checking.

**Thus each bar is**

`| rest rest rest rest <pedal?> <pedal?> <pedal?> <pedal?> rest rest rest rest <pedal?> <pedal?> <pedal?> <pedal?> |`
      
**For example, in bar 5**

`| rest rest rest rest <pedal> <no pedal> <no pedal> <pedal>  rest rest rest rest <no pedal> <no pedal> <no pedal> <pedal> |`

This yields chr(0x91), the fifth character in the key. The concatenation of all 25 yields the key.

This song was built in guitar pro, exported as MIDI, brought into Ableton (DAW), and an 808 was added for additional confusion.
