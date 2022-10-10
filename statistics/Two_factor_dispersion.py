# Main question: Is any of the individual parameters or combined make the results
# between 4 groups statistically significant?
# We have results from 4 tests Young-Low_dosis, Young-High_dosis, Old-Low_dosis, Old-High_dosis (see data link below)
# Our Zero hypothesis (H-zero) is that the results between groups are not statistically significant
# For H-zero to be true F has to be very small (close to 0) and P > 0.05
# A statistically significant test result (P ≤ 0.05) means that the Zero hypothesis is false or should be rejected
# For the results to be statistically significant F has to be not too small, definitely not close to 0 and P < 0.05
# (P > 0.05 is the probability that the null hypothesis is true)

# Process followed:
# 1. Import libraries
# 2. Import and read dataset
# 3. Clean dataset
# 4. Do EDA (exploratory data analysis) to see the data
# 5. Find F and P
# 6. Conclusion
# 7. References

# 1. Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import seaborn as sns
import statsmodels.api as sm
from statsmodels.formula.api import ols

# 2. Import and read dataset
url = 'https://raw.githubusercontent.com/betelgeus/fundamentals_of_statistics_notes/main/data/atherosclerosis.csv'
df = pd.read_csv(url, header=None, sep=',')
# print(df)

# 3. Clean dataset
# We need to clean the data: drop the first row and move column labels to header
# We set the column labels to equal the values in the 1st row (index location 0):
df.columns = df.iloc[0]
# print(df)

# Then we drop the 1st row using iloc
# We will save the new dataset as df_cleaned and will use this dataset from the rest of the operations
df_cleaned = df.iloc[pd.RangeIndex(len(df)).drop(0)]
# print(df_cleaned)

# We convert the 'expr' column data to numeric:
df_cleaned.expr = pd.to_numeric(df_cleaned['expr'], errors='coerce')

# Replace values in 'age' and 'dose' columns to Young, Old, Low and High
for i in range(len(df_cleaned)):
    if df_cleaned.iat[i, 1] == '1':
        df_cleaned.iat[i, 1] = 'Young'
        if df_cleaned.iat[i, 2] == 'D1':
            df_cleaned.iat[i, 2] = 'Low'
        elif df_cleaned.iat[i, 2] == 'D2':
            df_cleaned.iat[i, 2] = 'High'
    elif df_cleaned.iat[i, 1] == '2':
        df_cleaned.iat[i, 1] = 'Old'
        if df_cleaned.iat[i, 2] == 'D1':
            df_cleaned.iat[i, 2] = 'Low'
        elif df_cleaned.iat[i, 2] == 'D2':
            df_cleaned.iat[i, 2] = 'High'

# 4. Do EDA (exploratory data analysis) to see the data
# Let's explore data looking at boxplot by dose
# We can see the overlap of medians and boxes
# df_cleaned.boxplot('expr', by='dose', figsize=(12, 8), grid=True)
# plt.show()

# Let's explore data looking at boxplot by age
# In this case there is a bit more difference and the median of each group is outside the box of the other group
# df_cleaned.boxplot('expr', by='age', figsize=(12, 8), grid=True)
# plt.show()

# Another view is via pairplot (not too useful here)
# sns.pairplot(df_cleaned, y_vars="expr", x_vars=['age', 'dose'])
# plt.show()

# Let's get means, dispersion and how expression influenced by age, dose via pointplot
sns.set()
sns.pointplot(data=df_cleaned, x='dose', y='expr', hue='age', dodge=True, capsize=.1, errwidth=1, palette='colorblind')
plt.show()


# 5. Let's do the one-way ANOVA tests. The null hypothesis that four groups have the same population mean
# Create samples combining multiple conditions (e.g. row: 101.062276  Old  Low)
G1_A1_D1 = df_cleaned[(df_cleaned['age'] == 'Young') & (df_cleaned['dose'] == 'Low')]
G2_A1_D2 = df_cleaned[(df_cleaned['age'] == 'Young') & (df_cleaned['dose'] == 'High')]
G3_A2_D1 = df_cleaned[(df_cleaned['age'] == 'Old') & (df_cleaned['dose'] == 'Low')]
G4_A2_D2 = df_cleaned[(df_cleaned['age'] == 'Old') & (df_cleaned['dose'] == 'High')]

# Find F critical value
# Calculate Degree of freedom between groups (count of groups minus 1)
df_between = 4 - 1
# Calculate Degree of freedom within group (count of observations minus count of groups)
df_within = len(df_cleaned) - 4
# Significance level is 0.05
sign_level = 1 - .05

f_critical_value = stats.f.ppf(q=sign_level, dfn=df_between, dfd=df_within)
# print(f_critical_value)
# F critical value is 2.7580782958425805

# Create 4 groups (e.g. row: 107.351478)
Age1_D1 = df_cleaned[(df_cleaned['age'] == 'Young') & (df_cleaned['dose'] == 'Low')]["expr"]
Age1_D2 = df_cleaned[(df_cleaned['age'] == 'Young') & (df_cleaned['dose'] == 'High')]["expr"]
Age2_D1 = df_cleaned[(df_cleaned['age'] == 'Old') & (df_cleaned['dose'] == 'Low')]["expr"]
Age2_D2 = df_cleaned[(df_cleaned['age'] == 'Old') & (df_cleaned['dose'] == 'High')]["expr"]

# Find F-value and P-value
f_statistics_age_dose, p_value_age_dose = stats.f_oneway(Age1_D1, Age1_D2, Age2_D1, Age2_D2)
print("Results for all 4 groups", stats.f_oneway(Age1_D1, Age1_D2, Age2_D1, Age2_D2))

# Compare F critical value with F statistic and get result test
# If the F statistic is greater than F critical value (2.7580782958425805) and P-value < 0.05,
# then the results of the test are statistically significant, confirmed the alternative hypothesis.
# Having P-value > 0.05 and F statistic over 2.7, tells us that when compared all 4 groups there is no stat. sign.,
# but the results are "on the border".
# With F statistic over 2.7 we would look at each group separately to understand if there is anything interesting
# F and P for all groups (P-value is "on the border", P > 0.05, however by very little)
if round(p_value_age_dose, 2) > 0.05:
    print('We did not find significant statistical differences')
else:
    if round(f_statistics_age_dose, 3) >= round(f_critical_value, 3):
        print('We find significant statistical differences')
    else:
        print('We need look at each group separately to understand if there is anything interesting')

# F and P for Young and Low
age_young = df_cleaned[df_cleaned['age'] == 'Young']["expr"]
dose_low = df_cleaned[df_cleaned['dose'] == 'Low']["expr"]
f_statistics_young_low, p_value_young_low = stats.f_oneway(age_young, dose_low)
print('f_statistics_young_low:', f_statistics_young_low, 'p_value_young_low:', p_value_young_low)

# F and P for Old and Low
age_old = df_cleaned[df_cleaned['age'] == 'Old']["expr"]
f_statistics_old_low, p_value_old_low = stats.f_oneway(age_old, dose_low)
print('f_statistics_old_low:', f_statistics_old_low, 'p_value_old_low:', p_value_old_low)

# F and P for Young and High
dose_high = df_cleaned[df_cleaned['dose'] == 'High']["expr"]
f_statistics_young_high, p_value_young_high = stats.f_oneway(age_young, dose_high)
print('f_statistics_young_high:', f_statistics_young_high, 'p_value_young_high:', p_value_young_high)

# F and P for Young and Low
f_statistics_old_high, p_value_old_high = stats.f_oneway(age_old, dose_high)
print('f_statistics_old_high:', f_statistics_old_high, 'p_value_old_high:', p_value_old_high)

# F and P for Young and Old
# Here is where we see the most interesting results
# P < 0.05 and F is large (>7), this means that the groups split by age yield stat. sign. results
f_statistics_age, p_value_age = stats.f_oneway(age_young, age_old)
print('f_statistics_age:', f_statistics_age, 'p_value_age:', p_value_age)

# F and P for Dose 1 and Dose 2
# In this case we can see that P > 0.05 and F is close to 0
# In case of splitting by dose the Zero-H is true
f_statistics_dose, p_value_dose = stats.f_oneway(dose_low, dose_high)
print('f_statistics_dose:', f_statistics_dose, 'p_value_dose:', p_value_dose)

# F and P values, the sum_sq, mean_sq and df using anova
# Here we are using age + dose
# source https://www.statsmodels.org/devel/generated/statsmodels.stats.anova.anova_lm.html
expr_lm = ols('expr ~ age+dose', data=df_cleaned).fit()
# Type 2 Anova DataFrame
table_1 = sm.stats.anova_lm(expr_lm, type=2)
print(table_1)

# sum_sq for Therapy is SSB (=total sum of squares between groups)
# mean_sq for Therapy is SSB divide by degrees of freedom
# df for Therapy is degrees of freedom between groups
# sum_sq for Residual is SSW (=total sum of squares within groups)
# mean_sq for Residual is SSW divide by degrees of freedom
# df for Residual is degrees of freedom within groups

# Here we are using age*dose, to also see this as a combined parameter
# The Residual becomes 60, from 61 because we introduce this another group
expr_lm = ols('expr ~ age*dose', data=df_cleaned).fit()
table_2 = sm.stats.anova_lm(expr_lm, type=2)
print(table_2)


# 6. Conclusion
# If H-zero is TRUE then F has to be very small, close to 0 and P > 0.05
# We can see that in this vase the P is < 0.05 and F is fairly large (7,44) for the age group.
# This allows us to say that there is statistical significance in results grouped by age (Young and Old)
# For the dose and age:dose result P > 0.05 and F is very small, less than 1.
# This allows us to say that H-zero is true for dose and age:dose groups.


# 7. References
# Based on Masha Kubyshina, Statistics Basics Two Factor Dispersion
# https://github.com/MashaKubyshina/Data_Science_Scripts/blob/master/Statistics_Basics_Two_Factor_Dispersion.ipynb
