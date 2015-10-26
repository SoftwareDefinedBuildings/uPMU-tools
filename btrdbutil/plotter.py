import matplotlib.pyplot as plt
import datetime
import pytz

def plot_3phase_current_rawdata(fine1, fine2, fine3):
    ax1 = plt.subplot(313)
    ax1.set_ylabel('C1 (Amps)')
    plt.plot(*zip(*fine1))
    plt.setp( ax1, xticklabels=[])

    ax2 = plt.subplot(312, sharex=ax1, sharey=ax1)
    ax2.set_ylabel('C2 (Amps)')
    plt.plot(*zip(*fine2))
    plt.setp( ax2.get_xticklabels(), visible=False)

    ax3 = plt.subplot(311, sharex=ax1, sharey=ax1)
    ax3.set_ylabel('C3 (Amps)')
    plt.plot(*zip(*fine3))
    plt.setp( ax3.get_xticklabels(), visible=False)

    plt.xlim(fine1[0][0], fine1[-1][0])
    plt.title(datetime.datetime.fromtimestamp(fine1[0][0]/1000000000, pytz.timezone('America/Los_Angeles')).strftime('%Y-%m-%d %H:%M:%S')+'   to   '+datetime.datetime.fromtimestamp(fine1[-1][0]/1000000000, pytz.timezone('America/Los_Angeles')).strftime('%Y-%m-%d %H:%M:%S'))
    plt.tight_layout()
    plt.show()

def plot_3phase_voltage_rawdata(fine1, fine2, fine3, BVolt=1):
    ax1 = plt.subplot(313)
    ax1.set_ylabel('L1-E (p.u.)')
    plt.plot(zip(*fine1)[0], [x/BVolt for x in zip(*fine1)[1]])
    plt.setp( ax1, xticklabels=[])

    ax2 = plt.subplot(312, sharex=ax1, sharey=ax1)
    ax2.set_ylabel('L2-E (p.u.)')
    plt.plot(zip(*fine2)[0], [x/BVolt for x in zip(*fine2)[1]])
    plt.setp( ax2.get_xticklabels(), visible=False)

    ax3 = plt.subplot(311, sharex=ax1, sharey=ax1)
    ax3.set_ylabel('L3-E (p.u.)')
    plt.plot(zip(*fine3)[0], [x/BVolt for x in zip(*fine3)[1]])
    plt.setp( ax3.get_xticklabels(), visible=False)

    plt.xlim(fine1[0][0], fine1[-1][0])
    plt.title(datetime.datetime.fromtimestamp(fine1[0][0]/1000000000, pytz.timezone('America/Los_Angeles')).strftime('%Y-%m-%d %H:%M:%S')+'   to   '+datetime.datetime.fromtimestamp(fine1[-1][0]/1000000000, pytz.timezone('America/Los_Angeles')).strftime('%Y-%m-%d %H:%M:%S'))
    plt.tight_layout()
    plt.show()

def plot_rawdata(fine, threshold):
    plt.plot(*zip(*fine))
    plt.xlim(fine[0][0], fine[-1][0])
    plt.axhline(1-threshold, color="r")
    plt.title(datetime.datetime.fromtimestamp(fine[0][0]/1000000000, pytz.timezone('America/Los_Angeles')).strftime('%Y-%m-%d %H:%M:%S'))
    plt.show()
