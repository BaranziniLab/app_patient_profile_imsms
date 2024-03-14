import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st


patient_profile = pd.read_csv('data/patient_profile_site_included.csv')
patient_feature_array = patient_profile.drop(['CLIENT_SAMPLE_ID', 'gARMSS', 'armms_category'], axis=1).to_numpy()
distance_matrix = np.load('data/patient_profile_site_included_l1_distance.npy')

xmin = patient_profile.tsne1.min()-1
xmax = patient_profile.tsne1.max()+1
ymin = patient_profile.tsne2.min()-1
ymax = patient_profile.tsne2.max()+1


# Define colors for armms_category
color_map = {'Lower ARMSS': 'green', 'Higher ARMSS': 'red'}

st.sidebar.markdown("# Select Options:")



ucsf_check = st.checkbox('UCSF only')
if not ucsf_check:
    client_sample_id_list = patient_profile['CLIENT_SAMPLE_ID'].tolist()
    selected_client_sample_id = st.sidebar.selectbox('Select CLIENT_SAMPLE_ID:', [None] + client_sample_id_list)
    if selected_client_sample_id:
        num_top_l1_norms = st.sidebar.slider('Number of Top L1 Norms:', 1, 100, 10)
        patient_row_index = patient_profile[patient_profile.CLIENT_SAMPLE_ID==selected_client_sample_id].index.values[0]
        patient_distance_vector = list(distance_matrix[patient_row_index, :])
        patient_distance_df = pd.DataFrame(zip(client_sample_id_list, patient_distance_vector), columns=['patient-id', 'l1-distance-metric'])
        patient_distance_df = patient_distance_df.sort_values(by='l1-distance-metric', ascending=False).reset_index().drop(['index'], axis=1)
        st.table(patient_distance_df.head(num_top_l1_norms))

    fig = px.scatter(patient_profile, x='tsne1', y='tsne2', color='armms_category', color_discrete_map=color_map,
                     hover_data={'tsne1': False, 'tsne2': False, 'CLIENT_SAMPLE_ID': True, 'gARMSS': True}
                    )
else:
    patient_profile_ucsf_only = patient_profile[patient_profile.CLIENT_SAMPLE_ID.str.startswith('714')]
    client_sample_id_list = patient_profile_ucsf_only['CLIENT_SAMPLE_ID'].tolist()
    selected_client_sample_id = st.sidebar.selectbox('Select CLIENT_SAMPLE_ID:', [None] + client_sample_id_list)
    if selected_client_sample_id:
        num_top_l1_norms = st.sidebar.slider('Number of Top L1 Norms:', 1, 100, 10)
        patient_row_index = patient_profile_ucsf_only[patient_profile_ucsf_only.CLIENT_SAMPLE_ID==selected_client_sample_id].index.values[0]
        patient_distance_vector = list(distance_matrix[patient_row_index, :])
        patient_distance_df = pd.DataFrame(zip(client_sample_id_list, patient_distance_vector), columns=['patient-id', 'l1-distance-metric'])
        patient_distance_df = patient_distance_df.sort_values(by='l1-distance-metric', ascending=False).reset_index().drop(['index'], axis=1)
        st.table(patient_distance_df.head(num_top_l1_norms))

    
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


