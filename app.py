from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import csv, os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY','change-this-secret-key')
LEADS_FILE='leads.csv'

SERVICES=[
    {'slug':'apartment','icon':'🏠','title':'Apartment Booking','subtitle':'Holiday rentals with availability, extras and guest messages.','image':'https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=1200&q=80','features':['Availability calendar','Booking request form','Transfer and boat upsells','Owner dashboard']},
    {'slug':'restaurant','icon':'🍽️','title':'Restaurant','subtitle':'Menus, table reservations and WhatsApp enquiries.','image':'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=1200&q=80','features':['Digital menu','Table booking','Special offers','Google Maps']},
    {'slug':'cafe','icon':'☕','title':'Café','subtitle':'Beautiful café websites with offers, gallery and quick contact.','image':'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?auto=format&fit=crop&w=1200&q=80','features':['Menu and prices','Daily offers','Loyalty idea','Instagram style gallery']},
    {'slug':'taxi','icon':'🚕','title':'Taxi & Transfer','subtitle':'Airport transfer pages with fixed prices and WhatsApp booking.','image':'https://images.unsplash.com/photo-1549924231-f129b911e442?auto=format&fit=crop&w=1200&q=80','features':['Airport transfer form','Fixed route prices','Vehicle information','WhatsApp message presets']},
    {'slug':'boat','icon':'🚤','title':'Boat Trips','subtitle':'Private trips, sunset cruises and fishing experiences.','image':'https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1200&q=80','features':['Trip packages','Request booking','Photo gallery','Add-on experiences']},
    {'slug':'cleaning','icon':'🧹','title':'Cleaning Services','subtitle':'Local cleaning service websites with instant quote requests.','image':'https://images.unsplash.com/photo-1581578731548-c64695cc6952?auto=format&fit=crop&w=1200&q=80','features':['Service list','Quote form','Before/after gallery','Recurring jobs']},
    {'slug':'painting','icon':'🎨','title':'Painting Services','subtitle':'Professional pages for painters and home improvement companies.','image':'https://images.unsplash.com/photo-1562259949-e8e7689d7828?auto=format&fit=crop&w=1200&q=80','features':['Project gallery','Quote request','Service areas','Reviews']},
    {'slug':'mechanic','icon':'🔧','title':'Auto Mechanic','subtitle':'Garage websites with repair enquiry and service booking.','image':'https://images.unsplash.com/photo-1486262715619-67b85e0b08d3?auto=format&fit=crop&w=1200&q=80','features':['Repair booking','MOT/service info','WhatsApp photos','Customer reviews']},
]

PLANS=[
    {'name':'Basic','price':'€499','monthly':'€29 / month','tag':'Starter presence','items':['1 modern landing page','Mobile friendly design','WhatsApp button','Gallery and contact section','Basic SEO setup','Small monthly edits']},
    {'name':'Pro','price':'€999','monthly':'€49 / month','tag':'Most popular','items':['Multi-page website','Booking or quote form','Email notifications','Service pages','English + Spanish','Monthly support']},
    {'name':'Business','price':'€1,499','monthly':'€79 / month','tag':'Automation ready','items':['Admin dashboard','Bookings / requests management','Automated emails','Reports and statistics','Priority changes','Built for future expansion']},
]

@app.context_processor
def inject_globals():
    return dict(services=SERVICES, plans=PLANS, year=datetime.now().year)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/demo/<slug>')
def demo(slug):
    service=next((s for s in SERVICES if s['slug']==slug), None)
    if not service:
        return redirect(url_for('home'))
    return render_template('demo.html', service=service)

@app.route('/contact', methods=['GET','POST'])
def contact():
    if request.method=='POST':
        row={
            'created_at':datetime.now().isoformat(timespec='seconds'),
            'name':request.form.get('name',''),
            'business':request.form.get('business',''),
            'email':request.form.get('email',''),
            'phone':request.form.get('phone',''),
            'service':request.form.get('service',''),
            'message':request.form.get('message','')
        }
        exists=os.path.exists(LEADS_FILE)
        with open(LEADS_FILE,'a',newline='',encoding='utf-8') as f:
            writer=csv.DictWriter(f, fieldnames=row.keys())
            if not exists: writer.writeheader()
            writer.writerow(row)
        flash('Thank you — your request has been saved. We will contact you shortly.')
        return redirect(url_for('contact'))
    return render_template('contact.html')

@app.route('/admin')
def admin():
    leads=[]
    if os.path.exists(LEADS_FILE):
        with open(LEADS_FILE, newline='', encoding='utf-8') as f:
            leads=list(csv.DictReader(f))[-50:]
    return render_template('admin.html', leads=reversed(leads))

if __name__=='__main__':
    app.run(debug=True)
