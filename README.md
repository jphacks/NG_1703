# プロダクト名 「On You」

[![Product Name](https://raw.github.com/GabLeRoux/WebMole/master/ressources/WebMole_Youtube_Video.png)](https://www.youtube.com/channel/UC4PtjOfZTbVp9DwtJv82Lzg)

## 製品概要
### 音喩 X Tech

### 背景（製品開発のきっかけ、課題等）
* 感覚の拡張
人間の感覚の8割は視覚から得ていると言われています。そして，聴覚の場合に至っては1割程度と言われています。
この聴覚の情報を視覚の情報に変換することでより多くの情報を得ることができないかと考えました。
* 音の可読化
音の可視化音がどの方向から，どのくらいのボリュームで聞こえるかという意味での

### 製品説明（具体的な製品の説明）
* 音から
Mac内蔵カメラから映像と音を取得し，動画として画面に出力します。
取得した音が何の音かを判別し，判別した音を音喩に変換することができます。変換した音喩を動画上に重ねて出力します。
* 音喩
** 音喩(おんゆ)は漫画において書き文字として描かれたオノマトペを指す
* 音が読める情報になる!!!

### 特長
* 取得した音データをリアルタイムで解析
* 音を音喩として動画上に表示
* 音を読むことができる!!!

### 解決出来ること
* 聴覚障害者を補助
**  聴覚障害のある人にも音を聴覚障害者を始めとした、様々なシーンで視覚を拡張
* エンターテインメントの拡張

### 今後の展望
* 音を認識してから画面に文字を表示する応答速度の高速化
* 何の音かを自動で判別
* 理想としてはARゴーグルを使い、ARゴーグルを通して見える視界に音喩を付加

## 開発内容・開発技術
### 活用した技術
#### API・データ
* NEC物音認識API

#### フレームワーク・ライブラリ・モジュール
* Python
* OpenCV

#### デバイス
* Mac内臓カメラ

### 独自開発技術（Hack Dayで開発したもの）
#### 2日間に開発した独自の機能・技術
* 物音認識APIから受け取った情報から動画への音喩の付与
