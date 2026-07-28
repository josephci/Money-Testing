# 出街清單

一條龍嘅意思係：**所有唔需要你嘅帳戶、你嘅錢、你嘅身份嘅嘢,已經做晒。**

下面分兩部分。Part 1 唔使你做。Part 2 只有你做得到 —— 一共 **7 項**。

---

# Part 1：已經完成 ✅

| | 狀態 |
|---|---|
| 市場驗證（含反證搜尋） | ✅ [`docs/market-check.md`](docs/market-check.md) |
| 網站（50 版：首頁 + 9 平台 + 39 型號 + 1 文章） | ✅ [`battery-prices/`](battery-prices/) |
| $/Wh 計算引擎（標稱電壓、多支裝、資料校驗） | ✅ |
| SEO：canonical、sitemap、robots、JSON-LD、內部連結 | ✅ |
| 分享：OG card、Twitter card、篩選狀態入 URL | ✅ |
| 合規：聯盟披露、`nofollow sponsored`、24 小時價格警告 | ✅ |
| 價格歷史記錄（護城河） | ✅ `--import-csv` 自動 append |
| 規格核實進度追蹤 | ✅ `--check` 顯示進度條 |
| CI/CD（GitHub Actions → Pages） | ✅ [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml) |
| 防呆：示範數據唔會意外上線 | ✅ `--require-real-data` |
| 推廣計劃 | ✅ [`docs/traffic-plan.md`](docs/traffic-plan.md) · [`docs/quiet-launch.md`](docs/quiet-launch.md) |
| **所有出街文字（目錄、貼文、email）** | ✅ [`docs/launch-pack.md`](docs/launch-pack.md) |

---

# Part 2：只有你做得到（7 項）

## ① 買域名 · 15 分鐘 · 約 US$12/年

喺你部機跑（呢個環境嘅網絡政策擋咗 RDAP,我查唔到）：

```bash
for d in toolbatteryprices batteryperwh wattprices toolbatterydeals \
         batterypricing batterywatthours perwattprices; do
  printf '%-22s ' "$d.com"
  code=$(curl -s -o /dev/null -w '%{http_code}' "https://rdap.verisign.com/com/v1/domain/$d.com")
  case $code in 404) echo AVAILABLE;; 200) echo taken;; *) echo "?? $code";; esac
done
```

`404 = 未註冊`。推薦次序：`toolbatteryprices.com` → `batteryperwh.com` → `wattprices.com`

⚠️ **唔好用 `.io`** —— 你嘅買家係裝修佬,對佢哋嚟講 `.io` 似詐騙網。全部 `.com` 冇貨寧願用 `.net` 或者加一個字。

---

## ② 核實規格 · 半日 · ⚠️ 最重要

**呢個係唯一我做唔到而又必須做嘅嘢** —— 我攞唔到官方 spec sheet（外部主機一律 403）。

而個站嘅**全部信譽就係呢啲數字**。一個錯嘅 Wh,成個站就冇價值。

```bash
cd battery-prices
python3 scripts/update_prices.py --export-csv specs.csv
```

開 `specs.csv`,逐行對官方 spec sheet：

| 對咩 | 點對 |
|---|---|
| `amp_hours` | 官方頁 |
| `rated_wh` | 官方頁（通常寫喺運輸資料 / UN38.3） |
| `model` | 官方型號,唔好靠 Amazon 標題 |

對完填 `verified` = `yes`,順手填 `spec_url`。然後：

```bash
python3 scripts/update_prices.py --import-csv specs.csv
python3 scripts/update_prices.py --check
```

`--check` 會顯示進度條,做到 **39/39** 為止：

```
specs verified · [########################] 39/39
```

> 💡 **唔使一次過做完。** 一次做一個品牌,分五日。做幾多得幾多 —— 未 verify 嘅唔會令 `--check` 出 error。

---

## ③ 開 Amazon Associates · 30 分鐘

到 [affiliate-program.amazon.com](https://affiliate-program.amazon.com) 註冊,攞你嘅 tracking ID（例如 `yourname-20`）。

⚠️ 記住嗰個雞蛋問題：**180 日內要有 3 單合資格銷售,先攞到 PA-API**。所以頭幾個月一定要人手入價 —— 呢個係設計嚟繞開佢,唔係將就。

---

## ④ 入真價 · 每次 1 小時

```bash
python3 scripts/update_prices.py --export-csv prices.csv
```

填兩欄：

- `price` —— Amazon 現價
- `url` —— 帶你 tracking ID 嘅聯盟連結

```bash
python3 scripts/update_prices.py --import-csv prices.csv
```

會自動：`price_source` 由 `sample` 轉 `manual`（黃色 banner 消失）+ **append 一行去 `data/history.jsonl`**。

> ⭐ **每次 import 都要跑,就算價錢冇點變。** 呢個檔案係整盤生意唯一無法被抄嘅資產 —— 一年後你答得出「呢隻電池通常幾時最平」,遲入場嘅人永遠追唔返。
> 睇進度：`python3 scripts/update_prices.py --history`

---

## ⑤ 部署 · 20 分鐘

1. 開 `.github/workflows/deploy.yml`,改一行：
   ```yaml
   env:
     BASE_URL: https://你嘅域名.com
   ```
2. GitHub repo → Settings → Pages → Source 揀 **GitHub Actions**
3. Settings → Pages → Custom domain 填你個域名,跟指示改 DNS
4. Push 上 `main`

Workflow 會自動：`--check` → `--require-real-data` build → 部署。

**示範數據會令 build 失敗,呢個係故意嘅** —— 防止佔位價錢流出去。

---

## ⑥ 交搜尋引擎 · 10 分鐘 · 零社交

| 平台 | 做咩 |
|---|---|
| [Google Search Console](https://search.google.com/search-console) | 加 property → 驗證 → Sitemaps 交 `sitemap.xml` |
| [Bing Webmaster Tools](https://www.bing.com/webmasters) | 同上 |

⚠️ **唔做嘅話 Google 可能永遠唔知你存在。** 呢個係零社交路線嘅命脈。

---

## ⑦ 出街 · 一個週末 + 每星期少少

**全部文字喺 [`docs/launch-pack.md`](docs/launch-pack.md),貼上就用得。**

按曝光度由低到高：

| 動作 | 曝光度 | 時間 |
|---|---|---|
| 30–50 個目錄提交 | **零**（填表,冇人回覆你） | 一個週末 |
| GitHub awesome 清單發 PR | **零**（寫 code） | 1 小時 |
| 答 5–10 條舊帖 | 極低（冇人喺度睇） | 每次 10 分鐘 |
| 2 封 email（ToolGuyd + YouTuber） | 低（私人訊息） | 30 分鐘 |
| Reddit / Show HN 發帖 | 中 | 睇你 |

🚨 **貼之前**：`launch-pack.md` 入面所有數字都係示範數據算嘅,**要換成真實數字**。貼錯數字比唔貼更差。

---

# 順序（唔好跳）

```
① 買域名
      ↓
② 核實規格 ────────► --check 到 39/39
      ↓
③ 開 Associates
      ↓
④ 入真價 ──────────► banner 消失,history 開始累積
      ↓
⑤ 部署
      ↓
⑥ 交 Search Console  ← 唔做,前面全部白做
      ↓
⑦ 目錄 → 舊帖 → email → （想嘅話）發帖
```

**②→④ 唔可以跳。** 未核實嘅規格 + 假價錢上線,你會浪費咗唯一一次第一印象。

---

# 之後嘅節奏

| 幾時 | 做咩 |
|---|---|
| 每星期 | `--export-csv` → 更新價 → `--import-csv`（1 小時) |
| 每月 | `--history` 睇趨勢;答幾條舊帖 |
| 夠 3 單之後 | 實作 `cmd_paapi()`,自動化每日更新 |
| 6 個月後 | 加地區站（`.co.uk` / `.de` / `.ca` —— diskprices 一半收入嚟自呢度) |

---

# 老實嘅預期

| 時間 | 流量 | 收入 |
|---|---|---|
| Week 3 出街 | 爆發 500–3,000 | $5–30 |
| Week 5-8 | **跌返 100–400/月** ⚠️ | $5–25 |
| Month 5-6 | 1,000–3,000/月 | $60–190 |
| Month 7-12 | 2,000–6,000/月 | $125–375 |

**第 5-8 星期會覺得失敗咗。呢個係正常曲線** —— 爆發已散,SEO 未起。嗰段時間嘅工作係為三個月後鋪路。

---

# 仲有一件事

[`docs/market-check.md`](docs/market-check.md) 入面有一個假設我**證實唔到**：舊帖係咪真係冇人好好答。

我嘅搜尋工具索引 Reddit 索引得差,所以呢個我當時唔應該當事實講。

**花 10 分鐘自己查**（步驟喺 `market-check.md`）。10 條帖入面 5 條以上係「睇你用嚟做咩」呢類廢答案 → 你個表有價值。

花咗咁多功夫,值得確認個假設先落下一步。
