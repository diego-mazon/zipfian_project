from __future__ import division
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn
import lifelines
from lifelines.estimation import KaplanMeierFitter
from lifelines.estimation import NelsonAalenFitter
from lifelines.estimation import AalenAdditiveFitter
import lifelines.statistics
from lifelines.utils import datetimes_to_durations
import patsy
from lifelines.plotting import plot_lifetimes
from numpy.random import uniform, exponential
from lifelines import AalenAdditiveFitter
from lifelines.datasets import generate_rossi_dataset
from lifelines import CoxPHFitter
from lifelines.datasets import generate_regression_dataset
from lifelines.utils import k_fold_cross_validation
from lifelines import AalenAdditiveFitter


df = pd.read_csv('../data/data.csv')

def func(gender, age, country):

