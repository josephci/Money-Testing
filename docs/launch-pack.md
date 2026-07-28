# 出街文字包（貼上就用得）

所有你需要寫嘅字,我寫晒喺呢度。你嘅工作係**貼上 + 改數字**。

> 🚨 **所有百分比同價錢都係示範數據算出嚟嘅。**
> 入完真價之後,跑 `python3 scripts/build.py` 睇返真實數字,**逐個換返**。
> 貼錯數字比唔貼更差 —— 呢個圈嘅人會即刻捉到,而你只有一次第一印象。

---

# 1. 網站身份（目錄提交用）

### 名
```
Battery Prices
```

### 一句話（各種長度,目錄表格會限字數）

**50 字元以內**
```
Cordless tool batteries ranked by cost per watt-hour.
```

**100 字元以內**
```
Every cordless power tool battery, ranked by real cost per watt-hour. Amp-hours lie across voltages.
```

**160 字元以內（meta description 長度）**
```
Compare every cordless tool battery by real cost per watt-hour. DeWalt, Milwaukee, Makita, Ryobi and Bosch normalised to nominal voltage, so the comparison is honest.
```

**300 字元以內**
```
"20V MAX" and "18V" packs are electrically identical — five cells, 20V peak, 18V nominal. That makes amp-hours useless for comparing across brands and voltages. Battery Prices converts every pack to watt-hours using nominal voltage, divides multi-packs by their total energy, and ranks the lot by price per watt-hour.
```

### 分類同標籤
```
Categories: Tools, Price Comparison, Shopping, DIY, Home Improvement
Tags: power tools, batteries, price comparison, dewalt, milwaukee, makita, ryobi, bosch, cordless, watt-hours
```

---

# 2. 目錄提交

**呢個係你嘅最高價值動作 —— 填表,冇人會同你講嘢。**

一個週末,目標 30–50 個。搜以下字眼搵目錄：

```
"submit your startup"
"submit your tool" directory
"add your site" free directory
best free tool directories 2026
```

### 每次都會問嘅嘢（上面已經備定）

| 欄位 | 用邊段 |
|---|---|
| Name | Battery Prices |
| URL | 你嘅域名 |
| Tagline | 50 字元版 |
| Short description | 160 字元版 |
| Long description | 300 字元版 |
| Category | Tools / Price Comparison |
| Tags | 上面標籤列 |
| Logo / image | `assets/og.png` |
| Email | 開個專用 email,唔好用私人嗰個 |

### ⭐ GitHub awesome 清單（發 PR,唔係社交）

搜 `awesome tools github`、`awesome diy`、`awesome price comparison`,搵到相關清單就發 PR 加一行：

```markdown
- [Battery Prices](https://your-domain.com) — Cordless power tool batteries ranked by real cost per watt-hour (normalised to nominal voltage).
```

**呢個係寫 code,唔係發帖。** 對你嚟講應該係最舒服嘅一種。

---

# 3. Reddit 貼文草稿

> ⚠️ **貼之前一定要做嘅三件事**
> 1. 睇該 sub 嘅 self-promotion 規則（好多要 flair、要 karma、或者禁連結）
> 2. **唔好同一日貼晒**,分開幾日
> 3. **每個帖改到唔同** —— 下面已經寫到唔同,唔好合併

## r/MilwaukeeTool

**標題**
```
I worked out the cost per watt-hour of every M18 pack — the XC5.0 2-pack is the best value by a wide margin
```

**內文**
```
I kept going back and forth on which M18 battery is actually worth buying, so I
put every pack in a spreadsheet and worked out what a watt-hour actually costs.

Wh = 18V nominal x Ah, and for multi-packs you divide by the total energy of
the whole kit rather than one pack.

What surprised me:

- The XC5.0 2-pack works out cheapest per watt-hour
- The HD12.0 is one of the *worst* per watt-hour despite being the flagship
- Two mid-size packs beat one big pack on both cost and total energy

The full table is here, sorted by $/Wh: [link to /milwaukee-m18/]

Happy to add anything I've missed — I've only got the packs that are widely
available right now.
```

## r/Dewalt

**標題**
```
"20V MAX" is 18V. Here's what that means when you're comparing batteries
```

**內文**
```
Most people here know 20V MAX is a marketing number — five cells at 4.0V peak,
which settle to 3.6V nominal, so 18V, same as M18 and LXT.

What I hadn't seen anyone do is follow it through to what you should actually
compare. If the voltage label doesn't mean anything, amp-hours don't either
once you're crossing between 12V MAX and 20V MAX. Watt-hours do:

  Wh = 18V x Ah

DCB205 is 5.0Ah, so 90Wh — and that's exactly what DeWalt's own spec sheet says,
because manufacturers rate energy at nominal.

I ran every 20V MAX and FlexVolt pack through that and sorted by cost per
watt-hour: [link to /dewalt-20v-max/]

The 2-packs come out well ahead. The biggest packs are the worst value per Wh.
```

## r/Tools（全站）

**標題**
```
Every cordless tool battery, sorted by actual cost per watt-hour (DeWalt, Milwaukee, Makita, Ryobi, Bosch)
```

**內文**
```
The "$10 per amp-hour" rule of thumb that gets repeated here breaks as soon as
you compare across voltages, because an amp-hour measures charge, not energy.

An M12 6.0Ah pack is 64.8Wh. An M18 5.0Ah pack is 90Wh. The M12 has *more*
amp-hours and 39% less energy. Judged on $/Ah you'd pick the wrong one.

So I built a table of every pack I could find, converted to watt-hours using
nominal voltage (18V for 20V MAX / M18 / LXT, 10.8V for the 12V-class stuff),
divided multi-packs by total energy, and sorted by $/Wh: [link]

Cross-brand, Ryobi comes out cheapest per watt-hour. Within every brand, the
2-packs beat the singles and the flagship high-capacity packs are the worst
value.

Prices move, so it updates. Filters are in the URL if you want to link someone
straight to their own battery system.
```

## Show HN

**標題**（HN 標題要短,唔好加 emoji 同感嘆號）
```
Show HN: Disk Prices, but for power tool batteries
```

**第一個留言（自己貼,HN 嘅慣例）**
```
Cordless tool batteries are sold on amp-hours, which can't be compared across
voltages — an amp-hour is charge, not energy. Worse, the two big 18V-class
systems print different numbers for the identical pack: DeWalt advertises the
20V peak-off-charger reading, Milwaukee and Makita advertise the 18V nominal.
Same five cells either way.

So everything here is converted to watt-hours at nominal voltage, multi-packs
are divided by total energy, and the whole lot is sorted by $/Wh.

It's a static site — build script inlines the data into one file per page, no
JS framework, no requests at runtime. Prices are entered from a CSV on a
schedule; the Amazon API needs qualifying sales before they'll issue a key,
which is an awkward chicken-and-egg for a new site.

Affiliate links, disclosed in the footer. Ranking is purely $/Wh and doesn't
know or care about the links.
```

---

# 4. 舊帖回覆模板

**呢個係怕羞路線嘅主力。** 唔係發新帖,係答已經有人問過嘅問題。

搜法（喺 Reddit 內部搜,唔好靠 Google）：

```
r/Tools           "which battery"  "best value"  "worth it"
r/MilwaukeeTool   "which battery"  "HD12.0 worth"
r/Dewalt          "which battery"  "flexvolt worth"
r/electricians    "battery"  "which"
```

### 模板 A —— 有人問「邊隻電池抵」

```
Quick way to settle this: convert to watt-hours. Wh = nominal volts x Ah
(18V for M18 / 20V MAX / LXT — they're all the same 18V nominal), then divide
the price by that.

For [their platform] the [X] comes out cheapest at $[Y]/Wh. Table of all of
them here if it helps: [link to their platform page]
```

### 模板 B —— 有人問「20V 好過 18V？」

```
They're the same battery. Five cells: 4.0V each fully charged (5 x 4 = 20,
what DeWalt prints) and 3.6V nominal (5 x 3.6 = 18, what Milwaukee and Makita
print). Under load both sit at 18V.

Which means the useful comparison is watt-hours, not the voltage or the
amp-hours: [link to /20v-max-vs-18v/]
```

### 模板 C —— 有人問「大容量電池抵唔抵」

```
Usually not, per watt-hour. Flagship high-capacity packs carry a premium —
two mid-size packs normally beat one big one on both cost and total energy.

[Their platform] sorted by $/Wh: [link]
```

**用法規則：**

- ✅ 先答問題,連結擺最後
- ✅ 每次改到唔同,唔好逐字複製
- ❌ 唔好喺答案入面提「我做嘅網站」—— 講數字就夠
- ❌ 唔好一日答十條

---

# 5. Email 草稿

## 俾 ToolGuyd 編輯

**主旨**
```
Cost-per-watt-hour table for tool batteries — follow-up to your Wh vs Ah article
```

**內文**
```
Hi,

Your article on watt-hours vs amp-hours is the piece I kept sending people
when they asked which battery was better value, so I built the table that
article implies: every cordless pack I could find, converted to Wh at nominal
voltage, multi-packs divided by total energy, sorted by $/Wh.

[link]

Two things that fell out of it that might interest you:

- The "$10 per amp-hour" rule that circulates in forums inverts as soon as you
  cross voltage classes. M12 6.0Ah is 64.8Wh; M18 5.0Ah is 90Wh.
- Within every brand, the flagship high-capacity packs are the worst value per
  watt-hour, and 2-packs are consistently the best.

No ask — just thought it might be useful to you or your readers. Happy to add
any packs I've missed.

[your name]
```

**點解呢封得**：

- 提到佢**具體邊篇文**,證明你真係讀過
- 俾佢**兩個佢可以直接用嘅發現**,唔係求佢幫忙
- **「No ask」** —— 冇要求,壓力最低,回覆率最高

## 俾 YouTube 工具頻道

```
Subject: Battery value data if it's ever useful for a video

Hi [name],

I built a table that converts every cordless tool battery to cost per
watt-hour — nominal voltage, multi-packs divided by total energy:

[link]

The thing that surprised me: within every brand the flagship high-capacity
packs are the worst value per watt-hour, and the 2-packs are the best. Runs
against what the marketing pushes.

Free to use if it's ever useful for a video. No ask.

[your name]
```

---

# 6. 貼文之前最後檢查

- [ ] 所有數字換成真實數據算出嚟嘅
- [ ] 連結指向**對應嘅平台頁**,唔係首頁
- [ ] 該 sub 嘅 self-promotion 規則睇過
- [ ] 帳戶唔係全新（好多 sub 有 karma / 帳齡門檻）
- [ ] Footer 嘅聯盟披露顯示緊
- [ ] 手機打開睇過一次
