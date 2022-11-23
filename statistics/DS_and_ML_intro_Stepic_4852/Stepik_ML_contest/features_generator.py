import data_preparation as pr
import config as conf
from math import ceil


def users_metrics_by_days(events, users_metrics_n_days):
    sec_in_day = 24 * 60 * 60
    events['day_counter'] = (events.timestamp - events.first_timestamp) / sec_in_day
    events.day_counter = events.day_counter.apply(lambda x: ceil(x))
    events.day_counter = events.day_counter.replace(0, 1)
    users_metrics_by_days = events.pivot_table(index='user_id', columns=['action', 'day_counter'], values='step_id',
                                               aggfunc='count', fill_value=0).reset_index()
    users_metrics_n_days = users_metrics_n_days.merge(users_metrics_by_days, on='user_id', how='outer').fillna(0)
    users_metrics_n_days = users_metrics_n_days.set_index('user_id')
    return users_metrics_n_days


def features_generator(events, submissions):
    events = pr.first_timestamp(events)
    submissions = pr.first_timestamp(submissions)
    users_events = pr.event_aggregation(events, submissions)
    users_events = pr.time_preparation(users_events)
    users_course_complete = pr.course_complete(users_events, conf.ESTIMATION_PARAM, conf.ESTIMATION_VALUE)
    events, users_metrics_n_days = pr.metrics_n_days(users_events, users_course_complete, conf.DAY_THRESHOLD)
    users_metrics_n_days = users_metrics_by_days(events, users_metrics_n_days)
    return users_metrics_n_days
