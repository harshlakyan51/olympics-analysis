import streamlit as st
import pandas as pd
import preprocessor, helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

# Page Configurations
st.set_page_config(
    page_title="Olympics Data Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data
with st.spinner("Loading data..."):
    df = pd.read_csv('athlete_events.csv')
    region_df = pd.read_csv('noc_regions.csv')
    df = preprocessor.preprocess(df, region_df)

# Sidebar
st.sidebar.title("🏅 Olympics Analysis")
st.sidebar.image('https://e7.pngegg.com/pngimages/1020/402/png-clipart-2024-summer-olympics-brand-circle-area-olympic-rings-olympics-logo-text-sport.png')
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete wise Analysis')
)

# Medal Tally
if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years,country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year",years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in " + str(selected_year) + " Olympics")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " overall performance")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " performance in " + str(selected_year) + " Olympics")
    st.table(medal_tally)

# Overall Analysis
if user_menu == 'Overall Analysis':
    st.markdown("## 📊 Overall Analysis")

    editions = df['Year'].nunique() - 1
    cities = df['City'].nunique()
    sports = df['Sport'].nunique()
    events = df['Event'].nunique()
    athletes = df['Name'].nunique()
    nations = df['region'].nunique()

    col1, col2, col3 = st.columns(3)
    col1.metric("🏙️ Hosts", cities)
    col2.metric("🎽 Sports", sports)
    col3.metric("🧑‍🤝‍🧑 Athletes", athletes)

    col4, col5, col6 = st.columns(3)
    col4.metric("🎉 Editions", editions)
    col5.metric("🌍 Nations", nations)
    col6.metric("🏆 Events", events)

    tab1, tab2, tab3 = st.tabs(["📈 Trends", "🔥 Heatmap", "🏆 Athletes"])

    with tab1:
        nations_over_time = helper.data_over_time(df, 'region')
        fig = px.line(nations_over_time, x="Edition", y="region")
        st.markdown("### Participating Nations over the years")
        st.plotly_chart(fig)

        events_over_time = helper.data_over_time(df, 'Event')
        fig = px.line(events_over_time, x="Edition", y="Event")
        st.markdown("### Events over the years")
        st.plotly_chart(fig)

        athlete_over_time = helper.data_over_time(df, 'Name')
        fig = px.line(athlete_over_time, x="Edition", y="Name")
        st.markdown("### Athletes over the years")
        st.plotly_chart(fig)

    with tab2:
        st.markdown("### Events per Sport over the Years")
        fig, ax = plt.subplots(figsize=(20, 20))
        temp_df = df.drop_duplicates(['Year', 'Sport', 'Event'])
        pivot_df = temp_df.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0)
        sns.heatmap(pivot_df, annot=True, fmt='g', cmap='YlGnBu', ax=ax)
        st.pyplot(fig)

    with tab3:
        st.markdown("### Most Successful Athletes")
        sport_list = df['Sport'].unique().tolist()
        sport_list.sort()
        sport_list.insert(0, 'Overall')
        selected_sport = st.selectbox('Select a Sport', sport_list)
        successful_df = helper.most_successful(df, selected_sport)
        st.dataframe(successful_df)

# Country-wise Analysis
if user_menu == 'Country-wise Analysis':
    st.sidebar.title('Country-wise Analysis')
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox('Select a Country', country_list)

    st.markdown(f"## 🇨🇳 {selected_country} Analysis")

    country_df = helper.yearwise_medal_tally(df, selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.markdown("### Medal Tally Over the Years")
    st.plotly_chart(fig)

    pt = helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    sns.heatmap(pt, annot=True, fmt='g', cmap='YlOrRd', ax=ax)
    st.markdown("### Excellence in Sports")
    st.pyplot(fig)

    top10_df = helper.most_successful_countrywise(df, selected_country)
    st.markdown("### Top 10 Athletes")
    st.dataframe(top10_df)

# Athlete wise Analysis
if user_menu == 'Athlete wise Analysis':
    st.markdown("## 🧍 Athlete Wise Analysis")

    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall', 'Gold', 'Silver', 'Bronze'], show_hist=False, show_rug=False)
    fig.update_layout(width=1000, height=600)
    st.markdown("### Age Distribution")
    st.plotly_chart(fig)

    x, name = [], []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics', 'Art Competitions',
                     'Handball', 'Weightlifting', 'Wrestling', 'Water Polo', 'Hockey',
                     'Rowing', 'Fencing', 'Shooting', 'Boxing', 'Taekwondo', 'Cycling',
                     'Diving', 'Canoeing', 'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens', 'Beach Volleyball',
                     'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']

    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(width=1000, height=600)
    st.markdown("### Age Distribution by Sport (Gold Medalists)")
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df, selected_sport)
    fig, ax = plt.subplots()
    sns.scatterplot(x='Weight', y='Height', data=temp_df, hue='Medal', style='Sex', s=60, ax=ax)
    st.markdown("### Height vs Weight")
    st.pyplot(fig)

    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(width=1000, height=600)
    st.markdown("### Men vs Women Participation")
    st.plotly_chart(fig)

# Footer
st.markdown("---")
