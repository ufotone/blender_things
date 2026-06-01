# Bevel All Selected Object Edges

Blender 5 用のアドオンです。選択中のメッシュオブジェクトすべてに、全エッジ対象の Bevel モディファイアを追加します。

## 使い方

1. `bevel_all_selected_edges.zip` を Blender の `Edit > Preferences > Add-ons > Install...` からインストールします。
2. Add-ons で `Bevel All Selected Object Edges` を有効にします。
3. 3D View の `Item > Bevel All Edges` で設定を調整し、`Bevel All Edges` を実行します。
4. 実行後、左下のオペレーターパネルで値を変えると、その値も次回実行時の初期値として保存されます。

## 仕様

- 選択中のメッシュオブジェクトだけを処理します。
- `Bevel All Edges` という Bevel モディファイアを追加または更新します。
- `Limit Method` は `None` なので、すべての辺が対象です。
- `Apply` をオンにすると、モディファイアを即座に適用します。
- 設定値はアドオン Preferences に保存されるため、Blender を開き直しても再利用できます。
- 標準 Bevel の主要設定として、影響対象、幅タイプ、幅、セグメント、断面形状、マテリアル、法線のハード化、重複の回避、ループスライド、シーム、シャープ、留め継ぎ、面の強さを調整できます。
