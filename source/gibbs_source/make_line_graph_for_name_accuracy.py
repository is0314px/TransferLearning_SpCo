import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import sys
import math
from scipy import stats
from statistics import mean, stdev

plt.style.use('default')
sns.set()
sns.set_style('whitegrid')
sns.set_palette('Set1')

result = sys.argv[1]

def cilen(arr, alpha=0.95):
    if len(arr) <= 1:
        return 0
    m, e, df = np.mean(arr), stats.sem(arr), len(arr) - 1
    interval = stats.t.interval(alpha, df, loc=m, scale=e)
    cilen = np.max(interval) - np.mean(interval)

    if math.isnan(cilen):
        cilen = 0

    return cilen

#file_name = ["kappa_statistic_mixture_mixture","kappa_statistic_global_mixture","kappa_statistic_local_mixture","kappa_statistic_local_local"]
file_name = ["name_acc_specific"]
#models = ["spcoa","env_num_2","env_num_8","env_num_32"]
models = ["spcotransfer20+MI_16","spcotransfer20_16","spcotransfer19+MI_16","spcotransfer19_16"]
#x = np.array([0, 5, 10, 15, 20, 25, 30])
#x = [r'$\frac{0}{20}$',r'$\frac{4}{20}$',r'$\frac{8}{20}$',r'$\frac{12}{20}$',r'$\frac{16}{20}$',r'$\frac{20}{20}$']
x = [r'$\frac{0}{40}$',r'$\frac{8}{40}$',r'$\frac{16}{40}$',r'$\frac{24}{40}$',r'$\frac{32}{40}$',r'$\frac{40}{40}$']
dic_dim = 18
cl = np.array([1.0/dic_dim for i in range(len(x))])
print(cl)
y = []
e = []

for md in models:
    for fn in file_name:

        #f = "gibbs_result/similar_result/"+model+"/"+fn+".txt"
        f = "gibbs_result/sigverse_result/"+md+"/Name_evaluation/"+fn+".txt"
        data_all = np.loadtxt(f,delimiter=" ")

        data_per_0 = []
        data_per_20 = []
        data_per_40 = []
        data_per_60 = []
        data_per_80 = []
        data_per_100 = []

        for j in range(len(data_all)):
            if data_all[j][0] == 0:
                data_per_0.append(data_all[j][1])
            elif data_all[j][0] == 20:
                data_per_20.append(data_all[j][1])
            elif data_all[j][0] == 40:
                data_per_40.append(data_all[j][1])
            elif data_all[j][0] == 60:
                data_per_60.append(data_all[j][1])
            elif data_all[j][0] == 80:
                data_per_80.append(data_all[j][1])
            else:
                data_per_100.append(data_all[j][1])         

        means = np.array([mean(data_per_0),mean(data_per_20),mean(data_per_40),mean(data_per_60),mean(data_per_80),mean(data_per_100)])
        errors = np.array([stdev(data_per_0),stdev(data_per_20),stdev(data_per_40),stdev(data_per_60),stdev(data_per_80),stdev(data_per_100)])
        #errors = np.array([cilen(data_per_0),cilen(data_per_20),cilen(data_per_40),cilen(data_per_60),cilen(data_per_80),cilen(data_per_100)])

        y.append(means)
        e.append(errors)

y = np.array(y)
e = np.array(e)

fig = plt.figure()
fig.subplots_adjust(bottom=0.15)
ax = fig.add_subplot(1, 1, 1)

ax.plot(x, y[0], marker='.', markersize=7.5, label="SpCoTransfer'20+MI 16 env", color='red', linestyle="solid")
ax.fill_between(x, y[0]+e[0], y[0]-e[0], facecolor='red', alpha=0.2)

ax.plot(x, y[1], marker='^', markersize=7.5, label="SpCoTransfer'20 16 env", color='orange', linestyle="dotted")
ax.fill_between(x, y[1]+e[1], y[1]-e[1], facecolor='gold', alpha=0.2)

ax.plot(x, y[2], marker='s', markersize=7.5, label="SpCoTransfer'19+MI 16 env", color='cyan', linestyle="dashed")
ax.fill_between(x, y[2]+e[2], y[2]-e[2], facecolor='lightblue', alpha=0.2)

ax.plot(x, y[3], marker='*', markersize=7.5, label="SpCo Transfer'19 16 env", color='blue', linestyle="dashdot")
ax.fill_between(x, y[3]+e[3], y[3]-e[3], facecolor='blue', alpha=0.2)

ax.plot(x, cl, label="chance level", color='black', linestyle="dashed")

ax.set_ylim(0, 1)
ax.set_xlabel('Name teaching rate in a place in a new enviroment',fontsize=14)
ax.set_ylabel('accuracy',fontsize=14)
ax.set_xticks(x)

ax.legend(fontsize=7.5,loc='upper left')
plt.setp(ax.get_xticklabels(), fontsize=14)
plt.setp(ax.get_yticklabels(), fontsize=14)
plt.savefig("gibbs_result/"+result+"/Name_prediction_result/adaption/name_acc_specific.png",dpi=1000)

