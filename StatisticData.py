#######################################################################
# Test :                                             　               #
#                                                                     #
# ver 0                                                               #
# 200000:                                                             #
#######################################################################
import numpy as np
import pandas as pd
from RadarChart import RadarChartPlot

class StatisticClass:
    def __init__(self, path = None):
        self.IDNameDict    = {'No':'feedbackSheetID', '学部or院':'BorM', '学生番号':'studentID'}  
        self.BorMID        = {1:'学部生', 2:'院生'}  # 学部or院 : Bachelor or Master
        self.itemNameDict  = { '自尊'     :      'selfEsteem', '階梯'   :        'ladder', 
                               '人生満足' :'lifeSatisfaction', '困り感'  :'feelingTrouble', 
                               '抑うつ'    :      'depression', '不安'   :       'anxiety', 
                               'AQスコア'  :         'aqScore', 'サポート' :       'support',
                               'ADHDスコア':           'adhd'}
        self.isAntonymsDict = {'自尊'     :  False, '階梯'  : False, 
                               '人生満足' :  False, '困り感' :  True, 
                               '抑うつ'    :   True, '不安'  :  True, 
                               'AQスコア'  :   True, 'サポート': False,
                               'ADHDスコア':   True}
        self.labelDict = {  '自尊'      :        '自尊感情指数', '階梯'  :    '生活イメージ指数', 
                            '人生満足'  :      '人生満足度指数', '困り感' :    '快適／困難指数', 
                            '抑うつ'     :          'やる気指数', '不安'  :          '安心指数', 
                            'AQスコア'   : 'コミュニケーション力指数', 'サポート': 'ソーシャルサポート指数',
                            'ADHDスコア' :         '集中力指数'}
        if path is not None: 
            workSheetCSV = pd.read_csv(path, encoding="shift-jis")
            self.init(workSheetCSV)

    def init(self, workSheetCSV):
        self.workSheetCSV = workSheetCSV
        self.workSheetDF  = workSheetCSV.copy(deep=True)
        BorM         = [self.BorMID[id_] if (id_ == 1 or id_ == 2) else 'Unknown' for id_ in self.workSheetDF['学部or院']]
        self.workSheetDF['学部or院'] = BorM
        self.workSheetDF.set_index(list(self.IDNameDict.keys()), drop=True, inplace=True)     
        self.itemWorkSheet = self.workSheetDF.columns
        self.statDFDict    = self.computeStatisticBorM()   
        
    def plotGraph(self, feedbackSheetID, fontPath = None):
        score       = self.scoreDF.loc[feedbackSheetID]        
        itemLabels  = self.labelDict.values()
        valueList   = [i for i in range(6)]
        rcp         = RadarChartPlot(itemLabels, valueList)
        if fontPath is not None:            
            rcp.setFontPath(fontPath)
        values      = score[itemLabels].values.ravel()
        rcp.plot(values, color='red', linestyle='solid', marker='.', label=f'No {feedbackSheetID}', fill=True)
        # statDF      = self.statDF.loc['score_mean'][itemLabels]
        mean        = [3.0 for i in range(len(values))] # statDF[score_mean] = 3.0 となる(?)
        rcp.plot(mean, color='blue', linestyle='dashed', marker='.', label='mean', fill=False)
        self.fig = rcp.show()
        return self.fig
    
    def computeStatisticBorM(self): 
        statDFDict = {}
        itemWorkSheet = self.itemWorkSheet
        for grad in self.BorMID.values():
            workSheetDF = self.workSheetDF.xs(grad, level='学部or院')
            mean        = workSheetDF[itemWorkSheet].mean(skipna=True, numeric_only=True)
            std         = workSheetDF[itemWorkSheet].std(skipna=True, numeric_only=True)
            stafDF_     = pd.DataFrame([mean, std], index=['mean', 'std'])
            statDFDict[grad] = stafDF_
        #statDF  = pd.DataFrame([itemDict['mean'], itemDict['std']], index=itemDict['grad'], columns=['mean', 'std'])
        return statDFDict

    def computeStatistic(self, workSheetDF):    
        itemWorkSheet = self.itemWorkSheet
        mean   = workSheetDF[itemWorkSheet].mean(skipna=True, numeric_only=True)
        std    = workSheetDF[itemWorkSheet].std(skipna=True, numeric_only=True)
        zscore = (workSheetDF[itemWorkSheet] - mean) / std
        score  = (zscore * 2.0) / 3.0 + 3.0
        score  = score.clip(1.0, 5.0)
        
        reverse     = [key for key, val in self.isAntonymsDict.items() if val]
        score4Chart = score.copy(deep=True)
        score4Chart[reverse] = 1 + (5.0 - score[reverse])        
        score4Chart.rename(columns=self.labelDict, inplace=True)
        # self.statDF  = pd.DataFrame([mean, std, score.mean()], index=['mean', 'std', 'score_mean'])
        # self.statDF  = pd.DataFrame([score4Chart.mean()], index=['score_mean'])
        self.scoreDF = score4Chart
                

def test():
    dataDir = './Data'
    path = dataDir + '/dammyData.csv'
    #sc = StatisticClass(path=path)
    sc = StatisticClass()
    workSheetCSV = pd.read_csv(path, encoding="shift-jis")
    sc.init(workSheetCSV)
    # sc.computeStatistic(sc.workSheetDF.xs('学部生', level='学部or院'))
    sc.computeStatistic(sc.workSheetDF)
    sc.plotGraph(33)
    # print(sc.workSheetDF)
    
if __name__ == '__main__':    
    import time
    t0 = time.perf_counter()
    test()

    t1 = time.perf_counter()
    print ("elapsed_time:{%f} [sec]"%(t1-t0))