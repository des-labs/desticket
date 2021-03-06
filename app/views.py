from flask import render_template,request,url_for,redirect,jsonify
from wtforms import Form,validators, StringField,SubmitField,BooleanField
from app import app,query,resolve, jiracmd
import sys
import ast

class EnterText(Form):
    username = StringField(label='user',validators=[validators.Optional()])
    email = StringField(label='email',validators=[validators.Optional()])
    jiraticket = StringField(label='ticket',validators=[validators.Optional()])

    def validate(self):
        if not self.username.data and not self.email.data:
            return False
        return True

class ResetButton(Form):
    reset = BooleanField(label='reset',validators=[validators.Optional()])
    unlock = BooleanField(label='unlock',validators=[validators.Optional()])
    
    def validate(self):
        if self.reset.data is True and self.unlock.data is True:
            return False
        if self.reset.data is False and self.unlock.data is False:
            return False
        return True

class Search(Form):
    search = StringField(label='search', validators=[validators.InputRequired()])
    
class Manual(Form):
    name = StringField(label='name', validators=[validators.InputRequired()])
    email = StringField(label='email',validators=[validators.InputRequired()])
    unlock = BooleanField(label='unlock',validators=[validators.Optional()])

@app.route('/',methods=['POST','GET'])
def index(message=None):
    form = EnterText(request.form)
    if request.method == 'POST':
        input_username = request.form['username']
        input_email = request.form['email']
        input_jira = request.form['jiraticket']

    if form.validate():
        query_dict = query.main(username = input_username, email = input_email)
        return redirect(url_for('form_submission',user=query_dict['user'],
                email=query_dict['email'],count=query_dict['count'],jira_ticket=input_jira))
    
    return render_template('index.html',message=message)

@app.route('/form_submission/',methods=['POST','GET'])
def form_submission(user=None,email=None,jira_ticket=None,count=None):
    form = ResetButton(request.form)
    if request.method=='POST':
        reset = form.reset.data
        unlock = form.unlock.data

    if form.validate():
        jira = jiracmd.Jira()
        jira_ticket=request.args.get('jira_ticket')
        user = request.args.get('user')
        if jira_ticket and (jira_ticket.lower() !='none' or jira_ticket !=''):
            ticket = str(jira_ticket)
        else:
            issues = jira.search_for_issue(request.args.get('email'))
            if len(issues) > 1:
                message = "There are more than one open issues! Please resubmit form \
                           and specify the ticket number.\n \
                           {results}".format(results=[key.key for key in issues])
                return redirect(url_for('passwd_reset',user=user, 
                        email= request.args.get('email'), text=message))
            elif len(issues) == 0:
                return redirect(url_for('manual_reset',user=user,reset=reset,
                        unlock=unlock))
            else:
                ticket = issues[0].key.split('-')[1]
        # run resolve here...
        try:
            if str(reset).lower() == 'true':
                resolve.run_all(ticket,user)    
                message = "Ticket {ticket} has been resolved. Passwords reset/account unlocked for {user}!".format(ticket =ticket, user = user)
            else:
                resolve.run_all(ticket,user,reset=False)
                message = "Ticket {ticket} has been resolved. Account unlocked for {user}!".format(ticket =ticket, user = user)
            return redirect(url_for('passwd_reset',user=request.args.get('user'),text=message))
        except:
            message = "Failed to resolve DESHELP-{tix} for {user}: \
                       {errcls}:{err}!".format(tix=ticket, user = user, errcls = sys.exc_info()[0],err =sys.exc_info()[1])
            return redirect(url_for('passwd_reset',user=request.args.get('user'),text=message))


    return render_template('form_submission.html',user=user,email = email, count=count,jira_ticket = jira_ticket)

@app.route('/passwd_reset/<user>/',methods=['POST','GET'])
def passwd_reset(user=None,text=None):
    return render_template('passwd_reset.html',user=user,text=text)

@app.route('/search/',methods=['POST','GET'])
def search():
    form = Search(request.form)
    if request.method=='POST':
        search_text = request.form['search']
    if form.validate():
        results = query.search(search_text)
        return redirect(url_for('index',message=results))
            
    return render_template('search.html')

@app.route('/manual_reset/<user>/',methods=['POST','GET'])
def manual_reset(user=None,unlock=True,reset=False):
    form = Manual(request.form)
    if request.method == 'POST':
        input_name = request.form['name']
        input_email = request.form['email']
        input_reset = request.args.get('reset')

    if form.validate():
        try:
            if input_reset == 'True':
                resolve.run_manual(user = user, email = input_email, name = input_name)
                message = "Password reset/account unlocked for {user}!".format(user= user)
            else: 
                resolve.run_manual(user = user, reset=False, email = input_email, name = input_name)
                message = "Account unlocked for {user}!".format(user= user)

            return redirect(url_for('passwd_reset',user=user,text=message))
        except:
            message = "Failed to reset password/unlock account for {user}: \
                       {errcls}:{err}!".format(user = user, errcls = sys.exc_info()[0],
                                               err =sys.exc_info()[1])
            return redirect(url_for('passwd_reset',user=user,text=message))
    return render_template('manual_reset.html',user= user)


### API CALLS ###
@app.route('/api/v1/exists/',methods=['GET','POST'])
def api_exists():
    # user, email, jira_ticket
    data = ast.literal_eval(request.data.decode('utf-8'))
    query_dict = query.main(username = data['user'], email = data['email'])
  
    return jsonify(query_dict)

@app.route('/api/v1/search/',methods=['GET','POST'])
def api_search():
    data = ast.literal_eval(request.data.decode('utf-8'))
    results = {'message': query.search(data['search_string'])}
    return jsonify(results)

@app.route('/api/v1/reset/',methods=['GET','POST'])
def api_reset():
    # user, email, jira_ticket, reset
    data = ast.literal_eval(request.data.decode('utf-8'))
    user = data['user']
    email = data['email']
    jira_ticket = data['jira_ticket']
    reset = data['reset']

    jira = jiracmd.Jira()
    if jira_ticket=='None':
        issues = jira.search_for_issue(email)
        ticket = None
        if len(issues) > 1:
            message = "There are more than one open issues! Please resubmit form \
                       and specify the ticket number.\n \
                       {results}".format(results=[key.key for key in issues])
            status = 1
        elif len(issues) == 0:
            try:
                if reset == 'True':
                    resolve.run_manual(user = user, email = email, name = user)
                    message = "Password reset/account unlocked for {user}!".format(user= user)
                    status = 0
                else: 
                    resolve.run_manual(user = user, reset=False, email = email, name = user)
                    message = "Account unlocked for {user}!".format(user= user)
                    status = 0
            except:
                message = "Failed to resolve account for {user}: \
                   {errcls}:{err}!".format(user = user, errcls = sys.exc_info()[0],err =sys.exc_info()[1])
                status = 1

        else:
            ticket = issues[0].key.split('-')[1]
    else:
        ticket = jira_ticket
    # run resolve here...
    if ticket:
        try:
            if reset == 'True':
                resolve.run_all(ticket,user)    
                message = "Ticket {ticket} has been resolved. Passwords reset/account unlocked for {user}!".format(ticket =ticket, user = user)
                status = 0
            else:
                resolve.run_all(ticket,user,reset=False)
                message = "Ticket {ticket} has been resolved. Account unlocked for {user}!".format(ticket =ticket, user = user)
                status = 0
        except:
            message = "Failed to resolve DESHELP-{tix} for {user}: \
                       {errcls}:{err}!".format(tix=ticket, user = user, errcls = sys.exc_info()[0],err =sys.exc_info()[1])
            status = 1

    return jsonify({'message': message,'status': status})
