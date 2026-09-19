# 寫 App 推上 App Store —— 飽和咗未?仲有咩有肉食?

（2026-09 查證）

你問咗兩件事,而第一件嘅答案會決定第二件：

1. App 市場係咪飽和晒?
2. 仲有咩未飽和而有肉食?

> ⭐ **先講結論：App Store 唔係「飽和」,係「集中」。而呢兩個字嘅分別,決定咗你應唔應該行呢條路。**
> **而你自己嗰句「要搵潛在有需求嘅人」—— 呢句就係全部答案,數據完全站喺你嗰邊。**

---

# Part 1：App Store 2026 實況

## 硬數字

| | |
|---|---|
| App Store 上嘅 app | **約 220 萬**（Apple 2025 年底數）／第三方爬蟲約 240 萬 |
| **超過 90% 收入** | 去咗**排頭 1% 嘅 app** |
| **10 個新 app 有 8 個** | **一世都突破唔到 US$10,000** |
| 訂閱收入 | 頭 10% 嘅 app 食咗 **94.5%** |
| 下載來源 | 60% 嚟自搜尋 —— **但排名睇 review 數同 ASO 預算** |
| 全球 Day-30 留存中位數 | **5.4%** |
| 一個實例 | 有 indie 出咗 8 個 app,扣完 Apple 之後合共收到 **US$1,464** |

> 佢自己總結嗰句值得抄低：
> **「Marketing beats code. Every time.」**

## ⭐ 但「集中」同「飽和」唔同 —— 呢個分別好重要

**飽和** = 需求已經被滿足晒,你入去冇位。
**集中** = 需求仲喺度,但**分發渠道係贏家通吃**。

App Store 係第二種。**唔係 220 萬個 app 同你爭同一班用戶** —— 係你根本**冇渠道俾人見到你**。

呢個同 repo 入面 `other-options.md` 講過嘅分類完全對得上：

| | App Store | Fiverr／直接賣 |
|---|---|---|
| 平台類型 | **瀏覽型** | **招聘型** |
| 買家狀態 | 路過 | **已經決定要俾錢** |
| 你要做 | 喺 220 萬個入面被搵到 | 回覆一個搵緊你嘅人 |

**Chrome Store 嗰組數（70.4% 插件 ≤100 用戶,中位數 18 個用戶）同呢度係同一個故事。**

---

## 💀 對住你個目標,先計清楚條數

### 走 App Store

| | |
|---|---|
| Apple 開發者帳號 | **US$99／年**（未賺一蚊先付） |
| Apple 抽成（小型企業計劃） | 15% |
| 要**淨袋** US$240（一年 Pro） | 要毛收入 **US$399／年** ≈ $33／月 |
| 即係 | $2.99／月訂閱 × **11 個長期訂戶** |
| 要淨袋 US$2,400（一年 Max 20×） | **82 個訂戶** |

⚠️ 仲要留意 **Day-30 留存中位數 5.4%** —— 要維持 11 個長期訂戶,你上游要幾多下載,自己諗。

### 同一個 idea,做成 web 直接賣

| | |
|---|---|
| 上架費 | **$0** |
| 抽成 | Stripe 約 3% |
| 要淨袋 US$240／年 | $29／月 × **1 個客**（仲有找） |
| 要淨袋 US$2,400／年 | **7 個客** |

```
            一年 Pro           一年 Max 20×
App Store   11 個訂戶          82 個訂戶
直接賣      1 個客             7 個客
            ↑
      同樣嘅錢,差 11 倍人數
```

> **呢個唔係「App 做得差」,係「你俾咗 $99 去企喺一個冇人搵你嘅地方」。**

---

# Part 2：咁仲有咩有肉食?

## 先講一個好過癮嘅數字

> **7,880 間有收入數據嘅初創,MRR 中位數係約 US$136。**

**你個目標（$20–50／月）係低過中位數嘅。** 呢個唔係一個高難度目標 —— 難嘅唔係金額,係分發。

同埋：

> **73% 成功嘅 solopreneur SaaS,做嘅係「大公司懶得理嘅微型細分市場」。**

**呢句直接驗證咗你個直覺。**

---

## 📊 飽和 vs 未飽和（2026 實查）

### ❌ 已經死透

| 類別 | 實況 |
|---|---|
| **專案管理／task tracker** | **300+ 個「加咗 AI 嘅 to-do list」變體,絕大部分零評論** |
| 習慣追蹤、番茄鐘、記帳 | 同上,消費者工具最擠 |
| 通用生產力 | 你同 Notion、Apple 內置 app 爭 |
| 純 AI 包殼（ChatGPT wrapper） | 2023 年嘅機會,而家係紅海 |

### ✅ 仲有肉食（按數據）

| 方向 | 點解仲有肉 |
|---|---|
| ⭐ **垂直行業合規／監管工具**（醫療、法律、金融） | 有**死線**、有**罰則** —— 客戶係被逼要買 |
| ⭐ **付款追收 / dunning** | 毛利 70–90%,收入同客戶收入掛鈎 |
| **B2B 整合**（駁通兩個冷門系統） | 大公司唔會為咁細嘅市場寫 connector |
| **垂直工作流工具**（某一行嘅特定流程） | 定價高、流失率低,客當佢係必需品 |
| 窄範圍 AI 工具（唔係通用助手） | — |

> **垂直 micro SaaS 長期跑贏橫向工具：定得起價,而且流失率低,因為客當佢係工作流嘅一部分。**

---

## ⭐⭐ 最重要嗰個發現：呢啲數據驗證返你 repo 入面已經有嘅嘢

打開 [`docs/monitoring-directions.md`](monitoring-directions.md),你之前已經評過分：

| 方向 | 你評嘅分 | 2026 外部數據點名嘅高利潤類別 |
|---|---|---|
| **招標 / 政府採購公告監察** | **⭐ 8/8** | ✅ 合規／有死線類 |
| **監管 / 牌照 / 合規更新監察** | **⭐ 8/8** | ✅ **「垂直行業合規工具」—— 明確列為最賺錢嘅 micro SaaS 類別之一** |
| 資助 / 撥款截止監察 | 7/8 | ✅ 有死線類 |

**即係話：你唔需要搵新方向。你已經揀中咗 2026 年數據話最有肉嗰一格 —— 喺你查之前。**

---

# Part 3：🔧 飽和度自測（一個晚上跑得完）

唔好問我「呢個 niche 飽唔飽和」—— 用呢四格自己驗,因為答案會變,而方法唔會。

| # | 問題 | 想見到咩 | 🚩 危險訊號 |
|---|---|---|---|
| 1 | **有冇人喺度嘈?** 搜 `你個問題 site:reddit.com`、行業 forum、FB group | **同一條問題有人重複咁問** | 搜唔到人講 |
| 2 | **有冇人喺度賣緊?** | **有 2–5 個競爭者,但全部都幾爛** | **零競爭** |
| 3 | **佢哋收唔收錢?** | 已經有人肯每月俾錢 | 全部免費／開源 |
| 4 | **你講唔講得出嗰 11 個人喺邊?** | 講得出**具體地點**（某 forum／某目錄／某協會會員名單） | 「應該有人需要嘅」 |

## ⚠️ 第 2 格係最反直覺嗰個

**「零競爭」唔係空白,九成係冇錢賺。**

有人已經做緊而且做得唔靚 —— **呢個先係最好嘅訊號**：需求驗證咗,而你有位入。

## 🚩 死亡組合

```
冇人賣  +  冇人嘈  +  你講唔出去邊度搵人
                ↓
        呢個唔係「未飽和」
        呢個係「冇市場」
```

---

# Part 4：所以你應該點做

## ❌ 唔好由 App Store 開始

理由唔係「App 唔得」,係四個具體嘢：

1. **US$99／年先開始** —— 佔你第一年目標嘅 41%
2. **瀏覽型平台** —— 你冇分發,而分發正正係你最唔想做嗰樣
3. **ASO 鬥 review 數** —— 新 app 結構性輸
4. **11 個訂戶 vs 1 個客** —— 同樣嘅錢,難 11 倍

## ✅ 正確次序

```
① 揀一個「有死線 + 有罰則」嘅垂直市場
   （你已經評好分：招標監察 8/8、合規監察 8/8）
        ↓
② 跑上面四格測試 —— 一個晚上
   ⚠️ 第 4 格講唔出答案就換題目,唔好硬做
        ↓
③ 做成 web,唔好做 app。$0 上架費,可以賣俾公司
        ↓
④ 先人手交付、即刻收錢,之後先自動化
   （repo 主計劃已經係咁講）
        ↓
⑤ 真係有客而且佢哋要手機版 —— 嗰陣先俾嗰 $99
```

> **第 ⑤ 步先係 App Store 嘅正確位置：佢係「已經有客」之後嘅一個渠道,唔係攞第一個客嘅方法。**

---

## 一頁總結

| 問題 | 答案 |
|---|---|
| App 市場飽和咗未? | **唔係飽和,係集中。** 90% 收入去咗頭 1% |
| 消費者 app 仲有冇位? | ❌ 基本上冇（task tracker 有 300+ 個變體） |
| 咁邊度仲有肉? | ✅ **垂直行業合規／有死線嘅 B2B 工具** |
| 我個目標算唔算高? | **7,880 間初創 MRR 中位數 $136 —— 你個目標低過中位數** |
| 我應該寫 app 嗎? | **應該寫,但唔應該放 App Store 攞第一個客** |
| 我要搵新方向嗎? | **唔使。你 8/8 嗰兩個方向就係數據點名嗰格** |

---

## 資料來源

- [App Store Statistics 2026 — sqmagazine](https://sqmagazine.co.uk/app-store-statistics/) · [Apple App Store Statistics 2026 — expandedramblings](https://expandedramblings.com/index.php/itunes-app-store-stats/)
- [Why Indie iOS Apps Are Harder to Sustain in 2026 — Medium](https://ravi6997.medium.com/why-the-golden-age-of-indie-ios-apps-is-over-and-what-developers-must-do-now-8223542291fb) · [Indie iOS App Marketing Strategy 2026: An Honest Playbook — screenfast](https://screenfast.app/blog/indie-ios-app-marketing-strategy-2026)
- [App Store Fees Explained: What Apple and Google Really Take in 2026 — Week One Labs](https://weekonelabs.com/blog/app-store-fees-explained-2026)
- [The SaaS Niches That Are Underserved Right Now (According to Data, Not Hype) — DEV](https://dev.to/agenthustler/the-saas-niches-that-are-underserved-right-now-according-to-data-not-hype-3cjh)
- [15 Profitable Micro SaaS Ideas for Solo Founders in 2026 — MRR Story](https://www.mrrstory.com/blog/profitable-micro-saas-ideas-solo-founders-2026) · [How to Find Good Niche SaaS Ideas in 2026 — bigideasdb](https://bigideasdb.com/niche-saas-ideas-2026)
