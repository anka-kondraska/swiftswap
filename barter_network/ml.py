import pandas as pd    # data formatting
import numpy as np     # numeric library
from sklearn.neighbors import KNeighborsClassifier  # machine learning
import random

# DB TO DF FOR EACH TABLE
users_df = pd.read_sql_table('users', con='postgresql:///barternet',columns=["user_id","user_fname", "user_lname", "user_street_address","user_city","user_state","user_zipcode","user_dob","user_occupation","user_occupation_id","user_email","user_password","user_lat","user_lng"])

skills_df = pd.read_sql_table('skills', con='postgresql:///barternet',columns=["skill_id","skill_name","skill_value"])

userskills_df = pd.read_sql_table('userskills', con='postgresql:///barternet',columns=["user_id", "skill_id", "skill_direction","direction_id"])

# MERGING USERS_DF AND USERSKILLS_DF ON USER_ID
datauser = pd.merge(users_df, userskills_df, on='user_id',how='right')

# MERGING DATAUSER AND SKILLS_DF ON SKILL_ID
data = pd.merge(datauser, skills_df, on='skill_id', how="outer")

# LOCATING LAST TWO NAN ROWS AND DROPPING THEM IN PLACE
# print "BEFORE DROPNA",data.iloc[195:210]
# data.drop(data.index[[200]], inplace=True)

print data.dropna(axis=0,inplace=True)
# print "AFTER DROPNA",data.iloc[195:210]

# data["job_id"] = pd.factorize(data.user_occupation, sort=True)[0]

# to-1, from-0
# data["direction_id"] = pd.factorize(data.skill_direction, sort=True)[0] 

# BASED ON JOB PREDICT SKILL
df = data[["skill_id","user_occupation_id","direction_id"]] # to-1, from-0

print df.sort_values(["user_occupation_id"], axis=0,ascending=False)

data_to=df.loc[df['direction_id'] == 1]
data_from=df.loc[df['direction_id'] == 0]


job = data[["user_occupation","user_occupation_id"]]
skill = data[["skill_name","skill_id"]]

# job[job['job_id']==48]
# skill[skill['skill_id']==48]

# TEST DATA FROM/SKILL OFFERED - BASED ON JOB PREDICT SKILL OFFERED
rows_from = random.sample(data_from.index, 100)
train_small_from = data_from.ix[rows_from[:80]]
validation_small_from = data_from.ix[rows_from[20:]]

# TRAINING AND FITTING FROM SKILL OFFERED
knn_from = KNeighborsClassifier(n_neighbors=1)
knn_from.fit(train_small_from.iloc[:,1:], train_small_from.iloc[:,0]) #data labels
predictions_from = knn_from.predict(validation_small_from.iloc[:,1:])
validation_labels_from = validation_small_from.iloc[:,0].values

print predictions_from[:20]
print validation_labels_from[:20]

# for i in predictions_from[:2]:
#     print skill[skill['skill_id'] == i]
# for i in validation_labels_from[:2]:
#     print skill[skill['skill_id'] == i]

accuracy_from = sum(predictions_from == validation_labels_from)/float(len(predictions_from))
print accuracy_from

wrong_from = np.where(predictions_from != validation_labels_from)

for i in wrong_from:
    print "predicted: ", predictions_from[i], "answer: ", validation_labels_from[i]

# TEST DATA FROM/SKILL OFFERED - BASED ON JOB PREDICT SKILL OFFERED
rows_to = random.sample(data_to.index, 100)
train_small_to = data_to.ix[rows_to[:80]]
validation_small_to = data_to.ix[rows_to[20:]]

# TRAINING AND FITTING FROM SKILL OFFERED
knn_to = KNeighborsClassifier(n_neighbors=1)
knn_to.fit(train_small_to.iloc[:,1:], train_small_to.iloc[:,0]) #data labels
predictions_to = knn_to.predict(validation_small_to.iloc[:,1:])
validation_labels_to = validation_small_to.iloc[:,0].values

accuracy_to = sum(predictions_to == validation_labels_to)/float(len(predictions_to))
print accuracy_to

wrong_to = np.where(predictions_to != validation_labels_to)
print wrong_to

for i in wrong_to:
    print "predicted: ", predictions_to[i], "answer: ", validation_labels_to[i]

def predict(user_occupation_id):
    # if user_occupation_id
    # if job[job['job_id'] == user_occupation_id]:
    user_prediction_to = knn_to.predict([user_occupation_id[0],1])
    user_prediction_from = knn_from.predict([user_occupation_id[0],0])


    # predict with K nearst neighbour skill wanted, skill offered
    return user_prediction_to,user_prediction_from

# cm = confusion_matrix(validation_labels_to, predictions_to)
# pyplot.matshow(cm)
# pyplot.title('Confusion matrix')
# pyplot.colorbar()
# pyplot.ylabel('True label')
# pyplot.xlabel('Predicted label')
# pyplot.show()

# np.fill_diagonal(cm, 0)
# pyplot.matshow(cm)
# pyplot.title('Confusion matrix')
# pyplot.colorbar()
# pyplot.ylabel('True label')
# pyplot.xlabel('Predicted label')
# pyplot.show()


