import os
import numpy as np
import pandas as pd

# ---------- パスの取得 ---------- #
def get_path(folder_path):
    datapaths = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            datapaths.append(os.path.join(root, file))

    return datapaths

# 階層構造を定義した2次元マトリックスを取得する関数
def read_data(path, start_row, start_column, num):
    df = pd.read_excel(path, header=None, sheet_name="Sheet1", 
                       skiprows=start_row - 1, nrows=num, usecols=range(start_column - 1, start_column - 1 + num))
    
    data = np.where(df.values == 1, 1, 0)

    return data

# 行列取得⇒データフレーム化
def read_data_v2(datapath_list, sheet_name, word_num):
    df_sum = 0
    for datapath in datapath_list:
        df = pd.read_excel(datapath, sheet_name=sheet_name, usecols=[x for x in range(1, word_num+1)], nrows=word_num).fillna(0)
        df_sum += df
    return df_sum

# データフレーム⇒CSV
def df_to_csv(df_sum, border, generation, group):
    '''
    行列のデータフレームをcsvファイルに出力する

    Args:
        df_sum(df):グループ内の行列の和
        border(int or float):閾値
        group(str):A1 or A2 or B
    '''
    df = df_sum.where((df_sum <= 0) | (df_sum >= border), 0)
    df = df.where(df < border , 1) 
    df.to_csv(f"C:\WorkSpace\collaborative_research\ISM_Analysis\ISMfiles\{generation}\{group}_border\{group}_border{border}.csv", index=False , header = False)  