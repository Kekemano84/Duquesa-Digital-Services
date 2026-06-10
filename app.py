
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "change-this-secret-key"

WHATSAPP_NUMBER = "447584724809"

TRANSLATIONS = {
    "en": {
        "nav_services": "Services",
        "nav_demos": "Demos",
        "nav_pricing": "Pricing",
        "nav_try": "Try Demo",
        "nav_contact": "Contact",
        "hero_badge": "Costa del Sol Digital Agency",
        "hero_title": "Websites that bring bookings, messages and local customers.",
        "hero_text": "Modern websites, booking pages and WhatsApp automation for apartments, restaurants, cafés, taxis, boat trips and local services in Duquesa, Marbella and the Costa del Sol.",
        "hero_cta1": "View Live Demos",
        "hero_cta2": "Get a Quote",
        "services_title": "Not just a website. A small booking and enquiry machine.",
        "services_sub": "Built for local businesses that want more messages, more bookings and a better first impression.",
        "demos_title": "Choose a demo style",
        "pricing_title": "Simple setup fee + monthly support",
        "pricing_text": "The setup fee builds the website. The monthly fee covers hosting guidance, support, small edits, security updates and keeping the site running.",
        "try_title": "Try the demo flow",
        "try_text": "This is how a local business owner could request a demo or ask for a website package.",
        "contact_title": "Ready to build your local business website?",
        "contact_text": "Send a message and tell us what business you have. We will recommend the best package.",
        "admin_title": "Admin Preview",
        "admin_text": "Hidden preview area for managing future demo requests, client enquiries and plans.",
        "submit": "Send Request",
        "name": "Your Name",
        "email": "Email",
        "business": "Business Type",
        "message": "Message",
        "whatsapp": "WhatsApp",
        "open_demo": "Open Demo",
        "request_demo": "Request Demo",
        "included": "Included",
        "everything_basic": "Everything in Basic, plus:",
        "everything_pro": "Everything in Pro, plus:",
    },
    "es": {
        "nav_services": "Servicios",
        "nav_demos": "Demos",
        "nav_pricing": "Precios",
        "nav_try": "Probar Demo",
        "nav_contact": "Contacto",
        "hero_badge": "Agencia Digital Costa del Sol",
        "hero_title": "Páginas web que generan reservas, mensajes y clientes locales.",
        "hero_text": "Webs modernas, páginas de reserva y automatización de WhatsApp para apartamentos, restaurantes, cafeterías, taxis, barcos y servicios locales en Duquesa, Marbella y la Costa del Sol.",
        "hero_cta1": "Ver Demos",
        "hero_cta2": "Pedir Presupuesto",
        "services_title": "No solo una web. Una pequeña máquina de reservas y consultas.",
        "services_sub": "Creado para negocios locales que quieren más mensajes, más reservas y una mejor primera impresión.",
        "demos_title": "Elige un estilo de demo",
        "pricing_title": "Pago inicial + soporte mensual",
        "pricing_text": "El pago inicial crea la web. La cuota mensual cubre soporte, pequeños cambios, seguridad y mantenimiento.",
        "try_title": "Prueba el flujo demo",
        "try_text": "Así un negocio local puede pedir una demo o solicitar un paquete web.",
        "contact_title": "¿Listo para crear la web de tu negocio?",
        "contact_text": "Envíanos un mensaje y dinos qué negocio tienes. Te recomendaremos el mejor paquete.",
        "admin_title": "Vista Admin",
        "admin_text": "Área oculta para futuras solicitudes, consultas de clientes y planes.",
        "submit": "Enviar Solicitud",
        "name": "Tu Nombre",
        "email": "Email",
        "business": "Tipo de Negocio",
        "message": "Mensaje",
        "whatsapp": "WhatsApp",
        "open_demo": "Abrir Demo",
        "request_demo": "Pedir Demo",
        "included": "Incluido",
        "everything_basic": "Todo lo de Basic, más:",
        "everything_pro": "Todo lo de Pro, más:",
    }
}

DEMOS = [
    {
        "slug": "apartment", "icon": "🏖️", "name": "Apartment Booking", "name_es": "Reserva de Apartamento",
        "desc": "Holiday rental page with availability, extras and guest messages.",
        "desc_es": "Página para alquiler vacacional con disponibilidad, extras y mensajes.",
        "img": "https://images.unsplash.com/photo-1499793983690-e29da59ef1c2?auto=format&fit=crop&w=1200&q=80",
        "features": ["Availability request", "Guest details", "WhatsApp enquiry", "Gallery", "Extras"]
    },
    {
        "slug": "restaurant", "icon": "🍽️", "name": "Restaurant", "name_es": "Restaurante",
        "desc": "Modern menus, table reservations and WhatsApp enquiries.",
        "desc_es": "Menús modernos, reservas de mesa y consultas por WhatsApp.",
        "img": "https://images.unsplash.com/photo-1552566626-52f8b828add9?auto=format&fit=crop&w=1200&q=80",
        "features": ["Menu", "Table booking", "Opening hours", "Gallery", "Reviews"]
    },
    {
        "slug": "cafe", "icon": "☕", "name": "Café", "name_es": "Cafetería",
        "desc": "Colourful café pages with offers, gallery and quick contact.",
        "desc_es": "Webs coloridas para cafeterías con ofertas, galería y contacto rápido.",
        "img": "https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?auto=format&fit=crop&w=1200&q=80",
        "features": ["Special offers", "Coffee menu", "Gallery", "WhatsApp", "Location"]
    },
    {
        "slug": "taxi", "icon": "🚕", "name": "Taxi & Transfer", "name_es": "Taxi y Traslado",
        "desc": "Airport transfer pages with fixed prices and WhatsApp booking.",
        "desc_es": "Páginas para traslados con precios fijos y reserva por WhatsApp.",
        "img": "https://images.unsplash.com/photo-1594223274512-ad4803739b7c?auto=format&fit=crop&w=1200&q=80",
        "features": ["Malaga airport", "Gibraltar airport", "Mercedes Vito style", "Fixed prices", "Quote form"]
    },
    {
        "slug": "boat", "icon": "🐬", "name": "Boat Trips", "name_es": "Paseos en Barco",
        "desc": "Dolphin watching, sunset cruises and private charters.",
        "desc_es": "Avistamiento de delfines, atardeceres y tours privados.",
        "img": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1200&q=80",
        "features": ["Dolphin watching", "Sunset cruise", "Private charter", "Fishing trip", "Booking request"]
    },
    {
        "slug": "cleaning", "icon": "🧹", "name": "Cleaning Services", "name_es": "Limpieza",
        "desc": "Local cleaning service websites with instant quote requests.",
        "desc_es": "Webs para empresas de limpieza con solicitudes rápidas.",
        "img": "https://images.unsplash.com/photo-1581578731548-c64695cc6952?auto=format&fit=crop&w=1200&q=80",
        "features": ["Quote form", "Service list", "Before/after gallery", "WhatsApp", "Areas covered"]
    },
    {
        "slug": "painting", "icon": "🎨", "name": "Painting Services", "name_es": "Pintores",
        "desc": "Professional pages for painters and home improvement companies.",
        "desc_es": "Páginas profesionales para pintores y reformas.",
        "img": "https://images.unsplash.com/photo-1562259949-e8e7689d7828?auto=format&fit=crop&w=1200&q=80",
        "features": ["Quote request", "Portfolio", "Services", "WhatsApp", "Reviews"]
    },
    {
        "slug": "mechanic", "icon": "🔧", "name": "Auto Mechanic", "name_es": "Taller Mecánico",
        "desc": "Garage websites with repair enquiry and service booking.",
        "desc_es": "Webs para talleres con consultas de reparación y reservas.",
        "img": "https://images.unsplash.com/photo-1487754180451-c456f719a1fc?auto=format&fit=crop&w=1200&q=80",
        "features": ["Repair request", "Service booking", "MOT/diagnostic enquiry", "WhatsApp", "Gallery"]
    },
]

PLANS = [
    {
        "name": "Basic", "tag": "Starter online presence", "setup": "€499", "monthly": "€29 / month",
        "items": ["One-page website", "Mobile friendly design", "WhatsApp button", "Photo gallery", "Contact section", "Basic SEO setup"]
    },
    {
        "name": "Pro", "tag": "Most popular", "setup": "€999", "monthly": "€39 / month",
        "items": ["Everything in Basic", "Multi-page website", "Booking / enquiry form", "Email notifications", "Menu or service pages", "Reviews section", "Stronger design"]
    },
    {
        "name": "Business", "tag": "Automation ready", "setup": "€1,499", "monthly": "€49 / month",
        "items": ["Everything in Pro", "Client/demo dashboard", "Service automation", "Extra forms and workflows", "Multi-language EN/ES", "Priority support", "Future SaaS ready"]
    },
]

@app.context_processor
def inject_globals():
    lang = request.args.get("lang", session.get("lang", "en"))
    if lang not in TRANSLATIONS:
        lang = "en"
    session["lang"] = lang
    return {
        "lang": lang,
        "t": TRANSLATIONS[lang],
        "whatsapp": WHATSAPP_NUMBER
    }

@app.route("/")
def index():
    return render_template("index.html", demos=DEMOS, plans=PLANS)

@app.route("/demo/<slug>")
def demo(slug):
    demo = next((d for d in DEMOS if d["slug"] == slug), None)
    if demo is None:
        return redirect(url_for("index"))
    return render_template("demo.html", demo=demo)

@app.route("/try-demo", methods=["GET", "POST"])
def try_demo():
    if request.method == "POST":
        return render_template("thanks.html")
    return render_template("try_demo.html", demos=DEMOS, plans=PLANS)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        return render_template("thanks.html")
    return render_template("contact.html", demos=DEMOS, plans=PLANS)

@app.route("/admin")
def admin():
    return render_template("admin.html", demos=DEMOS, plans=PLANS)

if __name__ == "__main__":
    app.run(debug=True)
