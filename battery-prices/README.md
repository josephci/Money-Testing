# Battery Prices — 骨架

電動工具電池按**真實 $/Wh** 排序嘅比價站。diskprices.com 模式,套用喺一個實查證實冇人做嘅品類。

> 背景分析同市場數據見 [`../docs/price-comparison-sites.md`](../docs/price-comparison-sites.md)

---

## 個站解決緊咩

消費者面對「DeWalt 20V 5.0Ah」同「Makita 18V 6.0Ah」,**根本比唔到**。

因為：

| | |
|---|---|
| 5 粒鋰電 **峰值** 5 × 4.0V = **20V** | DeWalt 印呢個 |
| 5 粒鋰電 **標稱** 5 × 3.6V = **18V** | Milwaukee / Makita 印呢個 |

**兩者係同一件事。** 一離開充電器電壓就跌返 18V。

所以：

- ❌ 跨電壓比 `$/Ah` 冇意義（M12 vs M18、LXT vs XGT）
- ✅ `Wh = 標稱電壓 × Ah` 先係可比嘅單位

個站每一行都**用標稱電壓計**,唔係用貼紙上面個數,而且多支裝按總能量除。**呢個就係全部產品價值。**

實查結果：ToolGuyd 有文章討論,Home Depot 有目錄,**冇人做實時排序表**。

---

## 檔案

```
battery-prices/
├── index.html              頁面結構
├── assets/style.css        樣式（自動跟系統深色/淺色）
├── assets/app.js           計算、篩選、排序、渲染
├── data/batteries.json     ⭐ 資料源（39 個型號,9 個平台）
├── scripts/update_prices.py 驗證 + CSV 匯出/匯入 + PA-API stub
└── scripts/build.py        打包成單一 dist/index.html
```

## 點跑

```bash
# 開發（一定要用 http server,file:// 會被 CORS 擋)
python3 -m http.server 8000
# → http://localhost:8000

# 驗證資料
python3 scripts/update_prices.py --check

# 打包成單一檔案部署
python3 scripts/build.py          # → dist/index.html（自足,28KB,零外部請求）
```

`dist/index.html` 冇任何外部請求,直接掉上 Cloudflare Pages / GitHub Pages / S3 就得。

---

## ⚠️ 而家嘅狀態：示範數據

`data/batteries.json` 入面：

- **規格**（V / Ah / Wh）盡力查過,但**未逐個對過官方 spec sheet**
- **價格全部係假嘅佔位數字**
- **冇聯盟連結**

頁面會顯示黃色 banner 提你。`price_source` 改成 `manual` 之後 banner 自動消失。

**出街之前一定要做完下面 Step 1。**

---

## 落手次序

呢個次序係特登設計嚟繞開 Amazon PA-API 嘅雞蛋問題（要先有 3 單先攞到 API key)。

### Step 1 — 核實規格（半日）

逐個型號對官方 spec sheet 改 `data/batteries.json`,然後：

```bash
python3 scripts/update_prices.py --check
```

`--check` 會捉：重複 id、未知平台、`rated_wh` 同 `標稱V × Ah` 對唔上。**呢個對唔上就係整個站嘅信譽問題,一定要清零。**

目前 39 個型號 **0 errors**。

### Step 2 — 人手入價（每次約 1 個鐘）

```bash
python3 scripts/update_prices.py --export-csv prices.csv
# 用 Excel / Numbers 填 price 同 url 兩欄
python3 scripts/update_prices.py --import-csv prices.csv
```

匯入成功會自動將 `price_source` 由 `sample` 轉做 `manual`,banner 消失。

> 頭三個月就係咁做。一個禮拜更新一兩次已經夠 —— **唔好未有人用就去自動化。**

### Step 3 — 出街,攞頭 3 單

部署 `dist/index.html`,然後去：

- **r/Tools**、**r/DIY**、**r/electricians**
- ToolGuyd 留言區（佢哋讀者就係你目標客）
- Hacker News「Show HN」

⚠️ **每個社群嘅自我宣傳規則先睇清楚。** 帶價值咁分享（「我整咗個表發現 Ryobi 每 Wh 最平」）好過硬銷。

### Step 4 — 夠單先自動化

有 3 單合資格銷售之後申請 PA-API,實作 `scripts/update_prices.py` 入面 `cmd_paapi()` 個 stub（入面寫晒步驟）。用 GitHub Actions cron 每日跑一次,免費。

### Step 5 — 加地區站

diskprices **一半收入嚟自非美國站**。`.co.uk` / `.de` / `.ca` 係最抵做嘅擴張。

---

## 已經處理咗嘅合規要求

| 要求 | 喺邊 |
|---|---|
| 聯盟關係披露 | footer,永遠顯示 |
| 價格快取 ≤ 24 小時 | `--check` 會警告,頁面有 banner |
| 價格可能過時免責 | footer |
| `rel="nofollow sponsored"` | 所有 Buy 連結 |

---

## 已知未做

- [ ] 規格未逐個核實（Step 1）
- [ ] 冇真價、冇聯盟連結（Step 2）
- [ ] PA-API 係 stub（Step 4,要有單先做到）
- [ ] 只有美國市場（Step 5）
- [ ] 冇價格歷史 —— **但呢個係最值錢嘅護城河**。由第一日開始存低每日價格,一年後你有「邊隻電池幾時最平」嘅數據,新入場者永遠追唔返。建議 Step 2 開始就順手 append 一個 `history.jsonl`
- [ ] 冇「同平台內邊隻最抵」以外嘅推薦邏輯
