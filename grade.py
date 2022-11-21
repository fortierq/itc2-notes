import streamlit as st
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import HoverTool

st.set_page_config(page_title="Notes d'informatique commune", layout="wide")
st.title("Notes d'informatique commune")

height = 400

df_all = pd.read_csv("grade.csv", index_col="id")

classe = st.selectbox("Classe", df_all["classe"].unique())
df = df_all[df_all["classe"] == classe]
df.drop(columns=["classe"], inplace=True)
ranks = list(range(1, len(df) + 1))

col1, col2 = st.columns(2)

with col2:
    student = st.selectbox("Élève", df.index.sort_values())
    df_student = df.loc[[student], ::-1].dropna(axis=1)
    fig_line = figure(
        toolbar_location=None,
        title=f"Notes élève n°{student}",
        sizing_mode="stretch_width",
        height=height,
        y_axis_label="Note",
        x_axis_label=f"Moyenne : {df_student.iloc[0, :].mean():.2f}",
        y_range=(0, 20),
    )
    fig_line.line(list(range(len(df.columns))),
                  df_student.iloc[0], line_width=2)
    x = list(range(len(df_student.columns)))  # TODO : fix warning
    fig_line.xaxis.ticker = x
    fig_line.xaxis.major_label_overrides = {
        i: df_student.columns[i] for i in x}
    st.bokeh_chart(fig_line)

with col1:
    ds = st.selectbox("Devoir", df.columns)
    df_sort = df.sort_values(by=ds, ascending=False)
    df_sort["eleves"] = df_sort.index
    df_sort["rang"] = ranks
    df_sort["note"] = df_sort[ds]
    p = figure(toolbar_location=None,
               title=f"Classement {ds}\nMoyenne : {df[ds].mean():.2f}, Écart-type : {df[ds].var()**.5:.2f}",
               sizing_mode="stretch_width",
               height=height,
               x_axis_label="Rang",
               y_axis_label="Note",
               tooltips=[("Élève n°", "@eleves"), ("Note", "@note"), ("Rang", "@rang")])
    p.vbar(x="rang", top=ds, width=0.9, source=df_sort)
    st.bokeh_chart(p)

st.markdown("""---""")

df["mean"] = df.mean(axis=1)
df["eleves"] = df.index
df.sort_values(by="mean", ascending=False, inplace=True)
df["rang"] = ranks
fig_mean = figure(
    toolbar_location=None,
    title=f"Classement général\nMoyenne de classe : {df['mean'].mean():.2f}, Écart-type : {df['mean'].var()**.5:.2f}",
    sizing_mode="stretch_width",
    height=height,
    x_axis_label="Rang",
    y_axis_label="Note",
    tooltips=[("Élève n°", "@eleves"), ("Moyenne", "@mean"), ("Rang", "@rang")])
fig_mean.vbar(x="rang", source=df, top="mean", width=0.9)
st.bokeh_chart(fig_mean)
