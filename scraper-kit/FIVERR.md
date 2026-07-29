# Fiverr 實戰包

現成文字,貼上就用得。你唔使寫任何嘢。

**目標：$50/月 = 2 單 $25,或者 2 個月費客。**

> ⚠️ **落手前讀 [`../docs/ai-saturation.md`](../docs/ai-saturation.md)。**
> Fiverr 買家按年跌 13.6%,賣家 6 年多咗 4 倍,而「簡單資料處理」正正係被 AI 壓價最勁嗰類。
> **你嘅優勢唔係識做（人人都識),係識推單、會核對、肯長期負責。**
> 下面全部文字已經按呢個定位寫。

---

# 1. 開 gig（一次過,約 1 個鐘）

## Gig 標題

```
I will extract data from any website into a clean Excel spreadsheet
```

## 分類

`Data` → `Data Entry` 或者 `Data Processing`

## 標籤

```
web scraping, data extraction, excel, csv, data entry
```

## 描述（照抄）

```
I'll turn a web page into a clean, ready-to-use spreadsheet.

Send me the URL and tell me which fields you need — product names,
prices, links, images, listings, directory entries, whatever is on the
page — and you get back a tidy .xlsx and .csv.

WHAT YOU GET
- Clean Excel file with the columns you asked for
- CSV as well, for importing anywhere
- Duplicates removed
- Delivered within 24 hours

HOW IT WORKS
1. Send me the page URL
2. Tell me which fields you want
3. I check the site is scrapable and confirm before starting

PLEASE NOTE
I only work with publicly accessible pages. I don't scrape sites that
require a login, sites that block automated access in their robots.txt,
or personal data such as emails and phone numbers.

If your page turns out not to be workable I'll tell you straight away
rather than take the order and miss it.

Not sure if your page works? Message me the link first — I'll check for
free.
```

**⚠️ 呢段有三處係特登寫嘅,唔好刪：**

| 句 | 點解 |
|---|---|
| 「I'll tell you straight away rather than take the order and miss it」 | 大部分用 AI 嘅賣家問完 AI「做唔做到」就接單,然後撞正 JS 網站交唔到貨。**肯講「做唔到」係而家最強嘅信任訊號** |
| 「I don't scrape logins / personal data / robots-blocked sites」 | 喺一個人人講「乜都做到」嘅市場,**講清楚你唔做乜反而突出** |
| 「Message me the link first — I'll check for free」 | 你可以喺落單前篩走做唔到嘅,唔會攞差評 |

## 定價

| 級別 | 價 | 內容 |
|---|---|---|
| Basic | **$15** | 1 版,最多 5 欄 |
| Standard | **$35** | 最多 10 版,最多 10 欄 |
| Premium | **$60** | 最多 50 版 + 資料清理 |

**新帳戶就係要定平。** 頭 3 個評價比頭 3 舊錢重要好多 —— 有咗評價先加價。

Fiverr 抽 20%,所以 $35 你實收 $28。**2 單 Standard ≈ $56 = 達標。**

## 作品集

跑 `jobs/example.toml`,將出到嗰個 `.xlsx` 截圖,擺上去做 gig 圖片。

---

# 2. 客 message 你嗰陣（現成回覆）

## 有人問「我呢版做唔做到？」

```
Sure, send me the link and I'll check it now.
```

跑 `python3 scrape.py --inspect "條 URL"`,然後：

**做到 →**
```
Yes, that page works. I can pull [名稱, 價錢, 連結] — about [N] items
per page. How many pages do you need?

Standard package ($35) covers up to 10 pages. Happy to start whenever.
```

**做唔到 →**
```
I checked — that page loads its content with JavaScript / blocks
automated access, so I can't pull it reliably. I'd rather tell you now
than take the order and miss the deadline.

If you have another page with the same data, send it over and I'll look.
```

## 落咗單之後

```
Thanks! Starting now. I'll have the file to you within 24 hours.

Just to confirm the columns: [逐個列出]. Let me know if you want
anything else on there.
```

## 交貨

```
Done — file attached (.xlsx plus .csv).

[N] rows from [M] pages. I removed [X] duplicates. [如果有嘢要講就講,
例如：A few listings had no price shown on the page, so those cells are
blank rather than guessed.]

Let me know if you'd like anything adjusted.
```

**「有幾行冇價錢,我留空冇亂估」** —— 呢種老實嘅備註係攞 5 星嘅原因。

---

# 3. ⭐ 轉月費（$50/月 嘅關鍵）

**第一單交完就提,唔好等第二單。**

一次性單價會繼續俾 AI 壓,**月費客係你唯一唔受壓價影響嘅收入** —— 亦係 AI 助手用家做唔到嘅嘢（佢哋交完就走,個網站改版就冇人修）。

加呢一句：

```
One thing that might be useful — this page changes over time. I can run
this automatically every week and send you the updated sheet, so you
always have current data without having to ask.

That's $15/month. No pressure — just mention it if you want it set up.
```

## 點解呢句會 work

- 佢已經俾過你錢一次 → 信任已建立
- 你解決緊一個佢真實有嘅問題（資料會過時)
- $15 對做生意嘅人嚟講唔使諗
- **「No pressure」** 令你唔使推銷,亦令佢冇壓力

## 數學

| 客 | 月費 | 每月 |
|---|---|---|
| 2 個 | $15 | **$30** |
| 2 個 | $25 | **$50** ✅ |
| 4 個 | $15 | $60 |

**2 個客就掂。**

## 之後點做

設定檔已經喺 `jobs/` 度,所以每星期你只需要：

```bash
python3 scrape.py jobs/client-a.toml
```

跑一次,望一眼,傳俾佢。**每個客每星期 5 分鐘。**

⚠️ Fiverr 唔准引客離開平台交易。**經常性服務就繼續喺 Fiverr 度收**（佢有 Subscription 功能),唔好諗住轉去私下交易 —— 會封帳戶。

---

# 4. 頭一個月

| 週 | 做咩 | 時間 |
|---|---|---|
| 1 | 開 gig。跑 `jobs/example.toml` 截圖做作品集 | 1 小時 |
| 1 | 喺 Fiverr 搜 `web scraping`,睇頭 10 個 gig 點寫、幾錢 | 30 分鐘 |
| 2–4 | 等單。有人問就用上面嘅回覆 | 每次 10 分鐘 |
| 有第一單 | **做到最好**。頭 3 個評價決定之後有冇單 | 1–2 小時 |
| 交貨後 | 提月費 | 1 分鐘 |

**老實嘅預期**：新帳戶頭一單通常要等 **2–6 個星期**。呢段時間唔係你做錯嘢,係排名要時間。

---

# 5. 五件唔好做嘅事

| 唔好 | 點解 |
|---|---|
| 接你未 `--inspect` 過嘅單 | 交唔到貨 = 差評 = 之後冇單 |
| 為咗接單而開 `i_have_permission` | 法律風險,唔值 $30 |
| 一開始定 $50+ | 新帳戶冇評價,冇人肯試 |
| 同人鬥平 | 你鬥唔過 AI 農場。鬥可靠 |
| 淨係擺 Fiverr | Fiverr 買家跌緊。**同一份 gig 順手擺埋上 Upwork** |
| 承諾 12 小時內交 | 做唔到就死。寫 24 小時,15 小時交,客會驚喜 |
| 交貨前唔開個 .xlsx 望 | **最常見嘅低級失手** |

---

# 6. 記住個界線

**工具可以幫你做嘢。工具唔可以幫你答客。**

所以：**只接你 `--inspect` 過、確認做到嘅單。**

推一單做唔到嘅單,成本係零。硬接一單做唔到嘅,成本係你個帳戶。

呢個唔係限制 —— 呢個就係點解你會攞到 5 星:**你只交你交得到嘅嘢。**
