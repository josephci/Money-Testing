# 抓資料工具包

**用途**：客俾一條網址 → 你出一個 Excel 表。

**你唔使寫 code。** 每單只需要改一個設定檔嘅幾行字。

---

## 裝一次（只做一次）

```bash
pip install requests beautifulsoup4 openpyxl
```

如果話 `pip: command not found`,試 `pip3 install ...`。

---

## 每單客做三步

### 第 1 步 — 睇下應該填咩

```bash
python3 scrape.py --inspect "客俾你嗰條網址"
```

佢會吐返類似咁：

```
ok robots.txt allows this page.

Likely row_selector values — the one matching the number of items you
can see on the page is the right one:

  row_selector = "div.product-card"      (4 matches)
        h2.title                     -> Cordless Drill
        span.price                   -> $129
        a@href                       -> /item/1
        img@src                      -> /img/1.jpg
```

**點睇：**

- `(4 matches)` = 呢版有 4 件貨。**揀嗰個數字同你喺網頁上面數到嘅一樣嘅。**
- 下面縮咗入嘅幾行 = 每件貨入面有咩,`->` 右邊係真實抽到嘅嘢

### 第 2 步 — 開一個設定檔

複製 `jobs/example.toml`,改名做客個名,例如 `jobs/client-a.toml`,然後把上面抄落去：

```toml
url = "客俾你嗰條網址"
row_selector = "div.product-card"      # ← 抄第 1 步嗰個

[columns]
名稱 = "h2.title"                       # ← 左邊係 Excel 欄名,你自己改
價錢 = "span.price"
連結 = "a@href"

[options]
pages = 5                              # 抓幾多版
page_param = "?page={n}"               # 第 2 版點砌 URL
delay_seconds = 2
output = "out/client-a.csv"
```

> **左邊嘅欄名你話事**,中英文都得 —— 客要咩就寫咩。
> **右邊一定要照抄** `--inspect` 吐出嚟嗰個。

### 第 3 步 — 跑

```bash
python3 scrape.py jobs/client-a.toml
```

出兩個檔案喺 `out/`：`.csv` 同 `.xlsx`。**`.xlsx` 就係交俾客嗰個。**

---

## 點知第 2 版嘅 URL 點砌（`page_param`）

喺個網站撳「下一頁」,望住個網址點變：

| 網址變成 | `page_param` 填 |
|---|---|
| `site.com/list?page=2` | `"?page={n}"` |
| `site.com/list/page/2/` | `"page/{n}/"` |
| `site.com/list?p=2&sort=x` | `"?p={n}&sort=x"` |
| `site.com/list?offset=20`（每版 20 件） | ⚠️ 呢種算唔到,見下面 |

`{n}` 會自動變成 2、3、4…

**如果抓到中途變成 0 rows,工具會自動停,唔會出錯。** 咁樣代表已經抓晒。

---

## 出咗錯點算

工具嘅錯誤訊息會直接話你點做。以下係常見嗰幾個：

| 佢話 | 即係 | 你做咩 |
|---|---|---|
| `row_selector "..." matched nothing` | 揀錯咗個外殼 | 再跑一次 `--inspect`,揀第二個 |
| `These columns came out empty` | 有欄抽唔到嘢 | 嗰欄右邊嘅字填錯,對返 `--inspect` |
| `The job file has a typo` | 設定檔打錯 | 通常係漏咗引號 `" "` |
| `The site refused us (403)` | 網站封緊機械人 | **推返單客,做唔到** |
| `asking too fast (429)` | 抓得太快 | `delay_seconds` 調大到 5 |
| `Could not find repeating rows` | 個網頁用 JavaScript 砌出嚟 | **推返單客,做唔到** |

---

## ⚠️ 接單之前一定要檢查

### 1. 跑 `--inspect` 睇 robots.txt

```
ok robots.txt allows this page.        ← 可以做
!! robots.txt asks bots NOT to fetch   ← 推返單客
```

`robots.txt` 係網站寫明「畀唔畀機械人入」嘅檔案。佢話唔畀,你就唔好做。

> `i_have_permission = true` 呢個掣**只有喺客真係擁有嗰個網站、或者有書面授權**先可以開。唔好因為想接單而開佢。

### 2. 三種一定要推嘅單

| 類型 | 點解 |
|---|---|
| 要登入先睇到嘅嘢 | 通常違反服務條款,而且要客俾密碼你 —— 唔好掂 |
| 個人資料（email、電話、住址) | 好多地方有私隱法,罰得好重 |
| 網站明文禁止抓取 | 睇佢 Terms of Service |

**推單唔係蝕底。** 一單 $30 唔值得孭法律風險,而且做唔到而硬接,你會攞到差評。

**點推**（照抄）：

```
Thanks for reaching out. I checked the site and it blocks automated
access, so I'm not able to deliver this one reliably. I'd rather tell
you now than take the order and miss the deadline.

If you have another source for the same data, happy to take a look.
```

---

## 接到單之後嘅流程

```
1. 客傳條 URL 過嚟
      ↓
2. 跑 --inspect  ──► robots 唔畀 / 抓唔到 → 照上面推單
      ↓ 得
3. 抄設定檔,跑一次(先 pages = 1 試)
      ↓
4. 開個 .xlsx 望一眼 ← ⚠️ 唔好慳呢步
      ↓
5. pages 改返做全部,再跑
      ↓
6. 交 .xlsx
```

**第 4 步唔可以跳。** 自己開嚟望一眼有冇亂碼、有冇空欄、數字啱唔啱 —— 呢個就係你同一個爛 script 嘅分別,亦係你收到 5 星嘅原因。

---

## 交貨之後

睇 [`FIVERR.md`](FIVERR.md) —— 入面有 gig 點寫、定幾錢、同客講咩,全部現成文字。
