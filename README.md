# どうぶつのともだち（仮）

スマホのブラウザで遊べる、3Dの動物育成ゲーム（制作中・まぃの箱にはまだ載せていません）。

遊ぶURL: https://mai-104.github.io/himitsu-no-niwa/

---

## 見た目の差し替えかた

ゲームの中身はすべて `index.html` の1ファイルです。
絵やモデルは、**ファイルを置いて、`index.html` に「ファイル名を1行書く」だけ**で差し替わります。
書いていないものは、今の絵のまま表示されます。

### 手順

1. 画像（PNG）は `images` フォルダ、3Dモデル（GLB）は `models` フォルダ、音（MP3）は `sounds` フォルダに入れる
   - GitHubの「Add file」→「Upload files」で、フォルダ名ごと入れられます（例：`images/carrot.png`）
2. `index.html` を鉛筆マークで開いて、下の表の「書く場所」に1行足す
3. 保存（Commit changes）して、数分後にゲームを開き直す

> 画像は、背景が透明なPNGがおすすめです。アイコンは正方形（例：256×256）にすると、きれいに収まります。

---

### ① アイコン（2Dの絵）… `const IMAGES = {` の中に書く

書きかた（例）：

```js
const IMAGES = {
  carrot: "images/carrot.png",
  seed_sunflower: "images/seed_sunflower.png",
};
```

| 名前（キー） | 何の絵か |
|---|---|
| `carrot` `sunseed` `strawberry` `pumpkin` | 野菜（はたけ・おみせ・ごはんボタン・ごはんが飛ぶ絵） |
| `iwashi` `aji` `saba` `tai` | 魚 |
| `cookie` | おやつ |
| `seed_sunflower` `seed_strawberry` `seed_pumpkin` | おみせの「たね袋」 |
| `plot0` `plot1` `plot2` | はたけ（なにもない／芽が出た／葉っぱが育った） |
| `face_usagi` `face_pengin` `face_hamster` `face_neko` | 図鑑・おみせの動物の顔 |
| `decor_plant` `decor_lamp` `decor_cushion` `decor_vase` `decor_shelf` `decor_picture` `decor_clock` `decor_garland` `decor_rugRound` `decor_rugStar` `decor_ball` `decor_blocks` `decor_bear` | 家具・おもちゃのアイコン（おみせ・もようがえ） |
| `wear_ribbon` `wear_hat` `wear_flower` `wear_crown` | きせかえのアイコン |
| `coin` | コイン |
| `pet` `brush` `ball` `walk` `moon` `star` `hanger` `sofa` | おせわボタン（なでる・ブラシ・あそぶ・おさんぽ・ねかせる・げい・きせかえ・もようがえ） |
| `heart` `sprout` `rod` `bag` `book` | 下のタブ（おせわ・はたけ・つり・おみせ・ずかん） |
| `heartPink` `bubble` | なでた時のハート・ブラシの泡 |

### ② 動物（3Dモデル）… `const SPECIES = {` の中の `glb: null` を書きかえる

```js
usagi: { ..., glb: "models/usagi.glb", ... },
```

- 成長段階ごとにモデルを変えたい時は `glb: ["models/pen_baby.glb", "models/pen_kid.glb", "models/pen.glb"]` のように [あかちゃん, こども, おとな] の順に書きます（null の段階は作った見た目のまま）
- 大きさと足元の位置は自動で合わせます
- モデルにした動物は「全身の動き」（ジャンプ・くるくる・食べる・ふるふる）になります。
  耳だけ動く・まばたき・手を上げる・顔を洗う、は作った見た目の時だけです

### ②-2 成長段階ごとの色 … `SPECIES` の `looks:`

作った見た目のまま、成長段階ごとに色だけ変えられます。[あかちゃん, こども, おとな] の順に、変えたい色だけ書きます。

```js
looks: [{ body: 0x9095a0 }, { body: 0x5b6784 }, {}],   // ペンギン：あかちゃんは灰色
```

使える色の名前：うさぎ `fur` `inner` `pink`／ペンギン `body` `belly` `beak` `cheek`／ハムスター `fur` `white` `pink`／ねこ `fur` `white` `stripe` `pink`

### ③ 家具・おもちゃ（お部屋に置く物）… `const DECOR = {` の中に足す

```js
plant: { name: "かんようしょくぶつ", slot: "floor", shop: null, color: "#5fae5c", png: "images/room_plant.png", size: 1.2 },
```

- `glb: "models/plant.glb"` … 3Dモデル（どの角度から見ても自然）
- `png: "images/plant.png"` … 画像を板にして置く（かべの絵・時計・ラグはこれで自然。床の家具は横から見ると薄い板に見えます）
- `size:` … 大きさ（床の物は高さ、かべの物は高さ、ラグは幅。動物の高さがだいたい 2.8）

### ④ きせかえ … `const WEAR = {` の中に足す

```js
ribbon: { name: "リボン", price: 40, level: 2, color: "#f47b9b", png: "images/wear_ribbon.png", size: .4 },
```

`glb:` か `png:` と、`size:`（高さ）が使えます。頭のてっぺんにのります。

### ⑤ お部屋とつりの背景 … `const ROOM_IMAGES = {` の中に書く

| 名前 | 何か |
|---|---|
| `floor` | お部屋の床（くり返して敷きつめます） |
| `wall` | お部屋のかべ（くり返し） |
| `window` / `windowNight` | まどの外の景色（昼／夜） |
| `fishScene` | つりの背景（ペンギンと桟橋もこの絵に描いておく。うき・つりざお・ゲージはゲームが描きます） |

### ⑥ BGM・効果音 … `const SOUNDS = {` の中

音（MP3）は `sounds` フォルダに入れて、`null` をファイル名に書きかえます。例：`main: "sounds/bgm_room.mp3",`

**BGM（くり返し）**

| 名前 | いつ流れるか |
|---|---|
| `main` | ふだん（おせわ画面。ほかの画面の曲が空の時もこれ） |
| `night` | 夜（19時〜5時）のおせわ画面 |
| `farm` `fish` `shop` `zukan` | それぞれの画面 |

**効果音**

| 名前 | いつ鳴るか |
|---|---|
| `button` | ボタン・タブを押した時 |
| `eat` / `treat` | ごはん・おやつを食べた |
| `pet` / `brush` | なでた・ブラシした（こするたび） |
| `play` / `trick` | あそぶ・げい |
| `sleep` / `wake` | ねかせる・おこす |
| `walkOut` / `walkBack` | おさんぽに出かける・帰ってきた |
| `grow` / `levelup` | 動物が成長した・おせわレベルが上がった |
| `plant` / `water` / `harvest` | たねをまく・水やり・しゅうかく |
| `cast` / `bite` / `catch` / `miss` | つり：なげる・かかった・つれた・にげられた |
| `buy` / `sell` / `reward` / `adopt` | 買う・売る・おねがいのごほうび・なかまが来た |

- 音を1つでも入れると、ずかん画面に「音：ON／OFF」の切りかえが出ます
- スマホのきまりで、BGMは画面を最初にタップした時から流れます
- 音量は `volume:` で変えられます（0〜1）

---

## 数字の調整

`index.html` の上の方にまとまっています。

- `CONFIG` … おなかの減り方、おさんぽの時間、おせわレベルに必要な数、つりのタイミング など
- `ITEMS` … 売る値段
- `CROPS` … 育つ時間・たねの値段・お店に並ぶレベル
- `SPECIES` … 動物のおむかえの値段・お店に並ぶレベル・食べるもの
- `DECOR` / `WEAR` … 値段・お店に並ぶレベル

## 新しいものを増やす

`ITEMS` `CROPS` `FISHES` `DECOR` `WEAR` `SPECIES` に1行足すと、お店・はたけ・つり・図鑑に自動で出ます。
新しい動物を増やすときは、見た目を作る関数（`build`）か、3Dモデル（`glb`）が必要です。

## いま入っている素材

| ファイル | 中身 | 作りかた |
|---|---|---|
| `models/penguin.glb` | ペンギン（紺） | Meshy 6 Lite（無料プラン・CC BY 4.0）。画像を軽くするため、色の画像を1024pxにし、金属っぽさの画像は外しています |

> Meshy の無料プランで作ったモデルは CC BY 4.0 です。公開するときは「3Dモデル：Meshyで生成」の表記を入れてください。
