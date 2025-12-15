import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import random
from datetime import datetime, timedelta

def generate_dummy_data_list_structure(num_series=5):
    """
    指定された構造のダミーデータを生成する関数
    構造:
    {
      "John": [
        {"date": "2025-08-25", "level": 4.07},
        {"date": "2025-11-03", "level": 6.30}
      ],
      ...
    }
    """
    data_dict = {}
    base_date = datetime(2025, 1, 1)

    for i in range(num_series):
        name = f"User_{i}"
        user_records_list = []  # リストを用意
        
        current_date = base_date + timedelta(days=random.randint(0, 30))
        current_level = random.uniform(10, 50)
        num_points = random.randint(16, 30)
        
        for _ in range(num_points):
            # 1レコードを辞書として作成し、リストに追加
            record = {
                "date": current_date.strftime('%Y-%m-%d'),
                "level": round(current_level, 2)
            }
            user_records_list.append(record)
            
            # 次のデータ作成
            current_date += timedelta(days=random.randint(1, 8))
            current_level += random.uniform(-2, 2.5)
            
        data_dict[name] = user_records_list
        
    return data_dict

def plot_dict_data(data_dict):
    """
    {Name: [{'date':..., 'level':...}, ...]} 形式のデータを描画する関数
    """
    plt.figure(figsize=(12, 6))
    
    # 外側の辞書をループ: name="John", records_list=[{...}, {...}]
    for name, records_list in data_dict.items():
        dates = []
        levels = []
        
        # 値（リスト）の中身をループ
        for record in records_list:
            # キーを指定して取り出す
            date_str = record.get('date')
            level = record.get('level')

            if date_str is None or level is None:
                continue

            try:
                dt = datetime.strptime(date_str, '%Y-%m-%d')
                dates.append(dt)
                levels.append(level)
            except ValueError:
                continue

        if len(dates) > 0:
            # 日付順にソート (リスト内の順序がバラバラな場合に備えて)
            sorted_data = sorted(zip(dates, levels))
            sorted_dates, sorted_levels = zip(*sorted_data)

            plt.plot(
                sorted_dates, 
                sorted_levels, 
                marker='o',       
                markersize=3,     
                linestyle='-',    
                linewidth=1,      
                alpha=0.4,        
                color='blue'
            )

    # --- 軸・体裁の設定 ---
    ax = plt.gca()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gcf().autofmt_xdate()

    plt.xlabel("Date")
    plt.ylabel("Level")
    plt.title(f"Level Variation (List of Dicts Structure, N={len(data_dict)})")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()

# --- 実行部分 ---
if __name__ == "__main__":
    # 1. 新しい構造のダミーデータを生成
    # 実際はご自身のデータを使用してください
    my_data = generate_dummy_data_list_structure(num_series=20) 

    # 2. 描画
    plot_dict_data(my_data)