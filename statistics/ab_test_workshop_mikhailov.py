# Калькуляторы для AB тестирования: https://www.evanmiller.org/ab-testing/chi-squared.html

# import libraries
import pandas as pd
import numpy as np
from scipy.stats import binom_test
from scipy.stats import chi2_contingency
from statsmodels.stats.proportion import proportions_ztest


# Пример с Виноградным днем. Менеджер утверждает, что 80% покупателей довольны напитком. Мы опросили 100 человек,
# 75 ответили, что напиток им нравится
# My solution
# Input data
sample_size = 100
sample_proportion = 0.75
true_population_proportion = 0.80
a = 1.96

# Output
standard_error = (sample_proportion * (1 - sample_proportion) / sample_size) ** 0.5
print('standard_error:', standard_error)
margin_error = a * standard_error
print('margin_error:', margin_error)
lower_value = sample_proportion - margin_error
upper_value = sample_proportion + margin_error
print('lower_value:', lower_value)
print('upper_value:', upper_value)
if lower_value <= true_population_proportion <= upper_value:
    print('Менеджер не врет')
else:
    print('Менеджер врет')

# Lecturer solution
sample = np.random.binomial(1, 0.8, 100)
sample_mean = np.mean(sample)
print('sample_mean:', sample_mean)
p_value = np.mean([np.random.binomial(1, 0.8, 100).mean() <= sample_proportion for i in range(10000)])
print('p_value:', p_value)
print('binom_test:', binom_test(75, n=sample_size, p=0.8,  alternative='less'))
print('proportions_ztest:', proportions_ztest(75, 100, value=0.8, alternative='smaller'))


# Пример с лендингом. Провели AB: контрольная выборка: 700 пользователей, 300 экспериментальная группа,
# 70 конверсий в первой, 48 во второй.

# Создаем таблицу с результатами теста
data = pd.DataFrame({'Group': ['old landing (A)', 'new landing (B)'], 'Users': [700, 300], 'Sales': [70, 48]})

# Считаем процент конверсии
data['CR'] = data['Sales'] / data['Users']
print(data)


# Формулируем HO: На самом деле показатель конверсии не отличается. Какая вероятность получить такие же и
# более значимые различия между двумя вариантами?

# Считаем, что не было разделения на группы. Добавляем в таблицу строку с общими результатами
data.loc['Total'] = data.sum()
data['CR'] = data['Sales'] / data['Users']
print(data)


# Создаем математическую модель.
# С помощью генератора случайных выборок с биномиальным распределением генерируем выборки.

# Среднее для контрольной выборки
control_sample_mean = np.random.binomial(1, data.iat[2, 3], data.iat[0, 1]).mean()
print('control_sample_mean:', control_sample_mean)

# Среднее для тестовой выборки
treatment_sample_mean = np.random.binomial(1, data.iat[2, 3], data.iat[1, 1]).mean()
print('treatment_sample_mean:', treatment_sample_mean)

# Считаем фактическую разницу между средними групп A и B. Считаем в обе стороны, поэтому добавляем модуль.
ab_mean_diff = abs(data.iat[0, 3] - data.iat[1, 3])
print('ab_mean_diff:', ab_mean_diff)


# Находим вероятность того, что разница в конверсии может быть больше или равна фактической разнице.
# Создаем функцию, которая будет генерировать разницу между средними выборок. Разницу считаем в обе стороны.
# Для этого добавляем модуль.


def sample_generator():
    mean_diff = abs(np.random.binomial(1, data.iat[2, 3], data.iat[0, 1]).mean()
                    - np.random.binomial(1, data.iat[2, 3], data.iat[1, 1]).mean())
    return mean_diff


# Генерируем 10000 выборок
p_value = np.mean([sample_generator() >= ab_mean_diff for _ in range(10000)])
print('p_value:', p_value)

# Проверяем результат с помощью Z-теста. Подаем на вход два массива: 1 с кол-вом продаж, второй с размерами выборок
p_value_z = proportions_ztest([data.iat[0, 2], data.iat[1, 2]], [data.iat[0, 1], data.iat[1, 1]])
print('p_value_1:', p_value_z[1])

# Проверяем результат с помощью теста Хи квадрат Пирсона.
# Создадим массив, где [[вариант A продажи, вариант A пользователи без покупок],
# [вариант B продажи, вариант B пользователи без покупок]]
data_array = [[data.iat[0, 2], data.iat[0, 1] - data.iat[0, 2]], [data.iat[1, 2], data.iat[1, 1] - data.iat[1, 2]]]
# chi2, p_value_chi2, dof, ex = chi2_contingency(data_array, correction=False)
p_value_chi2 = chi2_contingency(data_array, correction=False)
print('p_value_chi2:', p_value_chi2[1])
# Вывод: вероятность менее 1% (0.7%), отвергаем H0, делаем вывод, что разница в конверсии стат. значимая.


# Делаем аналогичный тест, но уже со своими данными
my_data = pd.DataFrame({'Group': ['old order form (A)', 'new order form (B)'], 'Users': [18632, 25032], 'Orders': [169, 188]})
my_data['CR'] = my_data['Orders'] / my_data['Users']
print(my_data)


# Формулируем HO: На самом деле показатель конверсии не отличается. Какая вероятность получить такие же и
# более значимые различия между двумя вариантами?
my_data.loc['Total'] = my_data.sum()
my_data['CR'] = my_data['Orders'] / my_data['Users']
print(my_data)
control_sample_mean = np.random.binomial(1, my_data.iat[2, 3], my_data.iat[0, 1]).mean()
print('control_sample_mean:', control_sample_mean)
treatment_sample_mean = np.random.binomial(1, my_data.iat[2, 3], my_data.iat[1, 1]).mean()
print('treatment_sample_mean:', treatment_sample_mean)
ab_mean_diff = abs(my_data.iat[0, 3] - my_data.iat[1, 3])
print('ab_mean_diff:', ab_mean_diff)


def sample_generator():
    mean_diff = abs(np.random.binomial(1, my_data.iat[2, 3], my_data.iat[0, 1]).mean()
                    - np.random.binomial(1, my_data.iat[2, 3], my_data.iat[1, 1]).mean())
    return mean_diff


p_value = np.mean([sample_generator() >= ab_mean_diff for _ in range(10000)])
print('p_value:', p_value)
p_value_z = proportions_ztest([my_data.iat[0, 2], my_data.iat[1, 2]], [my_data.iat[0, 1], my_data.iat[1, 1]])
print('p_value_1:', p_value_z[1])
data_array = [[my_data.iat[0, 2], my_data.iat[0, 1] - my_data.iat[0, 2]], [my_data.iat[1, 2], my_data.iat[1, 1] - my_data.iat[1, 2]]]
p_value_chi2 = chi2_contingency(data_array, correction=False)
print('p_value_chi2:', p_value_chi2[1])
# Вывод: вероятность более 7% (7.69%), подтверждаем H0, делаем вывод, что разница в конверсии не статистически значимая.

# Если между конверсией двух выборок нет разницы, то p-value на гистограмме будет распределяться равномерно
