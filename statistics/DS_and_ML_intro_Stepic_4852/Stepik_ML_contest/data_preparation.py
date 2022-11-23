import pandas as pd
import config as conf
from math import ceil

pd.options.mode.chained_assignment = None


def first_timestamp(events):
    users_first_timestamp = events.groupby('user_id').aggregate({'timestamp': 'min'}) \
        .reset_index().rename(columns={'timestamp': 'first_timestamp'})
    events = events.merge(users_first_timestamp, on='user_id', how='outer')
    return events


def event_aggregation(events, submissions):
    user_events = pd.concat([events, submissions.rename(columns={'submission_status': 'action'})])
    user_events.action = pd.Categorical(user_events.action,
                                        ['discovered', 'viewed', 'started_attempt', 'wrong', 'passed', 'correct'],
                                        ordered=True)
    user_events = user_events.sort_values(['user_id', 'timestamp', 'action'])
    return user_events


def time_preparation(events):
    events['date'] = pd.to_datetime(events.timestamp, unit='s')
    events['day'] = events.date.dt.date
    return events


def drop_duplicates(events):
    events = events[~events.duplicated(['step_id', 'action', 'user_id']) | (events['action'] == 'correct')]
    return events


def course_complete(events, estimation_param, estimation_value):
    users_course_complete = events.pivot_table(index='user_id', columns='action', values='step_id', aggfunc='count',
                                               fill_value=0).reset_index()
    users_course_complete['course_complete'] = users_course_complete[estimation_param] > estimation_value
    users_course_complete = users_course_complete[['user_id', 'course_complete']]
    return users_course_complete


def metrics_n_days(events, users_course_complete, day_threshold):
    time_threshold = day_threshold * 24 * 60 * 60
    events['first_n_days'] = events.timestamp <= events.first_timestamp + time_threshold
    events_first_n_days = events[events.first_n_days == True]
    users_metrics_n_days = events_first_n_days.pivot_table(index='user_id', columns='action', values='step_id',
                                                           aggfunc='count', fill_value=0).reset_index()
    users_metrics_n_days = users_metrics_n_days.merge(users_course_complete, on='user_id', how='outer').fillna(0)
    users_metrics_n_days = users_metrics_n_days.set_index('user_id')
    return events_first_n_days, users_metrics_n_days


def data_preparation(events, submissions):
    events = first_timestamp(events)
    submissions = first_timestamp(submissions)
    users_events = event_aggregation(events, submissions)
    users_events = time_preparation(users_events)
    # users_events = drop_duplicates(users_events)
    users_course_complete = course_complete(users_events, conf.ESTIMATION_PARAM, conf.ESTIMATION_VALUE)
    _, users_metrics_n_days = metrics_n_days(users_events, users_course_complete, conf.DAY_THRESHOLD)
    return users_metrics_n_days
