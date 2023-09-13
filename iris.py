import altair as alt
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st
from PIL import Image


def show_description(species: str) -> None:
    @st.cache(suppress_st_warning=True)
    def _read_descriptions(species: str) -> str:
        with open(f'{species.lower()}_descriptions.txt', 'r') as f:
            return f.read()

    @st.cache(suppress_st_warning=True)
    def _load_images():
        st.write('Cache miss')
        images = {
            'Setosa': Image.open('setosa.jpg'),
            'Versicolor': Image.open('versicolor.jpg'),
            'Virginica': Image.open('virginica.jpg'),
        }
        return images

    col1, col2 = st.columns(2)
    description = _read_descriptions(species)
    images = _load_images()
    col1.header(species)
    col1.image(images[species], use_column_width=True)
    col2.header('Description')
    col2.write(description, unsafe_allow_html=True)


def home_page() -> None:
    st.title('Looking into Iris Dataset')
    st.image('all_three.jpg', caption='Three types of Iris flowers.')
    with st.expander('Show raw data'):
        st.write(df)
    st.header('General Information')
    selected_sepecies = st.radio('Select species', ['Setosa', 'Versicolor', 'Virginica'])
    show_description(selected_sepecies)


def dataset_page() -> None:
    st.title('Dataset')
    st.header('Statistics')
    stats_df = pd.concat([df.mean(), df.std()], axis=1, names=['mean', 'std']).rename(columns={0: 'mean', 1: 'std'})
    st.write(stats_df)
    sepal_len_lower = st.number_input('Lower bound for sepalLength',)
    sepal_upper = st.number_input('Upper bound for sepalLength', value=4.8)
    sepal_wid_lower = st.slider('Lower bound for sepalWidth', min_value=df['sepalWidth'].min().item(), max_value=df['sepalWidth'].max().item())
    sepal_wid_upper = st.slider('Upper bound for sepalWidth', min_value=df['sepalWidth'].min().item(), max_value=df['sepalWidth'].max().item(), value=3.7)
    filtered_df = df[(df['sepalLength'].between(sepal_len_lower, sepal_upper)) & (df['sepalWidth'].between(sepal_wid_lower, sepal_wid_upper))]
    st.write(filtered_df)


def graphs_page() -> None:
    st.title('Graphs')

    st.header('Seaborn (Matplotlib)')
    fig, ax = plt.subplots()
    ax = sns.scatterplot(data=df, x='petalWidth', y='petalLength', hue='species')
    st.pyplot(fig)

    st.header('Altair')
    st.write('*Interactive: can zoom-in and -out')
    alt_iris_graph = alt.Chart(df).mark_point().encode(
        x='petalWidth',
        y='petalLength',
        color='species'
    ).interactive()
    st.altair_chart(alt_iris_graph, use_container_width=True)

    st.header('*Can also support Plotly and Bokeh')


if __name__ == '__main__':
    df = pd.read_csv('iris.csv')

    selected_page = st.sidebar.selectbox(
        'Select Page',
        ('Home', 'Dataset', 'Graphs')
    )

    if selected_page == 'Home':
        home_page()
    elif selected_page == 'Dataset':
        dataset_page()
    else:
        graphs_page()
