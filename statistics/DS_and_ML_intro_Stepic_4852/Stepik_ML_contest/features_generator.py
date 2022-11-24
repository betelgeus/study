import numpy as np
import pandas as pd
import data_preparation as pr
import config as conf
from math import ceil
pd.options.mode.chained_assignment = None


def rename_columns(users_metrics_n_days):
    users_metrics_n_days = users_metrics_n_days.rename(columns={('discovered', 1): 'd_1', ('discovered', 2): 'd_2',
                                                                ('viewed', 1): 'v_1', ('viewed', 2): 'v_2',
                                                                ('started_attempt', 1): 's_1',
                                                                ('started_attempt', 2): 's_2', ('wrong', 1): 'w_1',
                                                                ('wrong', 2): 'w_2', ('passed', 1): 'p_1',
                                                                ('passed', 2): 'p_2', ('correct', 1): 'c_1',
                                                                ('correct', 2): 'c_2'})
    return users_metrics_n_days


def users_metrics_by_days(events, users_metrics_n_days):
    sec_in_day = 24 * 60 * 60
    events['day_counter'] = (events.timestamp - events.first_timestamp) / sec_in_day
    events.day_counter = events.day_counter.apply(lambda x: ceil(x))
    events.day_counter = events.day_counter.replace(0, 1)
    users_metrics_by_days = events.pivot_table(index='user_id', columns=['action', 'day_counter'], values='step_id',
                                               aggfunc='count', fill_value=0).reset_index()
    users_metrics_n_days = users_metrics_n_days.merge(users_metrics_by_days, on='user_id', how='outer').fillna(0)
    users_metrics_n_days = users_metrics_n_days.set_index('user_id')
    users_metrics_n_days = rename_columns(users_metrics_n_days)
    return users_metrics_n_days


def day_metrics_ratio(users_metrics_n_days):
    users_metrics_n_days['d_ratio'] = (users_metrics_n_days.d_1 / users_metrics_n_days.d_2).fillna(-1)
    users_metrics_n_days['v_ratio'] = (users_metrics_n_days.v_1 / users_metrics_n_days.v_2).fillna(-1)
    users_metrics_n_days['s_ratio'] = (users_metrics_n_days.s_1 / users_metrics_n_days.s_2).fillna(-1)
    users_metrics_n_days['w_ratio'] = (users_metrics_n_days.w_1 / users_metrics_n_days.w_2).fillna(-1)
    users_metrics_n_days['p_ratio'] = (users_metrics_n_days.p_1 / users_metrics_n_days.p_2).fillna(-1)
    users_metrics_n_days['c_ratio'] = (users_metrics_n_days.c_1 / users_metrics_n_days.c_2).fillna(-1)
    users_metrics_n_days.replace([np.inf, -np.inf], -1, inplace=True)
    return users_metrics_n_days


def agg_events(users_metrics_n_days):
    users_metrics_n_days['agg'] = users_metrics_n_days.discovered + users_metrics_n_days.viewed +\
                                  users_metrics_n_days.started_attempt + users_metrics_n_days.wrong + \
                                  users_metrics_n_days.passed + users_metrics_n_days.correct + \
                                  users_metrics_n_days.course_complete + users_metrics_n_days.d_1 + \
                                  users_metrics_n_days.d_2 + users_metrics_n_days.v_1 + users_metrics_n_days.v_2 + \
                                  users_metrics_n_days.s_1 + users_metrics_n_days.s_2 + users_metrics_n_days.w_1 + \
                                  users_metrics_n_days.w_2 + users_metrics_n_days.p_1 + users_metrics_n_days.p_2 + \
                                  users_metrics_n_days.c_1 + users_metrics_n_days.c_2
    return users_metrics_n_days


def correct_wrong_ratio(users_metrics_n_days):
    users_metrics_n_days['cw_ratio'] = (users_metrics_n_days.correct / users_metrics_n_days.wrong).fillna(0)
    users_metrics_n_days.replace([np.inf, -np.inf], -1, inplace=True)
    return users_metrics_n_days


def start_passed_ratio(users_metrics_n_days):
    users_metrics_n_days['sp_ratio'] = (users_metrics_n_days.started_attempt / users_metrics_n_days.passed).fillna(0)
    users_metrics_n_days.replace([np.inf, -np.inf], -1, inplace=True)
    return users_metrics_n_days


def features_generator(events, submissions):
    events = pr.first_timestamp(events)
    submissions = pr.first_timestamp(submissions)
    users_events = pr.event_aggregation(events, submissions)
    users_events = pr.time_preparation(users_events)
    users_course_complete = pr.course_complete(users_events, conf.ESTIMATION_PARAM, conf.ESTIMATION_VALUE)
    events, users_metrics_n_days = pr.metrics_n_days(users_events, users_course_complete, conf.DAY_THRESHOLD)
    users_metrics_n_days = users_metrics_by_days(events, users_metrics_n_days)
    # users_metrics_n_days = day_metrics_ratio(users_metrics_n_days)
    # users_metrics_n_days = agg_events(users_metrics_n_days)
    # users_metrics_n_days = correct_wrong_ratio(users_metrics_n_days)
    # users_metrics_n_days = start_passed_ratio(users_metrics_n_days)
    return users_metrics_n_days
