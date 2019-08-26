'''
This file is to draw some useful graphs for analysis
'''
import matplotlib.pyplot as plt
import matplotlib
import pickle
from math import *

from collections import Counter

'''
This function is to draw comparison
- data: the information for those categories
- category_list: list of categories compared
- method: type(string) 
'''
def draw_compare(data, category_list, method = ""):

    fig = plt.figure(figsize = (32, 16))
    for i in range(len(data)):
        year = []
        values = []
        for y_temp in data[i].keys():
            # delete the current year
            if y_temp != 2018:
                year.append(int(y_temp))
        year = sorted(year)
        for y in year:
            values.append(data[i][y])
        plt.plot(year,values, label = category_list[i])

    plt.xlabel('year', fontsize = 25)
    plt.ylabel('value', fontsize = 25)
    plt.title(method, fontsize = 30, fontweight = 'bold')
    plt.legend(loc = 'upper right', fontsize = 20)
    fig.savefig(('./pic/{0}.png').format(method), dpi = 100)
    plt.close()

'''
- x: type(list), the data for x
- y: type(list), the data for y
- title: type(string), the title of the histogram
- xlabel: type(string), the label for x-axis
- ylabel: type(string), the label for y-axis
'''
def drawHistogram(x, y, title, xlabel, ylabel = 'Fraction'):

    fig = plt.figure(figsize = (32, 16))
    plt.bar(x, y, width = 0.9, color = 'b')
    plt.title(title, fontsize = 30, fontweight = 'bold')
    plt.xlabel(xlabel, fontsize = 25)
    plt.ylabel(ylabel, fontsize = 25)
    '''
    ax = plt.gca()
    ax.tick_params(labelsize = 20)
    '''
    fig.savefig(('./pic/deg_distro/{0}.png').format(title), dpi = 100)
    plt.show()
    plt.close()


'''
To prepare the data for histogram drawing
'''
def drawHistogramSequence(sequence, node, title, xlabel, ylabel = 'Fraction'):

    temp = Counter(sorted(sequence, reverse = True))
    values, counts = zip(*temp.items())
    value = list(values)
    count = list(counts)
    value.pop(-1)
    count.pop(-1)
    count = [c/node for c in count]
    drawHistogram(value, count, title, xlabel, ylabel)


    
'''
To draw a log-log scatter plot
'''

def drawLogHistogram(sequence, node, signal, title, xlabel, ylabel = 'Fraction'):

    temp = Counter(sorted(sequence, reverse = True))
    values, counts = zip(*temp.items())
    values = list(values)
    counts = list(counts)
    values.pop(-1)
    counts.pop(-1)
    count = [c/node for c in counts]
    if(signal=="double_log"):
        log_val = [log(v) for v in values]
    else:
        log_val = values
    log_cnt = [log(c) for c in count]
    drawContDistribution(log_val, log_cnt, title, xlabel, ylabel)


'''
To draw a scatter plot for log-log data
'''
    
def drawContDistribution(x, y, title, xlabel, ylabel='Fraction'):

    fig = plt.figure(figsize = (32,16))
    plt.scatter(x, y, marker = 'o', alpha = 0.9)
    plt.title(title, fontsize = 30, fontweight = 'bold')
    plt.xlabel(xlabel, fontsize = 25)
    plt.ylabel(ylabel, fontsize = 25)
    fig.savefig(('./pic/deg_distro/{0}.png').format(title), dpi = 100)
    plt.show()
    plt.close()    


def drawScatterPlot(x, y, x_label, y_label, title):

    fig = plt.figure()
    plt.scatter(x, y, marker = 'o', alpha = 0.6)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    fig.savefig(('pic/{0}.png').format(title), dpi = 100)
    # plt.close()
    plt.show()


def drawProColQua(result, category):
    plt.rc('font', size = 18)
    
    pro = []
    col = []
    qua = []
    for item in result.keys():
        pro.append(result[item]['productivity'])
        col.append(result[item]['quality'])
        qua.append(result[item]['collaboration'])

    title = "Collaboration vs Productivity {0}".format(category)
    #x_label = 'Collaboration (Ave No. of authors per paper by each author)'
    #y_label = 'Productivity (No. of papers published by each author)'
    x_label = 'Collaboration'
    y_label = 'Productivity'
    drawScatterPlot(col, pro, x_label, y_label, title)

    title = "Collaboration vs Quality {0}".format(category)
    #x_label = 'Collaboration (Ave No. of authors per paper by each author)'
    #y_label = 'Quality (Ave. No. of citations of one paper by each author)'
    x_label = 'Collaboration'
    y_label = 'Quality'
    drawScatterPlot(col, qua, x_label, y_label, title)

    title = "Productivity vs Quality {0}".format(category)
    #x_label = 'Productivity (No. of papers published by each author)'
    #y_label = 'Quality (Ave. No. of citations of one paper by each author)'   
    x_label = 'Productivity'
    y_label = 'Quality'
    drawScatterPlot(pro, qua, x_label, y_label, title)
