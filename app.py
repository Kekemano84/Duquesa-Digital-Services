from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime
from urllib.parse import quote

app = Flask(__name__)
app.secret_key = "change-this-secret-key"

ADMIN_USER = "admin"
ADMIN_PASS = "admin123"
WHATSAPP_PHONE = "447584724809"
CONTACT_EMAIL = "seagoing8888@gmail.com"

DEMO_CARDS = [
    {"slug":"apartment", "emoji":"🏠", "title_en":"Apartment Booking", "title_es":"Reservas de Apartamentos", "desc_en":"Holiday rental pages with availability, extras and guest enquiries.", "desc_es":"Páginas para alquiler vacacional con disponibilidad, extras y consultas.", "img":"https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=1200&q=80"},
    {"slug":"restaurant", "emoji":"🍽️", "title_en":"Restaurant", "title_es":"Restaurante", "desc_en":"Menus, table reservation requests, gallery and WhatsApp enquiries.", "desc_es":"Menús, solicitudes de reserva, galería y consultas por WhatsApp.", "img":"https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=1200&q=80"},
    {"slug":"cafe", "emoji":"☕", "title_en":"Café", "title_es":"Cafetería", "desc_en":"Beautiful café websites with offers, opening hours and quick contact.", "desc_es":"Webs bonitas para cafeterías con ofertas, horarios y contacto rápido.", "img":"https://images.unsplash.com/photo-1509042239860-f550ce710b93?auto=format&fit=crop&w=1200&q=80"},
    {"slug":"taxi", "emoji":"🚕", "title_en":"Taxi & Transfer", "title_es":"Taxi y Traslados", "desc_en":"Airport transfer pages with fixed prices and WhatsApp booking messages.", "desc_es":"Páginas de traslados con precios fijos y reservas por WhatsApp.", "img":"https://images.unsplash.com/photo-1611348586804-61bf6c080437?auto=format&fit=crop&w=1200&q=80"},
    {"slug":"boat", "emoji":"🚤", "title_en":"Boat Trips", "title_es":"Paseos en Barco", "desc_en":"Private trips, sunset cruises, dolphin watching and fishing experiences.", "desc_es":"Paseos privados, atardeceres, avistamiento de delfines y pesca.", "img":"https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1200&q=80"},
    {"slug":"cleaning", "emoji":"🧹", "title_en":"Cleaning Services", "title_es":"Servicios de Limpieza", "desc_en":"Local cleaning websites with instant quote request forms.", "desc_es":"Webs para limpieza con formularios de presupuesto rápido.", "img":"https://images.unsplash.com/photo-1581578731548-c64695cc6952?auto=format&fit=crop&w=1200&q=80"},
    {"slug":"painting", "emoji":"🎨", "title_en":"Painting Services", "title_es":"Pintura y Reformas", "desc_en":"Professional pages for painters and home improvement companies.", "desc_es":"Páginas profesionales para pintores y empresas de reformas.", "img":"https://images.unsplash.com/photo-1562259949-e8e7689d7828?auto=format&fit=crop&w=1200&q=80"},
    {"slug":"mechanic", "emoji":"🔧", "title_en":"Auto Mechanic", "title_es":"Taller Mecánico", "desc_en":"Garage websites with repair enquiries, service booking and reviews.", "desc_es":"Webs para talleres con consultas, citas y reseñas.", "img":"https://images.unsplash.com/photo-1486262715619-67b85e0b08d3?auto=format&fit=crop&w=1200&q=80"},
]

PLANS = [
    {"name":"Basic", "tag_en":"Starter presence", "tag_es":"Presencia inicial", "setup":"€499", "monthly":"€29", "featured":False,
     "items_en":["1-page premium website", "Mobile responsive design", "WhatsApp contact button", "Gallery and service section", "Basic SEO setup", "Hosting guidance"],
     "items_es":["Web premium de 1 página", "Diseño adaptable a móvil", "Botón de WhatsApp", "Galería y sección de servicios", "SEO básico", "Guía de hosting"]},
    {"name":"Pro", "tag_en":"Most popular", "tag_es":"Más popular", "setup":"€999", "monthly":"€39", "featured":True,
     "items_en":["Everything in Basic", "Multi-page website", "Booking/enquiry form", "Email notifications", "English & Spanish content", "Demo page for your business", "Small monthly edits"],
     "items_es":["Todo lo incluido en Basic", "Web con varias páginas", "Formulario de reserva/consulta", "Notificaciones por email", "Contenido en inglés y español", "Página demo para tu negocio", "Pequeños cambios mensuales"]},
    {"name":"Business", "tag_en":"Automation ready", "tag_es":"Listo para automatización", "setup":"€1,499", "monthly":"€49", "featured":False,
     "items_en":["Everything in Pro", "Admin login area", "Client enquiry dashboard", "Automated WhatsApp messages", "Service packages and upsells", "Priority support", "Future payment integration ready"],
     "items_es":["Todo lo incluido en Pro", "Área admin con login", "Panel de consultas de clientes", "Mensajes automáticos de WhatsApp", "Paquetes y ventas extra", "Soporte prioritario", "Preparado para pagos online"]},
]

def lang():
    selected = request.args.get('lang') or session.get('lang') or 'en'
    if selected not in ('en','es'):
        selected='en'
    session['lang'] = selected
    return selected

def wa_link(message):
    return f"https://wa.me/{WHATSAPP_PHONE}?text={quote(message)}"

@app.route('/')
def index():
    l = lang()
    return render_template('index.html', lang=l, demos=DEMO_CARDS, plans=PLANS, wa=wa_link("Hello, I am interested in a Duquesa Digital Services website."))

@app.route('/demo/<slug>')
def demo(slug):
    l=lang()
    card = next((d for d in DEMO_CARDS if d['slug']==slug), None)
    if not card:
        return redirect(url_for('index'))
    return render_template('demo.html', lang=l, card=card, wa=wa_link(f"Hello, I am interested in the {card['title_en']} demo."))

@app.route('/contact', methods=['GET','POST'])
def contact():
    l=lang()
    if request.method == 'POST':
        enquiry = {k: request.form.get(k,'') for k in ['name','business','email','phone','service','plan','message']}
        session.setdefault('enquiries', [])
        enquiries = session['enquiries']
        enquiry['date'] = datetime.now().strftime('%Y-%m-%d %H:%M')
        enquiries.append(enquiry)
        session['enquiries'] = enquiries
        flash('Thanks. Your enquiry has been saved. Please message us on WhatsApp as well for the fastest reply.')
        text = f"Hello, I would like to discuss a website. Business: {enquiry['business']}. Service: {enquiry['service']}. Plan: {enquiry['plan']}."
        return redirect(wa_link(text))
    return render_template('contact.html', lang=l, plans=PLANS, demos=DEMO_CARDS, wa=wa_link("Hello, I would like to request a demo."))

@app.route('/login', methods=['GET','POST'])
def login():
    l=lang()
    if request.method == 'POST':
        if request.form.get('username') == ADMIN_USER and request.form.get('password') == ADMIN_PASS:
            session['admin'] = True
            return redirect(url_for('admin'))
        flash('Invalid login')
    return render_template('login.html', lang=l)

@app.route('/admin')
def admin():
    if not session.get('admin'):
        return redirect(url_for('login'))
    enquiries = session.get('enquiries', [])
    return render_template('admin.html', enquiries=enquiries, demos=DEMO_CARDS, plans=PLANS, lang=lang())

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
