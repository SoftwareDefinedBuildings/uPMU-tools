import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np
import datetime
import pytz

def plot_3phase_current_rawdata(fine1, fine2, fine3):
    formatter = FuncFormatter(formatter_time)

    ax1 = plt.subplot(313)
    ax1.set_ylabel('C1 (Amps)')
    plt.plot(*zip(*fine1))
    #plt.setp( ax1, xticklabels=[])

    ax2 = plt.subplot(312, sharex=ax1, sharey=ax1)
    ax2.set_ylabel('C2 (Amps)')
    plt.plot(*zip(*fine2))
    plt.setp( ax2.get_xticklabels(), visible=False)

    ax3 = plt.subplot(311, sharex=ax1, sharey=ax1)
    ax3.set_ylabel('C3 (Amps)')
    plt.plot(*zip(*fine3))
    plt.setp( ax3.get_xticklabels(), visible=False)

    plt.xlim(fine1[0][0], fine1[-1][0])
    plt.title('date : '+datetime.datetime.fromtimestamp(fine1[0][0]/1000000000, pytz.timezone('America/Los_Angeles')).strftime('%Y-%m-%d'))
    plt.tight_layout()
    plt.show()

def plot_3phase_voltage_rawdata(fine1, fine2, fine3, BVolt=1):
    formatter = FuncFormatter(formatter_time)

    ax1 = plt.subplot(313)
    ax1.set_ylabel('L1-E (p.u.)')
    ax1.xaxis.set_major_formatter(formatter)
    plt.plot(zip(*fine1)[0], [x/BVolt for x in zip(*fine1)[1]])
    #plt.setp( ax1, xticklabels=[])

    ax2 = plt.subplot(312, sharex=ax1, sharey=ax1)
    ax2.set_ylabel('L2-E (p.u.)')
    plt.plot(zip(*fine2)[0], [x/BVolt for x in zip(*fine2)[1]])
    plt.setp( ax2.get_xticklabels(), visible=False)

    ax3 = plt.subplot(311, sharex=ax1, sharey=ax1)
    ax3.set_ylabel('L3-E (p.u.)')
    plt.plot(zip(*fine3)[0], [x/BVolt for x in zip(*fine3)[1]])
    plt.setp( ax3.get_xticklabels(), visible=False)

    plt.xlim(fine1[0][0], fine1[-1][0])
    ax1.xaxis.set_ticks(np.arange(fine1[0][0],fine1[-1][0]+1,np.floor(fine1[-1][0]+1-fine1[0][0])/8))
    plt.title('date : '+datetime.datetime.fromtimestamp(fine1[0][0]/1000000000, pytz.timezone('America/Los_Angeles')).strftime('%Y-%m-%d'))
    plt.tight_layout()
    plt.show()

def plot_rawdata(fine):
    formatter = FuncFormatter(formatter_time)

    ax = plt.gca()
    ax.xaxis.set_major_formatter(formatter)
    ax.set_ylabel('Voltage')

    plt.plot(*zip(*fine))
    plt.xlim(fine[0][0], fine[-1][0])
    plt.xticks(np.arange(fine[0][0],fine[-1][0]+1,np.floor(fine[-1][0]+1-fine[0][0])/12), rotation=30)
    plt.title('date : '+datetime.datetime.fromtimestamp(fine[0][0]/1000000000, pytz.timezone('America/Los_Angeles')).strftime('%Y-%m-%d'))
    plt.show()

def visualize_tree_traversal(times,values,threshold):
    plt.plot(times,values, linestyle='-', color='k')
    plt.axhline(threshold, color="r")
    plt.xlim(times[0], times[-1])
    plt.ylim(ymax=1)
    if (max(times)-min(times))/1000000000 > 60*60*24:
        formatter = FuncFormatter(formatter_date)
        plt.title("decision variable")
    else:
        formatter = FuncFormatter(formatter_time)
        plt.title("decision variable - " + datetime.datetime.fromtimestamp(max(times)/1000000000,  pytz.timezone('America/Los_Angeles')).strftime('%Y-%m-%d'))
    plt.gca().xaxis.set_major_formatter(formatter)
    plt.xticks(np.arange(min(times),max(times)+1,np.floor(max(times)+1-min(times))/12), rotation=30)
    plt.show()

def formatter_date(t, pos):
    return datetime.datetime.fromtimestamp(t/1000000000,  pytz.timezone('America/Los_Angeles')).strftime('%Y-%m-%d')

def formatter_time(t, pos):
    return datetime.datetime.fromtimestamp(t/1000000000,  pytz.timezone('America/Los_Angeles')).strftime('%H:%M:%S')
