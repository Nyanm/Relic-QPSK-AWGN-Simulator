import numpy as np
# Overall frequency multiplicative factor: 1000 or 1k

# Recommended symbol rate: 1K Baud
rs = 1
ts = 1 / rs

# Recommended carrier frequency: 1M Hz
fc = 5
tc = 1 / fc

# Recommended roll-off facter: 0.2
alpha = 0.2

# Recommended upsampling times: 16
u_sample = 16

# Recommended filter order: 160
fir_order = 160
iir_order = 16

# Number of bits
length = 2000

# SNR
snr = 10
snr_liner = 10 ** (snr / 10.0)

# Bit rate in QPSK: 2 times of symbol rate
rb = 2 * rs
tb = 1 / rb

# Sampling frequency
f_sample = u_sample * fc
t_sample = 1 / f_sample

# Sampling sequence
sample_mark = np.arange(0, length * tb, t_sample)
bit_mark = sample_mark * 2
sample_num = len(sample_mark)
