import librosa
import librosa.display
import numpy as np
import soundfile as sf
from scipy import signal
from numba import jit

@jit(nopython=True)
def getChunkOfAudio(y, sr, tempo, bar, duration, fromEnd=False):
    duration_to_filter = 4 * duration * 60 / tempo
    barTime = 4 * bar * 60 / tempo

    duration_to_filter_samples = int(duration_to_filter * sr)
    barTime_samples = int(barTime * sr)

    if fromEnd:
        return y[:, y.shape[1] -barTime_samples - duration_to_filter_samples : y.shape[1] - barTime_samples]
    else:
        return y[:, barTime_samples : barTime_samples + duration_to_filter_samples]
    
def butter_highpass(cutoff, fs, order=5, type = "high"):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype=type, analog=False)
    return b, a

def butter_highpass_filter(data, cutoff, fs, order=5, type = "high"):
    b, a = butter_highpass(cutoff, fs, order=order, type = type)
    y = signal.filtfilt(b, a, data)
    return y


def main(file_path, tempo, start = True):
    print("Starting")

    # Load the audio file
    y, sr = librosa.load(file_path, sr=None, mono=False)
    print(sr)

    # Define the duration of the first 15 seconds
    duration_to_filter = 16*60/tempo  # seconds

    # Calculate the number of samples corresponding to the first 15 seconds
    samples_to_filter = int(duration_to_filter * sr)

    # Apply a high-pass filter to the first 15 seconds of each channel
    if start:
        y_filtered = np.array([librosa.effects.hpss(y[channel][:samples_to_filter])[0] for channel in range(y.shape[0])])

    else:
        y_filtered = np.array([librosa.effects.hpss(y[channel][y.shape[1] - samples_to_filter:])[0] for channel in range(y.shape[0])])

    # Concatenate the filtered audio with the rest of the original audio for each channel
    y_combined = np.concatenate((y_filtered, y[:, samples_to_filter:]), axis=1)

    # Save the combined audio
    filtered_file_path = 'filtered_audio.wav'
    sf.write(filtered_file_path, y_combined.T, sr, 'PCM_24')  # Transpose to make channels the first dimension

    print(f"Filtered audio saved as {filtered_file_path}")


def applyFilter(y, sr):
    return np.array([librosa.effects.hpss(y[channel])[0] for channel in range(y.shape[0])])

@jit(nopython=True)
def mix_audio_files2(y1, y2, exponent=5, exponent2=1):
    len_y1 = y1.shape[1]
    len_y2 = y2.shape[1]
    shorter_length = min(len_y1, len_y2)

    y1_cut = y1[:, :shorter_length]
    y2_cut = y2[:, :shorter_length]

    ratios = np.linspace(0, 1, shorter_length) ** exponent
    ratios = (1 - ratios ** exponent2, ratios)

    mixed_audio = y1_cut * ratios[0] + y2_cut * ratios[1]
    
    return mixed_audio


@jit(nopython=True)
def mix_audio_files(y1, y2, exponent=5, exponent2 = 1):

    len_y1 = y1.shape[1]
    len_y2 = y2.shape[1]

    if len_y1 < len_y2:
        shorter_length = len_y1
    else:
        shorter_length = len_y2

    y1_cut = y1[:, :shorter_length]
    y2_cut = y2[:, :shorter_length]

    mixed_audio = np.zeros_like(y1_cut)

    for i in range(shorter_length):
        ratio = min([1, (i / shorter_length) ** exponent])
        mixed_audio[:, i] = y1_cut[:, i] * (1 - ratio**exponent2) + y2_cut[:, i] * ratio

    return mixed_audio


@jit(nopython=True)
def custom_mix_audio(y1, y2):
    # Determine the length of the shorter track
    len_y1 = y1.shape[1]
    len_y2 = y2.shape[1]
    shorter_length = min(len_y1, len_y2)

    # Cut both audio files to the same length
    y1_cut = y1[:, :shorter_length]
    y2_cut = y2[:, :shorter_length]

    # Divide the track into segments
    first_half = shorter_length // 2
    middle_quarter = shorter_length // 4
    last_quarter = shorter_length - first_half - middle_quarter

    # Initialize the mixing ratios
    ratios1 = np.ones(shorter_length)
    ratios2 = np.zeros(shorter_length)

    # First half: fade-in secondary track
    ratios2[:first_half] = np.linspace(0, 1, first_half)

    # Middle quarter: both at full volume
    ratios1[first_half:first_half + middle_quarter] = 1
    ratios2[first_half:first_half + middle_quarter] = 1

    # Last quarter: fade-out primary track
    ratios1[first_half + middle_quarter:] = np.linspace(1, 0, last_quarter) ** 0.25
    ratios2[first_half + middle_quarter:] = 1

    totalRatios = ratios1 + ratios2

    # Apply the ratios to the audio
    mixed_audio = y1_cut * ratios1 + y2_cut * ratios2

    # Normalize to the -1,1 range
    max_amplitude = np.max(np.abs(mixed_audio))
    mixed_audio = np.clip(mixed_audio, -0.8, 0.8)

    return mixed_audio



def gradual_stretch_audio(y, tempo_ratio1, tempo_ratio2, num_segments=16):
    # Ensure y is a two-dimensional array
    if y.ndim != 2:
        raise ValueError("Input audio must be two-dimensional")

    # Calculate the length of each segment
    segment_length = y.shape[1] // num_segments
    
    # Initialize list to store segments
    stretched_segments = []

    # Interpolate the audio array for each channel for each segment
    for i in range(num_segments):
        # Calculate the start and end indices for this segment
        start_idx = i * segment_length
        end_idx = (i + 1) * segment_length if i < num_segments - 1 else y.shape[1]
        
        # Calculate the current tempo ratio for this segment
        current_tempo_ratio = tempo_ratio1 + (tempo_ratio2 - tempo_ratio1) * (i / (num_segments - 1))
        
        # Calculate the new length after stretching for this segment
        new_length = int((end_idx - start_idx) * current_tempo_ratio)
        
        # Create the new time indices for this segment
        new_time_indices = np.linspace(start_idx, end_idx - 1, new_length)
        
        # Interpolate the audio array for each channel for this segment
        stretched_segment = np.zeros((y.shape[0], new_length))
        for j in range(y.shape[0]):
            stretched_segment[j] = np.interp(new_time_indices,
                                              np.arange(start_idx, end_idx),
                                              y[j, start_idx:end_idx])
        
        # Append the stretched segment to the list
        stretched_segments.append(stretched_segment)
    
    # Concatenate all segments to form the stretched audio
    stretched_audio = np.concatenate(stretched_segments, axis=1)
    
    return stretched_audio
# Example usage:
# y is your input audio array
# tempo_ratio1 and tempo_ratio2 are the stretch factors for the two segments
# stretched_audio = gradual_stretch_audio(y, tempo_ratio1, tempo_ratio2)


def stretch_audio(y, stretch_factor):
    # Ensure y is a two-dimensional array
    if y.ndim != 2:
        raise ValueError("Input audio must be two-dimensional")

    # Calculate the new length after stretching
    new_length = int(y.shape[1] * stretch_factor)
    
    # Create the new time indices
    new_time_indices = np.linspace(0, y.shape[1] - 1, new_length)
    
    # Interpolate the audio array for each channel
    stretched_audio = np.zeros((y.shape[0], new_length))
    for i in range(y.shape[0]):
        stretched_audio[i] = np.interp(new_time_indices, np.arange(y.shape[1]), y[i])
    
    return stretched_audio

def time_stretch_without_pitch_change(y, sr, stretch_factor):
    # Perform time stretching using the phase vocoder algorithm
    y_stretched = librosa.effects.time_stretch(y, rate=stretch_factor)

    # Resample the stretched audio to match the original sampling rate
    #y_stretched_resampled = librosa.resample(y_stretched, orig_sr=int(sr*stretch_factor), target_sr=sr)

    return y_stretched