# unittest のドキュメント（mock 以外）を読んでざっと整理した

テストを学び始めようと思い，まずは自分が一番慣れている Python でテストを勉強することにした．そのさきがけとして，unittest のドキュメントを mock の部分を除いて全部読んで整理してみた．

## 概要

本記事はその写経，整理を行った記事．ドキュメントの日本語を意味が通じるように書き直したり，細かく章立して情報を整理したり，自分なりの解釈を書き加えたりしてみた．

一部，筆者が理解できなかった部分，細部に手を付ける必要が無いと思った部分は内容が薄くなっている．

## 本記事の目標

本記事の目指すところは，「次に unittest のドキュメントを読む時に副読本みたいに使える記事」である．なので unittest について勉強したい方はドキュメントに飛んだ方が良いかもしれない．

https://docs.python.org/ja/3/library/unittest.html

## TL;DR

以下の二つの図が理解できれば一先ず OK かなと思う．unittest で実行したテストの流れの図．

## unittest モジュールで出てくる概念

unittest は Python のユニットテストフレームワークであり，元々 JUnit（Java の単体テストモジュール）に触発されたもので，他の言語の主要なユニットテストフレームワークと同じような感じ．以下の 4 点をサポートしている．

- テストの自動化
- テスト用のセットアップやシャットダウンのコードの共有
- テストのコレクション化
- 報告フレームワークからのテストの独立性

これを実現するために，unittest はいくつかの重要な概念をオブジェクト指向の方法でサポートしている．以下に，unittest だけでなく，ソフトウェアのテストで一般的に用いられている用語を示した．unittest のドキュメントにも出てくるため把握しておくと良い．

- **テストフィクスチャ (test fixture)**

  - A test fixture represents the preparation needed to perform one or more tests, and any associated cleanup actions. This may involve, for example, creating temporary or proxy databases, directories, or starting a server process.
  - 「テストフィクチャ」はテストやそれに関連するあらゆるクリーンアップ処理を実行するのに必要な「準備」のことである．これは，例えば，一時的 / 代理の データベース，ディレクトリを作ったり，サーバのプロセスを起動するなどが含まれる．
  - 簡単に言うと，「テストコードのための一時的な実行環境」のことである．

- **テストケース (test case)**

  - テストケース (test case) はテストの独立した単位で，各入力に対する結果をチェックする．
  - テストケースを作成する場合は，unittest が提供する TestCase クラスを基底クラスとして利用することができる．

- <a name="test-suite">**テストスイート (test suite)**</a>

  - 個々のテストケース，またはテストスイートの集合で，同時に実行しなければならないテストをまとめる場合に使用する．
    - 「個々のテストケースの集合」のことを「テストスイート」と呼ぶが，「テストスイートの集合」のことも「テストスイート」と呼ぶので注意
  - 一般的に，テストは**テストする機能に従ってテストをまとめるように設計した方がよい**．

- **テストランナー (test runner)**
  - テストの実行を管理し結果を提供する要素のこと．ランナーはグラフィカルインターフェースやテキストインターフェースを使用しても構わないし，テストの実行結果を示す特別な値を返しても構わない．

## unittest の基本

### 基本的な使い方

簡単な例とともに unittest の使い方を説明する．

- `test_string.py`
  - 3 つの文字列をテストする Python コード

```Python
import unittest


class TestStringMethod(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])

        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)


if __name__ == "__main__":
    unittest.main()
```

テストケースは，`unittest.TestCase` のサブクラスとして作成する．メソッド名が test で始まる三つのメソッドがテストである．テストランナーはこの命名規約によってテストを行うメソッドを検索する．

- `test_**` というメソッドの命名規約に必ず従うこと

テストには unittest のテスト用の各種の関数が用いられる．例えば上記の例で使用している関数を以下に示した．

| テスト用の関数                  | 説明                                   |
| ------------------------------- | -------------------------------------- |
| `assertEqual()`                 | 予定の結果が得られていることを確認する |
| `assertTrue()`，`assertFalse()` | 条件のチェックを行う                   |
| `assertRaises()`                | 想定した例外が発生する事を確認する     |

Python の `assert` 文の代わりにこれらのメソッドを使用すると，テストランナーでテスト結果を集計してレポートを作成することができる．

また，`setUp()` および `tearDown()` メソッドによって各テストメソッドの前後に実行する命令を実装することが出来る．詳細は[テストコードの構成](https://docs.python.org/ja/3/library/unittest.html#organizing-tests)を参照．

`unittest.main()` は，テストモジュールのコマンドライン用インターフェースを提供する．コマンドラインから起動された場合，上記のモジュールは以下のような結果を出力する．

```sh
$ python test_string.py
...
----------------------------------------------------------------------
Ran 3 tests in 0.000s

OK
```

`-v`（`--verbose`，verbose は「冗長な」，「多弁な」という意味）オブションをモジュールの実行時にに渡すと，より詳細なテスト結果，特に，テストメソッド単位のテスト結果を出力してくれる．「テストメソッド」とは `unittest.TestCase` のサブクラスに定義したメソッドのことである．

```sh
$ python test_string.py
test_isupper (__main__.TestStringMethod) ... ok
test_split (__main__.TestStringMethod) ... ok
test_upper (__main__.TestStringMethod) ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.000s

OK
```

上の例が unittest モジュールで最もよく使われる機能であり，ほとんどのテストではこれで十分である．

### 落ちるテストケースを書いてみる

次に，あえて落ちるテストケースを書いてみる．「テストに落ちたときに修正して再度テストを実行する」のようなサイクルを回す場合がほとんどだと思うので，実際にその例を示してみる．

先ほどの 3 つの文字列をテストするモジュールに `test_wrong` というメソッドに必ず落ちるテストケースを追加してもう一度コマンドラインからテストを実行してみる．

- `test_string_wrong.py`

```python
import unittest


class TestStringMethod(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])

        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

    def test_wrong(self):
        # あえて絶対に落ちるテストケースを書く
        self.assertEqual('Hello', 'hello')


if __name__ == "__main__":
    unittest.main()
```

出力結果は以下．ここでは，全てのテストをパスした場合と出力が異なることを確認する．

```sh
$ python test_string_wrong.py
...F
======================================================================
FAIL: test_wrong (__main__.TestStringMethod)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "test_string_wrong.py", line 24, in test_wrong
    self.assertEqual('Hello', 'hello')
AssertionError: 'Hello' != 'hello'
- Hello
? ^
+ hello
? ^


----------------------------------------------------------------------
Ran 4 tests in 0.000s

FAILED (failures=1)
```

`-v` オプションを付けてテスト結果の詳細を出力してみる．

```sh
$ python test_string_wrong.py
test_isupper (__main__.TestStringMethod) ... ok
test_split (__main__.TestStringMethod) ... ok
test_upper (__main__.TestStringMethod) ... ok
test_wrong (__main__.TestStringMethod) ... FAIL

======================================================================
FAIL: test_wrong (__main__.TestStringMethod)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "test_string_wrong.py", line 24, in test_wrong
    self.assertEqual('Hello', 'hello')
AssertionError: 'Hello' != 'hello'
- Hello
? ^
+ hello
? ^


----------------------------------------------------------------------
Ran 4 tests in 0.001s

FAILED (failures=1)
```

## 目次

ここまではドキュメントのサンプル実行までだった．ここからはドキュメントの各項目を 1 つずつ辿っていく．

- <a href="#cli">コマンドラインインターフェイス</a>
- <a href="#discovery">テストディスカバリ</a>
- <a href="#test-code">テストコードの構成</a>
- <a href="#reuse">既存テストコードの再利用</a>
- <a href="#skip">テストのスキップと予期された失敗</a>
- <a href="#subtest">サブテストを利用して繰り返しテストの</a>区別を付ける
- <a href="#class-function">クラスと関数</a>
  - <a href="#testclass">テストクラス</a>
    - <a href="#alias">非推奨のエイリアス</a>
  - <a href="#grouping">テストのグループ化</a>
  - <a href="#load-test">テストのロードと起動</a>
    - <a href="#protocol">load_tests プロトコル</a>
- <a href="#fixture">クラスとモジュールのフィクスチャ</a>
  - <a href="#setupclass-teardownclass">setUpClass と tearDownClass</a>
  - <a href="#setupmodule-teardownmodule">setUpModule と tearDownModule</a>
- <a href="#signal-handling">シグナルハンドリング</a>

## <a name="cli">コマンドラインインターフェース</a>

- モジュール単位，クラス単位，個別のテストケース単位のテストの実行
- コマンドラインオプション

### モジュール単位，クラス単位，個別のテストメソッド単位のテストの実行

unittest はコマンドラインからのテストの実行をサポートしている．前節のようなモジュール単位のテストだけでなく，クラス単位，あるいは個別のテストメソッド単位のテストを実行することもできる．

- CLI から各単位でテストを実行

```sh
# モジュール単位
$ python -m unittest test_module
# 補足：複数のモジュールを同時にテストできる
$ python -m unittest test_module1 test_module2

# クラス単位
$ python -m unittest test_module.TestClass

# テストメソッド単位
$ python -m unittest test_module.TestClass.test_method
```

- テストモジュールをファイルパスで指定できる
  - テストモジュールを指定するのにシェルのファイル名補完が使える
  - 当然，指定されたファイルはモジュールとしてインポート可能でなければならない．モジュールとしてインポート可能でないテストファイルを実行したい場合，代わりにそのファイルを直接実行（`python foo.py`）するのが良い（インポートできない場合ってある？？）．
  - パスから `.py` を取り除き，パスセパレータを `.` に置き換えることでモジュール名に変換される（import と同じ方式）．

```sh
$ python -m unittest tests/test_something.py
$ python -m unittest tests/test_something  # 同じ
$ python -m unittest tests.test_something  # import と同じ方式

# 上記は以下と同様（直接実行する）
$ python tests/test_string.py
```

- テスト実行時に (より冗長な) 詳細を表示するには `-v` フラグを渡す

```sh
$ python -m unittest -v test_module
```

- 引数無しで実行すると[テストディスカバリ](https://docs.python.org/ja/3/library/unittest.html#unittest-test-discovery)が開始され，テストが見つかれば実行される
  - 「テストディスカバリ」とは，テスト実行前に，テストランナーがテストコードの命名規約により自動でテストコードを探索する仕組みのこと
  - unittest のテストランナーのテストディスカバリについては，ドキュメントの「[テストディスカバリ](https://docs.python.org/ja/3/library/unittest.html#unittest-test-discovery)」を参照

```sh
$ python -m unittest
```

---

- 注意点
  - バージョン 3.2 で変更: 以前のバージョンでは，個々のテストメソッドしか実行することができず，モジュール単位やクラス単位で実行することは不可能だった

### コマンドラインオプション

unittest にはいくつかのコマンドラインオプションがある．ここではそれを列挙する．

#### コマンドラインプションの一覧を表示

以下を実行することで，コマンドラインオプションの一覧を表示できる（`-h` はヘルプを表示するオプション）．

```sh
$ python -m unittest -h
```

#### コマンドラインオプション一覧

`-h`（ヘルプ），`-v`（）を除き，ここでは 5 つ紹介する．

- `-b`，`--buffer`

  - 標準出力と標準エラーのストリームをテストの実行中にバッファする．
  - テストが成功している間は結果の出力は破棄される．テストの失敗やエラーの場合，出力は通常通り表示され，エラーメッセージに追加される．

- `-c`，`--catch`

  - ctrl-C を実行中のテストが終了するまで遅延させ，そこまでの結果を出力する．二回目の ctrl-C は，通常通り `KeyboardInterrupt` の例外を発生させることができる．
  - この機能の仕組みについては，[シグナルハンドリング](https://docs.python.org/ja/3/library/unittest.html#signal-handling)を参照．

- `-f`，`--failfast`

  - テスト中にエラーが起きたとき（テストに落ちたとき）にテストを停止する．

- `-k [pattern]`

  - オプションに渡す文字列のパターンや部分文字列に合致したクラス，テストメソッドのみテストを実行する．

  - オプションに渡すパターン（ワイルドカード `*` を含めることができる）は，[`fnmatch.fnmatchcase()`](https://docs.python.org/ja/3/library/fnmatch.html#fnmatch.fnmatchcase)を用いたテスト名と照合される．
  - case-sensitive な部分文字列マッチングが行われる
    - `foo`，`Foo` が区別される
  - オプションに渡すパターンは，テストローダーによりインポートされた，完全修飾されたテストメソッド名（the fully qualified test method name）と照合される．
  - ex) `-k foo` は以下に合致する:
    - `foo_tests.SomeTest.test_something`
    - `bar_tests.SomeTest.test_foo`
    - NOT matches `bar_tests.FooTest.test_something`

- `--locals`
  - トレースバック内の局所変数を表示する．

---

- 注意点
  - バージョン 3.2 で追加: コマンドラインオプションの `-b`，`-c`，`-f` が追加された．
  - バージョン 3.5 で追加: コマンドラインオプション `--locals` が追加された．
  - バージョン 3.7 で追加: The command-line option `-k` が追加された．

コマンドラインからのテストの実行では，テストディスカバリを調節することができる．すなわち，プロジェクトの全テストを実行したりサブセットのみを実行したりすることが出来る．

## <a name="discovery">テストディスカバリ</a>

（バージョン 3.2 で追加）

- テストディスカバリ
  - テスト実行前に，テストランナーがテストコードの命名規約により自動でテストコードを探索する仕組みのこと

### テストディスカバリのための命名

unittest はシンプルなテストディスカバリをサポートする．テストディスカバリに対応するには，全テストファイルは，プロジェクトの最上位のディスカバリからインポート可能なモジュール（[名前空間パッケージ](https://docs.python.org/ja/3/glossary.html#term-namespace-package)を含む）か[パッケージ](https://docs.python.org/ja/3/tutorial/modules.html#tut-packages)でなければならない．

つまり，それらのファイル名は有効な[識別子](https://docs.python.org/ja/3/reference/lexical_analysis.html#identifiers)でなければならない．

### テストディスカバリの基本

テストディスカバリは `TestLoader.discover()` で実装されているが，コマンドラインから使う事も出来まる．基本的な使い方は以下の通り．

```sh
$ cd project_directory
$ python -m unittest discover  # `python -m unittest` と等価
```

- 注釈
  - `python -m unittest` は `python -m unittest discover` と等価なショートカットである．テストディスカバリに引数を渡したい場合，`discover` サブコマンドを明示的に使用しなければならない．

### discover サブコマンドのオプション

`discover` サブコマンドには以下の 5 つのオプションがある．

- `-v`，`--verbose`

  - 詳細な出力

- `-s [directory]`，`--start-directory [directory]`

  - ディスカバリを開始するディレクトリを指定する
  - デフォルトはカレントディレクトリ '.'
  - ex)
    - (default)`python -m unittest discover .`
    - `python -m unittest discover ../`
    - `python -m unittest discover ./tests`

- `-p [pattern]`, `--pattern [pattern]`

  - テストファイル名を識別するパターンを指定する
  - デフォルトは `test*.py`
    - モジュール名を `test**` にする理由がこれ

- `-t [directory]`，`--top-level-directory [directory]`
  - プロジェクトの最上位のディスカバリのディレクトリを指定する
  - デフォルトは開始のディレクトリ

`-s`，`-p`，および `-t` オプションは，この順番であれば位置引数として渡す事ができる（オプションを明示すると順不同になる）．例えば，以下の二つのコマンドは等価である．

```sh
python -m unittest discover -s project_directory -p "*_test.py"
python -m unittest discover project_directory "*_test.py"
```

パスと同様に，パッケージ名を `myproject.subpackage.test` のように，開始ディレクトリとして渡すことができる．指定したパッケージ名はインポートされ，そのファイルシステム上の場所が開始ディレクトリとして使われる．

- 注意点
  - テストディスカバリはインポートによりテストを読み込む．
  - テストディスカバリが，指定された開始ディレクトリから全テストファイルを見付けると，パスはインポートするパッケージ名に変換される．例えば，`foo/bar/baz.py` は `foo.bar.baz` としてインポートされる．

グローバルにインストールされたパッケージがあり，それとは異なるコピーでディスカバリしようとしたとき，誤った場所からインポートが行われる可能性がある．その場合，テストディスカバリは警告し，停止される．ディレクトリのパスではなくパッケージ名を開始ディレクトリに指定した場合，ディスカバリはインポートするいずれの場所も意図した場所とするため，警告を受けないはず．

テストモジュールとパッケージは，[`load_tests` プロトコル](https://docs.python.org/ja/3/library/unittest.html#load-tests-protocol)によってテストのロードとディスカバリをカスタマイズすることができる．

---

- 注意点
  - バージョン 3.4 で変更: ディスカバリが[名前空間パッケージ](https://docs.python.org/ja/3/glossary.html#term-namespace-package)をサポートした．

## <a name="test-code">テストコードの構成</a>

ユニットテストの基本的な構成要素は，テストケース --- **設定され正しさのためにチェックされるべき単独のシナリオ** --- である．

unittest では，テストケースは `unittest.TestCase` クラスのインスタンスで表現される．独自のテストケースを作成するには `TestCase` のサブクラスを記述するか，`FunctionTestCase` を使用しなければならない．

`TestCase` インスタンスのテストコードは完全に独立していなければならない．すなわち単独で，あるいは他の様々なテストケースの任意の組み合わせのいずれかで実行可能でなければならない．

最も単純な `TestCase` のサブクラスは、特定のテストコードを実行するためのテストメソッド (すなわち名前が test で始まるメソッド) を実装するだけで簡単に書くことができる：

```python
import unittest

class DefaultWidgetSizeTestCase(unittest.TestCase):
    def test_default_widget_size(self):
        widget = Widget('The widget')
        self.assertEqual(widget.size(), (50, 50))
```

何らかのテストを行うには，`TestCase` ベースクラスが提供する `assert*()` メソッドのうちの一つを使用する．テストが失敗した場合，例外が説明のメッセージとともに送出され，unittest はテスト結果を _failure_ とする．その他の例外は _error_ として扱われる（**failure と error の違いに注意**）．

### テスト実行時の設定を行うためのメソッド：`setUp()`

テストは多くなり，それらの設定は繰り返しになるかもしれない．幸いにも，`setUp()` メソッドを実装することで，テスト実行の際の設定コードをくくり出すことができる．これにより，テストの実行開始時に設定のための処理を噛ませることができる．

テストフレームワークは実行するテストごとに自動的に `setUp()` を呼んでくれる：

```python
import unittest

class WidgetTestCase(unittest.TestCase):
    def setUp(self):
        self.widget = Widget('The widget')

    def test_default_widget_size(self):
        self.assertEqual(self.widget.size(), (50,50), 'incorrect default size')

    def test_widget_resize(self):
        self.widget.resize(100,150)
        self.assertEqual(self.widget.size(), (100,150), 'wrong size after resize')
```

- 注釈
  - いろいろなテストが実行される順序は，文字列の組み込みの順序でテストメソッド名をソートすることで決まる．

テスト中に `setUp()` メソッドで例外が発生した場合，フレームワークはそのテストに問題があるとみなし，そのテストメソッドは実行されない．

### テスト実行後のクリーンアップ処理のためのメソッド：`tearDown()`

`setUp()` と同様に，テストメソッド実行後にクリーンアップ処理をする `tearDown()` メソッドを提供している．これにより，テスト実行終了時に任意のクリーンアップ処理を噛ませることができる:

```python
import unittest

class WidgetTestCase(unittest.TestCase):
    def setUp(self):
        self.widget = Widget('The widget')

    def tearDown(self):
        self.widget.dispose()
```

**`setUp()` が成功した場合，テストメソッドが成功したかどうかに関わらず `tearDown()` が実行される**．

`setUp()` や `tearDown()` のような，テストコードのための実行環境のことを「テストフィックスチャ」という．新しく生成される `TestCase` インスタンスは，個々のテストメソッドを実行する毎にユニークなテストフィックスチャとして生成される．

- `setUp()`
- `tearDown()`
- `__init__()`

以上の 3 つが「テストメソッド毎」に実行される．テストクラス毎ではなく「テストメソッド毎」という点に注意．以下の画像が分かりやすい．

![PythonUnitTest3]

（引用元[Unit Testing with Python](https://www.drdobbs.com/testing/unit-testing-with-python/240165163)）

例えば，以下のような 3 つのテストメソッドを定義したテストコードを実行した場合，上述したように `setUp()`，`tearDown()` が 3 回実行される．

- `test_string.py`

```python
import unittest


class TestStringMethod(unittest.TestCase):

    def setUp(self):
        # 出力の都合上 '\n' を入れている
        print('\n----- setUp() が実行されました -----')

    def tearDown(self):
        print('----- tearDown() が実行されました -----')

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])

        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)


if __name__ == "__main__":
    unittest.main()
```

出力結果を見ると，テストメソッド毎にテストフィックスチャ（テストコードのための実行環境）が生成されているのが分かる．

```sh
$ python -m unittest test_string.py
test_isupper (test_string.TestStringMethod) ...
----- setUp() が実行されました -----
----- tearDown() が実行されました -----
ok
test_split (test_string.TestStringMethod) ...
----- setUp() が実行されました -----
----- tearDown() が実行されました -----
ok
test_upper (test_string.TestStringMethod) ...
----- setUp() が実行されました -----
----- tearDown() が実行されました -----
ok

----------------------------------------------------------------------
Ran 3 tests in 0.000s

OK
```

### テストする機能に従ってテストをまとめる：`suite()`

- テストスイート (test suite)
  - テストスイート (test suite) はテストケース，またはテストスイートの集まりで，同時に実行しなければならないテストをまとめる場合に使用する．
  - 一般的に，テストはテストする機能に従ってテストをまとめるように設計した方がよい

一般的に，テストケースの実装では，**テストする機能に従ってテストをまとめる**のが良い．

unittest はテストする機能毎にテストをまとめるための機構，unittest の `TestSuite` クラスで表現される _test suite_ を提供する．`unittest.main()` の呼び出しによるテストの実行は，モジュールの全テストケースを集めて実行する．

しかし，`unittest.TestSuite` を利用した場合，どのテストケースを実行するかを自由に選択し，カスタマイズできる：

```python
def suite():
    suite = unittest.TestSuite()
    suite.addTest(WidgetTestCase('test_default_widget_size'))
    suite.addTest(WidgetTestCase('test_widget_resize'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
```

### テストコードとテスト対象コードを別のモジュールに分離することの利点

テストケースやテストコードの定義をテスト対象コードと同じモジュールに置くことは出来る．しかし，実際の開発の現場ではそのようなことは行われず，**テストコードとテスト対象コードを独立したモジュールに置く**ことが多い．これには，以下のような利点がある．

- テストモジュールだけをコマンドラインから独立に実行することができる．
- テストコードと出荷するコードをより簡単に分ける事ができる．
- 余程のことがない限り，テスト対象のコードに合わせてテストコードを変更することになりにくい．
- テストコードは，テスト対象コードほど頻繁に変更されない．
- テストコードをより簡単にリファクタリングすることができる．
- C で書いたモジュールのテストはどうせ独立したモジュールなのだから，同様にしない理由がない．
- テストの方策を変更した場合でも，ソースコードを変更する必要がない．

## <a name="reuse">既存テストコードの再利用</a>

既存のテストコードが有るとき，このテストを unittest で実行しようとするために古いテスト関数をいちいち `TestCase` クラスのサブクラスに変換するのは大変である．

このような場合，unittest では `TestCase` のサブクラスである `FunctionTestCase` クラスを使い，既存のテスト関数をラップする．先述した初期設定 `setUp()` と終了処理 `tearDown()` に相当する処理も実行できる．

以下のテストコードを例に説明する．

```python
def testSomething():
    something = makeSomething()
    assert something.name is not None
    # ...
```

オプションの `setUp` と `tearDown` メソッドを持った同等のテストケースインスタンスは次のように作成する：

```python
testcase = unittest.FunctionTestCase(
    testSomething,
    setUp=makeSomethingDB,
    tearDown=deleteSomethingDB
)
```

- 注釈
  - `FunctionTestCase` を使って既存のテストを unittest ベースのテスト体系に変換することができるが，この方法は推奨されない．
  - 時間を掛けて `TestCase` のサブクラスに書き直した方が将来的なテストのリファクタリングが限りなく易しくなる．

既存のテストが doctest を使って書かれている場合もある．その場合，doctest は `DocTestSuite` クラスを提供する．このクラスは，既存の doctest ベースのテストから，自動的に `unittest.TestSuite` のインスタンスを作成する．

## <a name="skip">テストのスキップと予期された失敗</a>

（バージョン 3.1 で追加）

### テストのスキップ：基本

unittest は特定のテストメソッドやテストクラス全体をスキップする仕組みを備えている．さらに，この機能はテスト結果を「**予期された失敗 (expected failure)**」とすることができ，**テストが失敗しても `TestResult` の失敗数にはカウントされなくなる**．

テストのスキップを行う際には以下の方法がある．

- `unittest.skip()` デコレータやその派生デコレータを使う
- `TestCase.skipTest()` を `setUp()` メソッドやテストメソッド内で呼ぶ
- `self.skipTest`（`TestCase.skipTest`）を直接 raise する

### テストのスキップ：例

#### 基本的なスキップ

以下 3 つのデコレータ の使用例を示す．

- `@unittest.skip(reason: str)`
- `@unittest.skipIf(condition: bool, reason: str)`
- `@unittest.skipUnless(condition: bool, reason: str)`

```python
class MyTestCase(unittest.TestCase):

    @unittest.skip("demonstrating skipping")
    def test_nothing(self):
        self.fail("shouldn't happen")

    @unittest.skipIf(mylib.__version__ < (1, 3),
                     "not supported in this library version")
    def test_format(self):
        # Tests that work for only a certain version of the library.
        pass

    @unittest.skipUnless(sys.platform.startswith("win"), "requires Windows")
    def test_windows_support(self):
        # windows specific testing code
        pass

    def test_maybe_skipped(self):
        if not external_resource_available():
            self.skipTest("external resource not available")
        # test code that depends on the external resource
        pass
```

このサンプルを冗長モードで実行すると以下のように出力される：

```sh
test_format (__main__.MyTestCase) ... skipped 'not supported in this library version'
test_nothing (__main__.MyTestCase) ... skipped 'demonstrating skipping'
test_maybe_skipped (__main__.MyTestCase) ... skipped 'external resource not available'
test_windows_support (__main__.MyTestCase) ... skipped 'requires Windows'

----------------------------------------------------------------------
Ran 4 tests in 0.005s

OK (skipped=4)
```

#### テストクラスのスキップ

- テストクラスに `@unittest.skip()` デコレータを付ける

```python
@unittest.skip("showing class skipping")
class MySkippedTestCase(unittest.TestCase):
    def test_not_run(self):
        pass
```

`TestCase.setUp()` もスキップすることができる．この機能はセットアップの対象のリソース（テストフィックスチャが依存している特定のリソース）が使用不可能な時に便利．

#### 「予期された失敗」の使用

- `expectedFailure()` デコレータを付ける

```python
class ExpectedFailureTestCase(unittest.TestCase):
    @unittest.expectedFailure
    def test_fail(self):
        self.assertEqual(1, 0, "broken")
```

#### 独自のスキップ用デコレータの作成

- 独自のデコレータのスキップしたい時点で `unittest.skip()` を呼ぶ

以下のデコレータはオブジェクトに指定した属性が無い場合にテストをスキップする：

```python
def skipUnlessHasattr(obj, attr):
    if hasattr(obj, attr):
        return lambda func: func
    return unittest.skip("{!r} doesn't have {!r}".format(obj, attr))
```

以下に示すデコレータと例外は，テストのスキップと "予期された例外"（**テストが失敗しても `TestResult` の失敗数にはカウントされなくなる例外**）を実装している．

- `@unittest.skip(reason)`

  - デコレートしたテストを無条件でスキップする．
  - `reason` にはテストをスキップした理由を str 型で記載する．

- `@unittest.skipIf(condition, reason)`

  - `condition` が真の場合，デコレートしたテストをスキップする．

- `@unittest.skipUnless(condition, reason)`

  - `condition` が偽の場合，デコレートしたテストをスキップする．
  - unless = if not

- `@unittest.expectedFailure`

  - ''
  - （原文）Mark the test as an expected failure. If the test fails it will be considered a success. If the test passes, it will be considered a failure.

- exception: `unittest.SkipTest(reason)`
  - この例外はテストをスキップするために送出される．
  - 普通はこれを直接送出する代わりに，`TestCase.skipTest()` やスキッピングデコレータの一つを使用する．

スキップしたテストの前後では，`setUp()` および `tearDown()` は実行されない．同様に，スキップしたクラスの前後では，`setUpClass()` および `tearDownClass()` は実行されない．スキップしたモジュールの前後では，`setUpModule()` および `tearDownModule()` は実行されない．

つまり，**テストがスキップされた場合，テストフィックスチャは実行されない**．

## <a name="subtest">サブテストを利用して繰り返しテストの区別を付ける</a>

（バージョン 3.4 で追加）

「**いくつかパラメータを振ってテストを実行したい**」など，テスト間に少しの差しかない場合，`unittest.subTest()` を用いて，テストメソッド内でそれらのテストを区別することができる（1 つのテストメソッド内で小さなテストをいくつか実行するイメージ！）．

例えば，以下のようなテストが考えられる：

```python
class NumbersTest(unittest.TestCase):

    def test_even(self):
        """
        Test that numbers between 0 and 5 are all even.
        """
        for i in range(0, 6):
            with self.subTest(i=i):
                self.assertEqual(i % 2, 0)
```

上記のテストの実行結果は以下のようになる．`i` が奇数のときにテストが失敗しているのが分かる．

```sh
======================================================================
FAIL: test_even (__main__.NumbersTest) (i=1)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "subtests.py", line 32, in test_even
    self.assertEqual(i % 2, 0)
AssertionError: 1 != 0

======================================================================
FAIL: test_even (__main__.NumbersTest) (i=3)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "subtests.py", line 32, in test_even
    self.assertEqual(i % 2, 0)
AssertionError: 1 != 0

======================================================================
FAIL: test_even (__main__.NumbersTest) (i=5)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "subtests.py", line 32, in test_even
    self.assertEqual(i % 2, 0)
AssertionError: 1 != 0
```

サブテスト無しの場合，最初の失敗で実行は停止し，i の値が表示されないためエラーの原因を突き止めるのは困難になる：

```sh
======================================================================
FAIL: test_even (__main__.NumbersTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "subtests.py", line 32, in test_even
    self.assertEqual(i % 2, 0)
AssertionError: 1 != 0
```

## <a name="class-function">クラスと関数</a>

この節では，unittest の API の詳細について説明する．

### <a name="class-function">テストクラス</a>

テストに関わる unittest のクラスを列挙する．

- [unittest- テストクラス](https://docs.python.org/ja/3/library/unittest.html#test-cases)

#### unittest のテストクラスの全体像，処理の依存関係

以下の画像を見れば，unittest でテストを走らせるときのクラス同士の関係が分かりやすい．これを念頭において各テストクラスを見ると unittest のフレームワークとしての全体像が掴みやすくなる．

[image]

（引用元[Unit Testing with Python](https://www.drdobbs.com/testing/unit-testing-with-python/240165163)）

#### `unittest.TestCase`

- `unittest.TestCase(methodName='run Test')`

  - `TestCase` クラスのインスタンスは，unittest の世界における論理的なテストの単位を示す．このクラスをベースクラスとして使用し，**必要なテストを具象サブクラスに実装する**．
  - `TestCase` クラスでは，以下 2 つが実装されている．
    - **テストランナーがテストを実行するためのインターフェース**
    - **各種のエラーをチェックしレポートするためのメソッド**
  - `TestCase` の各インスタンスは，`methodName` という名前の単一の基底メソッドを実行する．`TestCase` を使用する大半の場合 `methodName` を変更したりデフォルトの `runTest()` メソッドを再実装することはない．
  - `TestCase` のインスタンスのメソッドは 3 種類に大別される．
    - **テストの実行で使用されるメソッド**
      - `setUp()`，`tearDown()`，`skipTest()`，`subTest()` など
    - **テストで実装される条件のチェック，及び失敗のレポートを行うメソッド**
      - `assert*()`
      - どんな種類のテストケースを作れるかは，`assert*()` メソッドの一覧に目を通して把握しておくべき（[ここ](https://docs.python.org/ja/3/library/unittest.html#test-cases)から辿れる）
    - **問い合わせ用のメソッド（テスト自身の情報が収集される）**

- 注意点
  - バージョン 3.2 で変更: `TestCase` が `methodName` を指定しなくてもインスタンス化できるようになった．これにより対話的インタプリタから `TestCase` を簡単に試せるようになった．

#### `unittest.IsolatedAsyncioTestCase`

（バージョン 3.8 で追加）

- `unittest.IsolatedAsyncioTestCase`
  - `TestCase` と同様な API を持つが，特にコルーチンに対応している
    - 「コルーチン」とは，一旦処理を中断した後，続きから処理を再開できる処理のこと（並行処理などに用いられる）．

#### `unittest.FunctionTestCase`

- `unittest.FunctionTestCase`
  - `TestCase` インターフェースの内，テストランナーがテストを実行するためのインターフェースだけを実装しており，テスト結果のチェックやレポートに関するメソッドは実装していない．
  - **既存のテストコードを unittest によるテストフレームワークに組み込むために使用する**．

#### <a name="alias">非推奨のエイリアス</a>

歴史的な経緯で `TestCase` のいくつかのエイリアスが非推奨となった．以下のリンクに非推奨のエイリアスがまとまっている．

- [unittest - 非推奨のエイリアス](https://docs.python.org/ja/3/library/unittest.html#deprecated-aliases)

#### <a name="grouping">テストのグループ化：`unittest.TestSuite`</a>

この節では，テストのグループ化，つまり，個々のテストケースやテストスイートの集合であるテストスイートを扱うためのクラスを扱う（[参考リンク：unittest - テストのグループ化](https://docs.python.org/ja/3/library/unittest.html#grouping-tests)）．

- `unittest.TestSuite(tests=())`
  - <a href="#test-suite">テストスイート</a>の集合を表現する．テストをまとめてグループ化し，同時に実行する．
  - 通常のテストケースと同様に，テストランナーで実行するためのインタフェースを備えている．
  - `TestSuite` インスタンスを実行することは，スイートをイテレートして得られる個々のテストを実行することと同じである．
  - 引数 tests が指定された場合，それはテストケースに亘る繰り返し可能オブジェクトまたは内部でスイートを組み立てるための他のテストスイートでなければならない．後からテストケースやスイートをコレクションに付け加えるためのメソッドも提供されている．
  - `TestSuite` は `TestCase` オブジェクトのように振る舞う．`TestCase` との違いは，**スイートにはテストを実装しない点**にある．`TestSuite` 内ではテストケースの実装は行わず，あくまでも**テストスイートを構築するためだけ（テストケースをグループ化するためだけ）に使われる**．
  - `TestSuite` のインスタンスに（スイートの外に定義した）テストを追加するためのメソッドが用意されている．
    - `addTest`
      - `TestCase`，または `TestSuite` のインスタンスをテストスイートに追加する．
    - `addTests`
      - イテラブル tests に含まれる全ての `TestCase`，または `TestSuite` のインスタンスをスイートに追加する．
      - このメソッドは tests 上のイテレーションをしながらそれぞれのテストケースに対して `addTest` を呼び出すのと等価である．
  - 通常，`TestSuite` のテスト実行メソッド `run()` は，`TestRunner` が起動するため，ユーザが直接実行する必要はない．

#### <a name="load-test">テストのロードと起動</a>

テストのロードと起動に関するクラスは以下の 4 つ．

- **class: `unittest.TestLoader`**

  - テストクラス，テストモジュールからテストスイートを生成するためのクラス．
  - 通常，このクラスのインスタンスを明示的に生成する必要はない．テスト時に自動で生成される．
  - unittest の `unittest.defaultTestLoader` を共用インスタンスとして使用することができる．しかし，このクラスのサブクラスやインスタンスで，属性をカスタマイズすることもできる．
    - `unittest.defaultTestLoader`
      - `TestLoader` のインスタンス．パフォーマンスの関係で，各テストにて `TestLoader` を共用するのが目的．
  - **テストの実装者は特段意識する必要はない**．

- **class: `unittest.TestResult`**

  - どのテストが成功し，どのテストが失敗したかという情報を収集するのに使うクラス．
  - `TestResult` は複数のテスト結果を記録する．`TestCase` クラスと `TestSuite` クラスのテスト結果を正しく記録するため，**テスト開発者が独自にテスト結果を管理する処理を開発する必要はない**．
  - unittest を利用したテストフレームワークでは，`TestRunner.run()` が返す `TestResult` インスタンスを参照し，テスト結果をレポートする．
  - **テストの実装者は特段意識する必要はない**．
  - 覚えておくと良さげなメソッド
    - `expectedFailures`：予期されたエラーに関連

- **class: `unittest.TextTestResult`**

  - `TextTestRunner` に使用される `TestResult` の具象実装．
  - 注意点
    - バージョン 3.2 で追加: このクラスは以前 `_TextTestResult` という名前だった．以前の名前はエイリアスとして残っているが非推奨．

- **class: `unittest.TextTestRunner`**
  - 引数：`unittest.TextTestRunner(stream=None, descriptions=True, verbosity=1, failfast=False, buffer=False, resultclass=None, warnings=None, *, tb_locals=False)`
  - **結果をストリームに出力する，基本的なテストランナーの実装**．
  - `stream` が `None` の場合，デフォルトで `sys.stderr` が出力ストリームとして使われる．このクラスはいくつかの設定項目があるだけで，基本的に非常に単純である．
  - グラフィカルなテスト実行アプリケーションでは，独自のテストランナーを実装する必要がある．
  - テストランナーの実装は，unittest に新しい機能が追加されランナーを構築するインターフェースが変更されたときに備えて `**kwargs` を受け取れるようにするべき．
  - `TextTestRunner` における Warning の出力について
    - 「[デフォルトで無視](https://docs.python.org/ja/3/library/warnings.html#warning-ignored)」に設定されているとしても，このランナーのデフォルトでは `DeprecationWarning`，`PendingDeprecationWarning`，`ResourceWarning`，`ImportWarning` を表示する．
    - [unittest の非推奨メソッド](https://docs.python.org/ja/3/library/unittest.html#deprecated-aliases)で起きた非推奨警告も特別な場合として扱われ，警告フィルタが `'default'` もしくは `'always'` だったとき，対象の警告メッセージが出ないようにモジュールごとに 1 回だけ表示される．Python の `-Wd` オプションや `-Wa` オプション（「[警告の制御](https://docs.python.org/ja/3/using/cmdline.html#using-on-warnings)」を参照）を使ったり，`warnings` を `None` にしたりしておくと上述したデフォルトの動作を上書きできる．
  - 注意点
    - バージョン 3.2 で変更: `warnings` 引数が追加された．
    - バージョン 3.2 で変更: インポート時でなく，インスタンス化時にデフォルトのストリームが `sys.stderr` に設定される．
    - バージョン 3.5 で変更: `tb_locals` 引数が追加された．

#### テストクラスの全体像（再掲）

最後に復習として，テストクラスの全体像の画像を再度載せておく．テスト実行時にどのクラスがどのように使われているかを理解しておくと良い．

![PythonUnitTest1.gif](./PythonUnitTest1.gif)

（引用元[Unit Testing with Python](https://www.drdobbs.com/testing/unit-testing-with-python/240165163)）

#### <a name="protocol">load_tests プロトコル：テストディスカバリをカスタマイズする</a>

（バージョン 3.2 で追加）

モジュールやパッケージには，`load_tests` と呼ばれる関数を実装できる．これにより，通常のテスト実行時やテストディスカバリ時のテストのロードされ方をカスタマイズできる．

テストモジュールが `load_tests` を定義していると，それが `TestLoader.loadTestsFromModule()` から呼ばれる．引数は以下の通りで，戻り値は `TestSuite` であるべき：

```python
load_tests(loader, standard_tests, pattern) -> TestSuite:
```

- `load_tests` の引数
  - `loader`
    - ローディングを行う `TestLoader` のインスタンス．
  - `standard_tests`
    - そのモジュールからデフォルトでロードされるテスト．
    - これは，テストの標準セットのテストの追加や削除のみを行いたいテストモジュールに一般に使われる．
  - `pattern`
    - `loadTestsFromModule` からそのまま渡される．デフォルトは `None`．
    - この引数は，パッケージをテストディスカバリの一部としてロードするときに使われる．

特定の `TestCase` クラスのセットからテストをロードする典型的な `load_tests` 関数は以下のようになる：

```python
test_cases = (TestCase1, TestCase2, TestCase3)

def load_tests(loader, tests, pattern) -> TestSuite:
    suite = TestSuite()
    for test_class in test_cases:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    return suite
```

- テスト呼び出し時の挙動
  - コマンドラインからのテストの呼び出しや，`TestLoader.discover()` の呼び出しでも，パッケージを含むディレクトリで検索を始めた場合，そのパッケージの `__init__.py` をチェックし `load_tests` が探される．
    - `load_tests` 関数が存在しない場合，他のディレクトリであるかのようにパッケージの中を再帰的に検索する．
    - `load_tests` 関数が存在した場合，パッケージのテストの検索を `load_tests` に任され，`load_tests` が実行される．
      - これは**パッケージ内のすべてのテストを表す `TestSuite` を返すべき**である（`standard_tests` には、 `__init__.py` から収集されたテストのみが含まれる）．

要約すると，

- `load_tests` 関数はパッケージのテストディスカバリを自分で定義できる関数

のことである．

パターンは `load_tests` に渡されるので，パッケージは自由にテストディスカバリを継続（必要なら変更）できる．テストパッケージに '何もしない' `load_tests` 関数（デフォルトで走るテストディスカバリ）は以下のようになる：

```python
def load_tests(loader, standard_tests, pattern):
    # top  level directory cached on loader instance
    this_dir = os.path.dirname(__file__)
    package_tests = loader.discover(
        start_dir=this_dir,
        pattern=pattern
    )
    standard_tests.addTests(package_tests)
    return standard_tests
```

- バージョン 3.5 で変更: パッケージ名がデフォルトのパターンに適合するのが不可能なため，検索ではパッケージ名が `pattern` に適合するかのチェックは行われなくなった．

## <a name="fixture">クラスとモジュールのフィクスチャ</a>

- [unittest - クラスとモジュールのフィクスチャ](https://docs.python.org/ja/3/library/unittest.html#class-and-module-fixtures)

### クラス，モジュールレベルのテストフィクスチャ

クラスレベル，モジュールレベルのテストフィクスチャが TestSuite に実装されている．

- クラスレベルのテストフィックスチャ

  - テストスイートが新しいテストクラスでテストを始める時，前回のテストクラスの `tearDownClass()` を呼び出し，その後に新しいテストクラスの `setUpClass()` を呼び出す．
  - ex) `TestCase1.setUpClass()` -> `TestCase1.tearDownClass()` -> `TestCase2.setUpClass()` -> ...

- モジュールレベルのテストフィクスチャ
  - クラスと同様に，新しいテストモジュールでテストを始める時，そのモジュールが前回のテストモジュールとは異なる場合，以前のモジュールの `tearDownModule` を実行し，次に新しいモジュールの `setUpModule` を実行する．そして，新しいモジュールの全てのテストが実行された後，最後の `tearDownClass` と `tearDownModule` が実行されます。
  - ex) `test_foo.setUpModule()` -> `test_foo.tearDownModule()` -> `test_bar.setUpModule()` -> ... -> `test_bar.TestCaseBar.tearDownClass()` -> `test_bar.tearDownModule()`

上記のテストフィクスチャの生成からそれを `tearDown` メソッドでクリーンアップする流れは以下の図を見ると分かりやすい．これはユニットテストの一般的なフローである．

![Unit Test のフロー](./pattern.png)

（引用元：[Python UnitTest 快速上手](https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcQiNWlcN28Nuz0RPCFQA5hxl1wzVSCOO3sFcuZo3kPeCpBZDF6e&usqp=CAU)）

### テストの並列化時の共有フィクスチャの注意点

共有フィクスチャ（複数のテストクラス，テストモジュールに跨がるテストフィクスチャ）は，テストの並列化などの潜在的な機能と同時にはうまくいかず，テストの分離を壊してしまうため気をつけて使うべき．

unittest のテストローダによるテスト作成のデフォルトの順序では，同じモジュールやクラスからのテストはすべて同じグループにまとめられる．これにより，`setUpClass()`，`setUpModule()` などは，一つのクラスやモジュールにつき一度だけ呼ばれる．この順序をバラバラにし，異なるモジュールやクラスのテストが並ぶようにすると，共有フィクスチャ関数は一度のテストで複数回呼ばれるようにもなる．

共有フィクスチャは標準でない順序で実行されることを意図していない．共有フィクスチャをサポートしたくないフレームワークのために，`BaseTestSuite` が未だに存在している．

共有フィクスチャ関数（`setUpClass()`，`setUpModule()` など）のいずれかで例外が発生した場合，そのテストはエラーとして報告される．そのとき，対応するテストインスタンスが無いため（`TestCase` と同じインタフェースの) `_ErrorHolder` オブジェクトが生成され，エラーを表す．標準 unittest テストランナーを使っている場合はこの詳細は問題にならないが，unittest を用いてテストフレームワークを自作する場合は注意が必要．

### <a name="setupclass-teardownclass">クラスレベルのテストフィクスチャ：setUpClass と tearDownClass</a>

クラスレベルのテストフィクスチャである，`setUpClass()`，`tearDownClass()` はクラスメソッドとして実装されなければならない：

```python
import unittest

class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._connection = createExpensiveConnectionObject()

    @classmethod
    def tearDownClass(cls):
        cls._connection.destroy()
```

基底クラスの `setUpClass` および `tearDownClass` を使いたいなら，それらを自分で呼び出さなければならない．`unittest.TestCase` の実装はデフォルトで空である．

- `setUpClass` の中で例外が送出されたら，クラス内のテストは実行されず，`tearDownClass` も実行されない．
- スキップされたクラスは `setUpClass` も `tearDownClass` も実行されない．
- 例外が `SkipTest` 例外であれば，そのクラスはエラーではなくスキップされたものとして報告される（failure に換算されない）．

### <a name="setupmodule-teardownmodule">モジュールレベルのテストフィクスチャ：setUpModule と tearDownModule</a>

モジュールレベルのテストフィクスチャである，`setUpModule()`，`tearDownModule()` は関数として定義されなければならない：

```python
def setUpModule():
    createConnection()

def tearDownModule():
    closeConnection()
```

- `setUpModule` の中で例外が送出されたら，モジュール内のテストは実行されず，`tearDownModule` も実行されない．
- 例外が `SkipTest` 例外であれば，そのモジュールはエラーではなくスキップされたものとして報告される（failure に換算されない）．

例外が発生しても実行しなければならないクリーンアップ処理を追加するには，`unittest.addModuleCleanup` を使用する（[ドキュメント](https://docs.python.org/ja/3/library/unittest.html#class-and-module-fixtures)を参照）．

> To add cleanup code that must be run even in the case of an exception, use `addModuleCleanup`

### <a name="signal-handling">シグナルハンドリング</a>

（バージョン 3.2 で追加）

#### テストの中断

unittest の `-c`（`--catch`）コマンドラインオプションや，`unittest.main()` の `catchbreak` パラメータは，テスト実行中の ctrl-C の処理をより扱いやすくする．

**中断捕捉動作が有効である場合，ctrl-C が押されると，現在実行されているテストまで完了され**，そのテストランが終わると今までの結果が報告される．ctrl-C がもう一度押されると，通常通り `KeyboardInterrupt` が送出される．

つまり，テストを完全に中断したい場合，2 度 ctrl-C を押す必要がある．

#### シグナルハンドラの実装：unittest における ctrl-C の扱い方

シグナルハンドラを処理する ctrl-C は，独自の `signal.SIGINT` ハンドラをインストールするコードやテストの互換性を保とうとする．unittest ハンドラが呼ばれ，それがインストールされた `signal.SIGINT` ハンドラでなければ，すなわちテスト中のシステムに置き換えられて移譲されたなら，それはデフォルトのハンドラを呼び出す．インストールされたハンドラを置き換えて委譲するようなコードは，通常その動作を期待するからである．unittest の ctrl-C 処理を無効にしたいような個別のテストには`removeHandler()` デコレータが使える．

unittest では，フレームワークの作者がテストフレームワーク内で ctrl-C 処理を有効にするためのいくつかのユーティリティ関数が提供されている．

- `unittest.installHandler()`

  - ctrl-C ハンドラをインストールする．（主に，ユーザが ctrl-C を押すことにより）`signal.SIGINT` が受け取られると、登録した結果すべてに `stop()` が呼び出される．

- `unittest.registerResult(result)`

  - ctrl-C 処理のために `TestResult` を登録する．結果を登録するとそれに対する弱参照が格納されるため，結果がガベージコレクトされるのを妨げない．
  - ctrl-C 処理が有効でなければ，`TestResult` オブジェクトの登録には副作用がない．そのため，テストフレームワークは処理が有効か無効かにかかわらず，作成する全ての結果を無条件に登録できる．

- `unittest.removeResult(result)`

  - 登録された結果を削除する．一旦結果が削除されると，ctrl-C が押された際にその `TestResult` オブジェクトに対して `stop()` が呼び出されなくなる．

- `unittest.removeHandler(function=None)`
  - 引数なしで呼び出されると，この関数は Ctrl+C のシグナルハンドラを（それがインストールされていた場合）削除する．つまり，**テストを ctrl-C で止められなくなる**．
  - デコレータとしての用途
    - この関数はテストが実行されている間，ctrl+C のハンドラを一時的に削除するテストデコレータとしても使用可能である

```python
@unittest.removeHandler
def test_signal_handling(self):
    ...
```

## 終わりに

ドキュメントをざっと読んでみて，unittest がどういう使い方されるかとか，どういった流れでテストが実装されるかとかの概要は掴めた．また，「テストフィクスチャ」，「テストケース」，「テストスイート」，「テストランナー」というテストで一般的に使われる概念を学ぶことができたのは良かった．

次はテストを書く上で非常に重要な「モック」（mock）の書き方を学んでいこうかと思う．本記事で扱った unittest には `unittest.mock` という mock を書くためのモジュールが用意されているためそれを使って学んでいこうかな（以下のリンクを参照）．

https://docs.python.org/ja/3/library/unittest.mock-examples.html
https://docs.python.org/ja/3/library/unittest.mock.html

## 補足

### 用語：ストリーム stream

ストリームとは．

> ストリーム（英: stream）とは、連続したデータを「流れるもの」として捉え、そのデータの入出力あるいは送受信を扱うことであり、またその操作のための抽象データ型を指す[1]。出力ストリーム (output stream) を利用してデータの書き込みを行ない、また入力ストリーム (input stream) を利用してデータの読み出しを行なう。ファイルの入出力を扱うもの、メモリバッファの入出力を扱うもの、ネットワーク通信を扱うものなどさまざまなものがある。
>
> 特にオペレーティングシステムによって用意されている標準的な入力元や出力先に関しては、標準ストリームと呼ばれる特別なストリームが用意されていることもある。キーボードからの入力や、ディスプレイへの出力は標準ストリームによって抽象化され、個別のプログラムからはデバイスハードウェアを意識する必要がなくなる。

（引用元：[Wikipedia - ストリーム（プログラミング）](<https://ja.wikipedia.org/wiki/%E3%82%B9%E3%83%88%E3%83%AA%E3%83%BC%E3%83%A0_(%E3%83%97%E3%83%AD%E3%82%B0%E3%83%A9%E3%83%9F%E3%83%B3%E3%82%B0)>)）

要するに，「データの入出力のハードウェアの部分を抽象化してソフトウェア的に扱えるようにしたもの」ってこと？

## 参考書籍

- Python 実践入門
  - よく纏まってて Python の開発に必要な基礎知識はこれで身に付く．
  - Python 3.8 の機能を整理して解説してくれててとても良い．

<iframe style="width:120px;height:240px;" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" src="https://rcm-fe.amazon-adsystem.com/e/cm?ref=qf_sp_asin_til&t=pyteyon-22&m=amazon&o=9&p=8&l=as1&IS2=1&detail=1&asins=429711111X&linkId=72f3b529eaf9d4736a3ad82dfa67ba1b&bc1=000000&lt1=_blank&fc1=333333&lc1=0066c0&bg1=ffffff&f=ifr">
    </iframe>

- Effective Python
  - 自分の手元にあるのは翻訳版．原著は検索すれば PDF が落ちてる．

<iframe style="width:120px;height:240px;" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" src="https://rcm-fe.amazon-adsystem.com/e/cm?ref=qf_sp_asin_til&t=pyteyon-22&m=amazon&o=9&p=8&l=as1&IS2=1&detail=1&asins=4873117569&linkId=1f820d66065c247c4b7cd349f18cb805&bc1=000000&lt1=_blank&fc1=333333&lc1=0066c0&bg1=ffffff&f=ifr">
    </iframe>

- 初めての Python 第 3 版
  - 鈍器．内容濃い．重め．少し古い．

<iframe style="width:120px;height:240px;" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" src="https://rcm-fe.amazon-adsystem.com/e/cm?ref=qf_sp_asin_til&t=pyteyon-22&m=amazon&o=9&p=8&l=as1&IS2=1&detail=1&asins=4873113938&linkId=eb689f179f4a60e4fd9565144433e441&bc1=000000&lt1=_blank&fc1=333333&lc1=0066c0&bg1=ffffff&f=ifr">
    </iframe>
