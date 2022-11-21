import pandas as pd
import numpy as np


def event_aggregation(events, submissions):
    user_events = pd.concat([events, submissions.rename(columns={'submissions_status': 'action'})])
    return user_events


def data_preparation(events, submissions):
    user_events = event_aggregation(events, submissions)
    return user_events
