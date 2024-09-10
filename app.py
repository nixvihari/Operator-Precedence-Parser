from flask import Flask, render_template,request, url_for, redirect,session
from flask_session import Session
# import utils as ut
from . import op_parser as OPParser
# import op_parser as op

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.secret_key="032417e8317faf0da343f72a37e09322"

PLACEHOLDER_CODE = "Paste your CSV content here"

# # display dataset 
# no_of_instances = 0
# global current_page_index
# current_page_index = 0

@app.route('/', methods=["GET"])
def op_parser_main():
    if session.get('npr') is None or session.get('pr') is None or session.get('op') is None or session.get('input_string') is None:
        session['npr'] = ""
        session['pr'] = ""
        session['op'] = ""
        session['input_string'] = ""
    context = {
            "npr" : session['npr'],
            "pr" : session['pr'],
            "op" : session['op'],
            "input_string" : session['input_string'],
            "i_status" : False
    }
    return render_template('data_input.html', **context)

@app.route("/save_input", methods=["POST"])
def save_input():
    session['npr'] = request.form.get("num_production_rules")
    session['pr'] = request.form.get("production_rules")
    session['op'] = request.form.get("operators")
    session['input_string'] = request.form.get("input_string")
    return redirect(url_for("op_parser_main"))

@app.route("/call_parse", methods=["POST"])
def call_parse():
    npr = session.get('npr')
    pr = session.get('pr').replace('\r','')
    op = session.get('op')
    i_s = session.get('input_string')

    success, parse_table, parse_tracker = OPParser.OperatorPrecedenceParser(n=npr,rules=pr, operator=op, input_string=i_s)
    context = {
        'clrscr' : 0,
        'ss' : success,
        'pt' : parse_table,
        'ptr' : parse_tracker
    }
    return render_template('output.html', **context)


@app.route("/reset_session", methods=["POST"])
def reset_session():
    session.clear()
    session['npr'] = ""
    session['pr'] = ""
    session['op'] = ""
    session['input_string'] = ""
    return redirect(url_for("op_parser_main"))
