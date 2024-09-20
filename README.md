# ISM_Analysis
---
## 概要
ISM法による構造モデルの作成ツール.

## 使用方法
1. 実験データを`ISMfiles`に保存する．（全ての実験データは`ISMfiles/All`，X世代の実験データは`ISMfiles/X`，Z世代の実験データは`ISMfiles/Z`に保存）
2. `matrix_integration.py`で閾値毎の行列を作成する．
3. `ISM.py`でISM法による構造モデルを作成する．


## 各ファイルの概要

### matrix_integration.py

#### 概要
実験データを保存したフォルダ（`ISMfiles/All`，`ISMfiles/X`，`ISMfiles/Z`）内にある隣接行列を合計し，閾値毎に新たな隣接行列のファイルを作成する．

#### 実行手順
1. 実行するとターミナルにどのフォルダを参照するか記入を求められる．
    ```
    どのフォルダを参照しますか？（All or X or Z）:
    ```
    全ての実験データに適用する場合は`All`，X世代のデータに適用する場合は`X`，Z世代のデータに適用する場合は`Z`を入力する．

2. 実行が終わると`ISMfiles/All or X or Z/A1_border`，`ISMfiles/All or X or Z/A2_border`，`ISMfiles/All or X or Z/B_border`，に閾値毎の隣接行列のファイルが保存される．
    ex.)
    X世代のデータについて閾値を1に設定したA1のファイルは`ISMfiles/X/A1_border/A1_border1.csv`として保存される．

### ISM.py

#### 概要
`matrix_integration.py`で作成した閾値毎の隣接行列のファイルからISM法による構造モデルを1回の実行で全て作成する．

#### 実行手順
1. 実行するとターミナルにどのフォルダを参照するか記入を求められる．
    ```
    どのフォルダを参照しますか？（All or X or Z）:
    ```
    全ての実験データに適用する場合は`All`，X世代のデータに適用する場合は`X`，Z世代のデータに適用する場合は`Z`を入力する．

2. 入力すると各閾値におけるISM構造モデルが作成される．
    ```
    閾値1の図を作成完了
    閾値2の図を作成完了
    閾値3の図を作成完了
    閾値4の図を作成完了
    閾値5の図を作成完了
    …
    ```
    ISM構造モデルの図は`fig`のフォルダに全世代，X世代，Z世代毎に保存される．
    
    ex.)
    X世代のA1で閾値を1として作成した図は`fig/X/A1/border1_ISM-MODEL.png`として保存される．

### ISM_for_one.py

#### 概要
`matrix_integration.py`で作成した閾値毎の隣接行列の特定の1つのファイルからISM法による構造モデルを作成する．

#### 実行手順
1. 実行するとターミナルにどのフォルダを参照するか記入を求められる．
    ```
    どのフォルダを参照しますか？（All or X or Z）:
    ```
    全ての実験データに適用する場合は`All`，X世代のデータに適用する場合は`X`，Z世代のデータに適用する場合は`Z`を入力する．

2. 続いて閾値の入力が求められる．
    ```
    閾値の値を入力してください:
    ```
    お好みの数値を入力してください．


3. 入力すると各閾値におけるISM構造モデルが作成される．
    ```
    閾値nの図を作成完了
    ```
    ISM構造モデルの図は`fig`のフォルダに全世代，X世代，Z世代毎に保存される．
    
    ex.)
    X世代のA1で閾値を1として作成した図は`fig/X/A1/border1_ISM-MODEL.png`として保存される．