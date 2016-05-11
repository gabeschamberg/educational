# Packages for filtering
from scipy.signal import butter, lfilter

def lowpass(data,fs,cutoff,order=5):
    # The nyquist frequency is half of the sampling freq.
    nyq = 0.5 * fs
    # Find the cutoff frequency in digital domain
    low = cutoff / nyq
    # Get the filter coefficients
    b, a = butter(order, low, btype='low')
    # Apply the filter in time domain (Convolution)
    filtered_data = lfilter(b,a,data)
    return filtered_data

def highpass(data,fs,cutoff,order=5):
    nyq = 0.5 * fs
    high = cutoff / nyq
    b, a = butter(order, high, btype='high')
    filtered_data = lfilter(b,a,data)
    return filtered_data