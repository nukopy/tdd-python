# Python：unittest の色んな assert メソッドを試す

Python のユニットテストフレームワーク unittest でテストを記述するには，まず，`unittest.TestCase` クラスのサブクラスを定義する．そのクラスの中にテストを `test_*`という名前のメソッドとして記述する．

テストは，テスト対象から得られる値・状態が期待する内容と一致するかを比較する．つまり，**「動作により得られた結果」と「期待される結果」の比較を行う**．unittest を用いて比較する方法として， `unittest.TestCase` クラスに実装されている `assert*()` というメソッドを用いることができる．

本記事では，様々な assert メソッドを試し，「unittest でテストを書くときにどんなパターンのテストケースを記述できるのか」を把握するのを目標にする．要は「assert ってどんな種類あったっけ？」のインデックスを貼る作業．

本記事は「Python 実践入門」のユニットテストの章を参考にしている．

<iframe style="width:120px;height:240px;" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" src="https://rcm-fe.amazon-adsystem.com/e/cm?ref=qf_sp_asin_til&t=pyteyon-22&m=amazon&o=9&p=8&l=as1&IS2=1&detail=1&asins=429711111X&linkId=6b067c234d0745816a567ded3d796cb3&bc1=000000&lt1=_blank&fc1=333333&lc1=0066c0&bg1=ffffff&f=ifr">
</iframe>

unittest のドキュメント，また，それを読んでまとめた記事を以前に書いたのでリンクを貼っておく．「unittest って何？」って方は参照すると良い．

https://docs.python.org/ja/3/library/unittest.html
https://pyteyon.hatenablog.com/entry/2020/05/11/203000

## 開発環境

- Python 3.8.0
- IPython 7.14.0

## pytest を使わないの？

今後は，流行りでありデファクトになりつつある（らしい）pytest という別のテストフレームワークを使っていく予定である．しかし，pytest は unittest を使いやすく拡張したものであり，unittest を理解しておけばすんなり入れる（と思ってる）．そのため，まずは unittest を丁寧に学ぶことにした（pytest に限らず unittest をベースにしたフレームワークはいくつかあるみたい）．

結局，Python を使う上で言語標準のテスト用モジュールである unittest は避けられないし（OSS とかでも良く使われてる．Django のテストは unittest ベース．），長期的に見て unittest を勉強するのは必須であると筆者は考えている．

## assert メソッド一覧

何はともあれ，まずは `assert*()` と名の付くメソッドを全て表示してみる．全部で 41 個のメソッドが定義されている．

![`assert*()` メソッド一覧](./unittest-assert.png)

上記のメソッドの内，ドキュメントで言及されているもの整理してまとめた．

### 基本

下記メソッドは，最も一般的に使われる assert メソッドである．

| メソッド                       | Checks that               |
| ------------------------------ | ------------------------- |
| `assertEqual(a, b)`            | `a == b`                  |
| `assertNotEqual(a, b)`         | `a != b`                  |
| `assertTrue(x)`                | `bool(x) is True`         |
| `assertFalse(x)`               | `bool(x) is False`        |
| `assertIs(a, b)`               | `a is b`                  |
| `assertIsNot(a, b)`            | `a is not b`              |
| `assertIsNone(x)`              | `x is None`               |
| `assertIsNotNone(x)`           | `x is not None`           |
| `assertIn(a, b)`               | `a in b`                  |
| `assertNotIn(a, b)`            | `a not in b`              |
| `assertIsInstance(a, type)`    | `isinstance(a, type)`     |
| `assertNotIsInstance(a, type)` | `not isinstance(a, type)` |

尚，全ての assert メソッドは，`msg` というキーワード引数を取り，テスト失敗時に出力されるエラーメッセージを指定できる．ただし，いくつかのメソッド（`assertRaises()`，`assertRaisesRegex()`，`assertWarns()`，`assertWarnsRegex()`，後述）においては，メソッドをコンテキストマネージャとして使用した場合にのみ `msg` キーワード引数を使える．

### 例外，警告，ログメッセージの発生のテスト

例外（exception），警告（warning），ログメッセージの発生を確認する．ざっと説明すると以下のようになる．

- 例外のテスト
  - 期待通りの例外が発生するかを確認する
- 警告のテスト
  - 期待通りの警告が発生するかを確認する
- ログメッセージのテスト
  - 期待通りのログが吐き出されるかを確認する

メソッドを整理した．

| メソッド                                        | Checks that                                                                               |
| ----------------------------------------------- | ----------------------------------------------------------------------------------------- |
| `assertRaises(exc, fun, *args, **kwds)`         | `fun(*args, **kwds)` が例外 `exc` を送出するか                                            |
| `assertRaisesRegex(exc, r, fun, *args, **kwds)` | `fun(*args, **kwds)` が例外 `exc` を送出し，メッセージが正規表現 `r` とマッチするか       |
| `assertWarns(warn, fun, *args, **kwds)`         | `fun(*args, **kwds)` が警告 `warn` を送出するか                                           |
| `assertWarnsRegex(warn, r, fun, *args, **kwds)` | `fun(*args, **kwds)` が警告 `warn` を送出し，メッセージが正規表現 `r` とマッチするか      |
| `assertLogs(logger, level)`                     | `with` ブロックで使用．ログレベル `level` において，`logger` がログを吐き出すかを確認する |

これらのメソッドは主に with 文で使用する．コンテキストマネージャを返すメソッドであり，例えば，`assertLogs()` は以下のように使われる．

- `test_logger.py`

```python
import unittest
import logging

class TestLogger(unittest.TestCase):
    def test_logger(self):
        logger = logging.getLogger("TEST")
        with self.assertLogs(logger=logger, level=logging.DEBUG)
```

- 参考：[Python の unittest での，`assertLogs()` の使い方(2019/12, Qiita)](https://qiita.com/TakamiChie/items/2c9829a645d3b612642e)

## ドキュメント読み

各メソッドのドキュメント読んでまとめた．

### assertEqual

```python
assertEqual(first, second, msg=None)
```

## 補足

### Python：`a == b` と `a is b` の違い

### 用語

- **テストケース test case**

  - テストケースの粒度によって定義が変わる．「1 つのテスト項目」のこともあれば，「1 つのテスト対象に対する，入力・期待される結果のセット」を指すこともある．
    - 1 つのテスト項目：「この関数が期待通りの動きをするか」（粒度が大きい「テストケース」）
    - 1 つのテスト対象に対する入力・期待される結果のセット：Parameterized Test に使用する 1 つ 1 つのパラメータのこと（競プロの「計算量が大きいテストケースに落ちた」はこっち）

テストケースの構成は以下の通り．

- テストケースの構成
  - テストに用いる入力値や条件
  - テストを実行したときに期待する値・状態・動作
    - 最終的には，どんなテストでも**「動作により得られた結果」と「期待される結果」の「比較」**を行う

## 参考

- [Python：ユニットテストを書いてみよう](https://blog.amedama.jp/entry/python-unittest)
