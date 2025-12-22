import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cm as cm # カラーマップ用
import random
from datetime import datetime, timedelta
import sys
import my_common as my

def plot_level_historics(data_dict, save_path=None):
    """
    {Name: [{'date':..., 'level':...}, ...]} 形式のデータを描画する関数
    """
    
    # --- 前処理: データを整形し、開始日順にソートするためのリストを作成 ---
    valid_series = []

    for name, records_list in data_dict.items():
        dates = []
        levels = []
        
        for record in records_list:
            date_str = record.get('date')
            level = record.get('level')

            if date_str is None or level is None:
                continue

            try:
                dt = my.datetime_normalize(date_str)
                dates.append(dt)
                levels.append(level)
            except ValueError:
                continue

        if len(dates) > 0:
            # 日付順にソート
            sorted_data = sorted(zip(dates, levels))
            sorted_dates, sorted_levels = zip(*sorted_data)
            
            # ソート用の情報を含めてリストに格納
            # start_date: その系列の一番古い日付（ソートキー用）
            valid_series.append({
                'name': name,
                'start_date': sorted_dates[0], 
                'dates': sorted_dates,
                'levels': sorted_levels
            })

    # 開始日 (start_date) が早い順（若番）に並び替え
    valid_series.sort(key=lambda x: x['start_date'])

    # --- 描画設定 ---
    
    # 背景色と文字色の設定
    fig = plt.figure(figsize=(12, 6))
    fig.patch.set_facecolor('black') # 外側の背景
    
    ax = plt.gca()
    ax.set_facecolor('black')        # グラフ内の背景
    
    # 軸・ラベル・枠線の色を灰色に設定
    gray_color = '#AAAAAA'
    ax.spines['bottom'].set_color(gray_color)
    ax.spines['top'].set_color(gray_color) 
    ax.spines['right'].set_color(gray_color)
    ax.spines['left'].set_color(gray_color)
    ax.tick_params(axis='x', colors=gray_color)
    ax.tick_params(axis='y', colors=gray_color)
    ax.yaxis.label.set_color(gray_color)
    ax.xaxis.label.set_color(gray_color)
    ax.title.set_color(gray_color)

    # --- プロット実行 ---
    
    num_series = len(valid_series)
    
    # 標本数に応じて色相(hsv)を変化させる
    # hsvカラーマップを使って、0.0〜1.0の間を標本数で分割する
    colors = [cm.hsv(i / num_series) for i in range(num_series)]

    for i, series in enumerate(valid_series):
        plt.plot(
            series['dates'], 
            series['levels'], 
            marker=None,      # マーカー（点）を表示しない
            linestyle='-',    
            linewidth=1,      
            alpha=0.6,        # 線が重なっても見えるように少し透明度を入れる
            color=colors[i]   # 開始日順に計算した色を適用
        )

    # --- 軸・体裁の仕上げ ---
    
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gcf().autofmt_xdate()

    plt.xlabel("Date")
    plt.ylabel("Level")
    plt.title(f"Level Variation (Lines only, Ordered by Start Date, N={num_series})")
    
    # グリッドも灰色で控えめに
    plt.grid(True, linestyle='--', alpha=0.3, color=gray_color)
    
    plt.tight_layout()
    
    if save_path:
        # 保存時も背景色を維持する
        plt.savefig(save_path, facecolor=fig.get_facecolor(), edgecolor='none')
    else:
        plt.show()

if __name__ == "__main__":
    level_data = my.load_json(sys.argv[1])
    save_path = None
    if len(sys.argv) > 2:
        save_path = sys.argv[2]
    plot_level_historics(level_data, save_path)