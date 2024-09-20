import os
import sys

module_path = os.path.abspath('C:\WorkSpace\collaborative_research\ISM_Analysis\module')
if module_path not in sys.path:
    sys.path.append(module_path)

# モジュールのインポート
from module import file as f
import numpy as np
import pandas as pd

# 各グループのフォルダのパス
folder = input("どのフォルダを参照しますか？（All or X or Z）:")
A1_path = f"C:\WorkSpace\collaborative_research\ISM_Analysis\ISMfiles\{folder}\A1"
A2_path = f"C:\WorkSpace\collaborative_research\ISM_Analysis\ISMfiles\{folder}\A2"
B_path = f"C:\WorkSpace\collaborative_research\ISM_Analysis\ISMfiles\{folder}\B"

# ファイルのパスのリスト取得
A1_datapaths = f.get_path(A1_path)
A2_datapaths = f.get_path(A2_path)
B_datapaths = f.get_path(B_path)

# 評価シートの読み込み情報
start_row = 0
start_column = 0
A1_num = 29 # ワード数
A2_num = 20 # ワード数
B_num = 88

# グループ内の行列和を導出
A1_df_sum = f.read_data_v2(A1_datapaths, "A-1_評価", A1_num)
A2_df_sum = f.read_data_v2(A2_datapaths, "A-2_評価", A2_num)
B_df_sum = f.read_data_v2(B_datapaths, "Sheet1", B_num)

# データフレームをcsvで保存
for border in range(1, len(A1_datapaths)+1):
    f.df_to_csv(A1_df_sum, border, folder, "A1")
    f.df_to_csv(A2_df_sum, border, folder, "A2")
    f.df_to_csv(B_df_sum, border, folder, "B")