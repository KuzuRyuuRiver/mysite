#######################################################################
# Test :                                             　               #
#                                                                     #
# ver 0                                                               #
# 200000:                                                             #
#######################################################################
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
#import japanize_matplotlib
import numpy as np
from matplotlib.font_manager import FontProperties
import os

class RadarChartPlot:
    def __init__(self, itemLlabels, valueList, valueLabels = None):
        self.itemLlabels = itemLlabels
        self.valueList   = valueList
        self.itemValues  = []
        self.dic  = []
        self.fontprop = None
        if valueLabels is None:
            self.valueLabels = valueList
        else:
            self.valueLabels = valueLabels
    
    def setFontPath(self, path):
        self.fontprop = FontProperties(fname=path, size=10)

    def plot(self, values, color=None, linestyle='solid', marker='.', label=None, fill=False):
        self.itemValues.append(values)
        self.dic.append({'color':color, 'linestyle':linestyle, 'marker':marker, 'label':label, 'fill':fill})
        
    def show(self):
        self.fig = plt.figure()
        ax = self.fig.add_subplot(111, polar=True)
        
        # 項目軸
        thetagridAngle = np.linspace(0, 2 * np.pi, len(self.itemLlabels) + 1, endpoint=True) + 0.5 * np.pi
        ax.set_thetagrids(np.rad2deg(thetagridAngle[:-1]) % 360, self.itemLlabels, fontsize=10, font_properties=self.fontprop)  # 軸ラベル
        ax.set_thetagrids(np.rad2deg(thetagridAngle[:-1]) % 360, self.itemLlabels, fontsize=10)  # 軸ラベル
        ax.tick_params(axis='x', pad=30, left=True, length=6, width=1, direction='inout')
        
        # 数値軸
        ax.set_rlim(0 , np.max(self.valueList))   
        ax.set_rgrids(self.valueList, angle=90, labels=self.valueLabels, fontsize=8, font_properties=self.fontprop)
        ax.set_rgrids(self.valueList, angle=90, labels=self.valueLabels, fontsize=8)
        ax.tick_params(axis='y', pad=0, left=True, length=0, width=0, direction='inout')
        
        # 外形
        ax.spines['polar'].set_visible(False)  # 枠(外縁)を消す
        
        # プロット
        for values, dic in zip(self.itemValues, self.dic):
            idxNan = np.isnan(values)
            values = values.copy()
            if np.any(idxNan):
                values[idxNan] = 0
                meanVal = np.mean([0, np.max(self.valueList)])
                ax.plot(thetagridAngle[:-1][idxNan], meanVal*np.ones(len(idxNan))[idxNan], linestyle='None' , color=dic['color'], marker='x', label=dic['label']+' NaN')
            values = np.concatenate((values, [values[0]]))  # 閉じた多角形にする
            # ax.plot(thetagridAngle, values, color=dic['color'], linestyle=dic['linestyle'], marker=dic['marker'], label=dic['label'])  
            alpha     = 0.25 if dic['fill'] else 1.
            facecolor = dic['color'] if dic['fill'] else 'none'
            ax.fill(thetagridAngle, values, facecolor=facecolor, alpha=alpha, \
                    linestyle=dic['linestyle'], edgecolor= dic['color'], label=dic['label'])  # 塗りつぶし
        ax.legend(bbox_to_anchor=(1.35, -0.1), loc="lower right", borderaxespad=0, fontsize=10)
        #ax.legend(bbox_to_anchor=(1.35, -0.1), loc="lower right", borderaxespad=0, fontsize=10)
        self.fig.tight_layout()
        return self.fig
        
        
def test_polar(labels, values, imgname, r_max=250):
    angles = np.linspace(0, 2 * np.pi, len(labels) + 1, endpoint=True) + 0.5 * np.pi
    values = np.concatenate((values, [values[0]]))  # 閉じた多角形にする
    fig = plt.figure()
    ax = fig.add_subplot(111, polar=True)
    ax.plot(angles, values, 'o-')  # 外枠
    ax.fill(angles, values, alpha=0.25)  # 塗りつぶし
    ax.set_thetagrids(np.rad2deg(angles[:-1]) % 360, labels, fontsize=12)  # 軸ラベル
    
    
    ax.set_rlim(0 ,r_max)   
    r_label = [50*i for i in range(6)]
    val_rgrids = np.linspace(0, 250, len(r_label))
    ax.set_rgrids(val_rgrids, angle=90, labels=r_label, fontsize=8)
    ax.spines['polar'].set_visible(False)  # 枠(外縁)を消す
    # fig.savefig(imgname)
    # plt.close(fig)

def test():
    itemLabels = ['HP', 'Attack', 'Defense', 'Speed', 'Speed2']
    values = [155, 156, 188, 139, 100]
    # test_polar(itemLabels, values, "radar.png", r_max=250)
    
    valueList = [50*i for i in range(6)]
    rcp = RadarChartPlot(itemLabels, valueList)
    rcp.plot(values, color='red', linestyle='dashed', marker='.', label='test', fill=True)
    fig = rcp.show()
    return fig
    
if __name__ == '__main__':    
    import time
    t0 = time.perf_counter()
    fig = test()

    t1 = time.perf_counter()
    print ("elapsed_time:{%f} [sec]"%(t1-t0))