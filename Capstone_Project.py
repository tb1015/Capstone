#from calendar import c
#from datetime import datetime
#from turtle import filling
import streamlit as st
import pandas as pd
#import yfinance as yf
import numpy as np

import seaborn as sb
import matplotlib.pyplot as plt
#import numpy as np
#from sklearn import datasets

#today = datetime.today

#st.title("STOCK PRICE")
#with st.sidebar:
#    st.title("Mitigating Climate Change")

#st.set_page_config(layout="wide")
st.title("The Global Warming")
st.header("Introduction")
st.write("Economic development fueled by fossil energy increases Greenhouse Gasses (GHGs) accumulated in our atmosphere. \
        Such accumulation warms up our earth, as shown by the figure of global temperature anomaly bellow.\
        This increasing global temperature will lead to the well known climate change problem")
#st.write("The global warming leads to the well known climate change problem.")

# Global temperature data: https://climate.nasa.gov/vital-signs/global-temperature/
#Land-Ocean Temperature Index (C)

# read text file into pandas DataFrame
url1='https://drive.google.com/file/d/1GKoklFzLZ5Na3DLO7dkwaDwgM3beI61O/view?usp=sharing'
url1='https://drive.google.com/uc?id=' + url1.split('/')[-2]
df_gtemp = pd.read_csv(url1, sep="\t")
#df_gtemp = pd.read_csv("Data/global-temp.txt", sep="\t")
df_emission = pd.read_csv("Data/annual-co2-emissions-per-country.csv")

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
#print(df_emission_global)

data = df_emission_global[df_emission_global["Year"].between(1961,2020, inclusive=True)]
y_axis = "Annual CO2 emissions"
x_axis = "Year"
c_axis = "Temperature"

sb.set(font_scale=1.0, style="ticks") #set styling preferences
points = plt.scatter(data[x_axis], data[y_axis], c=data[c_axis], s=100, cmap="Spectral") #set style options

#add a color bar
cbar = plt.colorbar(points)
cbar.set_label(c_axis+"in ??C")

#set limits
plt.xlim(min(data[x_axis]), max(data[x_axis]))
plt.ylim(min(data[y_axis]), max(data[y_axis]))

#build the plot
plot = sb.regplot(x=x_axis,y=y_axis, data=data, scatter=True, color="black")#, logx=True)#,x_estimator=np.mean)
plot = plot.set(ylabel=y_axis+" in billion tCO2", xlabel=x_axis) #add labels
#plot = sb.lmplot(x=x_axis, y=y_axis, data=df_emission_global)
plt.grid()  

#sb.set(font_scale=1.0, style="ticks") #set styling preferences
#points = plt.scatter(df_gtemp["Lowess(5)"], df_gtemp["Year"],
#                    c=df_gtemp["No_Smoothing"], s=100, cmap="Spectral") #set style options

#add a color bar
#plt.colorbar(points)

#set limits
#plt.xlim(min(df_gtemp["Year"]), max(df_gtemp["Year"]))
#plt.ylim(min(df_gtemp["No_Smoothing"]), max(df_gtemp["No_Smoothing"]))

#build the plot
#Fig = sb.regplot(x="Year",y="Lowess(5)", data=df_gtemp, scatter=True, color="grey", logx=True)#,x_estimator=np.mean)
#Fig = Fig.set(ylabel='Temperature Anomaly (??C)', xlabel='Year') #add labels
#plot = sb.lmplot(x="Year", y="Lowess(5)", data=df_gtemp)
#plt.grid()

st.pyplot(plt.gcf())

## Change Global GDP vs CO2 emission per capita
st.header("Change Global GDP vs CO2 emission")

st.write("Significant historical emission has been released to our atmosphere to achieve today advance economy.\
        This can be seen statistically from the following graph showing annual CO2 emissions per capita and the corresponding GDP per capita. \
        Most of the GDP development in developing countries are fueled by fossil fuels. Thus, the global CO2 emission is likely continuing to rise. \
        Countries, especially the developed ones, have realized this condition and initiate to reduce their emissions through carbon pricing schemes driving the energy transition.\
        Carbon pricing alone without energy transition will only slow or retard the economy development.\
        Such solution is hardly realized in the developing countries. ")

url2='https://drive.google.com/file/d/1xMT64NajKlGgDdOWlI8mnA0ljUYZkmqr/view?usp=sharing'
url2='https://drive.google.com/uc?id=' + url2.split('/')[-2]

df_gdp_co2 = pd.read_csv(url2)
#df_gdp_co2 = pd.read_csv("Data/co2-emissions-and-gdp-long-term.csv")

y0b = st.select_slider("Select Initial Year",(np.linspace(1900,1960,7)).astype(int))
y1b = st.select_slider("Select End Year",np.linspace(1970,2020,6).astype(int))
country = st.text_input("Enter Country/Region")
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
st.pyplot(plt.gcf())

## Global CO2 emissions from fossil fuels and land use change
st.header("Global CO2 emissions from fossil fuels and land use change")

url3='https://drive.google.com/file/d/1iYmn0vxSuZJZ2gN0X1Ub5e6WV37GmNZu/view?usp=sharing'
url3='https://drive.google.com/uc?id=' + url3.split('/')[-2]
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

plt.xlim(min(data[x_axis]), max(data[x_axis]))
plt.ylim(min(data[y_axis]), max(data[y_axis]))

data.plot(x=x_axis, y=c_axis, ax=ax2, legend=False, color="r")
ax.figure.legend(loc="upper right")
plt.title(countryc, loc="left", size=20)
ax.set(ylabel=y_axis+" in billion tCO2")
ax2.set(ylabel=c_axis+" in billion tCO2")
plt.grid()  #just add this
st.pyplot(plt.gcf())

#st.subheader("Ini subheader")
#st.metric("Sales", 100, "-4%")
#st.dataframe(df_store.head())
#st.bar_chart(df_store['Quantity'].head(10))
#st.line_chart(df_store['Sales'].head(10))

#tickerSym = "GOOG"
#tickerSym = st.radio("Pick Stock", ['GOOGL', "AAPL", "TSLA"])
#tickerSym = st.selectbox("Pick Stock", ['GOOGL', "AAPL", "TSLA","BSSR.JK","BOSS.JK"])


#c1, c2 = st.columns(2)
    
#st.header(tickerSym)
#st.line_chart(tickerDf["Close"])
#st.dataframe(tickerDf)

#with c1:
#    tickerSym = st.text_input("Enter Ticker")
#    periodDat = st.select_slider("Select Period",["1d", "5d", "1mo", "3mo", "ytd"])
#    tickerDat = yf.Ticker(tickerSym)
#    tickerDf = tickerDat.history(period=periodDat, interval="1d")# start="2022-08-01", end="2022-10-03") # interval="1d"

#    st.header(tickerSym)
#    st.line_chart(tickerDf[["Open","Close"]])
#    st.dataframe(tickerDf)

#with c2:
#    tickerSym1 = st.text_input("Enter Ticker 2")
#    periodDat1 = st.select_slider("Select Period 2",["1d", "5d", "1mo", "3mo", "ytd"])
#    tickerDat1 = yf.Ticker(tickerSym1)
#    tickerDf1 = tickerDat1.history(period=periodDat1, interval="1d")# start="2022-08-01", end="2022-10-03") # interval="1d"

#    st.header(tickerSym1)
#    st.line_chart(tickerDf1["Close"])
    #st.dataframe(tickerDf1)s
    
#Scrapping dengan Beautiful Soup