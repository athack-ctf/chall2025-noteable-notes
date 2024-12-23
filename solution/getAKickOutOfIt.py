import librosa
import numpy as np

def split_audio_into_16th_notes(audio_file, bpm):
  """
  Splits an audio file into 16th notes based on the given BPM.

  Args:
    audio_file: Path to the audio file (e.g., 'audio.mp3').
    bpm: Beats per minute.

  Returns:
    A list of 16th note audio segments.
  """

  y, sr = librosa.load(audio_file)  # Load audio file
  
  # Calculate the duration of a 16th note in seconds
  seconds_per_beat = 60 / bpm
  seconds_per_16th_note = seconds_per_beat / 4

  # Calculate the number of samples per 16th note
  samples_per_16th_note = int(sr * seconds_per_16th_note)

  # Split audio into 16th note segments
  num_segments = int(len(y) / samples_per_16th_note)
  segments = np.array_split(y, num_segments)

  return segments, np.max(np.abs(librosa.stft(y)))

def detect_low_frequency_activity(segment, sample_rate, max_amplitude, threshold_db=-6, freq_range=(0, 60)):
  """
  Detects if the segment contains any signal above the threshold in the specified frequency range.

  Args:
    segment: Audio segment (numpy array).
    sample_rate: Sample rate of the audio.
    threshold_db: Threshold in decibels.
    freq_range: Tuple defining the lower and upper bounds of the frequency range.

  Returns:
    True if any signal above the threshold is found in the specified frequency range, False otherwise.
  """   
  # FFT over a sample segment of a 16th note
  D = librosa.stft(segment)

  # Compute the db of each frequency range produced in FFT
  S_db = librosa.amplitude_to_db(np.abs(D), ref=max_amplitude)
  
  # Returns a list of frequencies that represent each row of D
  freqs = librosa.fft_frequencies(sr=sample_rate, n_fft=2048)

  # Get the frequency indices between 0 and 100 Hz (where the bass pedal is present) 
  low_freq_idx = (freqs >= 0) & (freqs <= 100) 

  # Get the DB values within those frequencies
  S_db_low_freq = S_db[low_freq_idx, :] 

  # If any DB level goes above the threshold, we found a pedal note!
  for a in S_db_low_freq:
    if np.any(a >= threshold_db):
      return True
    
  return False

def analyze_audio(audio_file, bpm):
  """
  Analyzes the audio file for low-frequency activity in each 16th note.

  Args:
    audio_file: Path to the audio file.
    bpm: Beats per minute.

  Prints the results to the console.
  """

  segments, max_amp = split_audio_into_16th_notes(audio_file, bpm)

  sr = librosa.get_samplerate(audio_file)

  # [bar #, hex value from first 8 16th notes, hex valur from next 8 16th notes]
  # Note... the first four notes of each 8 never have as pedal since hex is 4 bits.
  # Thus each bar is:
  #  | rest rest rest rest <pedal?> <pedal?> <pedal?> <pedal?> rest rest rest rest <pedal?> <pedal?> <pedal?> <pedal?> |
  #  EX: bar 5 => | rest rest rest rest <pedal> <no pedal> <no pedal> <pedal>  rest rest rest rest <no pedal> <no pedal> <no pedal> <pedal> |
  # yiels [5, 0x9, 0x1]. This yields chr(0x91), one character in the key.
  bar_info = [1, 0x0, 0x0]
  key = []
  for i, segment in enumerate(segments):
    bar_number = (i // 16) + 1  # Calculate bar number (assuming 4 beats per bar)

    # We're at the next bar!
    if bar_number != bar_info[0]:
      key.append(chr((bar_info[1] << 4) | (bar_info[2])))
      bar_info = [bar_number, 0x0, 0x0]

    # Calculate position of note in bar
    sixteenth_note_in_bar = (i % 16) + 1

    if detect_low_frequency_activity(segment, sr, max_amp):
      if sixteenth_note_in_bar <= 8:
        bar_info[1] = (1 << 8 - sixteenth_note_in_bar) | bar_info[1]
      if sixteenth_note_in_bar > 8:
        bar_info[2] = (1 << 16 - sixteenth_note_in_bar) | bar_info[2]
      print(f"\tBass pedal activity detected in Bar {bar_number}, 16th note {sixteenth_note_in_bar}")
    
  key.append(chr((bar_info[1] << 4) | (bar_info[2])))
  print("KEY:", "".join(key))  

# Example Usage
audio_file = 'DRUM_CHALLENGE_REV1.wav' 
bpm = 120  # Example BPM

analyze_audio(audio_file, bpm)