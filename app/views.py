from flask import render_template,request,url_for,redirect,session
from wtforms import Form,validators, StringField
from app import app,query

class EnterText(Form):
    username = StringField(validators=[validators.InputRequired()])

@app.route('/',methods=['POST','GET'])
@app.route('/index',methods=['POST','GET'])
def index():
    message = None
    form = EnterText(request.form)
    if request.method == 'POST':
        text = request.form['username']
    else:
        text = None

    if form.validate():
        print(text)
        #exists = query.main(text)
        if text =='mjohns44':
            exists = True
        else:
            exists = False

        print(exists)
        return redirect(url_for('form_submitted',user=text,exists = exists))
    
    return render_template('index.html')

@app.route('/form_submitted/<user>/<exists>')
def form_submitted(user=None,exists=None):
    return render_template('form_submitted.html',user=user,exists=exists)
