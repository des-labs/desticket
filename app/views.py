from flask import render_template,request,url_for,redirect,session
from wtforms import Form,validators, StringField,SubmitField
from app import app,query,resolve, jiracmd
import sys

class EnterText(Form):
    username = StringField(label='user',validators=[validators.Optional()])
    email = StringField(label='email',validators=[validators.Optional()])
    jiraticket = StringField(label='ticket',validators=[validators.Optional()])

    def validate(self):
        if not self.username.data and not self.email.data:
            return False
        return True

class ResetButton(Form):
    button = SubmitField(label='reset')

class Search(Form):
    search = StringField(label='search', validators=[validators.InputRequired()])

@app.route('/',methods=['POST','GET'])
@app.route('/index',methods=['POST','GET'])
def index(message=None):
    print(message)
    form = EnterText(request.form)
    if request.method == 'POST':
        input_username = request.form['username']
        input_email = request.form['email']
        input_jira = request.form['jiraticket']

    if form.validate():
        query_dict = query.main(username = input_username, email = input_email)
        return redirect(url_for('form_submitted',user=query_dict['user'],
                email=query_dict['email'],count=query_dict['count']))
    
    return render_template('index.html',message=message)

@app.route('/form_submitted',methods=['POST','GET'])
def form_submitted(user=None,email=None,jira_ticket=None, count=None):
    form = ResetButton(request.form)
    if request.method=='POST':
        user = request.args.get('user')
        email = request.args.get('email')
        jira = jiracmd.Jira('jira-desdm')
        if jira_ticket:
            ticket = str(jira_ticket)
        else:
            issues = jira.search_for_issue(email)
            if len(issues) > 1:
                message = "There are more than one open issues! Please resubmit form \
                           and specify the ticket number.\n \
                           {results}".format(results=[key.key for key in iss])
                return redirect(url_for('passwd_reset',user=user, email= email, text=message))
            elif len(issues) == 0:
                message = "No ticket found for {user}!".format(user=user)
                return redirect(url_for('passwd_reset',user=user, text = message))
            else:
                ticket = issues[0].key.split('-')[1]
        # run resolve here...
        try:
            resolve.run_all(ticket,user)    
            message = "Ticket DESHELP-{tix} resolved and {user} password had been reset!".format(
                    tix=ticket, user= user)
            return redirect(url_for('passwd_reset',user=user,text=message))
        except:
            message = "Failed to resolve DESHELP-{tix} for {user}: \
                       {errcls}:{err}!".format(tix=ticket, user = user, errcls = sys.exc_info()[0],err =sys.exc_info()[1])
            return redirect(url_for('passwd_reset',user=user,text=message))


    return render_template('form_submitted.html',user=user,email = email, count=count)

@app.route('/passwd_reset/<user>',methods=['POST','GET'])
def passwd_reset(user=None,text=None):
    return render_template('passwd_reset.html',user=user,text=text)

@app.route('/search',methods=['POST','GET'])
def search():
    form = Search(request.form)
    if request.method=='POST':
        search_text = request.form['search']
    if form.validate():
        results = query.search(search_text)
        return redirect(url_for('index',message=results))
            
    return render_template('search.html')

