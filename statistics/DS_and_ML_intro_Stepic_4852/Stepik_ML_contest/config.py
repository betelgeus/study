import pandas as pd


TRAIN_EVENTS = pd.read_csv('https://stepik.org/media/attachments/course/4852/event_data_train.zip')
TRAIN_SUBMISSIONS = pd.read_csv('https://stepik.org/media/attachments/course/4852/submissions_data_train.zip')
TEST_EVENTS = pd.read_csv('https://stepik.org/media/attachments/course/4852/events_data_test.csv')
TEST_SUBMISSIONS = pd.read_csv('https://stepik.org/media/attachments/course/4852/submission_data_test.csv')

DAY_THRESHOLD = 2
# correct, passed
ESTIMATION_PARAM = 'correct'
ESTIMATION_VALUE = 40
