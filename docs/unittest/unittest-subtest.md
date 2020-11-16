# unittest を使う

## unittest で複数のテストケースをテストする

複数のテストケースをテストしたい場合，以下 2 つの方法がある．

- `unittest.subTest`
  - [Python の単体テストで大量の入力パターンを効率用区テストする方法](https://qiita.com/Asayu123/items/61ef72bb829dd8baba9f)
- parameterized モジュール
  - [GitHub: wolever/parameterized](https://github.com/wolever/parameterized)

## private メソッドのテスト

- リフレクションを用いると良い？
  - private メソッドをテストしなきゃいけない状況は，そもそもオブジェクト指向をなんか間違えてるから設計やり直した方が良いとは聞くがどうすれば良いか？
    - リフレクションを用いると良い．ドメイン駆動の有名な本でも，実際テスト時のみ利用するメソッド等を定義したり，リフレクション等を使って TDD を実践していたため，ありだと思う．
    - これを参考にしていた感じ：https://github.com/mockito/mockito/wiki/Mockito-And-Private-Methods

## 参考

- [アジャイル侍の次に読む技術書](https://www.slideshare.net/t_wada/books-to-read-next-to-agilesamurai)
