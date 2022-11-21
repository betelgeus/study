import pandas as pd
import config as conf

# DATA PREPARATION
train_events = conf.TRAIN_EVENTS
train_submissions = conf.TRAIN_SUBMISSIONS
test_events = conf.TEST_EVENTS
test_submissions = conf.TEST_SUBMISSIONS


def event_aggregation(events, submissions):
    user_events = pd.concat([events, submissions.rename(columns={'submission_status': 'action'})])
    return user_events


def data_preparation(events, submissions):
    user_events = event_aggregation(events, submissions)
    return user_events


train_data = data_preparation(train_events, train_submissions)
print(train_data.head())