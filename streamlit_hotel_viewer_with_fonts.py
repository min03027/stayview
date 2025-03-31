chart = alt.Chart(score_df).mark_bar().encode(
    x=alt.X('항목', sort=None, axis=alt.Axis(labelAngle=0)),
    y=alt.Y('점수', axis=alt.Axis(titleAngle=0)),
    color=alt.condition(
        alt.datum.점수 < 0,
        alt.value('crimson'),
        alt.value('steelblue')
    )
).properties(width=600, height=400)

st.altair_chart(chart, use_container_width=True)




