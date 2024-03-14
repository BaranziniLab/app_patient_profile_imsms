import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st


patient_profile = pd.read_csv('data/patient_profile_site_included.csv')
patient_feature_array = patient_profile.drop(['CLIENT_SAMPLE_ID', 'gARMSS', 'armms_category'], axis=1).to_numpy()

xmin = patient_profile.tsne1.min()-1
xmax = patient_profile.tsne1.max()+1
ymin = patient_profile.tsne2.min()-1
ymax = patient_profile.tsne2.max()+1


# Define colors for armms_category
color_map = {'Lower ARMSS': 'green', 'Higher ARMSS': 'red'}

ucsf_check = st.checkbox('UCSF only')
if not ucsf_check:
    # Plot
    fig = px.scatter(patient_profile, x='tsne1', y='tsne2', color='armms_category', color_discrete_map=color_map,
                     hover_data={'tsne1': False, 'tsne2': False, 'CLIENT_SAMPLE_ID': True, 'gARMSS': True}
                    )
else:
    patient_profile_ucsf_only = patient_profile[patient_profile.CLIENT_SAMPLE_ID.str.startswith('714')]
    fig = px.scatter(patient_profile_ucsf_only, x='tsne1', y='tsne2', color='armms_category', color_discrete_map=color_map,
                     hover_data={'tsne1': False, 'tsne2': False, 'CLIENT_SAMPLE_ID': True, 'gARMSS': True}
                    )

# Update legend names
fig.for_each_trace(lambda t: t.update(name=color_map[t.name]))

# Update legend title
fig.update_layout(legend_title_text='ARMSS Category')

fig.update_layout(height=500, width=700)
fig.update_traces(marker=dict(size=10))
fig.update_traces(
    name = "Lower ARMSS",
    selector=dict(name="green")
)
fig.update_traces(
    name = "Higher ARMSS",
    selector=dict(name="red")
)
fig.update_layout(
    xaxis=dict(
        title=dict(
            font=dict(size=20)  # Adjust the font size of the x axis label here
        ),
        range=[xmin, xmax]
    ),
    yaxis=dict(
        title=dict(
            font=dict(size=20)  # Adjust the font size of the y axis label here
        ),
        range=[ymin, ymax]
    )
)
# Display the plot
st.plotly_chart(fig)


