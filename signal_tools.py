from scipy import signal as sg
from scipy import fft
from scipy.integrate import quad
import plot_tools as p
from config import *

# Constant
pi = np.math.pi
sqrt_2 = np.math.sqrt(2)

# Low pass filter
cutoff_fre = (rs / f_sample) * 2
# # Butterworth LPF (Invalid)
# butter_b, butter_a = sg.butter(iir_order, cutoff_fre)
# # Windowed FIR LPF
fir_b, fir_a = sg.firwin(fir_order, cutoff_fre), 1.0
# # Ellipse LPF (Invalid)
# ell_b, ell_a = sg.ellip(3, 10, 30, 0.000125, btype='lowpass')


"""
cos_indicator = []
for index in range(sample_num):
    cos_indicator.append(sqrt_2 * np.math.cos(2 * pi * rs * sample_mark[index]))


rc_fre_half = np.zeros(sample_num)
band_1 = int((1 - alpha) * (length / 2))
band_2 = int((1 + alpha) * (length / 2))
for index in range(band_1):
    rc_fre_half[index] = (1 / rs)
for index in range(band_1, band_2 + 1):
    fre_cur = index / length
    rcf_cos = np.cos((pi * (fre_cur - (1 - alpha) * 0.5 * rs)) / (rs * alpha))
    rc_fre_half[index] = (1 / (2 * rs)) * (1 + rcf_cos)
rc_fre = rc_fre_half + rc_fre_half[::-1]

rc_impulse = fft.ifft(rc_fre)
"""


def cvt_2_signal(digital, period):
    sig = []
    for bit in digital:
        sig += [bit] * int(f_sample * period)
    return np.array(sig)


def cvt_2_impulse(digital, period):
    sig = []
    for bit in digital:
        sig += [bit]
        sig += [0] * int(f_sample * period - 1)
    return np.array(sig)


def polarize(bit_arr_01):
    return np.array(bit_arr_01) * 2 - 1


def raw_bit():
    bit_array = np.random.randint(0, 2, length)
    return bit_array


def orthogonal_decomposition(raw_bit_array):
    i_bit = raw_bit_array[:length - 1:2]
    q_bit = raw_bit_array[1:length:2]
    return i_bit, q_bit


def shaping(impulse_seq):
    rc_impulse_half = []
    for __index in sample_mark:
        rc_dividend = np.sin(pi * rs * __index) * np.cos(pi * alpha * rs * __index)
        rc_divisor = (1 - (2 * alpha * rs * __index) ** 2) * (pi * rs * __index)
        if rc_divisor == 0:
            rc_impulse_half.append(0)
            continue
        rc_impulse_half.append(rc_dividend / rc_divisor)
    rc_impulse_half.pop(0)
    rc_impulse = np.array(rc_impulse_half[::-1] + [1] + rc_impulse_half)

    shaped_sig = sg.convolve(impulse_seq, rc_impulse)
    return shaped_sig[sample_num - 1 - f_sample // 2: -(sample_num - 1 + f_sample // 2)]


def get_carrier(freq):
    cos_carrier = []
    for cos in range(sample_num):
        cos_carrier.append(sqrt_2 * np.math.cos(2 * pi * freq * (sample_mark[cos] + 0.25 * pi)))

    sin_carrier = []
    for sin in range(sample_num):
        sin_carrier.append(sqrt_2 * np.math.sin(2 * pi * freq * (sample_mark[sin] + 0.25 * pi)))

    return np.array(cos_carrier), np.array(sin_carrier)


def in_phase_modulate(i_signal, cos_carrier):
    return np.array(i_signal) * cos_carrier


def quadrature_modulate(q_signal, sin_carrier):
    return np.array(q_signal) * sin_carrier


def demodulate(r_signal, cos_carrier, sin_carrier):
    i_demodulate = r_signal * cos_carrier
    q_demodulate = r_signal * sin_carrier
    return np.array(i_demodulate), np.array(q_demodulate)


def awgn_noise(signal):
    s_power = sum(signal ** 2) / len(signal)
    band_n_power = s_power / snr_liner
    n_power = band_n_power * (f_sample / rb)
    return np.random.randn(len(signal)) * np.sqrt(n_power)


"""
def lpf_butter(signal):
    return sg.filtfilt(butter_b, butter_a, signal)"""


def lpf_fir(signal):
    signal_elongated = np.append(signal, np.zeros(int(fir_order / 2)))
    return sg.lfilter(fir_b, fir_a, signal_elongated)[int(fir_order / 2):]


"""
def lpf_ellipse(signal):
    return sg.filtfilt(ell_b, ell_a, signal)"""


def lpf_ideal(signal, bandwidth=rs):
    spec = fft.fft(signal)
    baseband_length = int((bandwidth / f_sample) * sample_num)
    spec[baseband_length + 1: sample_num - baseband_length] *= 0.001
    return np.real(np.fft.ifft(spec))


def correlation(signal, is_baseband=False):
    vertex_arr = []
    if is_baseband:
        sam_step = int(tb / t_sample)
    else:
        sam_step = int(ts / t_sample)
    separated_signal = [signal[sym_index:sym_index + sam_step] for sym_index in range(0, len(signal), sam_step)]
    for signal_symbol in separated_signal:
        vertex_arr.append(np.average(signal_symbol))
    return vertex_arr


def judgement(vertex_arr):
    judged = []
    for vertex in vertex_arr:
        if vertex >= 0:
            judged.append(1)
        else:
            judged.append(0)
    return judged


def fuse(i_bit, q_bit):
    fused = []
    for bit in range(len(i_bit)):
        fused.append(i_bit[bit])
        fused.append(q_bit[bit])
    return np.array(fused)


def ber_calculate(pri_bit, fin_bit):
    ber = np.average(pri_bit ^ fin_bit)
    if ber > 0.5:
        return 0.5
    return ber


def ser_calculate(pri_onto, fin_onto):
    ser = np.average((pri_onto[0] ^ fin_onto[0]) | (pri_onto[1] ^ fin_onto[1]))
    if ser > 0.5:
        return 0.5
    return ser


def filter_attribute(f_type):
    if f_type == 'butter':
        # f_b, f_a = butter_b, butter_a
        return
    elif f_type == 'fir':
        f_b, f_a = fir_b, fir_a
    elif f_type == 'ellipse':
        # f_b, f_a = ell_b, ell_a
        return
    else:
        print('Invalid filter name.')
        return
    fw, fh = sg.freqz(f_b, f_a)
    fw = (fw / pi) * f_sample
    fh = 20 * np.log10(abs(fh))
    p.filter_response(fw, fh)


def signal_spectrum(signal, resize_time=0):
    sig_length = len(signal)
    fy = (np.abs(fft.fft(signal)) / (sig_length * sqrt_2))[:sig_length // 2]
    fx = fft.fftfreq(sig_length, t_sample)[:sig_length // 2]
    if resize_time:
        p.quick_spectrum(fy, fx, resize_time)
    else:
        p.quick_spectrum(fy, fx)


def get_q_function(x):
    def integrand(t):
        return (1 / (np.sqrt(2 * pi))) * (np.e ** (-0.5 * (t ** 2)))

    return quad(integrand, x, np.Inf)[0]


"""
def get_5_spectrum(s1, s2, s3, s4, s5, n1, n2, n3, n4, n5):
    sig_length = len(s1)
    fx = fft.fftfreq(sig_length, t_sample)[:sig_length // 2]
    fy1 = (np.abs(fft.fft(s1)) / (sig_length * sqrt_2))[:sig_length // 2]
    fy2 = (np.abs(fft.fft(s2)) / (sig_length * sqrt_2))[:sig_length // 2]
    fy3 = (np.abs(fft.fft(s3)) / (sig_length * sqrt_2))[:sig_length // 2]
    fy4 = (np.abs(fft.fft(s4)) / (sig_length * sqrt_2))[:sig_length // 2]
    fy5 = (np.abs(fft.fft(s5)) / (sig_length * sqrt_2))[:sig_length // 2]
    p.spectrum_plot_5(fy1, fy2, fy3, fy4, fy5, n1, n2, n3, n4, n5, fx)


def get_3_spectrum(s1, s2, s3, n1, n2, n3):
    sig_length = len(s1)
    fx = fft.fftfreq(sig_length, t_sample)[:sig_length // 2]
    fy1 = (np.abs(fft.fft(s1)) / (sig_length * sqrt_2))[:sig_length // 2]
    fy2 = (np.abs(fft.fft(s2)) / (sig_length * sqrt_2))[:sig_length // 2]
    fy3 = (np.abs(fft.fft(s3)) / (sig_length * sqrt_2))[:sig_length // 2]
    p.spectrum_plot_3(fy1, fy2, fy3, n1, n2, n3, fx)

time_base = []
data = []
for index in range(-4, 25):
    x = index / 2
    x_liner = 10 ** (x / 10.0)
    time_base.append(x)
    data.append(get_q_function(np.sqrt(x_liner)))
print(time_base, data)
"""
