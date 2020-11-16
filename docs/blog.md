# pytest の勉強

## Python におけるテストの基本

以下 2 つの記事で Python でのテストの基礎をまとめている．

## テスト / Pytest の用語

テストや Pytest に関する用語のまとめ

### テストディスカバリ

- **テストディスカバリ** test discovery
  - テストフレームワークが実行するテストを検索，検出すること，またその実装

#### pytest におけるテストディスカバリ

`pytest` コマンドを実行した際，pytest がテストコードを検出できるようにするには，モジュール名，クラス名，メソッド名，関数名に以下の命名規則に準拠した名前を付ける必要がある．

- モジュール名：`test_<something>.py`
- クラス名：`Test<Something>`
- メソッド名，関数名：`test_<something>`

尚，テストディスカバリのルールを変更する設定を行うこともできるため，それについては後述する．

---

## pytest

### コマンド

- 現在のディレクトリ配下の全てのテストを実行

```sh
pytest -v
```

- 特定のディレクトリのテストのみを実行

```sh
pytest -v ./tests/mymodule
```

- 特定のテストモジュールのみのテストを実行

```sh
pytest -v ./tests/mymodule/test_my_functions.py
```

- 特定のメソッドのみのテストを実行
  - 下記は `test_my_functions.py` の `test_myfunc1`，`test_myfunc3` というテスト関数を実行

```sh
pytest -v \
  ./tests/mymodule/test_my_functions.py::test_myfunc1 \
  ./tests/mymodule/test_my_functions.py::test_myfunc3
```

### オプション

- オプション一覧

```sh
pytest -h
# pytest --help
```

- `--collect-only`
  - 実行されるテストを表示する．テストは実行されない．
  - 指定したオプション（後述）と構成に基づいてテストディスカバリが行われ，検出されたテストモジュール，クラス，メソッド，関数が表示される

```sh
pytest --collect-only
```

出力例

```sh
=========================================== test session starts ============================================
platform darwin -- Python 3.9.0, pytest-5.4.3, py-1.9.0, pluggy-0.13.1 -- /Users/pyteyon/Projects/basics/Languages/Python/tdd-python/venv/bin/python
cachedir: .pytest_cache
rootdir: /Users/pyteyon/Projects/basics/Languages/Python/tdd-python
collected 7 items
<Module tests/test_tmp.py>
  <Function test_tuple_comprehension>
    Check tuple comprehension with generator
  <Function test_skip>
  <Function test_tuple_comprehension_failing>
    Failing test
<Module tests/tasks/test_task.py>
  Test the "Task" data type.
  <Function test_defaults>
    Using no parameters should invoke defaults.
  <Function test_member_access>
    Check .field functionality of namedtuple.
  <Function test_asdict>
    _asdict() should return a dictionary.
  <Function test_replace>
    _replace() should change passed in fields.

========================================== no tests ran in 0.01s ===========================================
```

- `-k [フィルタリングの条件]`
  - 実行したいテストのフィルタリングを行う
  - 検索条件に基づき，テストモジュール名，クラス名，メソッド名，関数名を検索し，フィルタリングの条件を満たすテストをのみを実行する
  - `--collect-only` と組み合わせると，自分が実行したいテストを正しくフィルタリングできているかを表示できる
  - フィルタリングの条件については[ドキュメント](url)を参照

使用例

```sh
# 自作クラスとそのメソッドのテストコードのフィルタリング
$ pytest -k "MyModel and dict" --collect-only
=========================================== test session starts ============================================
platform darwin -- Python 3.9.0, pytest-5.4.3, py-1.9.0, pluggy-0.13.1 -- /Users/pyteyon/Projects/basics/Languages/Python/tdd-python/venv/bin/python
cachedir: .pytest_cache
rootdir: /Users/pyteyon/Projects/basics/Languages/Python/tdd-python
collected 5 items / 3 deselected / 2 selected
<Module samples/test_models.py>
  <Class TestMyModel>
      <Function test_from_dict>
      <Function test_to_dict>

========================================== 3 deselected in 0.01s ===========================================

# テストの実行
$ pytest -v -k "MyModel or create or dump"
=========================================== test session starts ============================================
platform darwin -- Python 3.9.0, pytest-5.4.3, py-1.9.0, pluggy-0.13.1 -- /Users/pyteyon/Projects/basics/Languages/Python/tdd-python/venv/bin/python
cachedir: .pytest_cache
rootdir: /Users/pyteyon/Projects/basics/Languages/Python/tdd-python
collected 5 items / 3 deselected / 2 selected

samples/test_models.py::TestMyModel::test_from_dict PASSED                                           [ 50%]
samples/test_models.py::TestMyModel::test_to_dict PASSED                                             [100%]

===================================== 2 passed, 3 deselected in 0.01s ======================================
```

- `-m [マーカーの条件]`

---

## pytest.mark

pytest では，`pytest.mark` モジュールを用いて，テスト関数の一部にデコレータでマークを付け，特定のマークが付与されたメソッド，関数のみをまとめて実行できるという機能がある．つまり，この機能を利用してテスト関数に対してメタデータを付与できるということである．

マーカーには，builtin マーカーとカスタムマーカーの 2 種類があり，とても便利．

- builtin マーカーの一部
  - `usefixtures`: use fixtures on a test function or class
  - `filterwarnings`: filter certain warnings of a test function
  - `skip`: always skip a test function
  - `skipif`: skip a test function if a certain condition is met
  - `xfail`: produce an “expected failure” outcome if a certain condition is met
  - `parametrize`: perform multiple calls to the same test function.
- 全ての builtin マーカーを知りたい場合は [API Reference](https://docs.pytest.org/en/latest/reference.html#marks-ref) を参照

カスタムマーカーの設定方法については以下を参照．

- 公式 doc：[Marking test functions with attributes](https://docs.pytest.org/en/latest/mark.html)
  - `pytest.ini` などの設定ファイルを利用してカスタムマーカーの設定を行う方法を紹介している

### builtin マーカーの例

- `skip`
  - テストをスキップする
  - このマーカーを付与することで，一旦避けておきたいテストをスキップできる．テスト結果にスキップしたことが明示されるため，スキップしたテストの存在を忘れることもない．

```python
@pytest.mark.skip()
def test_skip():
    lis = [i for i in range(2)]
    expected = [0, 1, 2]

    assert lis == expected
```

- `xfail`
  - 失敗することが想定されるテストに付与するマーカー
  - このマーカーを付与することで，テストのステータスが `FAILED` から `xfail` になり，開発者が「このテストは落ちることが分かってるよ」というのを明示できる
  - "expected failure" の略．

```python
import pytest


@pytest.mark.xfail()
def test_tuple_comprehension_failing():
    """ Failing test """

    tup = tuple(i for i in range(3))  # (0, 1, 2)
    expected = (1, 2, 3)

    # 以下のテストは落ちる
    assert tup == expected  # (0, 1, 2) == (1, 2, 3)
```

### カスタムマーカーの例

例えば，実行速度が遅いテスト関数に `slow` というマーカーを付与し，`-m "not slow"` というオプションを付けてテストを実行すれば，遅いテストを避けてテストを実行することができる．

```python
import pytest


def test_add_str():
    """ Failing test """

    string = "Hello" + "World"
    expected = "HelloWorld"

    assert string == world


@pytest.mark.slow()  # 名前解決は勝手にしてくれる
def test_slow_func():
    # なんか重い処理
```

テスト実行

```sh
# slow マーカーを検出できるかチェック
pytest -v -m "slow" --collect-only

# slow 以外のテストを実行
pytest -v -m "not slow"
```

- 注意点
  - `pytest.ini` などの設定ファイルにカスタムマーカーを登録していない場合，warning が出力される（テスト自体は実行される）
  - デフォルトでは，設定ファイルへのカスタムマーカーの登録はしなくてもテストを実行できる．
  - しかし，厳密にマーカーを管理したい場合，事前登録なしのカスタムマーカーを全てエラーにするという設定を行える．詳しくは以下のドキュメントを参照．
    - 公式 doc：[Marking test functions with attributes](https://docs.pytest.org/en/latest/mark.html)
