import streamlit as st
from generate_video import generate_video
from utils import convert_and_decode, get_color_mapping, get_data

# Streamlit UI
st.title('Basepaint Video Generator')
day = st.number_input('Enter the day value:', min_value=0, value=1, step=1)


@st.cache
def flipside_data():
    return get_data()

def process_df(df):
    # Transforming dataframe
    log_cols = ['author', 'day', 'tokenId', 'pixels']
    for col in log_cols:
        df[col] = df.decoded_log.apply(lambda x: x.get(col))
    df['coordinates_and_colors'] = df['pixels'].apply(lambda x: convert_and_decode(x))
    return df 
    
if st.button('Generate Video'):
    # Fetching data
    df = flipside_data()
    df = process_df(df)
    
    # Filtering dataframe based on day
    theme, color_mapping = get_color_mapping(day)
    filtered_df = df[df['day'] == day]
    print(f"filtered_df shape: {filtered_df.shape}")
    filtered_df_list = filtered_df['coordinates_and_colors'].explode().tolist()
    
    # Generating video
    video_path = './timelapse.mp4'
    generate_video(data=filtered_df_list, palette_mapping_dict=color_mapping, output_file=video_path)
    
    # Display video in Streamlit
    video_file = open('timelapse.mp4', 'rb')
    video_bytes = video_file.read()
    st.markdown(f'## Timelapse Video for day {day}: {theme}')
    st.video(video_bytes)
    # Link to download the video
    with open('timelapse.mp4', "rb") as fp:
      btn = st.download_button(
          label="Download VIDEO",
          data=fp,
          file_name="timelapse.mp4",
          mime="video/mp4"
      )
    # st.write('Download the video [here](./timelapse.mp4).')
