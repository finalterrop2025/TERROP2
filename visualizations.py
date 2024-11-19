import streamlit as st
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import json


def app():
   

    # Melt the DataFrame to reshape it for Plotly Express
    df = pd.read_csv('Clean_terrorism1.csv')
    melted_df_percentage_suicide_attack = pd.read_csv('melted_df_percentage_suicide_attack.csv')
    melted_df_suicide_and_non_suicide_attack = pd.read_csv('melted_df.csv')
    weapon_type_df = pd.read_csv('weapon_type.csv')
    weapon_target = pd.read_csv('weapon_target.csv')
    attacks_by_year = pd.read_csv('attacks_by_year.csv') 
    attack_weapon_type_success = pd.read_csv('attack_weapon_type_success.csv')
    filtered_terrorist_group_df = pd.read_csv('filtered_terrorist_group_df.csv')
    value_counts = pd.read_csv('value_counts.csv')
    geodataframe = pd.read_csv('geodataframe.csv')
    
    # Count occurrences of each day
    day_counts = df['day'].value_counts().reset_index()
    day_counts.columns = ['Day', 'Count']
    day_counts

    # Create a bar chart
    Number_of_Attack_by_Day_of_week_fig = px.bar(day_counts, x='Day', y='Count',
                title='Number of Attacks by Day of the  Week',
                labels={'Day': 'Day of the Week', 'Count': 'Count'})

    

    Terrorism_Count_by_State = df.groupby('State').size().reset_index(name='Count')

    # Create the bar chart
    Number_of_Attack_by_State_fig = px.bar(
        Terrorism_Count_by_State, 
        x='State', 
        y='Count', 
        title='Number of Terrorism Attacks by State',
        labels={'State': 'State', 'Count': 'Number of Attacks'},
    )

    # Customize layout
    Number_of_Attack_by_State_fig.update_layout(
        xaxis=dict(tickangle=90),  # Rotate x-axis labels
        #title_x=0.5,  # Center the title
        margin=dict(t=40, b=100)  # Adjust top and bottom margins
    )

    

    #Load GeoJSON file
    with open("nigeria_state_boundaries.geojson") as f:
        nigeria_geojson = json.load(f)

    #Create the choropleth map
    choropleth_map_fig = px.choropleth(
        geodataframe,
        geojson=nigeria_geojson,
        locations="State",  # Column in the DataFrame that matches the GeoJSON `admin1Name`
        featureidkey="properties.admin1Name",  # Path to match GeoJSON properties
        color="Number of Attacks",  # Column to determine color scale
        color_continuous_scale="Viridis",  # Color scale
        title="Choropleth Map Showing the Geographic Distribution of Attacks in Nigeria"
    )

    #Fit the map to the Nigerian states
    choropleth_map_fig.update_geos(fitbounds="locations", visible=False)


    # Create a crosstab of day and State
    crosstab_by_day_state = pd.crosstab(df['State'], df['day'])
    
    # Reset the index
    crosstab = crosstab_by_day_state.reset_index()

    # plot a stacked bar chart
    Number_of_Attack_by_Day_and_State_fig = px.bar(crosstab, x="State", y=["Fri", "Mon", "Sat", "Sun", "Thu", "Tue", "Wed"],
        title="Stacked Bar Chart Showing the Number of Attacks by Day and State",
            labels={"variable": "Day", "value": "Count", "State": "State"},
                height=800)


    # Normalize the crosstab to get the percentage of attack across the days of the week
    crosstab_by_day_state_percent = pd.crosstab(df['State'], df['day'], normalize='index')
    # Reset the index
    crosstab_percent = crosstab_by_day_state_percent.reset_index()
    
    Percentage_of_Attack_by_Day_and_State = px.bar(crosstab_percent, x="State", y=["Fri", "Mon", "Sat", "Sun", "Thu", "Tue", "Wed"], title="Stacked Bar Chart showing the Percentage of Attacks by Day and State",
            labels={"variable": "Day", "value": "Count", "State": "State"},
                height=800)



    # Plot a grouped bar chart using Plotly Express
    percentage_suicide_attack_fig = px.bar(melted_df_percentage_suicide_attack, x='State', y='Value', color='Variable', barmode='group',
                 labels={'Value': 'Value', 'Variable': 'Variable'})
    percentage_suicide_attack_fig.update_layout(title='No. of suicide and percentage of suicide attacks by state')


    suicide_and_non_suicide_attack_fig = px.bar(melted_df_suicide_and_non_suicide_attack, x='State', y='Value', color='Variable', barmode='group',
                  labels={'Value': 'Value', 'Variable': 'Variable'})
    suicide_and_non_suicide_attack_fig.update_layout(title='Number of non-suicide attack and suicide attack per state')

    weapon_type_fig = px.bar(weapon_type_df, x='weapon_subtype', y='proportion', title='Bar Chart Showing Percentage of Weopon Type')
    
    # Create a bar chart using Plotly Express
    weapon_target_fig = px.bar(weapon_target, x='weapon_subtype', y='Count', color='target_type', barmode='stack')
    weapon_target_fig.update_layout(title='Stacked Bar Chart Showing Weapon Subtype vs. Target Type')

    # Update layout to increase figure size and add title
    weapon_target_fig.update_layout(
        #title='Your Title Here',
        width=1000,  # Specify the width of the figure
        height=800,  # Specify the height of the figure
    )



    attacks_by_year_fig = px.line(attacks_by_year, x="year", y="Count", title="Line Plot Showing the Increase of Terrorist Attacks Each Year", labels={"year": "Year", "Count": "Number of Attacks"})
    
    
    
    # Create a bar chart using Plotly Express
    attack_weapon_type_success_fig = px.bar(attack_weapon_type_success, x='attacktype1_txt', y='success', color='weapon_subtype', barmode='stack')
    attack_weapon_type_success_fig.update_layout(title='Successful Attacks Based on Attacks Type and Weapon Subtype')



    # Calculate the value counts of group_name
    value_counts = df['group_name'].value_counts()

    # get group names in descending oder
    groups = value_counts.index

    # Sort the categories in descending order of counts
    sorted_categories = groups.tolist()

    # Filter the DataFrame
    filtered_df = df[df['group_name'].isin(groups)]

    # Create the count plot using Plotly Express
    Terrorist_Group_More_than_1_attack_fig = px.histogram(filtered_df, x='group_name',
                    title='Count Plot Showing Frequency of Attacks by Terrorist Group with More Than 1 Attacks',
                    height=1000, category_orders={'group_name': sorted_categories},
                    labels={'group_name': 'Terrorist Group Name'}
                    )

    # Calculate the percentage of each category
    value_counts = df['group_name'].value_counts(normalize=True) * 100
    value_counts = value_counts.reset_index()
    value_counts.columns = ['Group Name', 'Percentage']

    # Create the bar plot using Plotly Express
    Percentage_terrorism_by_terrorist_group_fig = px.bar(value_counts, x='Group Name', y='Percentage',
                title='Percentage of Terrorism by Terrorist Groups',
                height=1000,
                labels={'Group Name': 'Terrorist Group Name', 'Percentage': 'Percentage of terrorist activities'})


    st.markdown(
       """
       <style>
           @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
           
           .visualization-header {
               background-color: none;
               padding: 10px;
               border-radius: 5px;
               box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
               font-size: 40px;
               font-weight: bold;
               color: white; 
               font-family: 'Roboto', sans-serif;
           }
           .visualization-header span {
               font-size: 24px;
               font-weight: bold;
               color: #f5e487; 
           }
           .visualization-text {
               padding: 10px;
               width: 90%;
               font-size: 20px;
               font-weight: bold;
               color: white; 
           }
           .paragraph {
               color: black; 
               background-color: white;
               padding: 20px;
               margin: 20px;
               border-radius: 15px;
           } 

           #selected-plots {
             font-size: 30px;
             color: #f5e487;
             font-weight: bold;
             margin-bottom: 5px;
            }

            #number-of-attacks-by-day-of-the-week {
             font-size: 26px;
             color: white;
             font-weight: bold;
             margin-bottom: 5px;
            }
             #number-of-attacks-by-state {
             font-size: 26px;
             color: white;
             font-weight: bold;
             margin-bottom: 5px;
            }

             #choropleth-map-showing-the-geographic-distribution-of-attacks-by-state {
             font-size: 26px;
             color: white;
             font-weight: bold;
             margin-bottom: 5px;
            }

            #number-of-attacks-by-day-and-state {
             font-size: 26px;
             color: white;
             font-weight: bold;
             margin-bottom: 5px;
            }

             #percentage-of-attacks-by-day-and-state {
             font-size: 26px;
             color: white;
             font-weight: bold;
             margin-bottom: 5px;
            }

            #number-of-suicide-attacks-and-percentage-of-suicide-attacks-by-state {
             font-size: 26px;
             color: white;
             font-weight: bold;
             margin-bottom: 5px;
            }

            #number-of-suicide-and-non-suicide-attack {
             font-size: 26px;
             color: white;
             font-weight: bold;
             margin-bottom: 5px;
            }

            #bar-chart-showing-the-percentage-of-weapon-type {
             font-size: 26px;
             color: white;
             font-weight: bold;
             margin-bottom: 5px;
            }

             #stacked-bar-chart-showing-weopn-subtype-vs-target-type {
             font-size: 26px;
             color: white;
             font-weight: bold;
             margin-bottom: 5px;
            }

             #line-plot-showing-number-of-attacks-by-year {
             font-size: 26px;
             color: white;
             font-weight: bold;
             margin-bottom: 5px;
            }

              #stacked-bar-chart-showing-succesful-attacks-based-on-attack-type-and-weapon-subtype {
             font-size: 26px;
             color: white;
             font-weight: bold;
             margin-bottom: 5px;
            }

              #count-plot-of-terrorist-groups-with-more-than-1-attack {
             font-size: 26px;
             color: white;
             font-weight: bold;
             margin-bottom: 5px;
            }
             #percentage-of-terrorism-by-terrorist-group {
             font-size: 26px;
             color: white;
             font-weight: bold;
             margin-bottom: 5px;
            }

            #percentage-of-terrorism-by-terrorist-group {
             font-size: 26px;
             color: white;
             font-weight: bold;
             margin-bottom: 5px;
            }
       
           .st-emotion-cache-vdokb0.e1nzilvr4 {
               font-size: 12px;
               color: white;
               font-weight: bold;
               margin-top: 5px;
           }
       
           .st-emotion-cache-z1fhwk.e1nzilvr4 {
               font-size: 16px;
               color: white;
               font-weight: bold;
               margin-bottom: 10px;
           }
          
       </style>
       <div class="visualization-header">
           <h1 style='color:#a5abab;'>Visualization</h1>
       </div>
   
       <div class="visualization-text">
           <span style='color:#f5e487;'>Visualization of historical data</span>
           <div class="paragraph">
               <p style="font-size: 20px; text-align: justify;">
                   Explore interactive visualizations highlighting key areas at risk of terrorist attacks in Nigeria. 
                   Our dynamic maps and data-driven charts provide a clear view of past incidents and potential coordinates.
                   Use these insights to better understand the distribution and frequency of attacks, which will help inform preventive measures and strategic planning.
                   Navigate through the visuals to stay informed and proactive in enhancing security within vulnerable regions.
               </p>
           </div>
       </div>
       """,
       unsafe_allow_html=True
      )
    st.markdown(
       """
       <style>
           .st-emotion-cache-asc41u.e1nzilvr2 {
             font-size: 18px;
             color: white;
             font-weight: bold;
             margin-bottom: 5px;
            }

       </style>
       """,
       unsafe_allow_html=True
      )


    # plotly figures and interpretations

    # Group data by state and calculate total attacks, saving it to a column called 'Count'
    # Group data by state and calculate total attacks
    attacks_by_state = df.groupby('State')['State'].count()

    # Find the state with minimum and maximum attacks
    state_min_attacks = attacks_by_state.idxmin()
    state_max_attacks = attacks_by_state.idxmax()

    # Get the corresponding values
    min_attacks = attacks_by_state[state_min_attacks]
    max_attacks = attacks_by_state[state_max_attacks]
    
    
    plots = {
        "Number of Attacks by Day of the Week": {
        "fig": Number_of_Attack_by_Day_of_week_fig,
        "desc": "This plot shows the frequency of terrorism attacks across the days of the week."
                
    },
    "Number of Attacks by State": {
        "fig": Number_of_Attack_by_State_fig,
        "desc": f"This plot shows the frequency of terrorism attacks across the states. "
                f"State with maximum attacks: {state_max_attacks} ({max_attacks} attacks). "
                f"State with minimum attacks: {state_min_attacks} ({min_attacks} attacks)."
    },
        "Choropleth Map Showing the Geographic Distribution of Attacks by State": {
            "fig": choropleth_map_fig,
            "desc": "This map visualizes the geographical distribution of terrorism attacks across states in Nigeria, emphasizing hotspots of activity."
        },
        "Number of Attacks by Day and State": {
            "fig": Number_of_Attack_by_Day_and_State_fig,
            "desc": "This plot breaks down the number of attacks by day and state, helping to identify trends and patterns at a granular level."
        },
        "Percentage of Attacks by Day and State": {
            "fig": Percentage_of_Attack_by_Day_and_State,
            "desc": "This chart displays the percentage of attacks in each state on different days, offering insights into attack proportions."
        },
        "Number of Suicide Attacks and Percentage of Suicide Attacks by State": {
            "fig": percentage_suicide_attack_fig,
            "desc": "This plot shows the number of suicide attack in comparison to the percentage of suicide attacks, illustrating the frequency and proportions of such incidents."
        },
        "Number of Suicide and Non-Suicide Attack": {
            "fig": suicide_and_non_suicide_attack_fig,
            "desc": "This plot compares the frequency of suicide and non-suicide attacks, showing their frequency and how they compare."
        },
        "Bar Chart Showing the Percentage of Weapon Type": {
            "fig": weapon_type_fig,
            "desc": "This chart categorizes the types of weapons used in terrorism attacks, revealing the most and least common weapon choices."
        },
        "Stacked Bar Chart Showing Weopn Subtype vs Target Type": {
            "fig": weapon_target_fig,
            "desc": "This plot explores the weopon used for each targets of terrorism attacks, showing which groups or entities are most frequently attacked and weopon frequently used."
        },
        "Line Plot Showing Number of Attacks by Year": {
            "fig": attacks_by_year_fig,
            "desc": "This chart shows the number of attacks per year, providing a temporal view of terrorism trends over time."
        },
        "Stacked Bar Chart Showing Succesful Attacks Based on Attack Type and Weapon Subtype": {
            "fig": attack_weapon_type_success_fig,
            "desc": "This plot analyzes the success rates of attacks based on attack type and weapon types, offering insights into effectiveness."
        },
        "Count Plot of Terrorist Groups with More than 1 Attack": {
            "fig": Terrorist_Group_More_than_1_attack_fig,
            "desc": "This chart shows the frequency of Attacks by terrorist groups with more than one attack, highlighting the groups with significant activity."
        },
        "Percentage of Terrorism by Terrorist Group": {
            "fig": Percentage_terrorism_by_terrorist_group_fig,
            "desc": "This plot shows the percentage of total attacks attributed to each terrorist group, providing a comparative analysis."
        },
    }

    # Sidebar for plot selection
    selected_plots = []
    st.sidebar.header("Select Plots to Display")
    for plot_name in plots.keys():
        if st.sidebar.checkbox(plot_name, value=False):
            selected_plots.append((plot_name, plots[plot_name]))

    # Display selected plots with descriptions, two per row
    st.header("Selected Plots")
    if selected_plots:
        cols = st.columns(2)
        for idx, (plot_name, plot_data) in enumerate(selected_plots):
            col = cols[idx % 2]  # Alternate between two columns
            with col:
                st.subheader(plot_name)
                st.plotly_chart(plot_data["fig"])
                st.caption(plot_data["desc"])  # Add interpretation below the plot
    else:
        st.write("No plots selected. Use the sidebar to select plots.")



# Display the Plotly chart in Streamlit
   # st.plotly_chart(Attack_by_day_of_Week_fig)
    #st.plotly_chart(choropleth_map_fig)
    #st.plotly_chart(Number_of_Attack_by_Day_and_State_fig)
    #st.plotly_chart(Percentage_of_Attack_by_Day_and_State)
    #st.plotly_chart(suicide_attack_fig)
    #st.plotly_chart(non_suicide_attack_fig)
    #st.plotly_chart(weapon_type_fig)
    #st.plotly_chart(weapon_target_fig)
    #st.plotly_chart(attacks_by_year_fig) 
    #st.plotly_chart(attack_weapon_type_success_fig)
    #st.plotly_chart(Terrorist_Group_More_than_1_attack_fig)
    #st.plotly_chart(Percentage_terrorism_by_terrorist_group_fig).
