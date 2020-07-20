# DMVST
Deep Multi-View Spatial-Temporal Network for Taxi Demand Prediction

3 modules : 

a) spatial view 
- Handles Local CNN for spatial dependency among nearby regions 
- Why local CNN ? because including regions with weak correlations to predict a target region actually hurts the performance. Therefore, it is best   to consider spatially nearby regions. 

b) Temporal View  => LSTM
- models sequential relations in the demand time series
- The output of LSTM h i t contains both effects of temporal and spatial view

c) Semantic view 
- Locations sharing similar functionality may have similar demand patterns, these locations are not considered in the local CNN 
- construct a graph of locations representing functional similarity among regions
- Define the semantic graph of location as G = (V, E, D), where the set of locations L are nodes V = L, E ∈ V ×V is the edge set, and D is a set of   similarity on all the edges
- Dynamic time wrapping is used to measure the similarity between node I and j 
- In order to encode each node into a low dimensional vector and maintain the structural information => LINE embedding

Data pre processing : 

NewYork_regions.py: Divide New York City into different regions

Spatial_time_id_to_txt.py: 9*9 demand pixel matrix corresponding to the prediction area at a certain moment turns into an 81-dimensional vector and store it in a file

Temporal_weather_condition.py:  weather conditions in New York City, different weather corresponds to different numbers
'Clear' :1
'Scattered clouds':2
'Few clouds':3
'Cloudy':4
'Overcast':5
'Few clouds, mnist':6
'fog':7
'rain':8
'snow':9
'Overcast, mist':10
 'Overcast, rain':11
'Overcast, snow':12

Temporal_aq_data.py: Process air quality data for New York City

Temporal_time_data.py: What day is the corresponding moment in a week and is it a holiday?

Temporal_context_data_merge.py: Combine weather, air quality, day of the week, and whether it is a holiday information as the context data         entered at each moment in the time view

Semantic_demand_pattern.py: Determine the demand pattern of each forecast area

Semantic_weighted_graph.py: Determine the weight in the demand weight graph

Semantic_embedding.py: Use LINE method to generate semantic vector (C++ file is the implementation code of LINE method

