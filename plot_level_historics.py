import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import random
from datetime import datetime, timedelta

def generate_variable_dummy_data(num_series=200):
    """
    データ数が16〜30個の間でランダムに変動するダミーデータを生成
    """
    data_list = []
    base_date = datetime(2023, 1, 1)

    for i in range(num_series):
        dates = []
        levels = []
        
        # 開始日のランダム化
        current_date = base_date + timedelta(days=random.randint(0, 30))
        current_level = random.uniform(10, 50)
        
        # ★変更点: データ点数を16〜30の間でランダムに決定
        num_points = random.randint(16, 30)
        
        for _ in range(num_points):
            dates.append(current_date)
            levels.append(current_level)
            
            # 次のデータ作成
            current_date += timedelta(days=random.randint(1, 8))
            current_level += random.uniform(-2, 2.5)
            
        data_list.append((dates, levels))
        
    return data_list

def plot_variable_data(data_list):
    """
    データ長が異なっていても対応可能な描画関数
    """
    plt.figure(figsize=(12, 6))
    
    # 200個近いデータをループ
    for dates, levels in data_list:
        # ★安全策: 実データ用に、日付でソートして線が絡まないようにする
        if len(dates) > 0:
            # 日付とレベルをペアにして日付順に並び替え
            combined = sorted(zip(dates, levels))
            # 再度リストに戻す
            sorted_dates, sorted_levels = zip(*combined)
        else:
            continue

        plt.plot(
            sorted_dates, 
            sorted_levels, 
            marker='o',       
            markersize=3,     
            linestyle='-',    
            linewidth=1,      
            alpha=0.4,        # 重なりを見やすくする透明度
            color='blue'      # 単色で統一（必要ならランダム色に変更可）
        )

    # --- 軸・体裁の設定 ---
    ax = plt.gca()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    plt.gcf().autofmt_xdate()

    plt.xlabel("Date")
    plt.ylabel("Level")
    plt.title(f"Level Variation (Variable Length 16-30 points, N={len(data_list)})")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()

# --- 実行 ---
if __name__ == "__main__":
    # 1. 長さがバラバラなデータを生成
    my_data = generate_variable_dummy_data(num_series=200)

    # 2. 描画
    plot_variable_data(my_data)