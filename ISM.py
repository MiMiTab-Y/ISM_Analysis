import os
import sys

# module_path = os.path.abspath('C:\WorkSpace\collaborative_research\ISM_Analysis\module')
# if module_path not in sys.path:
#     sys.path.append(module_path)

# モジュールのインポート
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from module import ISM

# 各グループのフォルダのパス
folder = input("どのフォルダを参照しますか？（All or X or Z）:")

# データ数
if folder == "All":
    DIR = "C:\WorkSpace\collaborative_research\ISM_Analysis\ISMfiles\All\A1"
    roop = sum(os.path.isfile(os.path.join(DIR, name)) for name in os.listdir(DIR))
elif folder == "X":
    DIR = "C:\WorkSpace\collaborative_research\ISM_Analysis\ISMfiles\X\A1"
    roop = sum(os.path.isfile(os.path.join(DIR, name)) for name in os.listdir(DIR))
elif folder == "Z":
    DIR = "C:\WorkSpace\collaborative_research\ISM_Analysis\ISMfiles\Z\A1"
    roop = sum(os.path.isfile(os.path.join(DIR, name)) for name in os.listdir(DIR))

for border in range(1, roop+1):
    # ボーダーに応じたパスの指定
    A1path = f"C:\WorkSpace\collaborative_research\ISM_Analysis\ISMfiles\{folder}\A1_border\A1_border{border}.csv"
    A2path = f"C:\WorkSpace\collaborative_research\ISM_Analysis\ISMfiles\{folder}\A2_border\A2_border{border}.csv"
    Bpath =f"C:\WorkSpace\collaborative_research\ISM_Analysis\ISMfiles\{folder}\B_border\B_border{border}.csv"

    # csvファイルの読み込み
    A1matrix = np.genfromtxt(A1path, delimiter=',')
    A2matrix = np.genfromtxt(A2path, delimiter=',')
    Bmatrix = np.genfromtxt(Bpath, delimiter=',')
    matrixes = [A1matrix, A2matrix, Bmatrix]

    # 可達行列導出
    reachability_matrixes = []
    for matrix in matrixes:
        reach = ISM.reachability_matrix(matrix)
        reachability_matrixes.append(reach)

    # データフレーム作成
    df_list = []
    for reachability_matrix in reachability_matrixes:
        R = []
        A = []
        id = list(range(len(reachability_matrix)))

        R = ISM.get_RorA(reachability_matrix)
        A = ISM.get_RorA(np.transpose(reachability_matrix))
        RandA = ISM.extract_duplicates(R, A)

        for RandA_i in RandA:
            RandA_i.sort()

        df = pd.DataFrame({'id':id, 'R':R, 'A':A, 'RandA':RandA})
        df_list.append(df)

    # 関連度取得
    d_add_r_list = []
    for reachability_matrix in reachability_matrixes:
        # 各行の和を取得
        row_sums = np.sum(reachability_matrix, axis=1)    # ISM
        # row_sums = np.sum(matrix, axis=1)   # dematel

        # 各列の和を取得
        column_sums = np.sum(reachability_matrix, axis=0) # ISM
        # column_sums = np.sum(matrix, axis=0)    # dematel

        # 関連度
        d_add_r = row_sums + column_sums
        d_add_r_list.append(d_add_r)

    # 階層を取得
    levels_list = []
    for df in df_list:
        levels = {}
        c = 0
        initial_df_length = len(df)

        for k in range(len(df)):
            df, levels = ISM.get_new_df(df, k+1, levels)
            # print('len(lebels): ', len(levels[i+1]))
            c += len(levels[k+1])
            # print('c: ', c)

            if c == initial_df_length:
                break
        levels_list.append(levels)

    # ---------- ファイル名設定 ---------- #
    def group(i):
        if i == 0:
            return "A1"
        elif i == 1:
            return "A2"
        else:
            return "B"
        
    # グラフ作成と保存
    for i in range(3):
        # グラフを作成
        G = ISM.create_graph(levels_list[i], matrixes[i])

        # ノードの配置を取得
        pos = ISM.get_layer_positions(levels_list[i])

        # グラフを描画して表示
        plt.figure(figsize=(16, 16), dpi=600)
        nx.draw(G, pos, with_labels=True, node_size=1500, node_color="skyblue", font_size=10, font_weight="bold", arrowsize=15)
        plt.savefig(f'C:/WorkSpace/collaborative_research/ISM_Analysis/fig/{folder}/{group(i)}/border{border}_ISM-MODEL.png', format='png')
        # plt.show()
        plt.close()
    
    print(f"閾値{border}の図を作成完了")