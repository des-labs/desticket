from flask import render_template,request,url_for,redirect,session
from wtforms import Form,validators, StringField,SubmitField
from app import app,query,resolve

class EnterText(Form):
    username = StringField(validators=[validators.InputRequired()])

class ResetButton(Form):
    button = SubmitField()

@app.route('/',methods=['POST','GET'])
@app.route('/index',methods=['POST','GET'])
def index():
    form = EnterText(request.form)
    if request.method == 'POST':
        text = request.form['username']

    if form.validate():
        exists = query.main(text)
        return redirect(url_for('form_submitted',user=text,exists = exists))
    
    return render_template('index.html')

@app.route('/form_submitted/<user>/<exists>')
def form_submitted(user=None,exists=None):
    form = ResetButton(request.form)
    #if request.method=='POST':
        
    return render_template('form_submitted.html',user=user,exists=exists)
