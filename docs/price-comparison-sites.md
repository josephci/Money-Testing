# diskprices.com 模式：可行性分析 + 市場空白地圖

> 本文所有市場飽和度都係 2026-07 實際搜尋查證,唔係憑印象。價格/佣金率會變,落手前自己再查一次。

---

# Part 1：有冇數為？—— 有,而且好過廣告好多

## 真實數據基準

diskprices.com 嘅公開數字：

| 項目 | 數字 |
|---|---|
| 月收入 | **約 US$5,000** |
| 月訪客 | **約 80,000** |
| **每個訪客價值** | **約 US$0.0625** |
| 流量來源 | 直接訪問 52%、自然搜尋第二 |
| 國際站(非美國)佔比 | 約一半收入 |

## 換算返你嘅目標

**$100/月 ÷ $0.0625 = 每月約 1,600 個訪客 = 每日 53 個。**

對比之下,同樣 $100/月：

| 模式 | 需要月流量 | 效率 |
|---|---|---|
| **高單價聯盟比價** | **1,600** | 基準 |
| AdSense 廣告 | 10,000–50,000 | 差 6–30 倍 |

**呢個就係核心答案：有數為,而且效率完勝廣告。**

原因好簡單 —— 一部 $200 硬碟 3% 佣金 = $6。你要 3 萬人睇廣告先賺到 $6。

⚠️ 保守修正：diskprices 做咗好多年、多地區、單價高。新站喺單價低啲嘅品類,每訪客可能只有 $0.02–0.04 → **實際需要 2,500–5,000 月訪客**。一樣係細數字。

---

# Part 2：⚠️ 三個一定要知嘅實務陷阱

呢部分好多人做到一半先發現,直接勸退。

### 1. Amazon PA-API 有雞同蛋問題 ⭐最致命

要攞產品資料 API,你要**先有銷售**：

- **初次申請**：加入聯盟計劃後 180 日內要有 **3 單**合資格銷售
- **維持存取**：之後要持續有單。網上報告嘅門檻由「30 日內 3 單」到「30 日內 10 單」都有,而且 Amazon 收緊咗
- **冇單 → API key 被收回 → 你個站即刻冇資料 → 更加冇單**（死亡螺旋）

**解決方法**：起步階段**唔好靠 API**。用人手整理嘅資料、CSV、或者其他零售商嘅聯盟資料源,做出第一批銷售,再申請 API。

好消息係：你嘅目標 $100/月 ≈ 每月 20 單,過到門檻之後就穩定。**但頭三個月係硬關卡。**

### 2. 佣金率係 Amazon 話事,隨時改

- 電子產品/電腦類大約 **3%**(部分子分類 4.5%,亦有低至 1%)
- Amazon **每季**(3/6/9/12 月)更新一次費率表
- 2020 年佢試過一夜之間大幅削減多個分類 —— 好多聯盟站收入即刻腰斬

**你係喺租 Amazon 嘅生意,唔係擁有自己盤生意。** 呢個風險要接受先好入場。

### 3. 條款限制

- ⚠️ **價格快取唔可以超過 24 小時**,要顯示「截至某時間」
- ⚠️ 必須**披露**聯盟關係(法律要求 + Amazon 要求)
- ⚠️ 唔可以喺 email、PDF 入面放聯盟連結

---

# Part 3：飽和地圖（實查結果）

**壞消息：diskprices 個故事太紅,所有「明顯」嘅方向都俾人做晒。**

| 方向 | 狀況 | 已存在嘅玩家 |
|---|---|---|
| 硬碟 $/TB | ❌ 死 | diskprices 壟斷 |
| 便攜電站 $/Wh | ❌ 死 | WhichWatts(500+ 型號)、GearScouts |
| 蛋白粉 $/g 蛋白質 | ❌❌ **極死** | 起碼 8 個站：CompareProteinPrices、SupplementMath、ProteinMath、ProteinFinder… |
| 雲端 GPU $/小時 | ❌ 死 | getdeploying、gpucloudprices、Spheron |
| 空氣清新機 $/CADR | ❌ 死 | HouseFresh(130 型號)、Oransi、airpurifiercalculators |
| PC 零件 | ❌ 死 | PCPartPicker |
| Amazon 價格歷史 | ❌ 死 | CamelCamelCamel、Keepa |
| 太陽能板 $/watt | 🟡 半死 | EnergySage 等,但係做**報價**唔係做**產品比價** |

**規律**：呢啲全部都係**程式員自己會買嘅嘢**。因為 diskprices 喺 HN / IndieHackers 太出名,每個 dev 都試過做自己熟嗰個品類。

👉 **所以剩低嘅機會,喺程式員唔會踏足嘅市場。**

---

# Part 4：⭐ 最重要嘅發現 —— 計算機 ≠ 實時排序表

查嘅過程搵到一個好值錢嘅分別。搜某個品類嘅「$/單位」,通常搵到三種嘢：

| 類型 | 例子 | 做嘅難度 | 有冇護城河 |
|---|---|---|---|
| 📝 **內容文** | 「啞鈴幾錢一磅？」 | 極低 | 冇,SEO 垃圾滿地 |
| 🧮 **計算機** | 「入你自己個價,幫你計」 | 低 | 冇,靜態網頁 |
| 📊 **實時排序表** | **diskprices** —— 真實在售商品,按 $/單位 即時排序 | **中高** | **有** |

**大部分品類有前兩種,冇第三種。**

點解？因為頭兩種一個下晝做完,第三種要真資料管道、要正規化、要日日更新、要處理來源改版。

> 🎯 **搵空白嘅公式**：
> 搜 `"[品類] price per [單位]"`。
> 如果只搵到**計算機同 blog 文**,搵唔到**可以即刻買、按單位價排序嘅真實商品表** —— 咁就係空白。

呢條公式你可以無限重用。

---

# Part 5：實查後仲有空間嘅方向

### 1. ⭐ 電動工具電池 $/Wh（實查：有空白）

**盯咩**：Makita / DeWalt / Milwaukee / Bosch 各型號電池,按 $/Wh 或 $/Ah 排序,分品牌分電壓。

**現況**：ToolGuyd 有**文章**討論邊隻抵,Home Depot 有得逐個睇 —— **但冇實時排序表**。

**點解好**：
- 市場超級混亂：Ah、V、Wh 三個單位互相溝亂,消費者計唔掂
- **品牌鎖定** → 用家一世買同一個系統 → 重複購買 + 重複到訪
- 買家係裝修佬、DIY 佬 —— **完全唔識 code**
- 單價 $80–300,Amazon 工具類約 3%
- 平台常年做促銷,價格波動大 → 直接訪問回頭率高

**評分：8/10**

### 2. ⭐ 健身重量片 / 啞鈴 $/lb（實查：有空白）

**盯咩**：槓片、啞鈴、壺鈴,按每磅價格排序。

**現況**：一大堆「啞鈴幾錢」嘅內容文（GarageGymReviews 等）,**冇一個實時排序表**。

**點解好**：
- $/lb 係呢個圈**本身就通用**嘅術語(行內公認 $1.40–$3/lb 算合理) —— 需求已驗證
- 重貨,運費差異大 → 「連運費計嘅 $/lb」係大痛點,亦係你嘅差異化
- r/homegym 社群極度活躍,見到好嘢會瘋狂分享(呢個就係 diskprices 起飛嘅方式)
- 單價 $100–500

**評分：7/10** — 扣分位：好多主流品牌(Rogue、Titan)唔行 Amazon,要駁多個聯盟計劃。

### 3. 🟡 打印機墨水 每頁成本（實查：半空白）

**現況**：**計算機一大堆**(要你自己入數),但冇「全部墨盒按每頁成本排序」嘅表。

**點解有機會**：
- XL / XXL / 相容裝 嘅頁數標示混亂到出名,消費者永遠計錯
- **極高重複購買**
- 買家零技術

**扣分**：單價低($30–60)→ 佣金細,要更多流量。

**評分：6/10**

### 4. 🟡 被忽略嘅地區市場

diskprices **一半收入嚟自非美國站**。

**意思係：同一個 idea,喺一個未被覆蓋嘅地區/語言市場,可以重做一次。** 亞洲市場嘅比價工具遠遠冇歐美咁飽和。

⚠️ 但要確認嗰個地區有冇可用嘅聯盟計劃 —— 呢個係成敗關鍵,做之前一定要查。

---

# Part 6：呢個模式 vs 之前嘅監察 SaaS

| | 比價聯盟站 | 監察 SaaS |
|---|---|---|
| 要唔要客俾錢 | ❌ 免費用,零購買阻力 | ✅ 要說服 4 個人 |
| 客服負擔 | 幾乎冇 | 有 |
| 主要瓶頸 | **流量** | **搵客** |
| 收入控制權 | ❌ Amazon 話事 | ✅ 你話事 |
| 起步門檻 | ⚠️ PA-API 要先有 3 單 | 冇 |
| 達 $100/月 | 約 1,600–5,000 月訪客 | 4 個客 |
| 複利效應 | ✅ 高(直接訪問 52%,會回頭) | ✅ 高(訂閱續期) |

**兩者唔衝突,而且思路一致**:都係「一次建好、資料自動更新、你唔使逐單處理」。

---

# Part 7：建議

**如果你要揀一個,我推薦「電動工具電池 $/Wh」。**

理由:

1. ✅ **實查證實冇實時排序表**(得文章同零售商目錄)
2. ✅ 單位混亂(Ah vs V vs Wh)= 真痛點,而且**正規化呢件事有技術難度** = 護城河
3. ✅ 品牌鎖定 → 重複購買 → 直接訪問回頭客(diskprices 52% 流量嘅來源)
4. ✅ 買家完全唔識 code
5. ✅ 單價夠高($80–300),Amazon 工具類約 3%

## 起步次序（避開 PA-API 死亡螺旋）

```
Week 1-2  人手整理 100-200 隻電池嘅規格 → 一個靜態排序表
          （唔使 API,唔使自動化,先驗證有冇人要）
Week 3    出街：r/Tools、r/DIY、ToolGuyd 留言區、HN
          目標：頭 3 單合資格銷售
Week 4+   有咗 3 單 → 申請 PA-API → 自動化價格更新
之後      加地區站（記住：一半收入嚟自國際）
```

**呢個次序好重要** —— 先驗證再自動化,同時解決咗 API 門檻問題。

## 最後提醒

- ⚠️ 你係**租 Amazon 嘅生意**。佢改費率你冇得傾。所以：唔好 all-in,當佢係其中一條腿
- ⚠️ 呢個係**流量遊戲,唔係技術遊戲**。個站兩個週末做得完,之後 90% 精力係搵人用
- ✅ 但好處係：**冇客服、冇銷售、冇退款**,而且直接訪問會累積

---

## 資料來源

- [Diskprices.com makes $5k/month with affiliate marketing — Hacker News](https://news.ycombinator.com/item?id=39066480)
- [Interview with the founder of Disk Prices — BoringCashCow](https://boringcashcow.com/interview/interview-with-the-founder-of-disk-prices)
- [diskprices.com Traffic Analytics — Similarweb](https://www.similarweb.com/website/diskprices.com/)
- [Amazon Affiliate Commission Rates 2026 by Category](https://www.youfiliate.com/blog/amazon-affiliate-commission-rates)
- [Amazon PA-API "AssociateNotEligible" Error: Is There a New 10-Sales Rule?](https://www.keywordrush.com/blog/amazon-pa-api-associatenoteligible-error-is-there-a-new-10-sales-rule/)
- [Amazon Product API (PA-API) in 2026: Restrictions and Alternatives](https://dev.to/agenthustler/amazon-product-api-pa-api-in-2026-restrictions-alternatives-and-web-scraping-4l35)
- [WhichWatts — Compare 500+ Power Stations by Cost Per Watt](https://whichwatts.com/)
- [HouseFresh Air Purifier Comparison Tool](https://housefresh.com/air-purifier-comparison-tool/)
- [Compare Protein Prices](https://compareproteinprices.com/)
- [H100 Cloud Pricing: Compare 48+ Providers — GetDeploying](https://getdeploying.com/gpus/nvidia-h100)
- [Comparing Power Tool Battery Specs – Watt-Hours vs Amp-Hours — ToolGuyd](https://toolguyd.com/cordless-power-tool-battery-watt-hours/)
- [How Much Do Dumbbells Cost? — Horton Barbell](https://hortonbarbell.com/how-much-do-dumbbells-cost/)
