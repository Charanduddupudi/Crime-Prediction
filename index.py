from flask import *
import pandas as pd

app=Flask(__name__)

@app.route("/")
@app.route("/home",methods=["GET","POST"])
def home():
    if request.method=="POST":
        lat=float(request.form['lat'])
        lon=float(request.form['lon'])
        year=int(request.form['year'])
        month=int(request.form['month'])
        date=int(request.form['date'])
        hours=int(request.form['hour'])
        minutes=int(request.form['min'])
        
        df=pd.read_csv(r"C:\Users\Duddupudi\Desktop\ML Project\data.csv")
        df['timestamp']=pd.to_datetime(df.timestamp,errors='coerce')

        df['year'] = df['timestamp'].dt.year 
        df['month'] = df['timestamp'].dt.month 
        df['day'] = df['timestamp'].dt.day 
        df['hour'] = df['timestamp'].dt.hour 
        df['minute'] = df['timestamp'].dt.minute
        
        df=df.dropna(axis=0)
        df.dtypes
        x=df.iloc[:,[7,8,9,10,11,12,13]].values
        y=df.iloc[:,[1,2,3,4,5,6]].values

        from sklearn.model_selection import train_test_split
        x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.20,random_state=9)


        from sklearn.neighbors import KNeighborsClassifier
        model=KNeighborsClassifier(n_neighbors=1)
        model.fit(x_train,y_train)

        y_pred=model.predict(x_test)
        from sklearn import metrics
        #print(metrics.accuracy_score(y_test,y_pred)*100)
        acc=metrics.accuracy_score(y_test,y_pred)*100
  

        result = model.predict([[lat,lon,year,month,date,hours,minutes]])
        res=list(result[0])

        l=['Act 379','Act 13','Act 279','Act 323','Act 363','Act 302']
        output=l[res.index(1)]
        #print(output)  

        return render_template("home.html",acc=acc,output=output)

    return render_template("home.html")

if __name__=="__main__":
    app.run(debug=True)
