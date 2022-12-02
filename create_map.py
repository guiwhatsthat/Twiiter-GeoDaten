import pandas as pd
import plotly.express as px

# Read in data
df = pd.read_csv(f'twitter-trending-topics-clustering.csv')
fig = px.scatter_geo(df,lat='Latitude',lon='Longitude', hover_name="Type", color="Type", size="Depth", projection="natural earth")
fig.update_layout(title = 'Tweets by trend topic from the 02.12.2022', title_x=0.5, title_font_size=20, title_font_color='black', title_font_family='Arial')
fig.show()