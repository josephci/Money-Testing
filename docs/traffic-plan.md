# 流量計劃：由 0 到 $100/月

目標流量：**每月 1,600–5,000 訪客**（推算見 [`price-comparison-sites.md`](price-comparison-sites.md)）。

呢份係推廣計劃。**個站兩個週末做得完,之後 90% 精力係呢度。**

---

# Part 1：域名 —— 要,而且要「悶」

## 短答案：買,約 US$10–15/年,但唔好諗到咁creative

理由喺數據裏面：**diskprices 52% 流量係「直接訪問」**。

直接訪問嘅意思係 —— 有人**記得**個名,然後**打得出**。呢個就係全部要求。

所以域名唯一嘅任務係：**聽一次記得,講一次打得出。**

`diskprices.com` 唔係一個聰明名。佢係「品類 + prices」,悶到極點 —— 而佢正正因為咁贏。

## 命名規則

| ✅ 要 | ❌ 唔要 |
|---|---|
| 描述性（品類 + prices / deals / 單位） | 拼寫得出嘅雙關語 |
| 兩個字以內 | 三個字以上 |
| `.com` | `.io` `.xyz`（工人階層買家唔信呢啲） |
| 全細楷讀得出 | 連字符、數字 |

⚠️ 特別注意：你嘅買家係裝修佬,唔係科技人。**`.io` 對呢班人嚟講似詐騙網。** 呢個唔係小事。

## 候選名單

我喺呢個環境查唔到可用性（網絡政策擋咗 RDAP,curl 同 WebFetch 都 403）。**你要自己喺部機跑：**

```bash
for d in toolbatteryprices batteryperwh wattprices batterypricing \
         toolbatterydeals batterywatthours cheapestwh perwattprices \
         batteryvalue toolbattprices; do
  printf '%-22s ' "$d.com"
  code=$(curl -s -o /dev/null -w '%{http_code}' "https://rdap.verisign.com/com/v1/domain/$d.com")
  case $code in 404) echo AVAILABLE;; 200) echo taken;; *) echo "?? $code";; esac
done
```

（`rdap.verisign.com` 係 `.com` 註冊局嘅權威資料 —— 404 = 未註冊。比第三方查詢工具準,而且唔會偷你個名去搶註。）

**我推薦嘅次序**：
1. `toolbatteryprices.com` —— 最貼 diskprices 公式,SEO 同口耳相傳都最直接
2. `batteryperwh.com` —— 短,但 "Wh" 對非技術買家有認知門檻
3. `wattprices.com` —— 短又順口,但唔夠具體

⚠️ 如果 `.com` 全部被搶,**唔好退去 `.io`**。寧願用 `toolbatteryprices.net` 或者加一個字（`bestbatteryprices.com`）。

---

# Part 2：流量係三層,唔係一件事

新手嘅錯誤：以為推廣係「發一次帖」。實際上係三層疊上去,而**只有第三層係生意**。

```
第 1 層  社群爆發    一次過幾千訪客,兩星期後歸零
            ↓ 留低 backlink + 第一批書籤
第 2 層  SEO 長尾    3-6 個月開始,之後只升唔跌
            ↓ 持續帶新人入嚟
第 3 層  直接 + 回訪  ← diskprices 52% 喺呢層。呢個才係盤生意
```

**第 1 層唔係目標,係燃料。** 佢嘅作用係點燃第 2、3 層。好多人第一帖爆完就以為成功,兩個月後流量歸零就放棄 —— 因為佢哋冇做第 2 層。

---

# Part 3：第 1 層 —— 社群爆發（Week 3-4）

## ⭐ 最重要嘅一件事：唔好推廣個站,推廣個發現

| ❌ 死法 | ✅ 生法 |
|---|---|
| 「我做咗個電池比價網站,大家睇睇」 | 「我計晒所有 M18 電池,發現 XC5.0 雙支裝每 Wh 比 HD12.0 抵 15%」 |

第二種係**分享情報**,個連結只係證據。第一種係廣告,會俾人 downvote 同 ban。

## ⭐ 殺手策略：一個品牌一個帖

呢個係我今次改 code 嘅原因。**每個品牌 subreddit 都係一個獨立、精準、而且合理嘅帖。**

因為你有 `/milwaukee-m18/` 同 `?p=milwaukee-m18`,你去 r/MilwaukeeTool 發嘅時候,對方睇到嘅係**只有 M18 嘅表** —— 唔係一個要佢自己篩嘅通用網站。

**呢個唔算 spam,因為每個帖真係唔同內容。**

| Subreddit | 發咩 |
|---|---|
| r/MilwaukeeTool | `/milwaukee-m18/` + M18 嘅發現 |
| r/Dewalt | `/dewalt-20v-max/` + 「20V MAX 其實係 18V」呢個角度 |
| r/Makita | `/makita-18v-lxt/` + LXT vs XGT 對比 |
| r/ryobi | `/ryobi-one-18v/` + 「Ryobi 每 Wh 最平」（示範數據入面真係） |
| r/Tools | 全站 + 跨品牌對比 |
| r/DIY, r/electricians, r/Construction, r/HomeImprovement | 全站,但要配合當時討論 |

⚠️ **每個 sub 嘅自我宣傳規則一定要先睇。** 有啲要 flair、有啲禁連結、有啲要你先有 karma。**分開幾日發,唔好同一日 blast 晒** —— Reddit 會當你 spam。

## 其他渠道（按預期價值排）

**1. ToolGuyd —— 最高價值單一目標**

佢哋**已經寫過 Ah vs Wh 嘅文章**,讀者就係你嘅目標客。

- 去相關文章留言（真誠補充,唔係硬銷)
- **直接 email 編輯。** 工具 blog 寫一篇介紹 = 大量精準流量 + 一條高質 backlink。呢個一封 email 嘅期望值,高過十個 Reddit 帖

**2. Hacker News —— Show HN**

標題直接寫：**「Show HN: Disk Prices, but for power tool batteries」**

HN 圈自己人一睇就明,而且誠實交代咗靈感來源。diskprices 本身就係喺 HN 爆嘅,呢個 framing 命中率唔低。

**3. YouTube 工具評測頻道**

Project Farm、Torque Test Channel、Tools In Action 之類。留言 + email。單次成功率低,但一次提及可以帶幾千人。

**4. 論壇（SEO 加成）**

GarageJournal、Contractor Talk。流量細過 Reddit,但**論壇帖會被 Google 長期索引**,等於順手做咗 backlink。

---

# Part 4：第 2 層 —— SEO（Month 2-12,真正嘅引擎）

## 已經做好嘅：9 個平台頁

之前個站得一版,而家 `build.py` 生成 10 版,每版有自己嘅 title、description、H1、開場文字（由該平台嘅數據自動生成,唔係複製貼上）。

因為 **`milwaukee m18 battery comparison` 係一個有真實搜尋量嘅字**,而一個單頁站冇可能同時排到 9 個咁嘅字。

已包含：`sitemap.xml`、`robots.txt`、canonical、內部互連。

## ⭐ 下一個要做嘅頁：`20v-max-vs-18v`

呢個係整個品類**搜尋量最高**嘅問題,而**你個站嘅核心論點就係答案**。

- 寫一版 800 字解釋 5×4.0V vs 5×3.6V
- 結尾自然接落表格：「所以要比較,睇 $/Wh」
- **呢版帶人入嚟,表格轉化佢哋**

我查嘅時候見到 Pro Tool Reviews、ToolGuyd、SlashGear 都寫過呢題 —— 即係證實有量。你嘅優勢係：**佢哋只解釋,你有埋實時表格。**

## 其他值得做嘅字

| 關鍵字模式 | 例 |
|---|---|
| `[品牌] battery comparison` | ✅ 已有 9 版 |
| `20v max vs 18v` | ⬅️ 下一步,最高量 |
| `which [品牌] battery is best value` | 平台頁已部分覆蓋 |
| `[型號] vs [型號]` | 例：`dcb205 vs dcb206` |
| `power tool battery watt hours chart` | 一版對照表 |

⚠️ **唔好寫 SEO 內容農場文。** 你贏唔過已建立嘅 blog。你嘅優勢係**別人冇嘅實時數據**,唔係文章。

---

# Part 5：第 3 層 —— 護城河（由第一日開始累積）

## 1. Email 通知（最重要）

「呢隻電池跌到 $X 通知我」。

**呢個係你唯一擁有、Amazon 拿唔走嘅資產。** Amazon 隨時改佣金率（每季更新一次,2020 年試過一夜腰斬）—— 但 email list 係你嘅。

一個 500 人嘅精準 list,價值高過一萬個一次性訪客。

## 2. 價格歷史

我上次已經講過,再強調一次：**由第一日 append `history.jsonl`。**

成本近乎零,但一年後你答得出「M18 XC5.0 通常幾時最平」—— 新入場者永遠追唔返。**呢個係唯一會自動變深嘅護城河。**

（順帶一提：11-12 月係工具電池全年最平嘅時候。有歷史數據你就講得出,冇就講唔出。）

## 3. 地區站

diskprices **一半收入嚟自非美國站**。`.co.uk` / `.de` / `.ca` 係最抵做嘅擴張 —— 同一份 code,換聯盟 tag。

---

# Part 6：唔好做

| 唔好做 | 原因 |
|---|---|
| 買廣告 | 3% 佣金,CPC 一定蝕。數學上唔可能 |
| 同一日 blast 20 個 subreddit | 即刻俾人當 spam ban 埋 |
| 硬銷文案（「快啲買!」） | 呢個圈極反感,你賣嘅係中立比較 |
| X / Twitter | 呢班買家唔喺嗰度 |
| 內容農場文 | 排唔上,浪費時間 |
| 買 backlink | Google 罰,而且冇用 |

---

# Part 7：90 日時間表 + 老實嘅預期

| 時期 | 做咩 | 預期流量 |
|---|---|---|
| Week 1-2 | 核實規格、入真價、上聯盟連結 | 0 |
| Week 3 | 部署 + Show HN + r/Tools | **爆發 500–3,000** |
| Week 4 | 逐個品牌 sub（分開日發）+ ToolGuyd email | 再 500–2,000 |
| Week 5-8 | 流量跌返近零。**寫 `20v-max-vs-18v` 頁,做 email 通知** | 100–400/月 |
| Month 3-4 | Google 開始索引平台頁 | 300–1,000/月 |
| Month 5-6 | SEO 起飛 + 回頭客累積 | **1,000–3,000/月** |
| Month 7-12 | 直接訪問開始佔比 + 加地區站 | 2,000–6,000/月 |

## ⚠️ 兩個一定要有心理準備嘅事

**1. 第 4-8 星期會極度灰心。** 爆發完流量歸零,你會覺得失敗咗。**呢個係正常曲線,唔係失敗。** SEO 未起,爆發已散。呢段時間嘅工作（寫 SEO 頁、做 email）係為 3 個月後鋪路。

**2. 爆發唔係生意。** 一個 r/Tools 好帖可能一日就打到你嘅月目標 —— 然後歸零。**唔好因為爆發成功就以為搞掂,亦唔好因為爆發之後歸零就放棄。** 生意喺第 2、3 層。

---

# Part 8：今次已經改咗嘅技術嘢

推廣計劃唔係純建議 —— 上面幾樣嘢個站本身要支援得到,所以順手做埋：

| 改動 | 為咗解決 |
|---|---|
| **9 個平台頁**（`/milwaukee-m18/` 等） | 一版排唔到 9 個關鍵字;亦令「一個品牌一個帖」策略成立 |
| **篩選狀態入 URL**（`?p=milwaukee-m18`） | 之前分享唔到篩選後嘅表。而家「呢度係所有 M18 按 $/Wh」係一條可分享連結 |
| **短連結形式**（`?x=` 排除式） | 剔走一個平台唔會再產生 8 個 key 嘅醜 URL |
| **OG / Twitter card + `og.png`** | 貼上 Discord / Slack / Reddit 會出圖,唔係光禿禿一條連結 |
| **canonical + sitemap.xml + robots.txt** | 冇呢啲 Google 索引得又慢又亂 |
| **底部平台導航** | 內部連結,幫 Google 爬晒 9 版 |

**其中「篩選入 URL」係最關鍵嘅一個** —— 冇佢,「一個品牌一個帖」根本做唔到,你只可以重複貼同一條首頁連結,而咁樣一定俾人當 spam。
