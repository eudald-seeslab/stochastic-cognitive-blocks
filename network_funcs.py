import numpy as np


def assign_group(x):
    if x.Good >= x.Bad:
        return "Good" if x.Good >= x.Average else "Average"
    return "Bad" if x.Bad >= x.Average else "Average"


def assign_group2(x):
    if x.High >= x.Low:
        return "High" if x.High >= x.Average else "Average"
    return "Low" if x.Low >= x.Average else "Average"

def create_question_df(df, question):
    df = df.loc[df.question == question, ["period", "student", "value"]].drop_duplicates()
    df = df.dropna()
    df["value"] = df["value"].astype(int)
    return df

def add_relation_column(df, question_df, question_name):
    temp = df.merge(
        question_df,
        left_on=["student_id", "id"],
        right_on=["student", "value"],
        how="left"
    ).drop(columns=["student", "value"])
    temp[question_name] = np.where(temp["period"].isna(), 0, 1)
    return temp.drop(columns=["period"])
