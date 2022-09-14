# Калькуляторы для AB тестирования: https://www.evanmiller.org/ab-testing/chi-squared.html

# import libraries
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.stats.api as sms
from scipy.stats import binom_test
from scipy.stats import chi2_contingency
from statsmodels.stats.proportion import proportions_ztest

# План воркшопа
# 1. Пример с долей довольных покупателей
# 2. Пример с конверсией лендинга
# 3. Аналогичная модель, что и в п. 2, но на примере своих данных
# 4. Ошибки первого рода и alpha
# 5. Ошибки второго рода и мощность
# 6. Зачем нужны alpha и мощность

# 1. Пример с Виноградным днем. Менеджер утверждает, что 80% покупателей довольны напитком. Мы опросили 100 человек,
# 75 ответили, что напиток им нравится
print('=======1========')
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
print('p_value binom_test:', binom_test(75, n=sample_size, p=0.8,  alternative='less'))
print('p_value proportions_ztest:', proportions_ztest(75, 100, value=0.8, alternative='smaller')[1])


#  2. Пример с лендингом. Провели AB: контрольная выборка: 700 пользователей, 300 экспериментальная группа,
# 70 конверсий в первой, 48 во второй.
print('=======2========')

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


# 3. Делаем аналогичный тест, но уже со своими данными
print('=======3========')
my_data = pd.DataFrame({'Group': ['old order form (A)', 'new order form (B)'], 'Users': [18632, 25032], 'Orders': [169, 188]})
my_data['CR'] = my_data['Orders'] / my_data['Users']
my_data.loc['Total'] = my_data.sum()
my_data['CR'] = my_data['Orders'] / my_data['Users']
control_sample_mean = np.random.binomial(1, my_data.iat[2, 3], my_data.iat[0, 1]).mean()
treatment_sample_mean = np.random.binomial(1, my_data.iat[2, 3], my_data.iat[1, 1]).mean()
ab_mean_diff = abs(my_data.iat[0, 3] - my_data.iat[1, 3])


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


# 4. Ошибки первого рода — это когда мы отвергаем верную нулевую гипотезу. Например, конверсия не отличается, но
# в результате тестов мы получаем статистические данные, которые показывают, что есть отличие.
# Значение alpha показывает вероятность того, что мы ошибочно отклоним верную нулевую гипотезу. Как правило,
# используют alpha = 0.05, но при реальных тестах используют значение меньше.
print('=======4========')

# Проверим достоверность уровня статистической значимости alpha
n = 1000
result = []
for _ in range(n):
    a = np.random.binomial(1, 0.118, size=700)
    b = np.random.binomial(1, 0.118, size=300)
    diff = abs(a.mean() - b.mean())
    null_hyp_prob = np.concatenate([a, b]).mean()
    p_val = np.mean([abs(np.random.binomial(1, null_hyp_prob, size=300).mean()
                         - np.random.binomial(1, null_hyp_prob, size=700).mean()) >= diff for _ in range(1000)])
    result.append(p_val)
print('alpha probability:', (np.array(result) < 0.05).mean())

# Если между конверсией двух выборок нет разницы, то p-value на гистограмме будет распределяться равномерно
sns.histplot(result)
plt.show()


# 5. Ошибки второго рода — это когда мы принимаем неверную нулевую гипотезу. Например, на самом деле конверсия
# отличается, но в результате тестов мы получаем статистику, которая говорит, что отличий нет.
# Мощность показывает вероятность того, что мы отклоним неверную нулевую гипотезу. Обычно используют мощность равную 0.8
print('=======5========')

# Проверим вероятность подтвердить неверную нулевую гипотезу. Сгенерируем выборки, в которых средние отличаются.
n = 1000
result = []
for _ in range(n):
    a = np.random.binomial(1, 0.10, size=700)
    b = np.random.binomial(1, 0.16, size=300)
    diff = abs(a.mean() - b.mean())
    null_hyp_prob = np.concatenate([a, b]).mean()
    p_val = np.mean([abs(np.random.binomial(1, null_hyp_prob, size=300).mean()
                         - np.random.binomial(1, null_hyp_prob, size=700).mean()) >= diff for _ in range(1000)])
    result.append(p_val)
print('power probability:', (np.array(result) < 0.05).mean())
# Обрати внимание, что P-value распределяется неравномерно, большая часть значений близка к нулю.
# Это нормальное поведение для отличающихся средних.
pd.Series(result).hist()
plt.show()

# Расчет размера выборки:
# effectsize(0.10, 0.15) это ожидаемый эффект. 0.10 текущая конверсия, 0.15 планируемая конверсия
es = sms.proportion_effectsize(0.10, 0.15)
# ratio соотношение выборок
print(sms.NormalIndPower().solve_power(es, power=0.80, alpha=0.05, ratio=1))
# Калькулятор размера выборки: https://www.evanmiller.org/ab-testing/sample-size.html

# 6. Alpha и мощность позволяют учесть вероятность ошибок первого и второго рода, учесть их в модели,
# рассчитать необходимое количество наблюдений в выборке.
