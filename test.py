import streamlit as st
import pandas as pd
import math


#--------------レース一覧
st.title('レース一覧')
df = pd.read_csv('DB作成1.csv', index_col=0)
st.dataframe(df.fillna('-'), width=1500, height=500)
#--------------レース一覧

# df_list = list([df.index.tolist()])

# st.text(df_list)
# st.multiselect('ラベル', ['選択肢1', '選択肢2', '選択肢3'],"")



#--------------サイドバー
st.sidebar.header('ウマ娘を選択')
selection = st.sidebar.selectbox("", ['アグネスタキオン','ウイニングチケット','ウオッカ','エアグルーヴ','エルコンドルパサー','オグリキャップ','キングヘイロー','グラスワンダー','ゴールドシップ','サイレンススズカ','サクラバクシンオー','シンボリルドルフ','スーパークリーク','スペシャルウィーク','タイキシャトル','ダイワスカーレット','テイエムオペラオー','トウカイテイオー','ナイスネイチャ','ハルウララ','ビワハヤヒデ','マチカネフクキタル','マヤノトップガン','マルゼンスキー','ミホノブルボン','メジロマックイーン','メジロライアン','ライスシャワー','カレンチャン','ナリタタイシン'])
# st.write(f"{selection} を選択中")
st.sidebar.header("ファン数ボーナスを選択")
fanbonus = st.sidebar.slider('', 10, 150, 50, 1)
# st.write(f"{fanbonus} %ボーナス")
#--------------サイドバー



#--------------サイドバーで選んだ娘の目標
st.title(f"{selection} の目標レース一覧")
df1 = pd.read_csv('目標レース一覧.csv')    #----df1 は　ただの目標レース一覧
df_name  = df1[["競争名","期別","月","前後半",f"{selection}"]].rename(columns={f"{selection}": '条件'}).dropna(subset=['条件'])
  #----df1　の競争名と選択した娘の列のみ表示、さらに娘の列名を「条件」に書き換え、nullを含む行を削除（目標レースの行にのみ値が入っているため）してdf_nameに格納。
st.dataframe(df_name, width=1500, height=500)

# df12 = df1[["競争名",f"{selection}"]]
# df11 = df1[["競争名",f"{selection}"]].dropna()
# st.title('DF11の確認')
# st.dataframe(df11, width=1500, height=500)


#--------------ただのレース一覧に条件をくっつけて競争名でくくる
dfmerge = pd.merge(df, df_name, how='inner').fillna('')
st.title(f"{selection} の目標レース詳細")
st.dataframe(dfmerge, width=1500, height=500)


keisan1 = dfmerge['ファン数'].sum() + (dfmerge['ファン数'].sum() * (int(f"{fanbonus}") / 100 )) 
keisan2 = 320000 - keisan1

if keisan2 > 0:
    st.write("最低獲得可能ファン数は" + '{:,}'.format(math.floor(int(keisan1))) + "です(URA3戦を含む)。　" + "レジェンドまであと" + '{:,}'.format(math.floor(int(keisan2))) + "人足りません。")
else:
    st.write("最低獲得可能ファン数は" + '{:,}'.format(math.floor(int(keisan1))) + "です(URA3戦を含む)。　" + "目標レースすべて1着でレジェンド達成可能です。")





st.title(f"{selection} のおすすめレース")
st.text("（表示されているファン数はボーナス反映済み）")

dfmerge2 = pd.merge(df, df1, )
dfmerge2 = dfmerge2[["競争名","期別","月","前後半",f"{selection}"]].dropna(subset=[f"{selection}"])
# st.dataframe(dfmerge2, width=1500, height=500)


dfmerge3 = df.append(dfmerge2, ignore_index=True)

dfmerge3 = dfmerge3.drop_duplicates(subset=["競争名","期別","月","前後半"], keep=False).fillna('')

dfmerge3['ファン数'] = dfmerge3['ファン数'] * (1 + (int(f"{fanbonus}") / 100 ))
# dfmerge3 = pd.merge(df, dfmerge2, not on=["競争名","期別","月","前後半"])


st.dataframe(dfmerge3.round().sort_values('ファン数', ascending=False).drop([f"{selection}"], axis=1), width=1500, height=500)
