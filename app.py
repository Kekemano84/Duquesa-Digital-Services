from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = "change-this-secret-key"

PHONE = "+447584724809"
EMAIL = "seagoing8888@gmail.com"
WA_NUMBER = "447584724809"

def whatsapp_url(text):
    from urllib.parse import quote
    return f"https://wa.me/{WA_NUMBER}?text={quote(text)}"

SERVICES = [
    {"slug":"apartments", "icon":"🏖️", "title":"Apartment Booking", "title_es":"Reservas de apartamentos", "desc":"Direct booking website with availability, guest enquiry and upsell options.", "desc_es":"Web de reservas directas con disponibilidad, consulta de huéspedes y extras.", "image":"https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=1200&q=80"},
    {"slug":"restaurants", "icon":"🍽️", "title":"Restaurants", "title_es":"Restaurantes", "desc":"Menu, table booking, WhatsApp orders and special offers.", "desc_es":"Menú, reserva de mesas, pedidos por WhatsApp y ofertas.", "image":"https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=1200&q=80"},
    {"slug":"cafes", "icon":"☕", "title":"Cafés", "title_es":"Cafeterías", "desc":"Stylish café website with offers, gallery, loyalty and contact buttons.", "desc_es":"Web elegante con ofertas, galería, fidelización y contacto.", "image":"https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?auto=format&fit=crop&w=1200&q=80"},
    {"slug":"taxi-transfer", "icon":"🚐", "title":"Taxi & Airport Transfer", "title_es":"Taxi y transfer aeropuerto", "desc":"Private transfer pages with price requests and pre-filled WhatsApp messages.", "desc_es":"Páginas de transfer privado con solicitudes y WhatsApp preparado.", "image":"https://images.unsplash.com/photo-1610647752706-3bb12232b3eb?auto=format&fit=crop&w=1200&q=80"},
    {"slug":"boat-trips", "icon":"🛥️", "title":"Boat Trips", "title_es":"Excursiones en barco", "desc":"Trip cards, private tours, fishing experiences and enquiry automation.", "desc_es":"Tours privados, pesca, excursiones y automatización de consultas.", "image":"https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1200&q=80"},
    {"slug":"cleaning", "icon":"🧽", "title":"Cleaning Services", "title_es":"Servicios de limpieza", "desc":"Quote forms, before/after gallery, reviews and service areas.", "desc_es":"Formularios, galería antes/después, reseñas y zonas de servicio.", "image":"https://images.unsplash.com/photo-1581578731548-c64695cc6952?auto=format&fit=crop&w=1200&q=80"},
    {"slug":"painting", "icon":"🎨", "title":"Painting & Home Services", "title_es":"Pintura y servicios del hogar", "desc":"Professional local service page for jobs, quotes and portfolio.", "desc_es":"Página profesional para trabajos, presupuestos y portfolio.", "image":"https://images.unsplash.com/photo-1562259949-e8e7689d7828?auto=format&fit=crop&w=1200&q=80"},
    {"slug":"mechanic", "icon":"🔧", "title":"Auto Mechanic", "title_es":"Taller mecánico", "desc":"Garage website with service booking, MOT style enquiries and WhatsApp.", "desc_es":"Web para taller con reservas, consultas y WhatsApp.", "image":"https://images.unsplash.com/photo-1619642751034-765dfdf7c58e?auto=format&fit=crop&w=1200&q=80"},
]

PLANS = [
    {"name":"Basic", "tag":"Start online", "setup":"€499", "monthly":"€29/mo", "summary":"A premium one-page website for local businesses that need trust and enquiries.", "features":["Modern mobile website", "WhatsApp contact button", "Photo gallery", "Google Maps section", "Basic SEO setup", "Hosting guidance"]},
    {"name":"Pro", "tag":"Most popular", "setup":"€999", "monthly":"€49/mo", "summary":"A complete website with booking/request forms and automated email notifications.", "features":["Everything in Basic", "Multiple pages", "Booking or quote form", "Email notifications", "Service cards", "Basic admin page", "Monthly content edits"]},
    {"name":"Business", "tag":"For serious growth", "setup":"€1499", "monthly":"€79/mo", "summary":"A stronger system for bookings, services, upsells and business reporting.", "features":["Everything in Pro", "Admin dashboard", "Booking management", "Extra services / upsell", "English + Spanish", "Reports and exports", "Priority support"]},
]

@app.route('/')
def index():
    return render_template('index.html', services=SERVICES, plans=PLANS, phone=PHONE, email=EMAIL, whatsapp_url=whatsapp_url)

@app.route('/demo/<slug>')
def demo(slug):
    service = next((s for s in SERVICES if s['slug'] == slug), None)
    if not service:
        return redirect(url_for('index'))
    demo_message = f"Hello, I am interested in a {service['title']} website demo for my business in Duquesa."
    return render_template('demo.html', service=service, phone=PHONE, email=EMAIL, whatsapp=whatsapp_url(demo_message))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    selected_plan = request.args.get('plan', '')
    selected_service = request.args.get('service', '')
    if request.method == 'POST':
        name = request.form.get('name')
        business = request.form.get('business')
        plan = request.form.get('plan')
        service = request.form.get('service')
        message = f"Hello, my name is {name}. I run {business}. I am interested in {plan} for {service}."
        return redirect(whatsapp_url(message))
    return render_template('contact.html', plans=PLANS, services=SERVICES, selected_plan=selected_plan, selected_service=selected_service, phone=PHONE, email=EMAIL)

@app.route('/admin')
def admin():
    return render_template('admin.html', year=datetime.now().year)

if __name__ == '__main__':
    app.run(debug=True)
