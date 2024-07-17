#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 12:10:43 2023

@author: roteg
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



#%% Category: filter, modification
def plausibility_filter(h,ran,b_verbose=False):
    """
    Range filter that removes timestamps with values or derivatives of them outside a defined range/marks them as invalid. The definition of the range is based on empirical values.
    Arguments:
        h: pandas DataFrame where values should be checked and filtered if necessary
        ran: list with the following conditions that must be fulfilled
            0: lower limit
            1: upper limit
            3: OPTIONAL: list of regular expressions where at least one of them should match to the respective column name to be included in the check
            4: OPTIONAL: define the degree of derivative of the values that should be checked and filtered instead of the actual values
        b_verbose: If set True, print exceed rate
    Returns: Initial DataFrame with values filtered where conditions fulfilled
    """
    if len(ran)>3: derivative=ran[3];
    else: derivative=0;
    if len(ran)>2: colindex=loc_colreg(h,ran[2],b_or_operation=True).columns;
    else: colindex=h.columns
    h_=h.copy(deep=True)
    if derivative>0:
        #filter before interpolation, which first of all should only be applied on the original data (not the derivation of it)
        hh=h_[colindex]
        for dc in range(1,derivative+1): #derivation before interpolation
            hh=hh.diff(axis=0)
        cond=((hh>=ran[0]) & (hh<=ran[1]))  #filter before interpolation
        h_[colindex]=h_[colindex][cond]
        
        #Interpolation must definitely occur before this step, as otherwise, in the case of gaps in counter measurement series (usually intended for gradient filtering for these data points), information is lost.
        h_=(h_).interpolate()
        hh=h_[colindex]
        for dc in range(1,derivative+1):  #derivate
            hh=hh.diff(axis=0)
        cond=((hh>=ran[0]) & (hh<=ran[1]))  #filter
        hh=hh[cond]
        for ic in range(1,derivative+1):    #integrate
            hh=hh.cumsum(axis=0)
        h_[colindex]=hh 
        h_.loc[h_.index[0],colindex]=0     #The first line is replaced by 0 due to NaN (caused by the diff operation) and because the value at the beginning of cumsum must be 0
    else:
        cond=((h_>=ran[0]) & (h_<=ran[1]))
        h_[colindex]=h_[cond][colindex]
    if b_verbose: 
        exceed_rate=(1-cond.sum()/cond.shape[0])[colindex].sort_index() 
        print("Filter rate:", exceed_rate)
    return(h_)


def loc_colreg(df,regexs,bs_inverse=False,b_or_operation=False):
    """Using regular expressions, data point names can be filtered. One or more regular expressions can be provided (string or list of strings).
    If a list of search patterns is provided, per default, all of them must match (AND operation).
    If b_or_operation=True is set, only one of them must match (OR operation). The regular expressions can alternatively provided in one single string separated by |.
    If bs_inverse=True is set, none of them must match (NOT operation).
    Arguments:
        df: pandas DataFrame
        regexs: One or multiple regular expressions to search in the columns of the provided DataFrame
        bs_inverse: Activate negation of search results (see above)
        b_or_operation: Activate OR operation with search matches (see above)     
    """
    if type(regexs)==str and "|" in regexs: 
        print("Neuer Modus: Aufsplitten und Veroderung bei | in einzelner regex")
        regexs=regexs.split("|")
        b_or_operation=True
        print("regexs:",regexs,"\nb_or_operation:",b_or_operation,"\nbs_inverse:",bs_inverse)
    df=df.sort_index(axis=1)
    cols=df.columns.values
    c=0;
    while c<len(cols): 
        cols[c]=str(cols[c]);c+=1;
    cols=pd.Index(cols)
    if not type(regexs) is list: regexs=[regexs]
    if not type(bs_inverse)is list:bs_inverse=[bs_inverse]
    if len(bs_inverse)!=len(regexs):
        #print("##Warning: unequal length of regex- and bs_inverse lists")
        #print("--> if bs_inverse list is shorter, it will be padded with false")
        for c in range(len(bs_inverse),len(regexs)):
            bs_inverse.append(False)
    if b_or_operation:
        b_cols=(cols!=cols) #create index matching list with same shape of columns list and all negative matches (will be modified later by ORing with the real matching list)
        b_cols=cols==cols #create index matching list with same shape of columns list and all positive (will be modified later by ANDing with the real matching list)  
    for loczip in zip(regexs,bs_inverse):
        regex=loczip[0]
        if "(" in regex or ")" in regex:
            print("Parenthesizing of ( or ) (--> [)], as regex groups are should not be used here")
            regex=regex.replace("(","[(]").replace(")","[)]")
            print(regex)
        b_inverse=loczip[1]
        if b_or_operation:
            if b_inverse: 
                b_cols|=~cols.str.contains(regex,flags=re.IGNORECASE)
            else:
                b_cols|=cols.str.contains(regex,flags=re.IGNORECASE) 
        else:
            if b_inverse: 
                b_cols&=~cols.str.contains(regex,flags=re.IGNORECASE)
            else:
                b_cols&=cols.str.contains(regex,flags=re.IGNORECASE)
    return(df.loc[:,b_cols])



def plot_conditional_marking4(cond,color="yellow",alpha=.5,ax=None,limits=None,label="_hidden",b_use_fill_between=True):
    """Plots an marker erea in time periods where a given condition is fulfilled over an axisting plot
    Arguments:    
        cond: pandas DataFrame with boolean values indicating if condition is fulfilled
        color: color of marking area
        alpha: opacity of marking area
        ax: existing matplotlib axis object where marking area should be plotted
        limits: list of lower and upper limit of marking area
        label: label of marking area for legend (defaults to "_hidden" so that it's not shown in the legend
        b_use_fill_between: use matplotlibs fill_between function
     Returns: 
         ax: modified matplotlib axis object
    """
    cond=todf(cond)
    cond.columns=[label]
    if not(ax): ax=plt.gca()
    if not(limits): ylim1,ylim2=ax.get_ylim()
    else: ylim1,ylim2=limits
    if b_use_fill_between:
        ax.fill_between(x=cond.index,y1=cond.mul(ylim1).squeeze().values, y2=cond.mul(ylim2).squeeze().values, \
                        label=label, color=color, alpha=alpha, step='post', linewidth=0)
        legend()
    else:
        cond.mul(ylim1).plot(x_compat=False,ax=ax,alpha=alpha,kind="area",color=color,style="",linewidth=0, label=label)#,secondary_y=True)
        todf(cond,"_"+cond.columns[0]).mul(ylim2).plot(x_compat=False,ax=ax,alpha=alpha,kind="area",color=color,style="",linewidth=0, label="_"+label)#,secondary_y=True)
    ax.set_ylim(ylim1,ylim2)
    return(ax)


def df_time_intersection(df1,df2):
    """Calculates the temporal intersection of two pandas DataFrames and returns the two DataFrames with reduced, but common time range.
    Arguments:  
        df1: DataFrame 1
        df2: DataFrame 2
    Return:
        df1: DataFrame 1 with common time range
        df2: DataFrame 2 with common time range
    """
    if type(df1)==pd.core.series.Series:
        if df1.name==None: df1=todf(df1,"df1")
        else: df1=todf(df1);
    if type(df2)==pd.core.series.Series:
        if df2.name==None: df2=todf(df2,"df2");
        else: df2=todf(df2)
    df=df1.join(df2,how="inner",rsuffix="RSUFFIX")
    df1=df.loc[:,df1.columns.astype("str")]
    df2=df.loc[:,df2.columns.astype("str")]
    return(df1,df2)


def detect_real_timeresolution(s):
    """Detects real time resolution in a time serie in which values are actualized. Expects a time series as an argument and outputs the temporal resolution (in which no NaN values are present).
    Arguments: pandas time series
    returns: pandas time series of time resolutions
    """
    s=tos(s)
    s_nnans=s.dropna()
    s_timedeltas=s_nnans.index[1:]-s_nnans.index[0:-1]
    na_timedeltas=np.array(s_timedeltas.astype(int)/60/1e9)
    na_timedeltas=np.insert(na_timedeltas,0,np.nan)
    s_nnans[:]=na_timedeltas
    s_nnans=resample2equidistance(s_nnans)
    return(s_nnans)
def detect_real_timeresolution_df(df):
    """Detects real time resolution in a time serie in which values are actualized
    Arguments: pandas DataFrame
    returns: pandas DataFrame of time resolutions
    DataFrame version of detect_real_timeresolution
    """
    for c in df.columns:
        print(c)
        c_tr=detect_real_timeresolution(df[c])
        df=df.reindex(c_tr.index)
        df.loc[c_tr.index,c]=c_tr
    return(df)

def identify_supply_return(df, c=4.18):
    """Checks where more energy flows, supply or return
        Arguments: pandas DataFrame of heat meter time series: "flow", "return" and "supply" temperature
                   c specific heat capacity of medium (defaults to water)
        Returns: pandas DataFrame of netto energy return and supply
    Comumns in argument DataFrame must be uniquely identified as follows:
        flow: "flow" 
        return temperature: "return"
        supply temperature: "supply"
    """
    conversion_factor=1/3600 * 1000 *  c   #for conversion into kW #
    df=df.copy(deep=True)
    df_supplyenergy=(loc_colreg(df,"supply")*loc_colreg(df,"flow").values*conversion_factor).sum()/60  #reference point 0°C, with conversion from kWmin into kWh
    df_returnenergy=(loc_colreg(df,"return")*loc_colreg(df,"flow").values*conversion_factor).sum()/60
    print("Evaluation period:",df.index[0],"bis",df.index[-1])
    energy_netto=(df_supplyenergy.values-df_returnenergy.values)[0]
    print(round(abs(energy_netto),2),"kWh")
    if df_supplyenergy.values>df_returnenergy.values:print("Heat supply (unit to system):",df_supplyenergy.index[0],  "\nCold return (system to unit):",df_returnenergy.index[0])
    elif df_supplyenergy.values<df_returnenergy.values:print("Cold supply (unit to system):",df_supplyenergy.index[0],"\nHeat return (system to unit):",df_returnenergy.index[0])
    else:print("determinable ... supply and return energy equal?")
    print("\n")
    print(df_supplyenergy)
    print(df_returnenergy)
    return(energy_netto)

def df_clusterTime_function(d,function=None):
    """Determination of the time intervals at which a specific condition (e.g. threshold exceeded) occurs and calculation of the desired quantity (e.g. average value, length, etc.) for each time interval.
        Arguments: pandas time series
        Returns: pandas time series
    """
    d=d.copy(deep=True)
    dd=pd.isna(d).mul(1).diff().replace(-1,0).cumsum()
    if function==None: ddd=d.groupby(dd.squeeze()).mean()
    elif function=="function_cumsum_not_nan":  #counts the minutes of each cluster, reset on end of each cluster
        ddd=(~pd.isna(d.resample("min").mean())).mul(1).cumsum()
        ddd=(ddd-ddd[ddd.diff()==0].ffill())
        return(ddd)
    else: ddd=d.groupby(dd.squeeze()).apply(function)
    dd[dd.columns[0]]=ddd.loc[dd[dd.columns[0]].fillna(0).values].values
    dd=dd[~pd.isna(d)]
    dd.columns+="_Cluster-Mean"
    return(dd)


def pullzero(df):
    """For the period under consideration, the initial value of each counter time series is subtracted so that all time series start at 0."
        Arguments: 
            df: pandas DataFrame of counter time series that should all start at zero
        Returns: pandas DataFrame of counter time series that start at zero
    """
    return(df-df.fillna(method="bfill").iloc[0])

def resample2equidistance(df,freq="min"):
    """Completes the time series for each time step based on a defined temporal resolution, possibly adding a timestamp and setting the corresponding measurement value to unknown (NaN).
        Arguments:
            df: pandas DataFrame with time series that should be equidistanciated
            freq: string that parameterizes the time unit that should be used to equidistantiate
        Returns: 
            pandas DataFrame with equiudistantiated time series
    """
    df=df.sort_index()
    return(df.reindex(pd.date_range(start=df.index[0],end=df.index[-1],freq=freq)))

def desum_formBased(ts, threshold=5, ws=30, min_periods=5, b_visualize=False):
    """Divides a data series into two summands based on given criteria. 
        Disaggregation of the value of a time series into two time series based on different, pre-known performance profiles. A load profile is e.g. separated into base load and another, well identiable consumer.
        Arguments:
                ts: pandas time series data
                threshold: threshold that must be exceeded for second part to be considered as active (e.g. consumer switched on)
                ws: window size for the moving average calculation of the first part (e.g. base load)
                min_periods: minimum time units that threshold must be exceededor second part to be considered as active (e.g. consumer switched on)
                b_visualize: if set True, results will be plotted
        Returns:
            two pandas time series representing the splitted time series
    """
    step_width = detect_real_timeresolution(ts)
    if step_width.max() > 1:
        print("###Warning - there are", int(step_width[step_width > 1].sum()), "data gaps (not NaN, but missing rows), on average", step_width[step_width > 1].mean(), "minutes wide. -> not equidistant")
    summand2 = (ts[ts > threshold] - ts[ts <= threshold].rolling(window=ws, min_periods=min_periods, center=True).mean()).fillna(0)
    summand1 = ts - summand2.values
    summand2.columns += "_form-based Disaggregation(>" + str(threshold) + " within " + str(ws) + "min)_Part2"
    summand1.columns += "_Part1"
    if b_visualize: pd.concat([ts, summand1, summand2], axis=1).plot()
    return pd.concat([summand1, summand2], axis=1)


def desum_period_based(p,characterizing_periods=[60,1440],b_visualize=True): 
    """Disaggregation of the values of a time series into multiple time series based on different, pre-known periodicities.
Divides a time series into n periodic parts, each with its own period -> assuming the periodicity of the time series and the distinguishability of the parts based on different periods.
        Arguments: 
            p: pandas time series that should be disaggregated
            characterizing_periods: list of characterizing period durations in minutes (e.g. that caracterize the suspected consumers)
            b_visualize: if set to true, plot a visualization of the disaggregated time series
        Returns:
            multiple pandas time series representing the splitted time series
    """
    p=todf(p)
    p_rest=p
    pp=[]
    characterizing_periods_list=characterizing_periods
    if type(characterizing_periods)==dict: characterizing_periods_list=list(characterizing_periods.keys())
    characterizing_periods_list.sort()
    for period2cut in characterizing_periods_list:
        offsets=range(1,period2cut+1,1) 
        pfw_min=p_rest #corresponds to displacement 0
        pbw_min=p_rest
        for offset in offsets:
            #use numpy.where, as it is faster than pd.concat(..).min() ... (min needs to be calculated in the loop due to memory constraints)
            pfw=p_rest.shift(offset)
            b_pfw_nan=np.isnan(pfw)
            pfw_min=np.where((pfw>pfw_min) | b_pfw_nan ,pfw_min,pfw)
            pbw=p_rest.shift(-offset)
            b_pbw_nan=np.isnan(pbw)
            pbw_min=np.where((pbw>pbw_min) | b_pbw_nan ,pbw_min,pbw)
        p_rest_last=p_rest
        pfw_min=pd.DataFrame(pfw_min,index=p.index)
        pbw_min=pd.DataFrame(pbw_min,index=p.index)
        p_rest=todf(pd.concat([pfw_min,pbw_min],axis=1).max(axis=1),p.columns[0]+"_periodDuration>" +str(period2cut)+" min_baseLoad")
        descr="";
        if type(characterizing_periods)==dict: descr=characterizing_periods[period2cut]
        p_separated=todf(tos(p_rest_last)-tos(p_rest),p.columns[0]+"periodDuration<=" +str(period2cut)+" min_"+descr)
        pp.append(p_separated)
    pp.append(p_rest)
    pp=pd.concat(pp[::-1],axis=1)  #[::-1] -> reverse list, etc..
    if b_visualize:
        pp[pp>0].plot(kind="area",alpha=.5)
        p.plot(ax=gca(),linewidth=1,ms=1,alpha=.5)
        title("offsets:"+str(offsets))
    return(pp)

