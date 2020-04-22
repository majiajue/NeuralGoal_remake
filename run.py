#rp= Repository()
#df=rp.main_table.select_all(as_dataframe=True)
#y = df['result']
#df.groupby('result').count()
#print(df.groupby('result').count())

from keras.callbacks import TensorBoard
from Persistent.repository import main_table
from Persistent.repository import Repository
from keras.layers.core import Dense,Activation,Dropout
from keras.models import Sequential
import time
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, MinMaxScaler,RobustScaler,StandardScaler
import math

#region calc_nodes
def CalculateNodesInFirstLayer(n, m):
    return math.sqrt(n * (m + 2)) + 2 * math.sqrt(n / (m + 2)) - 1


def CalculateNodesInSecondLayer(n, m):
    return m * math.sqrt(n / (m + 2)) - 1
#endregion
#region Calculating accuracy tools
def training_predict(model, x_test,y_test,threshold,verbose): #prediction for test phase
    print("# Make Prediction in Training mode")
    prediction = model.predict_proba(x_test,verbose=verbose)
    y_pred = pd.DataFrame(prediction)
    columns_names = y_test.columns
    y_pred.columns=columns_names
    return binary_classification_with_prob_threshold(y_test,y_pred,threshold,verbose)

def binary_classification_with_prob_threshold(y_test,y_pred, threshold,verbose=1):
    binary_prediction = (y_pred>threshold)
    acc = calculate_accuracy(y_test, binary_prediction,verbose)
    return binary_prediction,acc

def calculate_accuracy(y_test,y_pred,verbose=1):
    from sklearn.metrics import accuracy_score
    if(verbose==1):
        print (get_confustion_metrix(y_test,y_pred))
        print ("Accuracy: ", accuracy_score(y_test,y_pred))
    return accuracy_score(y_test,y_pred)

def get_confustion_metrix(target_test,target_predicts):
    from sklearn.metrics import multilabel_confusion_matrix
    target_predicts = pd.DataFrame(target_predicts)
    columns_names = target_test.columns
    target_predicts.columns=columns_names
    #return confusion_matrix(target_test.idxmax(axis=1), target_predicts.argmax(axis=1))
    #return confusion_matrix(target_test.idxmax(axis=1), target_predicts.idxmax(axis=1))
    return multilabel_confusion_matrix(target_test, target_predicts)

#params prediction - numpy array of the prediction
def prediction_to_excel(self, prediction,path):
    import pandas as pd
    from datetime import date
    df = pd.DataFrame(prediction)
    file = path+'prediction_'+self.model_name+"_"+str(date.today())+'.xlsx'
    df.to_excel(file, index=False)
#endregion

def list_to_csv(list):
    import csv
    with open('accuracy_list', 'w', newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(list)

rp= Repository()
df=rp.main_table.select_all(as_dataframe=True)
x=df.loc[:,'home_team_rank':'away_odds_n']
y=df.loc[:, 'result':]

labelencoder = LabelEncoder()
y['result'] = labelencoder.fit_transform(y['result'])  # X:2 ,2:1, 1:0
print('#result label Encoding')
le_name_mapping = dict(zip(labelencoder.classes_, labelencoder.transform(labelencoder.classes_)))
print(le_name_mapping)

y = pd.get_dummies(y['result'], prefix="result")

sc = MinMaxScaler()
#x=x.loc[:,'home_team_rank':'away_odds_n']
#x=sc.fit_transform(x)


x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.2,random_state=2,shuffle=True)

decending_layers=[0,1]
hidden_layers=[1,2,3]
layer_sizes=[16,32,64,512]
batch_sizes=[10]

model_acc=[]

#hidden_layer=2
#layer_size=16
#batch_size=8
#mod=0
#mod_name='fully'


for mod in decending_layers:
    if mod==0:
        mod_name='full'
    else:
        mod_name='dec'
    for hidden_layer in hidden_layers:
        for layer_size in layer_sizes:
            for batch_size in batch_sizes:
                NAME = "{}-nw-{}-layer-{}-size-{}-batch-{}".format(mod_name,hidden_layer,layer_size,batch_size,(int)(time.time()))
                #print(NAME)
                tensorboard = TensorBoard(log_dir='logs\\italy_0804experiment\\{}'.format(NAME))

                model = Sequential()
                model.add(Dense(input_dim=x_train.shape[1], units=layer_size, kernel_initializer='uniform', activation='relu'))

                for l in range(hidden_layer):
                    if mod==1:
                        units=(int)(layer_size/math.ceil((math.pow(2,hidden_layer))))
                    else:
                        units=(int)(layer_size)
                    #print('units:',units)
                    model.add(Dense(units=units, kernel_initializer='uniform', activation='relu'))


                model.add(Dense(units=3, kernel_initializer='uniform', activation='softmax'))
                model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

                model.fit(x_train, y_train, batch_size=batch_size, epochs=100, validation_data=(x_test,y_test),callbacks=[tensorboard])
                mat, acc = training_predict(model,x_test,y_test,0.75,1)
                new_record = [NAME,acc]
                model_acc.append(new_record)

list_to_csv(model_acc)

