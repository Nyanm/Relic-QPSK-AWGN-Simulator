import matplotlib.pyplot as plt
from config import *


def quick_signal_plot(signal, time_base=sample_mark):
    plt.figure(figsize=(12, 8))
    plt.plot(time_base, signal)
    plt.xlabel('Symbol n')
    plt.ylabel('Signal Amplitude V')
    plt.grid()
    plt.show()


def rc_shaping_plot(signal, bit_seq, time_base=sample_mark):
    plt.figure(figsize=(12, 8))
    plt.plot(time_base, signal)
    for index in range(len(bit_seq)):
        plt.scatter(index + 0.5, bit_seq[index], marker='x', color='black')
        plt.plot([index + 0.5, index + 0.5], [0, bit_seq[index]], color='black', linestyle='--')
    plt.xlabel('Symbol n')
    plt.ylabel('Signal Amplitude V')
    plt.grid()
    plt.show()


def phase_check(i_cos, q_sin, addition, timebase=sample_mark):
    plt.figure(figsize=(12, 10))
    plt.subplot(3, 1, 1)
    plt.plot(timebase, i_cos)
    plt.title('Modulated In-phase Signal')
    plt.subplot(3, 1, 2)
    plt.plot(timebase, q_sin)
    plt.title('Modulated Quadrature Signal')
    plt.subplot(3, 1, 3)
    plt.plot(timebase, addition)
    plt.title('Transmission Signal')
    plt.show()


def qpsk_constellation_map(i_vertex, q_vertex):
    plt.figure(figsize=(10, 10))
    plt.title('QPSK Constellation Map', fontsize=15)
    plt.xlabel('In-phase Vertex')
    plt.ylabel('Quadrature Vertex')
    plt.axis([-2, 2, -2, 2])
    plt.plot([-2, 2], [0, 0], linestyle='--', color='dimgrey', linewidth=3)
    plt.plot([0, 0], [-2, 2], linestyle='--', color='dimgrey', linewidth=3)
    plt.annotate('', xy=(1.73, 1.73), xytext=(-1.73, -1.73), arrowprops=dict(arrowstyle="->", connectionstyle="arc3"))
    plt.annotate('', xy=(-1.73, 1.73), xytext=(1.73, -1.73), arrowprops=dict(arrowstyle="->", connectionstyle="arc3"))
    for index in range(len(i_vertex)):
        plt.scatter(i_vertex[index], q_vertex[index], s=50)
    plt.scatter(1, 1, s=200, marker='+', c='r', linewidths=2)
    plt.scatter(-1, 1, s=200, marker='+', c='r', linewidths=2)
    plt.scatter(1, -1, s=200, marker='+', c='r', linewidths=2)
    plt.scatter(-1, -1, s=200, marker='+', c='r', linewidths=2)
    plt.show()


def filter_response(fw, fh):
    plt.figure(figsize=(14, 10))
    plt.plot(fw, fh)
    plt.xlabel('Frequency kHz')
    plt.ylabel('Amplitude dB')
    plt.grid()
    plt.show()


def quick_spectrum(fy, fx, resize_time=0):
    plt.figure(figsize=(14, 10))
    plt.plot(fx, fy)
    if resize_time:
        plt.xlim((0, resize_time * fc))
    plt.xlabel('Frequency (B:kHz)')
    plt.ylabel('Amplitude (W)')
    plt.grid()
    plt.show()


"""
def signal_plot_5(s1, s2, s3, s4, s5, n1, n2, n3, n4, n5, timebase=sample_mark):
    plt.figure(figsize=(12, 24))
    plt.subplots_adjust(left=0.07, bottom=0.03, right=0.93, top=0.97)

    plt.subplot(5, 1, 1)
    plt.plot(timebase, s1)
    plt.grid()
    plt.xlabel('Symbol n')
    plt.ylabel('Signal Amplitude V')
    plt.title(n1)

    plt.subplot(5, 1, 2)
    plt.plot(timebase, s2)
    plt.grid()
    plt.xlabel('Symbol n')
    plt.ylabel('Signal Amplitude V')
    plt.title(n2)

    plt.subplot(5, 1, 3)
    plt.plot(timebase, s3)
    plt.grid()
    plt.xlabel('Symbol n')
    plt.ylabel('Signal Amplitude V')
    plt.title(n3)

    plt.subplot(5, 1, 4)
    plt.plot(timebase, s4)
    plt.grid()
    plt.xlabel('Symbol n')
    plt.ylabel('Signal Amplitude V')
    plt.title(n4)

    plt.subplot(5, 1, 5)
    plt.plot(timebase, s5)
    plt.grid()
    plt.xlabel('Symbol n')
    plt.ylabel('Signal Amplitude V')
    plt.title(n5)
    plt.show()


def spectrum_plot_5(s1, s2, s3, s4, s5, n1, n2, n3, n4, n5, timebase):
    plt.figure(figsize=(12, 24))
    plt.subplots_adjust(left=0.07, bottom=0.03, right=0.93, top=0.97)

    plt.subplot(5, 1, 1)
    plt.plot(timebase, s1)
    plt.xlim((0, 4 * fc))
    plt.grid()
    plt.xlabel('Frequency kHz')
    plt.ylabel('Amplitude (W)')
    plt.title(n1)

    plt.subplot(5, 1, 2)
    plt.plot(timebase, s2)
    plt.xlim((0, 4 * fc))
    plt.grid()
    plt.xlabel('Frequency kHz')
    plt.ylabel('Amplitude (W)')
    plt.title(n2)

    plt.subplot(5, 1, 3)
    plt.plot(timebase, s3)
    plt.xlim((0, 4 * fc))
    plt.grid()
    plt.xlabel('Frequency kHz')
    plt.ylabel('Amplitude (W)')
    plt.title(n3)

    plt.subplot(5, 1, 4)
    plt.plot(timebase, s4)
    plt.xlim((0, 4 * fc))
    plt.xlabel('Frequency kHz')
    plt.ylabel('Amplitude (W)')
    plt.grid()
    plt.title(n4)

    plt.subplot(5, 1, 5)
    plt.plot(timebase, s5)
    plt.xlim((0, 4 * fc))
    plt.grid()
    plt.xlabel('Frequency kHz')
    plt.ylabel('Amplitude (W)')
    plt.title(n5)
    plt.show()


def signal_plot_3(s1, s2, s3, n1, n2, n3, bit_seq, timebase=sample_mark):
    plt.figure(figsize=(12, 16))
    plt.subplots_adjust(left=0.07, bottom=0.06, right=0.93, top=0.94)
    plt.subplot(3, 1, 1)
    plt.plot(timebase, s1)
    plt.grid()
    plt.xlabel('Symbol n')
    plt.ylabel('Signal Amplitude V')
    plt.title(n1)
    plt.subplot(3, 1, 2)
    plt.plot(timebase, s2)
    for index in range(len(bit_seq)):
        plt.scatter(index + 0.5, bit_seq[index], marker='x', color='black')
        plt.plot([index + 0.5, index + 0.5], [0, bit_seq[index]], color='black', linestyle='--')
    plt.grid()
    plt.xlabel('Symbol n')
    plt.ylabel('Signal Amplitude V')
    plt.title(n2)
    plt.subplot(3, 1, 3)
    plt.plot(timebase, s3)
    plt.grid()
    plt.xlabel('Symbol n')
    plt.ylabel('Signal Amplitude V')
    plt.title(n3)

    plt.show()


def spectrum_plot_3(s1, s2, s3, n1, n2, n3, timebase):
    plt.figure(figsize=(12, 16))
    plt.subplots_adjust(left=0.07, bottom=0.06, right=0.93, top=0.94)

    plt.subplot(3, 1, 1)
    plt.plot(timebase, s1)
    plt.xlim((0, 4 * fc))
    plt.grid()
    plt.xlabel('Frequency kHz')
    plt.ylabel('Amplitude (W)')
    plt.title(n1)

    plt.subplot(3, 1, 2)
    plt.plot(timebase, s2)
    plt.xlim((0, 4 * fc))
    plt.grid()
    plt.xlabel('Frequency kHz')
    plt.ylabel('Amplitude (W)')
    plt.title(n2)

    plt.subplot(3, 1, 3)
    plt.plot(timebase, s3)
    plt.xlim((0, 4 * fc))
    plt.grid()
    plt.xlabel('Frequency kHz')
    plt.ylabel('Amplitude (W)')
    plt.title(n3)

    plt.show()


def ber_graph():
    plt.figure(figsize=(8, 8))
    plt.yscale('log')
    the_x = [-2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5,
             8.0, 8.5, 9.0, 9.5, 10.0, 10.5, 11.0, 11.5, 12.0]
    the_y = [0.2135021855040062, 0.20006329518300173, 0.1863972813913738, 0.17256927028429592, 0.15865525393145707,
             0.14474212166788783, 0.1309272967555245, 0.11731780139111983, 0.10402863708538865, 0.09118037349115202,
             0.07889587198172439, 0.06729612795479283, 0.056495301749361675, 0.046595122631295637, 0.03767898814746339,
             0.029806228538614622, 0.023007138877862744, 0.017279466061438695, 0.01258703312214377,
             0.008861051096347517, 0.006004386400163446, 0.0038986298895198903, 0.00241331041963386,
             0.0014161190721791292, 0.0007827011290012757, 0.0004045622434670238, 0.0001939854720258317,
             8.55105465882245e-05, 3.430262386310578e-05]

    rea_x = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0]
    rea_y = [0.17109, 0.15901, 0.14509, 0.12929, 0.11648,
             0.10366,
             0.09186,
             0.07824,
             0.06866,
             0.05777,
             0.04657,
             0.03764,
             0.03039,
             0.02379, 0.01825, 0.01345, 0.00961, 0.00594, 0.00413, 0.00266, 0.00158]
    l1, = plt.plot(the_x, the_y)
    l2, = plt.plot(rea_x, rea_y)

    plt.xlabel('SNR(Es/N0) dB')
    plt.ylabel('BER')
    plt.title('QPSK BER Curve')
    plt.xlim((-2, 12))
    plt.subplots_adjust(left=0.1, bottom=0.06, right=0.95, top=0.96)
    plt.legend(handles=[l1, l2], labels=['Theoretical value', 'Actual value'], loc='upper right')

    plt.grid()
    plt.show()
"""
