#!/usr/bin/env python
# coding: utf-8

# ### Imports

import numpy as np
# modules for functions
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
from matplotlib import pyplot as plt
import seaborn as sns
pio.templates.default = "plotly_dark"

# Parametric Tests

#Scipy.stats imports for normality tests
from scipy.stats import (kruskal, kstest, pearsonr, ranksums, shapiro,
                         spearmanr, ttest_ind, f_oneway)
from statsmodels.graphics.gofplots import qqplot


### General Utilities

## Get name of provided values in fuctions
def get_df_name(df):
    return [x for x in globals() if globals()[x] is df][0]

## Statistical Tests
#Define significance level
alpha = 0.05
normality=True
normalityRuns=0


def normality_eda(data):
    #dataName=get_df_name(data)
    
    # Print Descriptive Statistics
    print('Descriptive Statistics:')
    print(data.describe())
    print('\nVisual Normality Tests:')
    print('\n', 'Variable plots:')
    data=np.array(data, dtype='float64')
    
    #plot Histogram
    plt.hist(data, bins=10)
    print('\n', 'Variable Histogram')
    plt.axvline(data.mean(), color='k', linestyle='dashed', linewidth=1)
    plt.show()

    #plot Boxplot
    plt.boxplot(data)
    print('Boxplot')
    plt.show()

    #plot QQplot
    qqplot(data, line='s')
    print('QQplot')
    plt.show()

def normality_test(data):
    """
    Normality test function
    data: numpy array of observations from data to check
    """
    #dataName=get_df_name(data)
    global normality
    global normalityRuns
    # Perform Shapiro Test
    stat, p = shapiro(data)
    print('\nShapiro Test Statistics=%.3f, p=%.3f' % (stat, p))

    # Interpret Test
    if p > alpha:
        print('Variable', (normalityRuns +1), 'looks Gaussian (fail to reject H0)')
        normality=normality and True
    else:
        print('Variable', (normalityRuns +1), 'does not look Gaussian (reject H0)')
        normality=False
    normalityRuns+=1
    if normalityRuns>1:
       normalityRuns=0
       normality=True


def significance_test(dataset1, dataset2):
    global stat, p
    if normality: 
        stat, p = ttest_ind(dataset1, dataset2)          
    else: 
        stat, p = ranksums(dataset1, dataset2)
    print('Statistics=%.3f, p=%.3f' % (stat, p))
    
    # interpret
    if p > alpha:    
        print('The difference between the datasets is not significant (fail to reject H0)')
    else:
        print('The difference between the datasets is significant (reject H0)')
    return stat, p


def correlation_test(dataset1, dataset2):
    #dataName1=get_df_name(dataset1)
    #dataName2=get_df_name(dataset2)
    #dataName1=testing_column1
    #dataName2=testing_column2
    global stat, p
    if normality: 
        stat, p = pearsonr(dataset1, dataset2)          
    else: 
        stat, p = spearmanr(x=dataset1, y=dataset2)
    print('Statistics=%.3f, p=%.3f' % (stat, p))

    # interpret
    if (p < alpha) & (stat > 0):
        print('The two datasets are positively corelated')
    elif (p < alpha) & (stat < 0):
        print('The two datasets are negatively corelated')
    else:
        print('The two datasets are not corelated')
    return stat, p
      
def testing(testType: str, dataset1, dataset2, eda: bool = False):
    if eda:
      normality_eda(dataset1)
      normality_eda(dataset2)
    normality_test(dataset1)
    normality_test(dataset2)
    if testType =='Significance':
       significance_test(dataset1, dataset2)
    elif testType =='Correlation': 
      correlation_test(dataset1, dataset2)
    else:
      print("testType must be either Significance or Correlation")
    return stat, p
