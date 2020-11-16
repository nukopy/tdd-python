# Python：標準モジュール logging の使い方

Python で他人のコードを読むときに，logging が入ってるとうわってなってた．長い間「早く logging やらないとなぁ」と思ってて要約重い腰を上げたのが本記事．

アプリケーション開発なり，パッケージ開発なり，ソフトウェアを書くに当たっては「ロギング」をの吐き出し方は必須事項なのでログを学ばないといけないなぁと思ったので

## ロギングとは？

以下，[IT 用語辞典 - ロギング【logging】](http://e-words.jp/w/%E3%83%AD%E3%82%AE%E3%83%B3%E3%82%B0.html)より引用．

- **ロギング logging**
  - 起こった出来事についての情報などを一定の形式で記録・蓄積すること．
  - そのように記録されたデータを「ログ」（log）という．
  - コンピュータシステムの場合，利用者などによる操作や，機器や装置，ソフトウェアなどの稼働状況，通信機能による外部との通信などの記録を残すことを「ロギング」ということが多い．

本記事の文脈はコンピュータシステムである．また，「記録を残す」場合，テキストファイル（`.log` などの拡張子の付いたログファイル），または DB に「記録を残す」ことが多い．「ログファイルにログを残す」ことを「ログを（に）吐く」などと言うこともある．

## logging の基本

### ログレベル

### ログレベルの設定

### ロガーの定義

## logging ドキュメント

### logging の全体像

### オブジェクト

- ロガーオブジェクト
  - ロギングレベル
- ハンドラオブジェクト
- フォーマッタオブジェクト
- フィルタオブジェクト
- LogRecord オブジェクト
  - LogRecord 属性
- LoggerAdapter オブジェクト

### その他

- スレッドセーフ性
- モジュールレベルの関数
- モジュールレベル属性
- warnings モジュールとの統合