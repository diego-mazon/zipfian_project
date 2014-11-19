
from __future__ import division
import pandas as pd
import numpy as np
from lifelines import AalenAdditiveFitter
import dill
import pickle

def kfoldcv(data, k=5, m=10, penalizer=0.5, timeinterval=np.linspace(1,20,20), duration_col='ndays_act', event_col='observed'):
    """
    Trains data with AalenAdditiveFitter and (k-fold) cross validate it.
    Based on lifelines library for survival analysis in Python.
    
    data: a Pandas dataframe.
    k: number of folds
    m: number of time units to be included in the cross validation
    penalizer: argument of class AalenAdditiveFitter (lifelines library)
    timeinterval: argument of AalenAdditiveFitter().fit method. Time points that are fitted.
    duration_col: last column from data. It contains the lifetime of each case.
    event_col: second-to-last column from data. It contains the censorships. So far this function
                only works without censorships, that is, all death events must be observed. 
                Therefore, it must be a column of ones.
                
    Prints: Average relative error of the predicted probabilities. 

    """
    
    aaf = AalenAdditiveFitter(penalizer=penalizer)
    n, d = data.shape
    data = data.copy()
    data = data.reindex(np.random.permutation(data.index)).sort(event_col)
    scores = []
    assignments = np.array((n // k + 1) * list(range(1, k + 1)))
    assignments = assignments[:n]

    testing_columns = data.columns - [duration_col, event_col]

    for i in range(1, k + 1):

        ix = assignments == i
        training_data = data.ix[~ix]
        testing_data = data.ix[ix]

        T_actual = testing_data[duration_col].values
        E_actual = testing_data[event_col].values
        X_testing = testing_data[testing_columns]

        aaf.fit(training_data, duration_col=duration_col, event_col=event_col, timeline=timeinterval)

        used_ind = []
        prec_sum = 0
        rel_sum = 0
        rel_error_list = []
        df = testing_data
        #ndays must be the last column, and observed the second-to-last
        for j,row in df.iterrows():
        
            if not j in used_ind:
                
                a = df[np.all(df.ix[:,0:-2].values==df.ix[j,:-2].values, axis=1)]
                list_ = a.index.tolist()
                used_ind += list_
                
                actual_rate_series = a.ndays_act.value_counts() / a.shape[0]
                mini = min(actual_rate_series.shape[0], m)
                actual_rate = np.array(actual_rate_series)[:mini]
                pred_df = aaf.predict_survival_function(a.iloc[0,:-2][None,:])
                pred_array = np.array(pred_df)              
                pred_rate = np.zeros(mini)
                pred_rate[0] = 1 - pred_array[0]
                
                for alpha in range(1, mini):
                    pred_rate[alpha] = pred_array[alpha-1] - pred_array[alpha]
                      
                maxi = np.maximum(pred_rate, actual_rate)
                rel_error = np.abs(pred_rate - actual_rate) / maxi
                rel_error_list.append(rel_error)
                succes_rate = len(rel_error[rel_error <= 0.15]) / mini
                prec_sum += succes_rate * len(a)
                rel_sum += np.sum(rel_error) / mini * len(a)
                
        precision = prec_sum / df.shape[0]
        relative = rel_sum / df.shape[0]
        scores.append(precision)
        
        print "Average relative error: ", relative
        
        #pickle it if you want to save your training 
        #with open('path_file', 'wb') as f:
        #    pickle.dump(aaf, f)
        
    