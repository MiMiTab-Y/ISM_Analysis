import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

# ---------- 各種関数の定義 ---------- #
# 可到達行列を導出する関数
def reachability_matrix(matrix):

    ###----------可達行列作成処理----------###
    # 行列のサイズを取得
    n = len(matrix)

    # print('\n----------隣接行列----------')
    matrix = matrix.astype(bool)
    I = np.eye(n).astype(bool)
    adj_matrix = np.logical_or(matrix, I)
    # print(adj_matrix.astype(int))

    # print('\n----------可達行列----------')
    reachability_matrix = adj_matrix.copy()
    while not np.array_equal(reachability_matrix, reachability_matrix @ adj_matrix):
        reachability_matrix = reachability_matrix @ adj_matrix  #@演算子を利用することで行列積を求める（bool演算）
    # print(reachability_matrix.astype(int))

    return reachability_matrix

# ノードの配置を取得する関数
def get_layer_positions(removed_rows_dict, custom_pos={}):
    positions = {}
    current_x = 0
    for layer, nodes in removed_rows_dict.items():
        for node in nodes:
            positions[node] = (current_x, -layer)
            current_x += 1
        current_x = 0

    # custom_posで指定したノード番号のx座標を辞書リストに追加する
    for node, x_coord in custom_pos.items():
        positions[node] = (x_coord, positions[node][1])

    return positions

# グラフオブジェクトを作成する関数
def create_graph(removed_rows_dict, matrix):    # matrixを追加
    G = nx.DiGraph()

    # ノードをグラフに追加
    for i in range(matrix.shape[0]):
        G.add_node(i)

    # matrixを参照しエッジを追加する関数
    def add_edges(source_node, target_nodes, target_layer_dict):
        sorted_target_nodes = sorted(target_nodes, key=lambda node: target_layer_dict[node], reverse=True)
        for target_node in sorted_target_nodes:
            if source_node != target_node and not nx.has_path(G, source_node, target_node) and not nx.has_path(G, target_node, source_node):
                G.add_edge(source_node, target_node)
                print('Edge added:', source_node, '->' , target_node)

    sorted_removed_rows_dict = dict(sorted(removed_rows_dict.items()))  # 階層を昇順にソート

    # target_nodeが属する階層の情報を辞書リストとして取得
    target_layer_dict = {}
    for layer, nodes in removed_rows_dict.items():
        for node in nodes:
            target_layer_dict[node] = layer
    
    print('\n--------エッジ追加処理--------')
    for layer, nodes in sorted_removed_rows_dict.items():
        target_nodes = []
        for node in nodes:
            target_nodes = matrix[node].nonzero()[0]
            add_edges(node, target_nodes, target_layer_dict)
    
    return G

# R, A列を取得する関数
def get_RorA(reachability_matrix):
    R_or_A = []
    for i in range(len(reachability_matrix)):
        temp = []
        for j in range(len(reachability_matrix[i])):
            if reachability_matrix[i][j] == 1:
                temp.append(j)
        R_or_A.append(temp)
    return R_or_A

# 重複する要素を抽出する関数
def extract_duplicates(list1, list2):
    # 各リスト内の各サブリストの集合を作成
    set_a = [set(sublist) for sublist in list1]
    set_b = [set(sublist) for sublist in list2]

    # 各リスト内で同じ位置にあるサブリストから重複する要素を抽出
    duplicates = [list(set_a[i] & set_b[i]) for i in range(min(len(set_a), len(set_b)))]

    return duplicates

# 特定の数字を除去する関数
def remove_number(lst, num):
    return [x for x in lst if x != num]

# 新しいデータフレームを取得する関数
def get_new_df(df, i, removed_rows_dict):
    remove_idx = []
    remove_id = []
    remove_num = []
    for j in range(len(df)):
        if df['R'][j] == df['RandA'][j]:
            remove_idx.append(j)
            remove_id.append(df['id'][j])
            for num in df['R'][j]:
                remove_num.append(num)

    remove_idx, remove_num
    # print('remove_idx:', remove_idx)
    # print('remove_num:', remove_num)
    removed_rows_dict[i] = remove_id

    # dfを更新
    df = df.drop(remove_idx)

    # 特定の数字をリスト内からすべて除去する
    for num in remove_num:
        to_remove = num
        # print(num)
        # df = df.applymap(lambda x: [elem for elem in x if elem != to_remove])
        # df = df.applymap(lambda x: remove_number(x, to_remove))
        df['R'] = df['R'].apply(lambda x: remove_number(x, to_remove))
        df['A'] = df['A'].apply(lambda x: remove_number(x, to_remove))
        df['RandA'] = df['RandA'].apply(lambda x: remove_number(x, to_remove))

    return df.reset_index(drop=True), removed_rows_dict
