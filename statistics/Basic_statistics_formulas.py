# IMPORT LIBRARIES
import pandas as pd
import numpy as np
import random
from scipy import stats
import matplotlib.pyplot as plt
plt.style.use('seaborn')

# _1. min and max value, count of observations in sample, frequency, unique values
# good material https://www.statology.org/frequency-tables-python/
# Input data
# data set
data_set_1 = [1, 2, 2, 3, 4,  3, 4, 5, 6, 7, 7, 7, 8, 9, 10, 12, 12, 13]
# intervals from min to max in range data set
bins_data_set_1 = [0, 2, 4, 6, 8, 10, 12, 14]
# count of intervals from min to max in range data set
count_intervals_1 = 4

# Outcome
# max value
max_value_1 = max(data_set_1)

# min value
min_value_1 = min(data_set_1)

# count of observations in sample
cnt_observations_1 = len(data_set_1)

# create frequency table with input count intervals
frequency_1, intervals_1 = np.histogram(data_set_1, bins=count_intervals_1)
data_frame_1 = pd.DataFrame(index=np.linspace(1, count_intervals_1, count_intervals_1), columns=['start', 'end', 'frequency', 'relative frequency'])
# assign the intervals
data_frame_1['start'] = intervals_1[:-1]
data_frame_1['end'] = intervals_1[1:]
# assign absolute frequency
data_frame_1['frequency'] = frequency_1
# assign relative frequency
data_frame_1['relative frequency'] = frequency_1 / cnt_observations_1 * 100

# create frequency table with input bins
frequency_1_1, intervals_1_1 = np.histogram(data_set_1, bins=bins_data_set_1)
data_frame_1_1 = pd.DataFrame(index=np.linspace(1, len(bins_data_set_1)-1, len(bins_data_set_1)-1), columns=['start', 'end', 'frequency', 'relative frequency'])
# assign the intervals
data_frame_1_1['start'] = intervals_1_1[:-1]
data_frame_1_1['end'] = intervals_1_1[1:]
# assign absolute frequency
data_frame_1_1['frequency'] = frequency_1_1
# assign relative frequency
data_frame_1_1['relative frequency'] = frequency_1_1 / cnt_observations_1 * 100

# unique values
data_unique_1 = set(data_set_1)

# Output result
print(f'max_value_1:{max_value_1}, min_value_1:{min_value_1}, cnt_observations_1:{cnt_observations_1}, data_frame_1:{data_frame_1}, data_frame_1_1:{data_frame_1_1}')
print('+++++++++++++')


# _2. import data from excel, find unique objects, create frequency bar
# Input
# import data
data_frame_2 = pd.read_excel('/Users/mitya/Documents/Coursera Data for Business/example_data_set_trucks.xlsx')
# find columns name
data_columns_name = data_frame_2.columns[0]

# Outcome
# create new frame with group by first columns
frequency_data_frame_2 = data_frame_2.groupby([data_columns_name])
# create new table with absolute frequency and sort from max to min
frequency_data_table_2 = frequency_data_frame_2.value_counts()
frequency_data_table_2 = frequency_data_table_2.sort_values(ascending=False)
# quick method to get count, mean, standard deviation, minimum value, maximum value and 25%, 50% and 75% percentiles
measures_central_tendency = frequency_data_table_2.describe()

# create frequency bar, X axis = .keys, Y axis = .values
plt.bar(frequency_data_table_2.keys(), frequency_data_table_2.values,  color='blue', ec='black', alpha=0.5)
# add labels and modify size
plt.ylabel('Absolute Frequency', fontsize=14)
plt.xlabel(data_columns_name, fontsize=14)
plt.xticks(fontsize=8)
plt.yticks(fontsize=14)
# add title
plt.title('ABSOLUTE FREQUENCY HISTOGRAM', fontsize=16)
plt.show()


# _3. Measure of Central Tendency and Measure of Dispersion (Variation)
# Input
# import data
data_frame_3 = pd.read_excel('/Users/mitya/Documents/Coursera Data for Business/example_data_set_temperature.xlsx')
# find columns name
data_columns_name_3 = data_frame_3.columns[2]

# Outcome
mean_3 = data_frame_3[data_columns_name_3].mean()
median_3 = data_frame_3[data_columns_name_3].median()
st_deviation_3 = data_frame_3[data_columns_name_3].std()

# Output
print(f'mean_3:{mean_3}, median_3:{median_3}, st_deviation_3:{st_deviation_3}')


# _4. Z-score and percentile by mean, standard deviation and x
# Input
# example data
mean_4 = 54030
st_deviation_4 = 8600
x_4 = 65000

# Outcome
z_score_4 = (x_4 - mean_4) / st_deviation_4
percentile_4 = stats.norm(mean_4, st_deviation_4).cdf(x_4)
p_value_right_4 = (stats.norm(mean_4, st_deviation_4).sf(x_4))

# Output
print(f'z_score_4:{z_score_4}, percentile_4:{percentile_4}, p_value_right_4:{p_value_right_4}')


# _5. Z-score and percentile by z-score and percentile
# Input
# example data
z_score_5 = 1.275581395
percentile_5 = 0.8989482328784237

# Outcome
z_score_outcome_5 = stats.norm.ppf(percentile_5)
percentile_outcome_5 = stats.norm.cdf(z_score_5)
p_value_right_5 = stats.norm.sf(z_score_5)

# Output
print(f'z_score_outcome_5:{z_score_outcome_5}, percentile_outcome_5:{percentile_outcome_5}, p_value_right_5:{p_value_right_5}')


# _6. Expected value for random variables
# Input
# import data
data_frame_6 = pd.read_excel('/Users/mitya/Documents/Coursera Data for Business/example_data_set_ipad.xlsx')
# find columns name
column_one_name_6 = data_frame_6.columns[0]
column_two_name_6 = data_frame_6.columns[1]

# Outcome
# calculate total sum for all observed
sum_6 = data_frame_6[column_two_name_6].sum()
# add probability column in table
data_frame_6['Probability'] = data_frame_6[column_two_name_6] / sum_6


# calculate expected value
def sum_product_excel_function(values, weights):
    values = np.asarray(values)
    weights = np.asarray(weights)
    return (values * weights).sum() / weights.sum()


expected_value_6 = sum_product_excel_function(data_frame_6[column_one_name_6], data_frame_6['Probability'])

# add (x-mu(expected value))^2 column in table
data_frame_6['x-mu^2'] = (data_frame_6[column_one_name_6] - expected_value_6) ** 2
# calculate standart deviation
st_deviation_6 = sum_product_excel_function(data_frame_6['x-mu^2'], data_frame_6['Probability']) ** 0.5

# Output
print(f'data_frame_6:{data_frame_6}, sum_6:{sum_6}, expected_value_6:{expected_value_6}, st_deviation_6:{st_deviation_6}')


# _7. Probability between two x values
# Input
# example data
mean_7 = 500
st_deviation_7 = 100
x_one_7 = 490
x_two_7 = 550

# Outcome
percentile_x_one_7 = stats.norm(mean_7, st_deviation_7).cdf(x_one_7)
percentile_x_two_7 = stats.norm(mean_7, st_deviation_7).cdf(x_two_7)
probability_7 = percentile_x_two_7 - percentile_x_one_7

# Output
print(f'probability_7:{probability_7}')


# _8. Create simple random sample from population in file, calculate mean, standard deviation, standard error for sample
# Input
# import data
data_frame_8 = pd.read_excel('/Users/mitya/Documents/Coursera Data for Business/example_data_set_population.xlsx')
# find columns name
column_name_8 = data_frame_8.columns[0]
# create list with observation from population
population_8 = data_frame_8[column_name_8].tolist()
st_deviation_for_population_8 = np.std(population_8)
# define sample size
sample_size_8 = 35
# define count of sample
sample_count_8 = 600
# create empty table with columns mean, standard deviation, standard error
sampling_means_and_st_dev_8 = pd.DataFrame({'Mean': [], 'St. Deviation': [], 'St. Error': []})

# Outcome
for i in range(sample_count_8):
    sample_8 = random.sample(population_8, sample_size_8)
    sampling_means_and_st_dev_8.loc[i] = (round(np.mean(sample_8)), round(np.std(sample_8), 5), round(np.std(sample_8)/sample_size_8 ** 0.5, 5))

# create frequency table with count mean values (e.g. mean: 65, count: 12), table without name of columns
means_frequency_table_8 = sampling_means_and_st_dev_8['Mean'].value_counts(sort=False)

average_for_means_8 = np.mean(sampling_means_and_st_dev_8['Mean'])
st_dev_for_all_sample_8 = np.std(sampling_means_and_st_dev_8['Mean'])
st_error_for_all_sample_8 = st_deviation_for_population_8 / sample_size_8 ** 0.5
median_for_all_sample_8 = np.median(sampling_means_and_st_dev_8['Mean'])

# Output
print(sampling_means_and_st_dev_8['Mean'].describe())
print('median:', median_for_all_sample_8)
print('standard error:', st_error_for_all_sample_8)
# create frequency bar for table without name of columns, X axis = .keys, Y axis = .values
plt.bar(means_frequency_table_8.keys(), means_frequency_table_8.values,  color='blue', ec='black', alpha=0.5)
# create box plot
plt.boxplot(sampling_means_and_st_dev_8['Mean'], vert=False, widths=max(means_frequency_table_8.values) / 5, showmeans=True, manage_ticks=False, autorange=True)

plt.axvline(x=average_for_means_8 - st_error_for_all_sample_8 * 3, color='red', linestyle='-.', ymin=0.1, linewidth=0.5)
plt.axvline(x=average_for_means_8 + st_error_for_all_sample_8 * 3, color='red', linestyle='-.', ymin=0.1, linewidth=0.5)
y_hlines = max(means_frequency_table_8.values) - max(means_frequency_table_8.values) * 0.5
xmin_hlines = average_for_means_8 - st_error_for_all_sample_8 * 3
xmax_hlines = average_for_means_8 + st_error_for_all_sample_8 * 3
plt.hlines(y_hlines, xmin=xmin_hlines, xmax=xmax_hlines,  color='red', linestyle='dotted', linewidth=1)
text_x = average_for_means_8
text_y = max(means_frequency_table_8.values) - max(means_frequency_table_8.values) * 0.5
plt.text(text_x, text_y, '99,7% observations (mean ± 3 standard error)', color='black', va='bottom', ha='center')

plt.axvline(x=average_for_means_8 - st_error_for_all_sample_8 * 2, color='blue', linestyle='-.', ymin=0.1, linewidth=0.5)
plt.axvline(x=average_for_means_8 + st_error_for_all_sample_8 * 2, color='blue', linestyle='-.', ymin=0.1, linewidth=0.5)
y_hlines = max(means_frequency_table_8.values) - max(means_frequency_table_8.values) * 0.3
xmin_hlines = average_for_means_8 - st_error_for_all_sample_8 * 2
xmax_hlines = average_for_means_8 + st_error_for_all_sample_8 * 2
plt.hlines(y_hlines, xmin=xmin_hlines, xmax=xmax_hlines,  color='blue', linestyle='dotted', linewidth=1)
text_x = average_for_means_8
text_y = max(means_frequency_table_8.values) - max(means_frequency_table_8.values) * 0.3
plt.text(text_x, text_y, '95,5% observations (mean ± 2 standard error)', color='black', va='bottom', ha='center')

plt.axvline(x=average_for_means_8 - st_error_for_all_sample_8, color='green', linestyle='-.', ymin=0.1, linewidth=0.5)
plt.axvline(x=average_for_means_8 + st_error_for_all_sample_8, color='green', linestyle='-.', ymin=0.1, linewidth=0.5)
y_hlines = max(means_frequency_table_8.values) - max(means_frequency_table_8.values) * 0.1
xmin_hlines = average_for_means_8 - st_error_for_all_sample_8
xmax_hlines = average_for_means_8 + st_error_for_all_sample_8
plt.hlines(y_hlines, xmin=xmin_hlines, xmax=xmax_hlines,  color='green', linestyle='dotted', linewidth=1)
text_x = average_for_means_8
text_y = max(means_frequency_table_8.values) - max(means_frequency_table_8.values) * 0.1
plt.text(text_x, text_y, '68,0% observations (mean ± 1 standard error)', color='black', va='bottom', ha='center')

# add labels and modify size
plt.ylabel('Absolute Frequency', fontsize=14)
plt.xlabel('Mean', fontsize=14)
plt.xticks(fontsize=8)
plt.yticks(fontsize=14)
# add title
plt.title('Mean of sample distribution', fontsize=16)
plt.show()


# _9. Student's T-test, T-value
# Input data
mean_for_sample_one_9 = 45
mean_for_sample_two_9 = 34
st_dev_for_sample_one_9 = 9
st_dev_for_sample_two_9 = 10
first_sample_size_9 = 100
second_sample_size_9 = 100

# Outcome
st_error_for_sample_one_9 = st_dev_for_sample_one_9 / first_sample_size_9 ** 0.5
st_error_for_sample_two_9 = st_dev_for_sample_two_9 / second_sample_size_9 ** 0.5
st_error_for_div_9 = (st_error_for_sample_one_9 ** 2 + st_error_for_sample_two_9 ** 2) ** 0.5
t_value_9 = (mean_for_sample_one_9 - mean_for_sample_two_9) / st_error_for_div_9
# second param is degree of freedom
p_value_9 = stats.t.sf(t_value_9, first_sample_size_9 + second_sample_size_9 - 2)

# Output
print('st_error_for_sample_one_9:', st_error_for_sample_one_9)
print('st_error_for_sample_two_9:', st_error_for_sample_two_9)
print('st_error_for_div_9:', st_error_for_div_9)
print('t_value:', t_value_9)
print('p_value_9:', p_value_9)
