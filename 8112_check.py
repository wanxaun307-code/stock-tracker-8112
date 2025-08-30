import yfinance as yf
import pandas as pd
from datetime import datetime

# 股票代號 (台股要加 ".TW")
ticker = "8112.TW"

# 下載近 120 日資料
df = yf.download(ticker, period="6mo", interval="1d")

# 計算均線
df['MA5'] = df['Close'].rolling(5).mean()
df['MA10'] = df['Close'].rolling(10).mean()
df['MA20'] = df['Close'].rolling(20).mean()
df['MA60'] = df['Close'].rolling(60).mean()  # 季線
df['VOL5'] = df['Volume'].rolling(5).mean()

# 最新一天資料
latest = df.iloc[-1]

price = latest['Close']
ma5, ma10, ma20, ma60 = latest['MA5'], latest['MA10'], latest['MA20'], latest['MA60']
vol, vol5 = latest['Volume'], latest['VOL5']

# 判斷條件
break_season = price > ma60
golden = ma5 > ma10 > ma20
vol_confirm = vol > vol5

# 判斷訊號
if break_season and golden:
    signal = "✅ 符合條件，可關注進場機會"
else:
    signal = "❌ 未符合條件，建議觀望"

# 輸出報告文字
report = f"""
📈 8112 至上 每日追蹤報告
日期: {datetime.today().date()}

收盤價: {price:.2f}
季線(MA60): {ma60:.2f}
MA5: {ma5:.2f}, MA10: {ma10:.2f}, MA20: {ma20:.2f}

成交量: {vol:.0f}, 5日均量: {vol5:.0f}

條件檢查:
- 是否突破季線? {'是' if break_season else '否'}
- 均線多頭排列 (MA5>MA10>MA20)? {'是' if golden else '否'}
- 量能是否大於5日均量? {'是' if vol_confirm else '否'}

結論: {signal}
"""

# 存成檔案 (給 GitHub Actions 寄信用)
with open("result.txt", "w", encoding="utf-8") as f:
    f.write(report)

# 同時印出 (方便在 log 也能看)
print(report)
