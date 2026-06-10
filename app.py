from flask import Flask, render_template, request, redirect, url_for, session, flash
from urllib.parse import quote

app = Flask(__name__)
app.secret_key = "change-this-secret-key"
WHATSAPP_PHONE = "447584724809"
CONTACT_EMAIL = "seagoing8888@gmail.com"

DEMO_CARDS = [
    {"slug":"apartment", "emoji":"🏖️", "title_en":"Apartment Booking", "title_es":"Reservas de Apartamentos", "desc_en":"Holiday rental websites with availability, extras, guest enquiry forms and WhatsApp follow-up.", "desc_es":"Webs para alquiler vacacional con disponibilidad, extras, formularios y WhatsApp.", "img":"https://images.unsplash.com/photo-1499793983690-e29da59ef1c2?auto=format&fit=crop&w=1200&q=80"},
    {"slug":"restaurant", "emoji":"🍽️", "title_en":"Restaurant", "title_es":"Restaurante", "desc_en":"Modern menus, table reservation requests, food galleries and instant enquiries.", "desc_es":"Menús modernos, solicitudes de mesa, galerías y consultas rápidas.", "img":"https://images.unsplash.com/photo-1528605248644-14dd04022da1?auto=format&fit=crop&w=1200&q=80"},
    {"slug":"cafe", "emoji":"☕", "title_en":"Café", "title_es":"Cafetería", "desc_en":"Colourful café pages with offers, opening hours, loyalty ideas and quick contact.", "desc_es":"Páginas coloridas para cafeterías con ofertas, horarios, fidelización y contacto.", "img":"https://images.unsplash.com/photo-1554118811-1e0d58224f24?auto=format&fit=crop&w=1200&q=80"},
    {"slug":"taxi", "emoji":"🚐", "title_en":"Taxi & Transfer", "title_es":"Taxi y Traslados", "desc_en":"Airport transfer pages with fixed prices, route options and ready WhatsApp messages.", "desc_es":"Páginas de traslados con precios fijos, rutas y mensajes de WhatsApp preparados.", "img":"https://images.unsplash.com/photo-1592853625600-6dcc9367bc45?auto=format&fit=crop&w=1200&q=80"},
    {"slug":"boat", "emoji":"⛵", "title_en":"Boat Trips", "title_es":"Paseos en Barco", "desc_en":"Private boat trips, sunset cruises, dolphin watching and fishing experiences.", "desc_es":"Barcos privados, atardeceres, delfines y experiencias de pesca.", "img":"https://images.unsplash.com/photo-1505839673365-e3971f8d9184?auto=format&fit=crop&w=1200&q=80"},
    {"slug":"cleaning", "emoji":"✨", "title_en":"Cleaning Services", "title_es":"Servicios de Limpieza", "desc_en":"Local cleaning websites with instant quote requests and professional trust sections.", "desc_es":"Webs de limpieza con presupuestos rápidos y secciones de confianza.", "img":"https://images.unsplash.com/photo-1527515637462-cff94eecc1ac?auto=format&fit=crop&w=1200&q=80"},
    {"slug":"painting", "emoji":"🎨", "title_en":"Painting Services", "title_es":"Pintura y Reformas", "desc_en":"Professional pages for painters, decorators and home improvement companies.", "desc_es":"Páginas para pintores, decoradores y empresas de reformas.", "img":"https://images.unsplash.com/photo-1562259949-e8e7689d7828?auto=format&fit=crop&w=1200&q=80"},
    {"slug":"mechanic", "emoji":"🔧", "title_en":"Auto Mechanic", "title_es":"Taller Mecánico", "desc_en":"Garage websites with service booking, repair enquiries, offers and reviews.", "desc_es":"Webs para talleres con citas, consultas de reparación, ofertas y reseñas.", "img":"https://images.unsplash.com/photo-1486262715619-67b85e0b08d3?auto=format&fit=crop&w=1200&q=80"},
]

PLANS = [
    {"name":"Basic", "tag_en":"Starter presence", "tag_es":"Presencia inicial", "setup":"€499", "monthly":"€29", "featured":False,
     "items_en":["1-page modern website", "Mobile-first design", "WhatsApp contact button", "Photo gallery", "Service/pricing section", "Basic SEO setup", "Hosting guidance"],
     "items_es":["Web moderna de 1 página", "Diseño primero para móvil", "Botón de WhatsApp", "Galería de fotos", "Servicios/precios", "SEO básico", "Guía de hosting"]},
    {"name":"Pro", "tag_en":"Most popular", "tag_es":"Más popular", "setup":"€999", "monthly":"€39", "featured":True,
     "items_en":["Everything in Basic", "Multi-page website", "Booking/enquiry form", "Email-ready enquiries", "English & Spanish pages", "Business-specific demo flow", "Small monthly edits"],
     "items_es":["Todo lo incluido en Basic", "Web con varias páginas", "Formulario de reserva/consulta", "Consultas preparadas para email", "Páginas en inglés y español", "Demo específica para el negocio", "Pequeños cambios mensuales"]},
    {"name":"Business", "tag_en":"Best for automation", "tag_es":"Mejor para automatización", "setup":"€1,499", "monthly":"€49", "featured":False,
     "items_en":["Everything in Pro", "Simple client dashboard", "Enquiry tracking", "Automated WhatsApp message templates", "Packages and upsells", "Priority support", "Ready for future online payments"],
     "items_es":["Todo lo incluido en Pro", "Panel simple para el cliente", "Seguimiento de consultas", "Plantillas automáticas de WhatsApp", "Paquetes y ventas extra", "Soporte prioritario", "Preparado para pagos online"]},
]

def current_lang():
    selected = request.args.get('lang') or session.get('lang') or 'en'
    if selected not in ('en','es'):
        selected='en'
    session['lang'] = selected
    return selected

def with_lang(endpoint, **values):
    values.setdefault('lang', current_lang())
    return url_for(endpoint, **values)

@app.context_processor
def inject_helpers():
    return {"url_lang": with_lang, "contact_email": CONTACT_EMAIL}

@app.route('/')
def index():
    l = current_lang()
    return render_template('index.html', lang=l, demos=DEMO_CARDS, plans=PLANS)

@app.route('/demo/<slug>')
def demo(slug):
    l = current_lang()
    card = next((d for d in DEMO_CARDS if d['slug']==slug), None)
    if not card:
        return redirect(url_for('index', lang=l))
    message = f"Hello, I would like to see a demo for {card['title_en']} from Duquesa Digital Services."
    if l == 'es':
        message = f"Hola, me gustaría ver una demo para {card['title_es']} de Duquesa Digital Services."
    wa = f"https://wa.me/{WHATSAPP_PHONE}?text={quote(message)}"
    return render_template('demo.html', lang=l, card=card, wa=wa)

@app.route('/contact', methods=['GET','POST'])
def contact():
    l = current_lang()
    if request.method == 'POST':
        enquiry = {
            'name': request.form.get('name',''),
            'business': request.form.get('business',''),
            'phone': request.form.get('phone',''),
            'email': request.form.get('email',''),
            'service': request.form.get('service',''),
            'plan': request.form.get('plan',''),
            'message': request.form.get('message','')
        }
        session.setdefault('enquiries', [])
        enquiries = session['enquiries']
        enquiries.append(enquiry)
        session['enquiries'] = enquiries
        msg = f"New Duquesa Digital enquiry%0AName: {enquiry['name']}%0ABusiness: {enquiry['business']}%0AService: {enquiry['service']}%0APlan: {enquiry['plan']}%0APhone: {enquiry['phone']}%0AEmail: {enquiry['email']}%0AMessage: {enquiry['message']}"
        return redirect(f"https://wa.me/{WHATSAPP_PHONE}?text={msg}")
    return render_template('contact.html', lang=l, demos=DEMO_CARDS, plans=PLANS)

@app.route('/register', methods=['GET','POST'])
def register():
    l = current_lang()
    if request.method == 'POST':
        session['client'] = {
            'name': request.form.get('name','Demo User'),
            'business': request.form.get('business','Demo Business'),
            'type': request.form.get('type','Apartment Booking'),
            'plan': request.form.get('plan','Pro')
        }
        flash('Demo account created.' if l=='en' else 'Cuenta demo creada.')
        return redirect(url_for('client_dashboard', lang=l))
    return render_template('register.html', lang=l, demos=DEMO_CARDS, plans=PLANS)

@app.route('/dashboard')
def client_dashboard():
    l = current_lang()
    client = session.get('client') or {'name':'Demo User','business':'Demo Business','type':'Restaurant','plan':'Pro'}
    enquiries = session.get('enquiries', [])
    return render_template('dashboard.html', lang=l, client=client, enquiries=enquiries)

@app.route('/admin')
def admin():
    l = current_lang()
    enquiries = session.get('enquiries', [])
    return render_template('admin.html', lang=l, demos=DEMO_CARDS, plans=PLANS, enquiries=enquiries)

if __name__ == '__main__':
    app.run(debug=True)
