import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import statsmodels
import seaborn as sb
import matplotlib.pyplot as plt


#kasih subtopik di tiap paragraf di bagian bawah
#GDP Dunia?

#Plotly untuk tampilan data yang interaktif
#Gunakan juga space disamping


##==================================================================================================================================
st.set_page_config(layout="wide")
st.title("Global Warming in Economic Perspective")
st.write("*Author: Thomas Budiarto*")

st.header("Introduction")

col1, col2 = st.columns(2)

with col1:
    st.write("Economic development fueled by fossil energy increases Greenhouse Gasses (GHGs) accumulated in our atmosphere. \
        Such accumulation intensifies the Greenhouse effect in atmosphere leading to increasing global temperature (as shown by the figure of global temperature anomaly bellow).\
        This increasing global temperature will lead to the well known climate change problem.")

# Global temperature data: https://climate.nasa.gov/vital-signs/global-temperature/
# Land-Ocean Temperature Index (C)

# read text file into pandas DataFrame
df_gtemp = pd.read_csv("https://github.com/tb1015/Capstone/blob/main/global-temp.txt?raw=true", sep="\t")
df_emission = pd.read_csv("https://github.com/tb1015/Capstone/blob/main/annual-co2-emissions-per-country.csv?raw=true")

Fig = plt.figure(figsize=(6,5))
df_emission_global = df_emission[df_emission["Entity"]=="World"]
y0a = min(df_gtemp["Year"]) #1951 #
#y0a = #st.select_slider("Select Initial Year",(np.linspace(1900,1960,7)).astype(int))
y1a = max(df_gtemp["Year"]) #2020 #
#y1a = st.select_slider("Select End Year",np.linspace(1970,2020,6).astype(int))

#Combining the emission data and the temperature data with the same year
df_emission_global = df_emission_global[df_emission_global['Year'].between(y0a, y1a, inclusive=True)].reset_index() #filter the enussuib data and reset the index
df_emission_global["Temperature"] = df_gtemp[df_gtemp["Year"].between(y0a, y1a, inclusive=True)]["Lowess(5)"] # Combine the emission and the temperature data
df_emission_global["Annual CO2 emissions"] = df_emission_global["Annual CO2 emissions"]*1e-9

data = df_emission_global[df_emission_global["Year"].between(1961,2020, inclusive=True)]
y_axis = "Annual CO2 emissions"
x_axis = "Year"
c_axis = "Temperature"

sb.set(font_scale=1.0, style="ticks") #set styling preferences
points = plt.scatter(data[x_axis], data[y_axis], c=data[c_axis], s=100, cmap="Spectral") #set style options

#add a color bar
cbar = plt.colorbar(points)
cbar.set_label("Anomaly "+c_axis+" in °C")

#set limits
plt.xlim(min(data[x_axis]), max(data[x_axis]))
plt.ylim(min(data[y_axis]), max(data[y_axis]))

#build the plot
plot = sb.regplot(x=x_axis,y=y_axis, data=data, scatter=True, color="black")#, logx=True)#,x_estimator=np.mean)
plot = plot.set(ylabel="Global "+y_axis+" in billion tCO2", xlabel=x_axis) #add labels
#plot = sb.lmplot(x=x_axis, y=y_axis, data=df_emission_global)
plt.grid()  
plt.text(1950, 4.5, 'Data sources: climate.nasa.gov, Global Carbon Project (2021)')


with col2:
    #st.pyplot(plt.gcf())
    st.write("**Figure 1: Annual CO2 Emissions (in billion tCO2) and Annomaly Temperature (in °C)**")
    st.write("*Data sources: climate.nasa.gov, Global Carbon Project (2021)*")
    fig = px.scatter(data, x=x_axis, y=y_axis, color=c_axis, trendline="ols",
                     labels=dict(Temperature="Annomaly in °C"))
   
    fig.update_traces(marker=dict(size=8,
                              line=dict(width=1,
                                        color='White')),
                  selector=dict(mode='markers'))
    
    st.plotly_chart(fig, use_container_width=True)
    
    
##==================================================================================================================================
## Change Global GDP vs CO2 emission per capita
st.header("Change Global GDP vs CO2 emission")
st.write("Significant historical emission has been released to our atmosphere to achieve today advance economy.\
        This can be seen statistically from the following graph showing annual CO2 emissions per capita and the corresponding GDP per capita. \
        Most of the GDP development in developing countries are fueled by fossil fuels. Thus, the global CO2 emission is likely continuing to rise. \
        Countries, especially the developed ones, have realized this condition and initiate to reduce their emissions through carbon pricing schemes driving the energy transition.\
        Carbon pricing alone without energy transition will only slow or retard the economy development.\
        Such solution is hardly realized in the developing countries. ")

#url2='https://drive.google.com/file/d/1xMT64NajKlGgDdOWlI8mnA0ljUYZkmqr/view?usp=sharing'
#url2='https://drive.google.com/uc?id=' + url2.split('/')[-2]
#url2 = "Data/co2-emissions-and-gdp-long-term.csv"
url2 = "https://github.com/tb1015/Capstone/blob/main/co2-emissions-and-gdp-long-term.csv?raw=true"
df_gdp_co2 = pd.read_csv(url2)

col1, col2 = st.columns(2)

with col1:
    st.write("**Please select the time range and the region for the emission & GDP chart.**")
    y0b = st.selectbox("Initial year",(np.linspace(1900,1960,7)).astype(int), index=5)
    #st.write('You selected:', y0b)
    y1b = st.selectbox("Final year",np.linspace(1970,2020,6).astype(int), index=5)
    #st.write('You selected:', y1b)
    #country = st.text_input("Enter Country/Region")
    country = st.selectbox("Enter Country/Region",df_gdp_co2["Entity"].unique(),index=103)
    #st.write('You selected:', country)

df_Ggdp_co2 = df_gdp_co2[df_gdp_co2["Entity"]==country].reset_index(drop=True)

data = df_Ggdp_co2[df_Ggdp_co2["Year"].between(y0b,y1b, inclusive=True)]
y_axis = "Annual CO2 emissions (per capita)"
c_axis = "GDP per capita"
x_axis = "Year"#"Temperature (C)"

#st.header(tickerSym)
#st.line_chart(data[[y_axis,c_axis]])
#st.dataframe(data)

sb.set(font_scale=1.0, style="ticks") #set styling preferences
ax = data.plot(x=x_axis, y=y_axis, legend=False)
ax2 = ax.twinx()
data.plot(x=x_axis, y=c_axis, ax=ax2, legend=False, color="r")
ax.figure.legend(loc="upper right")
plt.title(country, loc="left", size=20)
ax.set(ylabel=y_axis+" in tCO2e")
ax2.set(ylabel=c_axis+" in US$")
plt.grid()  #just add this
#plt.show()

with col2:
    st.write("**Figure 2: Annual CO2 emissions and GDP per capita**")
    st.write("*Data sources: Global Carbon Project (2021)*")
    st.pyplot(plt.gcf())


##=================================================================================================================
## Global CO2 emissions from fossil fuels and land use change
st.header("Global CO2 emissions from fossil fuels and land use change")

col1,col2 = st.columns(2)

with col1:
    st.write("Most of our emission comes from fossil fuels, either for fueling our industry or our transportation system.")

url3='https://drive.google.com/file/d/1iYmn0vxSuZJZ2gN0X1Ub5e6WV37GmNZu/view?usp=sharing'
url3='https://drive.google.com/uc?id=' + url3.split('/')[-2]
#url3 = "Data/global-co2-fossil-plus-land-use.csv"
df_co2_fossil = pd.read_csv(url3)

#df_co2_fossil = pd.read_csv("Data/global-co2-fossil-plus-land-use.csv")
#y0c = st.select_slider("Select Initial Year",(np.linspace(1900,1960,7)).astype(int))
#y1c = st.select_slider("Select End Year",np.linspace(1970,2020,6).astype(int))
countryc = "World"#st.text_input("Enter Country/Region")

df_co2_fossil = df_co2_fossil[df_co2_fossil["Entity"]==countryc].reset_index(drop=True)
df_co2_fossil[[df_co2_fossil.columns[3],df_co2_fossil.columns[4],df_co2_fossil.columns[5]]]=df_co2_fossil[[df_co2_fossil.columns[3],df_co2_fossil.columns[4],df_co2_fossil.columns[5]]]*1e-9

data = df_co2_fossil[df_co2_fossil["Year"].between(y0b,y1b, inclusive=True)]
y_axis = df_co2_fossil.columns[4]
c_axis = df_co2_fossil.columns[5]
x_axis = df_co2_fossil.columns[2]

ax = data.plot(x=x_axis, y=y_axis, legend=False)
ax2 = ax.twinx()

#plt.xlim(min(data[x_axis]), max(data[x_axis]))
#plt.ylim(min(data[y_axis]), max(data[y_axis]))

data.plot(x=x_axis, y=c_axis, ax=ax2, legend=False, color="r")
ax.figure.legend(loc="upper right")
plt.title(countryc, loc="left", size=20)
ax.set(ylabel=y_axis+" in billion tCO2")
ax2.set(ylabel=c_axis+" in billion tCO2")
plt.grid()  #just add this

with col2:
    st.write("**Figure 3: CO2 Emissions from Energy Use and Land Use**")
    st.write("*Data sources: Global Carbon Project (2021)*")
    st.pyplot(plt.gcf())

st.header("Carbon Pricing and Energy Transition")

st.write("Developed countries have realized this condition and initiate to reduce their emissions through carbon pricing schemes driving the energy transition")
st.write("Carbon pricing without energy transition will only slow or retard the economy development. Such solution is hardly realized in the developing country.")

st.write("Energy transition needs research and new industrial development, which require huge investment. Such investment is too expensive or often un-affordable for most of developing countries, even with help of good carbon pricing scheme.")
st.write("Clean tech R&D and industrialization are beyond developing countries economical capability.\
        Utilization of fossil fuel by developing countries is not only the best practice but also often the only available economical solution.\
        This condition will lead to more emission that will be produced by the developing countries (future GHG emission potential) during their way to the developed economy.")

st.write("Access to affordable clean technologies and resources required to manufacture the technology is necessary to mitigate the GHG emission potential while also allowing developing countries to grow their economy cleanly.")
st.write("How to obtain the affordable clean technology and manufacture? Sharing resources to grow businesses producing the technology and infrastructure as close as possible to the implementation site.")

