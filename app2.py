#######################################################################
# Test :                                             　               #
#                                                                     #
# ver 0                                                               #
# 200000:                                                             #
#######################################################################
import numpy as np
import streamlit as st
import pandas as pd
from StatisticData import StatisticClass
#st.set_page_config(layout="wide")
import pathlib
HERE     = pathlib.Path(__file__).parent
FONTPATH = HERE.joinpath('.fonts', 'ipaexg.ttf')

@st.cache
def loadData(path):    
    workSheetCSV = pd.read_csv(path, encoding="shift-jis")
    return workSheetCSV

def main():
    # サイドバー
    workSheetFile = st.sidebar.file_uploader('ファイルの場所', type='csv')
    # 学部生 or 院生
    selBorM = st.sidebar.selectbox('学部生 or 院生',('学部生/院生', '学部生', '院生'))

    # 学生番号検索
    searchID = st.sidebar.text_input('search', '')

    if workSheetFile is not None:
        _main(workSheetFile, selBorM, searchID)
    else:
        st.header('サイドバーよりファイルを選択してください')
        pass

def _main(workSheetFile, selBorM, searchID):
    workSheetCSV = loadData(workSheetFile)
    statInst = StatisticClass()
    statInst.init(workSheetCSV)
    statInst.computeStatistic(statInst.workSheetDF)

    # 学部生 or 院生
    selWorkSheet = statInst.workSheetDF.xs(selBorM, level='学部or院') if selBorM in statInst.BorMID.values() else statInst.workSheetDF

    # 学生番号検索
    studentIDList   = list(map(str, list(selWorkSheet.index.get_level_values('学生番号'))))
    resultIDList    = [int(item) for item in studentIDList if item.find(str(searchID)) != -1]
    selectID        = st.sidebar.selectbox('学生番号:', resultIDList)  # st.sidebar.multiselect
    boolIdx         = statInst.workSheetDF.index.get_level_values('学生番号') == selectID
    feedbackSheetID = statInst.workSheetDF.index.get_level_values('No')[boolIdx].values[0]

    # ページ選択
    pages = { 'Graph': graphPage, '統計データ' : statisticPage, '個人RawData' : rawdataPage}
    page = st.sidebar.radio("ページ選択", tuple(pages.keys()))
    stateDict = {'statInst' : statInst, 'feedbackSheetID' : feedbackSheetID}
    pages[page](stateDict)

def graphPage(stateDict):
    # メイン画面
    st.header('Graph')

    statInst        = stateDict['statInst']
    feedbackSheetID = stateDict['feedbackSheetID']

    d1 = dict(selector=".col1", props=[('min-width', '100px')]) # name
    d2 = dict(selector=".col2", props=[('min-width', '3000px')]) # pref
    # アップロードファイルをメイン画面にデータ表示    fig = statInst.fig
    fig = statInst.plotGraph(feedbackSheetID, fontPath = FONTPATH)
    st.pyplot(fig)
    st.header('スコア')
    table = statInst.scoreDF.loc[feedbackSheetID].reset_index().assign(hack='').set_index('hack')
    idxHalf = int(np.ceil(len(statInst.itemWorkSheet)/2))
    tableA = list(statInst.labelDict.values())[:idxHalf]
    tableB = list(statInst.labelDict.values())[idxHalf:]
    st.table(table[tableA])
    st.table(table[tableB])

def statisticPage(stateDict):
    statInst      = stateDict['statInst']    
    statBachelor  = statInst.statDFDict['学部生']
    statMaster    = statInst.statDFDict['院生']
    st.header('学部生')
    st.table(statBachelor.T)
    st.header('院生')
    st.table(statMaster.T)

def rawdataPage(stateDict):
    st.header('スコア(Raw Data)')
    statInst        = stateDict['statInst']    
    feedbackSheetID = stateDict['feedbackSheetID']
    table           = statInst.workSheetDF.loc[feedbackSheetID].reset_index().assign(hack='').set_index('hack')[statInst.itemWorkSheet]
    st.table(table.T)

#最後にmain()を入れて実行する。
main()
    