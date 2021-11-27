import numpy as np

import signal_tools as s
import plot_tools as p
from config import *


def baseband_transmission():
    # Generate random binary bit sequence as primitive data
    primitive_bit = s.raw_bit()
    # Polarize signal, means change 0/1 bit sequence into -1/+1 bit sequence
    polar_bit = s.polarize(primitive_bit)
    # Multiply bit sequence with sampling frequency(and signal period), convert them into signal array
    base_signal = s.cvt_2_signal(polar_bit, tb)
    # Add Gasses Noise of AWGN channel
    gasses_noise = s.awgn_noise(base_signal)
    receive_signal = base_signal + gasses_noise
    # Apply LPF to baseband signal
    base_filtered = s.lpf_ideal(receive_signal, rb)
    # Using correlation receiver to identify each bit
    base_vertex = s.correlation(base_filtered, True)
    # Sampling judgement for every bit
    receive_bit = s.judgement(base_vertex)
    # Calculate real BER
    ber = s.ber_calculate(primitive_bit, receive_bit)
    print('BER(SNR=', snr, '): ', ber, sep='')


def modulated_transmission(c_map=False, carrier_fre=fc, freq_shift=0.0):
    # Generate random binary bit sequence as primitive data
    primitive_bit = s.raw_bit()
    # Polarize signal, means change 0/1 bit sequence into -1/+1 bit sequence
    polar_bit = s.polarize(primitive_bit)
    # Split primitive signal into in-phase sequence and quadrature sequence
    # Odd sequence ->  In-phase sequence /// Even sequence -> Quadrature sequence
    i_bit, q_bit = s.orthogonal_decomposition(polar_bit)
    # Multiply bit sequence with sampling frequency(and signal period), convert them into signal array
    i_signal, q_signal = s.cvt_2_signal(i_bit, ts), s.cvt_2_signal(q_bit, ts)
    # Generate carrier signal
    cos_carrier, sin_carrier = s.get_carrier(carrier_fre)
    # Up conversion for both signal paths
    i_modulated, q_modulated = s.in_phase_modulate(i_signal, cos_carrier), s.quadrature_modulate(q_signal, sin_carrier)
    # Add them up, namely transmit signal
    transmit_signal = i_modulated + q_modulated
    # Add Gasses Noise of AWGN channel
    gasses_noise = s.awgn_noise(transmit_signal)
    receive_signal = transmit_signal + gasses_noise
    # Down conversion
    if freq_shift:
        cos_shift, sin_shift = s.get_carrier(fc * freq_shift)
        i_receive, q_receive = s.demodulate(receive_signal, cos_shift, sin_shift)
    else:
        i_receive, q_receive = s.demodulate(receive_signal, cos_carrier, sin_carrier)
    # Apply LPF to both signals
    """i_filtered, q_filtered = s.lpf_fir(i_receive), s.lpf_fir(q_receive)"""
    i_filtered, q_filtered = s.lpf_ideal(i_receive), s.lpf_ideal(q_receive)
    # Using correlation receiver to identify each symbol
    i_vertex, q_vertex = s.correlation(i_filtered), s.correlation(q_filtered)
    # Sampling judgement for every symbol
    i_judged, q_judged = s.judgement(i_vertex), s.judgement(q_vertex)
    # Fuse In-phase signal and Quadrature signal
    receive_bit = s.fuse(i_judged, q_judged)
    # Calculate real BER
    ber = s.ber_calculate(primitive_bit, receive_bit)
    print('BER(SNR=', snr, '): ', ber, sep='')
    ser = s.ser_calculate(s.orthogonal_decomposition(primitive_bit), [i_judged, q_judged])
    print('SER(SNR=', snr, '): ', ser, sep='')

    if c_map:
        p.qpsk_constellation_map(i_vertex, q_vertex)

    return ber


def modulated_rc_transmission():
    # Generate random binary bit sequence as primitive data
    primitive_bit = s.raw_bit()
    # Polarize signal, means change 0/1 bit sequence into -1/+1 bit sequence
    polar_bit = s.polarize(primitive_bit)
    # Split primitive signal into in-phase sequence and quadrature sequence
    # Odd sequence ->  In-phase sequence /// Even sequence -> Quadrature sequence
    i_bit, q_bit = s.orthogonal_decomposition(polar_bit)
    # Upsampling bit message into impulse signal sequences
    i_impulse, q_impulse = s.cvt_2_impulse(i_bit, ts), s.cvt_2_impulse(q_bit, ts)
    # Calculate the convolution of discrete message impulse sequence with RC signal
    i_signal, q_signal = s.shaping(i_impulse), s.shaping(q_impulse)
    # Generate carrier signal
    cos_carrier, sin_carrier = s.get_carrier(fc)
    # Up conversion for both signal paths
    i_modulated, q_modulated = s.in_phase_modulate(i_signal, cos_carrier), s.quadrature_modulate(q_signal, sin_carrier)
    # Add them up, namely transmit signal
    transmit_signal = i_modulated + q_modulated
    # Add Gasses Noise of AWGN channel
    gasses_noise = s.awgn_noise(transmit_signal)
    receive_signal = transmit_signal + gasses_noise
    # Down conversion
    i_receive, q_receive = s.demodulate(receive_signal, cos_carrier, sin_carrier)
    # Apply LPF to both signals
    """i_filtered, q_filtered = s.lpf_fir(i_receive), s.lpf_fir(q_receive)"""
    i_filtered, q_filtered = s.lpf_ideal(i_receive), s.lpf_ideal(q_receive)
    # Using correlation receiver to identify each symbol
    i_vertex, q_vertex = s.correlation(i_filtered), s.correlation(q_filtered)
    # Sampling judgement for every symbol
    i_judged, q_judged = s.judgement(i_vertex), s.judgement(q_vertex)
    # Fuse In-phase signal and Quadrature signal
    receive_bit = s.fuse(i_judged, q_judged)
    # Calculate real BER
    ber = s.ber_calculate(primitive_bit, receive_bit)
    print('BER(SNR=', snr, '): ', ber, sep='')
    ser = s.ser_calculate(s.orthogonal_decomposition(primitive_bit), [i_judged, q_judged])
    print('SER(SNR=', snr, '): ', ser, sep='')


if __name__ == '__main__':
    modulated_transmission(c_map=True, freq_shift=0.99999)
