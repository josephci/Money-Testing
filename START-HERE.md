# 你要自己做嘅嘢

呢個 repo 有好多文件。**呢一份係唯一你需要跟嘅。**

---

> ⭐ **最快見到錢嘅一條路：AI 資料標註。**
> **中文/廣東話係加價項目($30–75/小時),即係每月 1.5–2.5 個鐘 = $50。成功率 70–80%,零本金、零推廣、唔使面對人。**
> 點申請、邊個最易入、入門測試點準備 → [`docs/annotation-apply.md`](docs/annotation-apply.md)
>
> 點解「自動化跑量」唔存在、「信息差」點解係啱方向 → [`docs/two-directions.md`](docs/two-directions.md)

## 兩條路,揀一條

| | 🛠 **抓資料 → Fiverr** | 📊 電池比價站 |
|---|---|---|
| 第一蚊要等幾耐 | **2–6 星期** | 5–8 個月 |
| $50/月 機會 | **35–45%** | 25–30% |
| 要唔要同人傾偈 | 要（文字,有現成範本） | 唔使 |
| 被唔被動 | 半自動 | 全自動 |
| 而家狀態 | ✅ 可以即刻開始 | ⏸ 要先核實 39 隻電池規格 |

**先做左邊嗰條。** 右邊嗰個站已經砌好,唔會走,遲啲有時間先算。

> ⚠️ 左邊嗰個機會由 60–70% 下調咗做 35–45% —— Fiverr 買家跌緊,而且 AI 壓緊價。
> **你嘅優勢唔係識做,係識推單、會核對、肯長期負責。** 詳見 [`docs/ai-saturation.md`](docs/ai-saturation.md)。

---

# 第 0 步 — 攞啲 code 落你部機（10 分鐘）

**呢個係第一步,因為而家啲嘢淨係喺雲端,你部機未有。**

開 Terminal（Mac 撳 `⌘+空格` 打「terminal」／Windows 開「PowerShell」）：

```bash
git clone https://github.com/josephci/Money-Testing.git
cd Money-Testing/scraper-kit
```

### 檢查有冇 Python

```bash
python3 --version
```

- 見到 `Python 3.11` 之類 → ✅ 得
- 話 `command not found` → 去 [python.org/downloads](https://www.python.org/downloads/) 裝。**Windows 裝嗰陣記住剔「Add Python to PATH」**

### 裝三個工具

```bash
pip install requests beautifulsoup4 openpyxl
```

（唔 work 就試 `pip3 install ...`）

---

# 第 1 步 — 試跑一次（10 分鐘,今日就做得）

```bash
python3 scrape.py jobs/example.toml
```

跑完 `out/` 入面會有 `example.xlsx`。**開嚟望一眼。**

呢個就係你將來交俾客嘅嘢。**順手截個圖**,第 2 步要用。

> 如果呢一步跑得成 —— 你已經有能力交第一單。

---

# 第 2 步 — 開 Fiverr gig（1 小時,一次過）

1. 去 [fiverr.com](https://www.fiverr.com) 開帳戶（免費）
2. `Become a Seller` → `Create a New Gig`
3. **標題、描述、標籤、價錢全部喺 [`scraper-kit/FIVERR.md`](scraper-kit/FIVERR.md) 度,照抄**
4. Gig 圖片用你第 1 步嗰個截圖
5. 出街

### 定價（新帳戶就係要平）

| | 價 | 內容 |
|---|---|---|
| Basic | $15 | 1 版,5 欄 |
| Standard | $35 | 10 版,10 欄 |
| Premium | $60 | 50 版 + 清理 |

**頭 3 個評價比頭 3 舊錢重要好多。** 有評價先加價。

---

# 第 3 步 — 有人搵你（每次 10–30 分鐘）

```
客傳條 URL 過嚟
      ↓
python3 scrape.py --inspect "條URL"
      ↓
   ┌──┴──┐
做唔到    做到
   │       │
推返單    抄設定檔 → 跑 → 開個 xlsx 望一眼 → 交
（範本喺 FIVERR.md）        ↑
                    ⚠️ 唔可以跳呢步
```

**交完貨加一句**（範本喺 `FIVERR.md`）：

> 「呢版資料會變。我可以每星期自動跑一次寄俾你,$15/月。冇壓力,想要先講。」

**2 個客肯 = $30/月。收 $25 就 $50/月。**

---

# 只有你做得到嘅嘢（就係呢 6 樣）

| | 時間 |
|---|---|
| ① Clone + 裝 Python | 10 分鐘 |
| ② 跑一次 example,截圖 | 10 分鐘 |
| ③ 開 Fiverr 帳戶 + 貼 gig | 1 小時 |
| ④ **回覆客嘅 message** | 每次 5 分鐘 |
| ⑤ **決定接定推**（跑完 `--inspect` 就知） | 每次 2 分鐘 |
| ⑥ **開個 xlsx 望一眼先交** | 每次 3 分鐘 |

**①②③ 係一次過,加埋約 1.5 個鐘。④⑤⑥ 係每單重複。**

---

# 我做唔到嘅嘢 —— 講清楚

**④ 係避唔到嘅。** 有人落單,佢會 message 你,你要覆。

我可以俾晒你範本(已經俾咗),但我唔可以喺你嗰邊撳掣。

不過呢種傾偈同你怕嘅嘢唔同：

| | Reddit 發帖 | Fiverr 覆客 |
|---|---|---|
| 有冇人圍觀 | 有,全 sub | **冇,得你同佢** |
| 會唔會俾人評價你個人 | 會 | **唔會,佢只係想攞份 Excel** |
| 講咩 | 「睇我做嘅嘢」 | 「收到,24 小時內交」 |

**你唔使推銷,唔使講自己。你只需要答「做唔做到」同「幾時交」。**

---

# 第一日做咩（30 分鐘）

```
□ git clone
□ python3 --version    冇就去裝
□ pip install requests beautifulsoup4 openpyxl
□ python3 scrape.py jobs/example.toml
□ 開 out/example.xlsx 望一眼
□ 截個圖
```

**做完呢六格,你已經有貨可以賣。** 第 2 步（開 gig）第二日再做都得。

---

# 電池站點算

放喺度,唔使理。想做嗰陣睇 [`LAUNCH.md`](LAUNCH.md)（7 項)同 [`docs/will-this-work.md`](docs/will-this-work.md)（老實成功率)。

⚠️ 但**唔好兩條路一齊做**。電池站要 30 個鐘先見到第一個訊號,Fiverr 兩星期。先攞到第一蚊,再講。

---

# 卡住嘅時候

指令跑唔郁、錯誤訊息睇唔明、客問咗啲你唔識答嘅嘢 —— **直接問我,連埋錯誤訊息原文貼過嚟。**

呢個唔係考試,唔使自己死頂。
