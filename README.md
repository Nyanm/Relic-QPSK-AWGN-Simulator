# Relic-QPSK-AWGN-Simulator

QPSK modulation/demodulation simulator (in AWGN channel), based on SciPy and Matplotlib.

UESTC 2021春季 通信原理 邵士海,赵宏志班 课程实验 基于SciPy和Matplotlib的AWGN信道下的QPSK(BPSK)过程模拟器

原本这个实验是一个简单的，在MATLAB-Simulink上搭积木模拟QPSK过程的实验，但是出于对MATLAB这款软件以及这门语言的深仇大恨，决定在Python环境下从头开始搭建QPSK收发机、AWGN信道等工具。

最终实现了QPSK编码译码、载波调制解调、脉冲整形、低通滤波、误码率计算、星座图绘制等实验工具，又由这些实验工具搭建了基带传输、载波传输、RC整形传输三大功能。

config.py中可以自由调节如信噪比、载波频率等参数。

注释掉的大段代码是写报告时需要画图临时写的绿皮代码，不影响程序运行。

现在想一想应该用tensor加速，当时真的是一杯茶一包烟（并没有）一行代码跑一天。

MATLAB，不行；Python，彳亍！