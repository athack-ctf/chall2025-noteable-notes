# How to Solve the Challenge?

- Install requirements
- Run code. Make sure the path to the .wav file is correct

What the participants will have to do.
1. Find out the song's BPM
2. Split the song into 16th note segments, accordingly
3. Perform FFT over each segment
4. Filter out frequencies above 100Hz, leaving the bass pedal lows
5. Convert the FFT segment to db (relative to the maximum amplitude of the track, thus DB values are all negative)
6. If any db value is above threshold (say -6dB), then pedal is present.
7. Tracking the pedals over time yields a series of hex values that produce the key (see the [source/README.md](../source/README.md) for details)

They can, of course, bring the .wav into a DAW or software with 16th note divisions and mark the pedals by hand, however without the programmatic technique, it will be difficult for them to A) try different note lengths to realize the 16th note pattern, b) test different combinations and spacings.
