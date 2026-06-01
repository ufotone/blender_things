# Auto Highlight in Outliner

Blender 5 用のシンプルなアドオンです。3D View などで選択したアクティブオブジェクトを、表示中の Outliner 上で自動的に展開してハイライトします。

## 使い方

1. `auto_highlight_in_outliner.zip` を Blender の `Edit > Preferences > Add-ons > Install...` からインストールします。
2. Add-ons で `Auto Highlight in Outliner` を有効にします。
3. Outliner を表示した状態でオブジェクトを選択します。

## 設定

- `Auto Highlight`: 選択変化に合わせた自動ハイライトのオン / オフ。
- `Poll Interval`: 選択変化を確認する間隔。小さいほど反応が速くなります。
- `Use View Layer Mode`: Outliner を `View Layer` 表示に切り替えてから表示対象を探します。

## 補足

Blender の Outliner 操作は UI エリアに依存するため、Outliner エディタが画面に表示されている時だけ動作します。表示中の Outliner が複数ある場合は、それぞれでアクティブオブジェクトを表示します。
