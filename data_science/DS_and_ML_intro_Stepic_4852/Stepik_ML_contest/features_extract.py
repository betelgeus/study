from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()


def features_extract(users_data, drop_cols=['course_complete']):
    X = users_data.drop(drop_cols, axis=1)
    scaler.fit(X)
    X = scaler.transform(X)
    y = users_data['course_complete']
    return X, y
