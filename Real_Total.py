import pandas as pd
import numpy as np
from collections import Counter
import random
from sklearn.metrics import roc_auc_score

def confu (conf) :
    accuracy = (conf[0][0] + conf[1][1]) / (conf[0][0] + conf[1][0] + conf[0][1] + conf[1][1])
    precision = (conf[1][1] ) / (conf[1][1] + conf[0][1] )
    recall = (conf[1][1]) / (conf[1][0]  + conf[1][1])
    f1 = 2*(1/(1/recall + 1/precision))
    print(conf)
    print('accuracy = {:.3f}'.format( accuracy))
    print('precision = {:.3f}'.format(precision))
    print('recall = {:.3f}'.format(recall))
    print('f1-score = {:.3f}'.format(f1))
    return 


df_15 = pd.read_csv("C:/Users/빈운기/Downloads/archive/pl_15-16.csv", encoding='cp949')
df_16 = pd.read_csv("C:/Users/빈운기/Downloads/archive/pl_16-17.csv", encoding='cp949')
df_17 = pd.read_csv("C:/Users/빈운기/Downloads/archive/pl_17-18.csv", encoding='cp949')
df_18 = pd.read_csv("C:/Users/빈운기/Downloads/archive/pl_18-19.csv", encoding='cp949')
df_19 = pd.read_csv("C:/Users/빈운기/Downloads/archive/pl_19-20.csv", encoding='cp949')
df_20 = pd.read_csv("C:/Users/빈운기/Downloads/archive/pl_20-21.csv", encoding='cp949')




df_15 = df_15.iloc[:,2:(len(df_15.columns))]
df_16 = df_16.iloc[:,2:(len(df_16.columns))]
df_17 = df_17.iloc[:,2:(len(df_17.columns))]
df_18 = df_18.iloc[:,2:(len(df_18.columns))]
df_19 = df_19.iloc[:,2:(len(df_19.columns))]
df_20 = df_20.iloc[:,2:(len(df_20.columns))]


df_15.fillna(0, inplace = True)
df_16.fillna(0, inplace = True)
df_17.fillna(0, inplace = True)
df_18.fillna(0, inplace = True)
df_19.fillna(0, inplace = True)
df_20.fillna(0, inplace = True)

X_15 = df_15.drop(['MVP'], axis=1)
X_16 = df_16.drop(['MVP'], axis=1)
X_17 = df_17.drop(['MVP'], axis=1)
X_18 = df_18.drop(['MVP'], axis=1)
X_19 = df_19.drop(['MVP'], axis=1)
X_20 = df_20.drop(['MVP'], axis=1)



X_15 = pd.get_dummies(X_15)
X_16 = pd.get_dummies(X_16)
X_17 = pd.get_dummies(X_17)
X_18 = pd.get_dummies(X_18)
X_19 = pd.get_dummies(X_19)
X_20 = pd.get_dummies(X_20)




y_15 = df_15['MVP']
y_16 = df_16['MVP']
y_17 = df_17['MVP']
y_18 = df_18['MVP']
y_19 = df_19['MVP']
y_20 = df_20['MVP']


y = pd.concat([y_15, y_16, y_17, y_18, y_19, y_20 ], ignore_index=True)

from sklearn.preprocessing import MinMaxScaler
MMscaler = MinMaxScaler()
X_15M = MMscaler.fit_transform(X_15)
X_16M = MMscaler.fit_transform(X_16)
X_17M = MMscaler.fit_transform(X_17)
X_18M = MMscaler.fit_transform(X_18)
X_19M = MMscaler.fit_transform(X_19)
X_20M = MMscaler.fit_transform(X_20)

X_15M = pd.DataFrame(X_15M)
X_16M = pd.DataFrame(X_16M)
X_17M = pd.DataFrame(X_17M)
X_18M = pd.DataFrame(X_18M)
X_19M = pd.DataFrame(X_19M)
X_20M = pd.DataFrame(X_20M)



X = pd.concat([X_15M, X_16M, X_17M, X_18M, X_19M, X_20M], ignore_index=True)





#li = list(range(2,(len(df.columns)-1)))

#df[['Goals']].hist()
#df[['Goals conceded']].hist()
#df[['Assists']].hist()
#df[['Passes']].hist()



X.columns = X_15.columns




from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X,  y, test_size=0.3, random_state=1, stratify = y)

print(Counter(y))








Log_reg_penalty = ['l1', 'l2', 'elasticnet', 'none']
Log_reg_solver = ['saga', 'lbfgs', 'saga', 'lbfgs']
Log_reg_c = [100, 10 , 1, 0.1 , 0.01]
Log_reg_l1_ratio = ['none','none',0.5,'none']



Log_conf_train_acc = np.zeros((len(Log_reg_penalty), len(Log_reg_c)))
Log_conf_train_pre = np.zeros((len(Log_reg_penalty), len(Log_reg_c)))
Log_conf_train_rec = np.zeros((len(Log_reg_penalty), len(Log_reg_c)))
Log_conf_train_f1 = np.zeros((len(Log_reg_penalty), len(Log_reg_c)))
Log_conf_train_AUC = np.zeros((len(Log_reg_penalty), len(Log_reg_c)))


Log_conf_test_acc = np.zeros((len(Log_reg_penalty), len(Log_reg_c)))
Log_conf_test_pre = np.zeros((len(Log_reg_penalty), len(Log_reg_c)))
Log_conf_test_rec = np.zeros((len(Log_reg_penalty), len(Log_reg_c)))
Log_conf_test_f1 = np.zeros((len(Log_reg_penalty), len(Log_reg_c)))
Log_conf_test_AUC = np.zeros((len(Log_reg_penalty), len(Log_reg_c)))   


from sklearn.linear_model import LogisticRegression

for i in range(len(Log_reg_penalty)) : 
    for j in range(len(Log_reg_c)) :

        Log_reg = LogisticRegression(penalty= Log_reg_penalty[i], random_state=1, C = Log_reg_c[j], solver = Log_reg_solver[i], l1_ratio = Log_reg_l1_ratio[i])
        Log_reg.fit(X_train, y_train)
        conf_train_Log = confusion_matrix(y_train,Log_reg.predict(X_train))
        conf_test_Log = confusion_matrix(y_test,Log_reg.predict(X_test))
        
        accuracy_train = (conf_train_Log[0][0] + conf_train_Log[1][1]) / (conf_train_Log[0][0] + conf_train_Log[1][0] + conf_train_Log[0][1] + conf_train_Log[1][1])
        precision_train = (conf_train_Log[1][1] ) / (conf_train_Log[1][1] + conf_train_Log[0][1] )
        recall_train = (conf_train_Log[1][1]) / (conf_train_Log[1][0]  + conf_train_Log[1][1])
        
        Log_conf_train_acc[i][j] = accuracy_train
        Log_conf_train_pre[i][j] = precision_train
        Log_conf_train_rec[i][j] = recall_train                                 
        Log_conf_train_f1[i][j] = 2/(1/Log_conf_train_pre[i][j]+1/Log_conf_train_rec[i][j])
        Log_conf_train_AUC[i][j] = round(roc_auc_score(y_train, Log_reg.predict(X_train)),2)
        
        accuracy_test = (conf_test_Log[0][0] + conf_test_Log[1][1]) / (conf_test_Log[0][0] + conf_test_Log[1][0] + conf_test_Log[0][1] + conf_test_Log[1][1])
        precision_test = (conf_test_Log[1][1] ) / (conf_test_Log[1][1] + conf_test_Log[0][1] )
        recall_test = (conf_test_Log[1][1]) / (conf_test_Log[1][0]  + conf_test_Log[1][1])
        
        Log_conf_test_acc[i][j] = accuracy_test
        Log_conf_test_pre[i][j] = precision_test
        Log_conf_test_rec[i][j] = recall_test  
        Log_conf_test_f1[i][j] = 2/(1/Log_conf_test_pre[i][j]+1/Log_conf_test_rec[i][j])
        Log_conf_test_AUC[i][j] = round(roc_auc_score(y_test, Log_reg.predict(X_test)),2)
        
        
        print('')
        print('confusion_matrix_Log_train')
        print('penalty = ', Log_reg_penalty[i] )
        print('C = ',  Log_reg_c[j])
        confu(conf_train_Log)
        print('ROC AUC = ',round(roc_auc_score(y_train,Log_reg.predict(X_train)),2))
        print('')
        
        print('')
        print('confusion_matrix_Log_test')
        print('penalty = ', Log_reg_penalty[i] )
        print('C = ',  Log_reg_c[j])
        confu(conf_test_Log)
        print('ROC AUC = ',round(roc_auc_score(y_test,Log_reg.predict(X_test)),2))
        print('')
    

Log_conf_train_acc = pd.DataFrame(Log_conf_train_acc)
Log_conf_train_acc.columns = Log_reg_c
Log_conf_train_acc.index = Log_reg_penalty

Log_conf_train_pre = pd.DataFrame(Log_conf_train_pre)
Log_conf_train_pre.columns = Log_reg_c
Log_conf_train_pre.index = Log_reg_penalty

Log_conf_train_rec= pd.DataFrame(Log_conf_train_rec)
Log_conf_train_rec.columns = Log_reg_c
Log_conf_train_rec.index = Log_reg_penalty

Log_conf_train_f1= pd.DataFrame(Log_conf_train_f1)
Log_conf_train_f1.columns = Log_reg_c
Log_conf_train_f1.index = Log_reg_penalty



Log_conf_test_acc= pd.DataFrame(Log_conf_test_acc)
Log_conf_test_acc.columns = Log_reg_c
Log_conf_test_acc.index = Log_reg_penalty

Log_conf_test_pre = pd.DataFrame(Log_conf_test_pre)
Log_conf_test_pre.columns = Log_reg_c
Log_conf_test_pre.index = Log_reg_penalty

Log_conf_test_rec = pd.DataFrame(Log_conf_test_rec)
Log_conf_test_rec.columns = Log_reg_c
Log_conf_test_rec.index = Log_reg_penalty

Log_conf_test_f1 = pd.DataFrame(Log_conf_test_f1)
Log_conf_test_f1.columns = Log_reg_c
Log_conf_test_f1.index = Log_reg_penalty



Log_conf_train_AUC= pd.DataFrame(Log_conf_train_AUC)
Log_conf_train_AUC.columns = Log_reg_c
Log_conf_train_AUC.index = Log_reg_penalty


Log_conf_test_AUC = pd.DataFrame(Log_conf_test_AUC)
Log_conf_test_AUC.columns = Log_reg_c
Log_conf_test_AUC.index = Log_reg_penalty


























































knn_n_neighbors = [3,5,7,9]
knn_p = [2,3,5,7,9]


knn_conf_train_acc = np.zeros((len(knn_n_neighbors), len(knn_p)))
knn_conf_train_pre = np.zeros((len(knn_n_neighbors), len(knn_p)))
knn_conf_train_rec = np.zeros((len(knn_n_neighbors), len(knn_p)))
knn_conf_train_f1 = np.zeros((len(knn_n_neighbors), len(knn_p)))
knn_conf_train_AUC = np.zeros((len(knn_n_neighbors), len(knn_p)))

knn_conf_test_acc = np.zeros((len(knn_n_neighbors), len(knn_p)))
knn_conf_test_pre = np.zeros((len(knn_n_neighbors), len(knn_p)))
knn_conf_test_rec = np.zeros((len(knn_n_neighbors), len(knn_p)))
knn_conf_test_f1 = np.zeros((len(knn_n_neighbors), len(knn_p)))
knn_conf_test_AUC = np.zeros((len(knn_n_neighbors), len(knn_p)) )   

from sklearn.neighbors import KNeighborsClassifier


for i in range(len(knn_n_neighbors)) : 
    for j in range(len(knn_p)) :
        knn = KNeighborsClassifier(n_neighbors = knn_n_neighbors[i], p = knn_p[j])   # n_neighbors = 3 , 5 , 7  p = 5 ~ 10
        knn.fit(X_train, y_train)
        conf_train_knn = confusion_matrix(y_train, knn.predict(X_train))
        conf_test_knn = confusion_matrix(y_test, knn.predict(X_test))
        
        accuracy_train = (conf_train_knn[0][0] + conf_train_knn[1][1]) / (conf_train_knn[0][0] + conf_train_knn[1][0] + conf_train_knn[0][1] + conf_train_knn[1][1])
        precision_train = (conf_train_knn[1][1] ) / (conf_train_knn[1][1] + conf_train_knn[0][1] )
        recall_train = (conf_train_knn[1][1]) / (conf_train_knn[1][0]  + conf_train_knn[1][1])
        
        knn_conf_train_acc[i][j] = accuracy_train
        knn_conf_train_pre[i][j] = precision_train
        knn_conf_train_rec[i][j] = recall_train                                 
        knn_conf_train_f1[i][j] = 2/(1/knn_conf_train_pre[i][j]+1/knn_conf_train_rec[i][j])
        knn_conf_train_AUC[i][j] = round(roc_auc_score(y_train, knn.predict(X_train)),2)
        
        accuracy_test = (conf_test_knn[0][0] + conf_test_knn[1][1]) / (conf_test_knn[0][0] + conf_test_knn[1][0] + conf_test_knn[0][1] + conf_test_knn[1][1])
        precision_test = (conf_test_knn[1][1] ) / (conf_test_knn[1][1] + conf_test_knn[0][1] )
        recall_test = (conf_test_knn[1][1]) / (conf_test_knn[1][0]  + conf_test_knn[1][1])
        
        knn_conf_test_acc[i][j] = accuracy_test
        knn_conf_test_pre[i][j] = precision_test
        knn_conf_test_rec[i][j] = recall_test  
        knn_conf_test_f1[i][j] = 2/(1/knn_conf_test_pre[i][j]+1/knn_conf_test_rec[i][j])
        knn_conf_test_AUC[i][j] = round(roc_auc_score(y_test, knn.predict(X_test)),2)
        
        print('')
        print('confusion_matrix_KNN_train')
        print('n_neighbors = ', knn_n_neighbors[i] )
        print('p = ', knn_p[j] )
        confu(conf_train_knn)
        print('ROC AUC = ', round(roc_auc_score(y_train, knn.predict(X_train)),2))
        print('')
        
        print('')
        print('confusion_matrix_KNN_test')
        print('n_neighbors = ', knn_n_neighbors[i] )
        print('p = ', knn_p[j] )
        confu(conf_test_knn)
        print('ROC AUC = ', round(roc_auc_score(y_test, knn.predict(X_test)),2))
        print('')

knn_conf_train_acc = pd.DataFrame(knn_conf_train_acc)
knn_conf_train_acc.columns = knn_p
knn_conf_train_acc.index = knn_n_neighbors

knn_conf_train_pre = pd.DataFrame(knn_conf_train_pre)
knn_conf_train_pre.columns = knn_p
knn_conf_train_pre.index = knn_n_neighbors

knn_conf_train_rec= pd.DataFrame(knn_conf_train_rec)
knn_conf_train_rec.columns = knn_p
knn_conf_train_rec.index = knn_n_neighbors

knn_conf_test_acc= pd.DataFrame(knn_conf_test_acc)
knn_conf_test_acc.columns = knn_p
knn_conf_test_acc.index = knn_n_neighbors

knn_conf_test_pre = pd.DataFrame(knn_conf_test_pre)
knn_conf_test_pre.columns = knn_p
knn_conf_test_pre.index = knn_n_neighbors

knn_conf_test_rec = pd.DataFrame(knn_conf_test_rec)
knn_conf_test_rec.columns = knn_p
knn_conf_test_rec.index = knn_n_neighbors

knn_conf_train_f1= pd.DataFrame(knn_conf_train_f1)
knn_conf_train_f1.columns = knn_p
knn_conf_train_f1.index = knn_n_neighbors


knn_conf_test_f1 = pd.DataFrame(knn_conf_test_f1)
knn_conf_test_f1.columns = knn_p
knn_conf_test_f1.index = knn_n_neighbors



knn_conf_train_AUC= pd.DataFrame(knn_conf_train_AUC)
knn_conf_train_AUC.columns = knn_p
knn_conf_train_AUC.index = knn_n_neighbors


knn_conf_test_AUC = pd.DataFrame(knn_conf_test_AUC)
knn_conf_test_AUC.columns = knn_p
knn_conf_test_AUC.index = knn_n_neighbors






































svm_kernel = ['linear', 'rbf', 'poly', 'sigmoid']
svm_c = [100, 10 , 1, 0.1 , 0.01]


svm_conf_train_acc = np.zeros((len(svm_kernel), len(svm_c)))
svm_conf_train_pre = np.zeros((len(svm_kernel), len(svm_c)))
svm_conf_train_rec = np.zeros((len(svm_kernel), len(svm_c)))
svm_conf_train_f1 = np.zeros((len(svm_kernel), len(svm_c)))
svm_conf_train_AUC = np.zeros((len(svm_kernel), len(svm_c)))

svm_conf_test_acc = np.zeros((len(svm_kernel), len(svm_c)))
svm_conf_test_pre = np.zeros((len(svm_kernel), len(svm_c)))
svm_conf_test_rec = np.zeros((len(svm_kernel), len(svm_c)))
svm_conf_test_f1 = np.zeros((len(svm_kernel), len(svm_c)))
svm_conf_test_AUC = np.zeros((len(svm_kernel), len(svm_c)))     



from  sklearn.svm import SVC
for i in  range(len(svm_kernel)) :
    for j in range(len(svm_c)) :
        svm = SVC(kernel = svm_kernel[i], C = svm_c[j], random_state=1)  # kernel : linear, rbf, poly, sigmoid  ,  C  = 0.1 ~ 10 
        svm.fit(X_train, y_train)
        conf_train_svm = confusion_matrix(y_train, svm.predict(X_train))
        conf_test_svm = confusion_matrix(y_test, svm.predict(X_test))
        
        accuracy_train = (conf_train_svm[0][0] + conf_train_svm[1][1]) / (conf_train_svm[0][0] + conf_train_svm[1][0] + conf_train_svm[0][1] + conf_train_svm[1][1])
        precision_train = (conf_train_svm[1][1] ) / (conf_train_svm[1][1] + conf_train_svm[0][1] )
        recall_train = (conf_train_svm[1][1]) / (conf_train_svm[1][0]  + conf_train_svm[1][1])
       
        svm_conf_train_acc[i][j] = accuracy_train
        svm_conf_train_pre[i][j] = precision_train
        svm_conf_train_rec[i][j] = recall_train                                 
        svm_conf_train_f1[i][j] = 2/(1/svm_conf_train_pre[i][j]+1/svm_conf_train_rec[i][j])
        svm_conf_train_AUC[i][j] = round(roc_auc_score(y_train, svm.predict(X_train)),2)
        
        accuracy_test = (conf_test_svm[0][0] + conf_test_svm[1][1]) / (conf_test_svm[0][0] + conf_test_svm[1][0] + conf_test_svm[0][1] + conf_test_svm[1][1])
        precision_test = (conf_test_svm[1][1] ) / (conf_test_svm[1][1] + conf_test_svm[0][1] )
        recall_test = (conf_test_svm[1][1]) / (conf_test_svm[1][0]  + conf_test_svm[1][1])
       
        svm_conf_test_acc[i][j] = accuracy_test
        svm_conf_test_pre[i][j] = precision_test
        svm_conf_test_rec[i][j] = recall_test  
        svm_conf_test_f1[i][j] = 2/(1/svm_conf_test_pre[i][j]+1/svm_conf_test_rec[i][j])
        svm_conf_test_AUC[i][j] = round(roc_auc_score(y_test, svm.predict(X_test)),2)
        
        
        print('')
        print('confusion_matrix_SVM_train')
        print('kernel = ', svm_kernel[i] )
        print('C = ', svm_c[j] )
        confu(conf_train_svm)
        print('ROC AUC = ', round(roc_auc_score(y_train, svm.predict(X_train)),2))
        print('')
        
        print('')
        print('confusion_matrix_SVM_test')
        print('kernel = ', svm_kernel[i] )
        print('C = ', svm_c[j] )
        confu(conf_test_svm)
        print('ROC AUC = ', round(roc_auc_score(y_test, svm.predict(X_test)),2))
        print('')











svm_conf_train_acc = pd.DataFrame(svm_conf_train_acc)
svm_conf_train_acc.columns = svm_c
svm_conf_train_acc.index = svm_kernel

svm_conf_train_pre = pd.DataFrame(svm_conf_train_pre)
svm_conf_train_pre.columns = svm_c
svm_conf_train_pre.index = svm_kernel

svm_conf_train_rec= pd.DataFrame(svm_conf_train_rec)
svm_conf_train_rec.columns = svm_c
svm_conf_train_rec.index = svm_kernel

svm_conf_test_acc= pd.DataFrame(svm_conf_test_acc)
svm_conf_test_acc.columns = svm_c
svm_conf_test_acc.index = svm_kernel

svm_conf_test_pre = pd.DataFrame(svm_conf_test_pre)
svm_conf_test_pre.columns = svm_c
svm_conf_test_pre.index = svm_kernel

svm_conf_test_rec = pd.DataFrame(svm_conf_test_rec)
svm_conf_test_rec.columns = svm_c
svm_conf_test_rec.index = svm_kernel

svm_conf_train_f1= pd.DataFrame(svm_conf_train_f1)
svm_conf_train_f1.columns = svm_c
svm_conf_train_f1.index = svm_kernel


svm_conf_test_f1 = pd.DataFrame(svm_conf_test_f1)
svm_conf_test_f1.columns = svm_c
svm_conf_test_f1.index = svm_kernel



svm_conf_train_AUC= pd.DataFrame(svm_conf_train_AUC)
svm_conf_train_AUC.columns = svm_c
svm_conf_train_AUC.index = svm_kernel


svm_conf_test_AUC = pd.DataFrame(svm_conf_test_AUC)
svm_conf_test_AUC.columns = svm_c
svm_conf_test_AUC.index = svm_kernel
































dtc_criterion = ['gini', 'entropy']
dtc_md = [3,4,5,6,7,8,9,10]


dtc_conf_train_acc = np.zeros((len(dtc_criterion), len(dtc_md)))
dtc_conf_train_pre = np.zeros((len(dtc_criterion), len(dtc_md)))
dtc_conf_train_rec = np.zeros((len(dtc_criterion), len(dtc_md)))
dtc_conf_train_f1 = np.zeros((len(dtc_criterion), len(dtc_md)))
dtc_conf_train_AUC = np.zeros((len(dtc_criterion), len(dtc_md)))

dtc_conf_test_acc = np.zeros((len(dtc_criterion), len(dtc_md)))
dtc_conf_test_pre = np.zeros((len(dtc_criterion), len(dtc_md)))
dtc_conf_test_rec = np.zeros((len(dtc_criterion), len(dtc_md)))
dtc_conf_test_f1 = np.zeros((len(dtc_criterion), len(dtc_md)))
dtc_conf_test_AUC = np.zeros((len(dtc_criterion), len(dtc_md)))                        

from sklearn import tree


for i in range(len(dtc_criterion)) :
    for j in range(len(dtc_md)) :
        dtc = tree.DecisionTreeClassifier(criterion = dtc_criterion[i], max_depth = dtc_md[j], random_state = 1)   # criterion = gini, entropy , max_depth = 3 ~ 10 정도?
        dtc.fit(X_train, y_train)
        conf_train_dtc = confusion_matrix(y_train, dtc.predict(X_train))
        conf_test_dtc = confusion_matrix(y_test, dtc.predict(X_test))
        
        
        accuracy_train = (conf_train_dtc[0][0] + conf_train_dtc[1][1]) / (conf_train_dtc[0][0] + conf_train_dtc[1][0] + conf_train_dtc[0][1] + conf_train_dtc[1][1])
        precision_train = (conf_train_dtc[1][1] ) / (conf_train_dtc[1][1] + conf_train_dtc[0][1] )
        recall_train = (conf_train_dtc[1][1]) / (conf_train_dtc[1][0]  + conf_train_dtc[1][1])
       
        dtc_conf_train_acc[i][j] = accuracy_train
        dtc_conf_train_pre[i][j] = precision_train
        dtc_conf_train_rec[i][j] = recall_train                                 
        dtc_conf_train_f1[i][j] = 2/(1/dtc_conf_train_pre[i][j]+1/dtc_conf_train_rec[i][j])
        dtc_conf_train_AUC[i][j] = round(roc_auc_score(y_train, dtc.predict(X_train)),2)
        
       
        accuracy_test = (conf_test_dtc[0][0] + conf_test_dtc[1][1]) / (conf_test_dtc[0][0] + conf_test_dtc[1][0] + conf_test_dtc[0][1] + conf_test_dtc[1][1])
        precision_test = (conf_test_dtc[1][1] ) / (conf_test_dtc[1][1] + conf_test_dtc[0][1] )
        recall_test = (conf_test_dtc[1][1]) / (conf_test_dtc[1][0]  + conf_test_dtc[1][1])
       
        dtc_conf_test_acc[i][j] = accuracy_test
        dtc_conf_test_pre[i][j] = precision_test
        dtc_conf_test_rec[i][j] = recall_test  
        dtc_conf_test_f1[i][j] = 2/(1/dtc_conf_test_pre[i][j]+1/dtc_conf_test_rec[i][j])
        dtc_conf_test_AUC[i][j] = round(roc_auc_score(y_test, dtc.predict(X_test)),2)
        
        print('')
        print('confusion_matrix_DT_train')
        print('criterion = ', dtc_criterion[i] )
        print('max_depth = ', dtc_md[j] )
        confu(conf_train_dtc)
        print('ROC AUC = ',round(roc_auc_score(y_train, dtc.predict(X_train)),2))
        print('')
        
        print('')
        print('confusion_matrix_DT_test')
        print('criterion = ', dtc_criterion[i] )
        print('max_depth = ', dtc_md[j] )
        confu(conf_test_dtc)
        print('ROC AUC = ',round(roc_auc_score(y_test, dtc.predict(X_test)),2))
        print('')




dtc_conf_train_acc = pd.DataFrame(dtc_conf_train_acc)
dtc_conf_train_acc.columns = dtc_md
dtc_conf_train_acc.index = dtc_criterion

dtc_conf_train_pre = pd.DataFrame(dtc_conf_train_pre)
dtc_conf_train_pre.columns = dtc_md
dtc_conf_train_pre.index = dtc_criterion

dtc_conf_train_rec= pd.DataFrame(dtc_conf_train_rec)
dtc_conf_train_rec.columns = dtc_md
dtc_conf_train_rec.index = dtc_criterion

dtc_conf_test_acc= pd.DataFrame(dtc_conf_test_acc)
dtc_conf_test_acc.columns = dtc_md
dtc_conf_test_acc.index = dtc_criterion

dtc_conf_test_pre = pd.DataFrame(dtc_conf_test_pre)
dtc_conf_test_pre.columns = dtc_md
dtc_conf_test_pre.index = dtc_criterion

dtc_conf_test_rec = pd.DataFrame(dtc_conf_test_rec)
dtc_conf_test_rec.columns = dtc_md
dtc_conf_test_rec.index = dtc_criterion


dtc_conf_train_f1= pd.DataFrame(dtc_conf_train_f1)
dtc_conf_train_f1.columns = dtc_md
dtc_conf_train_f1.index = dtc_criterion


dtc_conf_test_f1 = pd.DataFrame(dtc_conf_test_f1)
dtc_conf_test_f1.columns = dtc_md
dtc_conf_test_f1.index = dtc_criterion

dtc_conf_train_AUC= pd.DataFrame(dtc_conf_train_AUC)
dtc_conf_train_AUC.columns = dtc_md
dtc_conf_train_AUC.index = dtc_criterion


dtc_conf_test_AUC = pd.DataFrame(dtc_conf_test_AUC)
dtc_conf_test_AUC.columns = dtc_md
dtc_conf_test_AUC.index = dtc_criterion



from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV

params = {
    'criterion' : ['gini', 'entropy'],
    'max_depth' : [3,4,5,6,7,8,9,10]
    
}

score = ['accuracy', 'precision', 'recall', 'f1', 'roc_auc']


dtc = DecisionTreeClassifier()


for score1 in score :
    grid_tree = GridSearchCV(dtc, param_grid=params, cv=3, scoring=score1)
    grid_tree.fit(X_train, y_train)
    print('best parameters of ', score1, ': ' , grid_tree.best_params_)
    print('best score : ', grid_tree.best_score_)















params = {
    'kernel' : ['linear', 'rbf', 'poly', 'sigmoid'],
    'C' : [100, 10 , 1, 0.1 , 0.01]
    
}

score = ['accuracy', 'precision', 'recall', 'f1', 'roc_auc']


svm = SVC()


for score1 in score :
    grid_tree = GridSearchCV(svm, param_grid=params, cv=3, scoring=score1)
    grid_tree.fit(X_train, y_train)
    print('best parameters of ', score1, ': ' , grid_tree.best_params_)
    print('best score : ', grid_tree.best_score_)









params = {
    'n_neighbors' : [3,5,7,9],
    'p' : [2,3,5,7,9]
    
}

score = ['accuracy', 'precision', 'recall', 'f1', 'roc_auc']


knn = KNeighborsClassifier()


for score1 in score :
    grid_tree = GridSearchCV(knn, param_grid=params, cv=3, scoring=score1)
    grid_tree.fit(X_train, y_train)
    print('best parameters of ', score1, ': ' , grid_tree.best_params_)
    print('best score : ', grid_tree.best_score_)










