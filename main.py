from flask.views import MethodView
from wtforms import Form, StringField, SubmitField
from flask import Flask, render_template, request
from flatmates_bill import flat

# Creation of the central App object (instance of the Flask class)
app = Flask(__name__) # __name__ contains the string of the current folder path

# Definition of Pages in our App
class HomePage(MethodView):
    def get(self):
        return render_template("index.html") # By convention Flask knows it should look for the HTML file in the "templates" folder

class BillFormPage(MethodView):
    
    def get(self):
        bill_form = BillForm()
        return render_template("bill_form_page.html", billform=bill_form)

class ResultsPage(MethodView):
    
    def post(self):
        billform = BillForm(request.form)
        
        # Coming from the App Bill Form:
        amount = billform.amount.data
        period = billform.amount.data
        name1= billform.name1.data
        days_in_house1 = billform.days_in_house1.data
        name2= billform.name1.data
        days_in_house2 = billform.days_in_house2.data
        
        # Coming from the Backend Calc tool using the form Inputs:
        the_bill = flat.Bill(float(amount), period)
        flatmate1 = flat.Flatmate (name1, float(days_in_house1))
        flatmate2 = flat.Flatmate (name2, float(days_in_house2))
        return render_template("results.html",
                                 name1= flatmate1.name, 
                                 amount1=flatmate1.pays(the_bill,flatmate2),
                                 name2= flatmate2.name, 
                                 amount2=flatmate2.pays(the_bill,flatmate1),)

class BillForm(Form):
    amount = StringField("Bill Amount: ", default="100")
    period = StringField("Bill Period: ", default= "December 2022")

    name1 = StringField("Name: ", default="Jorge")
    days_in_house1= StringField("Days in the house: ", default = "10")
    name2 = StringField("Name: ", default= "Vero")
    days_in_house2= StringField("Days in the house: ", default = "20")

    button = SubmitField("Calculate")

# Creating URL for our App pages
app.add_url_rule('/', view_func= HomePage.as_view('home_page'))
app.add_url_rule('/bill', view_func= BillFormPage.as_view('bill_form_page'))
app.add_url_rule('/results', view_func= ResultsPage.as_view('results_page'))


app.run(debug=True) # debug allows us to not have to stop and run the app every time we make changes 