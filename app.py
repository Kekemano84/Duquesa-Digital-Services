
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
        "slug": "apartment", "icon": "🏖️",
        "name": "Apartment Booking", "name_es": "Reserva de Apartamento",
        "desc": "A complete holiday rental demo with availability, gallery, extras and guest enquiry.",
        "desc_es": "Demo completo para alquiler vacacional con disponibilidad, galería, extras y consulta del huésped.",
        "img": "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=1600&q=80",
        "hero": "Luxury coastal apartment demo", "hero_es": "Demo de apartamento costero de lujo",
        "sub": "Turn visitors into booking enquiries with a premium mobile-first apartment website.",
        "sub_es": "Convierte visitantes en solicitudes de reserva con una web premium optimizada para móvil.",
        "sections": [
            {"title": "Availability Calendar", "title_es": "Calendario de Disponibilidad", "text": "Guests can request dates, number of guests and optional extras.", "text_es": "Los huéspedes pueden solicitar fechas, número de personas y extras."},
            {"title": "Extras & Upsell", "title_es": "Extras y Servicios", "text": "Airport transfer, boat trips and welcome packs can be added.", "text_es": "Se pueden añadir traslados, paseos en barco y packs de bienvenida."},
            {"title": "Owner Enquiry", "title_es": "Consulta para el Propietario", "text": "Every enquiry arrives clearly with all guest details.", "text_es": "Cada consulta llega clara con todos los datos del huésped."}
        ],
        "cards": ["4 guests", "No pets", "Check-in after 14:00", "WhatsApp booking"],
        "cards_es": ["4 huéspedes", "No mascotas", "Entrada después de 14:00", "Reserva por WhatsApp"]
    },
    {
        "slug": "restaurant", "icon": "🍽️",
        "name": "Restaurant", "name_es": "Restaurante",
        "desc": "Restaurant demo with menu, table booking, offers and WhatsApp enquiries.",
        "desc_es": "Demo de restaurante con menú, reservas de mesa, ofertas y consultas por WhatsApp.",
        "img": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=1600&q=80",
        "hero": "Mediterranean restaurant website", "hero_es": "Web para restaurante mediterráneo",
        "sub": "Show your menu, take table requests and receive WhatsApp enquiries instantly.",
        "sub_es": "Muestra tu menú, recibe solicitudes de reserva y consultas por WhatsApp al instante.",
        "sections": [
            {"title": "Digital Menu", "title_es": "Menú Digital", "text": "Beautiful food cards with prices and descriptions.", "text_es": "Cartas visuales con precios y descripciones."},
            {"title": "Table Reservation", "title_es": "Reserva de Mesa", "text": "Simple booking form for date, time and number of guests.", "text_es": "Formulario sencillo para fecha, hora y número de personas."},
            {"title": "Special Offers", "title_es": "Ofertas Especiales", "text": "Promote lunch deals, tapas nights and wine offers.", "text_es": "Promociona menús de día, noches de tapas y ofertas de vino."}
        ],
        "cards": ["Seafood paella €18.90", "Grilled sea bass €22", "Tapas selection €14.50", "Book a table"],
        "cards_es": ["Paella de marisco €18.90", "Lubina a la plancha €22", "Selección de tapas €14.50", "Reservar mesa"]
    },
    {
        "slug": "cafe", "icon": "☕",
        "name": "Café", "name_es": "Cafetería",
        "desc": "Café demo with breakfast menu, offers, gallery and quick WhatsApp contact.",
        "desc_es": "Demo de cafetería con desayunos, ofertas, galería y contacto rápido por WhatsApp.",
        "img": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?auto=format&fit=crop&w=1600&q=80",
        "hero": "Colourful café landing page", "hero_es": "Página colorida para cafetería",
        "sub": "Perfect for cafés that want to show daily specials and attract tourists nearby.",
        "sub_es": "Perfecto para cafeterías que quieren mostrar ofertas diarias y atraer turistas cercanos.",
        "sections": [
            {"title": "Daily Offers", "title_es": "Ofertas del Día", "text": "Coffee and croissant, breakfast combos and cake specials.", "text_es": "Café con croissant, desayunos combinados y tartas especiales."},
            {"title": "Photo Gallery", "title_es": "Galería de Fotos", "text": "Show the atmosphere, coffee, cakes and seating area.", "text_es": "Muestra el ambiente, cafés, tartas y zona de mesas."},
            {"title": "Opening Hours", "title_es": "Horario", "text": "Clear opening hours and Google Maps location.", "text_es": "Horario claro y ubicación con Google Maps."}
        ],
        "cards": ["Coffee + croissant €4.50", "Breakfast deal", "Fresh cakes", "Open 08:00-18:00"],
        "cards_es": ["Café + croissant €4.50", "Oferta desayuno", "Tartas frescas", "Abierto 08:00-18:00"]
    },
    {
        "slug": "taxi", "icon": "🚕",
        "name": "Taxi & Transfer", "name_es": "Taxi y Traslado",
        "desc": "Transfer demo for airport pickups, fixed prices and private van enquiries.",
        "desc_es": "Demo para traslados al aeropuerto, precios fijos y consultas de van privada.",
        "img": "https://images.unsplash.com/photo-1549924231-f129b911e442?auto=format&fit=crop&w=1600&q=80",
        "hero": "Private airport transfer demo", "hero_es": "Demo de traslado privado al aeropuerto",
        "sub": "Ideal for Mercedes Vito style 6-passenger transfers around Malaga, Gibraltar and Duquesa.",
        "sub_es": "Ideal para traslados tipo Mercedes Vito de 6 pasajeros por Málaga, Gibraltar y Duquesa.",
        "sections": [
            {"title": "Fixed Routes", "title_es": "Rutas con Precio Fijo", "text": "Malaga Airport, Gibraltar Airport, Marbella and local trips.", "text_es": "Aeropuerto de Málaga, Gibraltar, Marbella y trayectos locales."},
            {"title": "Flight Details", "title_es": "Datos del Vuelo", "text": "Customers can send arrival time and flight number.", "text_es": "Los clientes pueden enviar hora de llegada y número de vuelo."},
            {"title": "WhatsApp Booking", "title_es": "Reserva por WhatsApp", "text": "Prepared message includes pickup, destination and passengers.", "text_es": "El mensaje preparado incluye recogida, destino y pasajeros."}
        ],
        "cards": ["Malaga → Duquesa from €120", "Gibraltar → Duquesa from €90", "Up to 6 passengers", "Large luggage space"],
        "cards_es": ["Málaga → Duquesa desde €120", "Gibraltar → Duquesa desde €90", "Hasta 6 pasajeros", "Espacio para equipaje"]
    },
    {
        "slug": "boat", "icon": "🐬",
        "name": "Boat Trips", "name_es": "Paseos en Barco",
        "desc": "Boat trip demo for dolphin watching, sunset cruises and private charters.",
        "desc_es": "Demo para paseos en barco, delfines, atardeceres y tours privados.",
        "img": "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?auto=format&fit=crop&w=1600&q=80",
        "hero": "Dolphin watching and sunset cruises", "hero_es": "Delfines y paseos al atardecer",
        "sub": "Show packages, prices and booking requests for private boat experiences.",
        "sub_es": "Muestra paquetes, precios y solicitudes para experiencias privadas en barco.",
        "sections": [
            {"title": "Dolphin Watching", "title_es": "Avistamiento de Delfines", "text": "Family-friendly sea experience with clear package cards.", "text_es": "Experiencia familiar en el mar con paquetes claros."},
            {"title": "Sunset Cruise", "title_es": "Paseo al Atardecer", "text": "Premium evening offer with drinks, music and photos.", "text_es": "Oferta premium de tarde con bebidas, música y fotos."},
            {"title": "Private Charter", "title_es": "Charter Privado", "text": "Customers can request custom routes and group sizes.", "text_es": "Los clientes pueden pedir rutas personalizadas y grupos."}
        ],
        "cards": ["Dolphin trip from €120", "Sunset cruise from €220", "Fishing trip from €220", "Private charter"],
        "cards_es": ["Delfines desde €120", "Atardecer desde €220", "Pesca desde €220", "Charter privado"]
    },
    {
        "slug": "cleaning", "icon": "🧹",
        "name": "Cleaning Services", "name_es": "Limpieza",
        "desc": "Cleaning demo for quote requests, service lists and before/after galleries.",
        "desc_es": "Demo para limpieza con presupuestos, servicios y galerías antes/después.",
        "img": "https://images.unsplash.com/photo-1585421514284-efb74c2b69ba?auto=format&fit=crop&w=1600&q=80",
        "hero": "Local cleaning quote website", "hero_es": "Web para presupuestos de limpieza",
        "sub": "Perfect for cleaners serving apartments, villas, offices and holiday rentals.",
        "sub_es": "Perfecto para limpieza de apartamentos, villas, oficinas y alquiler vacacional.",
        "sections": [
            {"title": "Instant Quote Request", "title_es": "Solicitud de Presupuesto", "text": "Ask property type, bedrooms and preferred cleaning date.", "text_es": "Pregunta tipo de propiedad, habitaciones y fecha preferida."},
            {"title": "Service Packages", "title_es": "Paquetes de Servicio", "text": "Regular, deep clean, end-of-tenancy and Airbnb changeover.", "text_es": "Regular, profunda, fin de alquiler y cambio Airbnb."},
            {"title": "Before / After", "title_es": "Antes / Después", "text": "Visual proof helps new customers trust the business.", "text_es": "La prueba visual ayuda a generar confianza."}
        ],
        "cards": ["Apartment cleaning", "Deep cleaning", "Airbnb changeover", "Window cleaning"],
        "cards_es": ["Limpieza apartamento", "Limpieza profunda", "Cambio Airbnb", "Limpieza ventanas"]
    },
    {
        "slug": "painting", "icon": "🎨",
        "name": "Painting Services", "name_es": "Pintores",
        "desc": "Painter demo with project gallery, service list and estimate request.",
        "desc_es": "Demo para pintores con galería, servicios y solicitud de presupuesto.",
        "img": "https://images.unsplash.com/photo-1562259929-b4e1fd3aef09?auto=format&fit=crop&w=1600&q=80",
        "hero": "Painting and home improvement demo", "hero_es": "Demo de pintura y reformas",
        "sub": "A professional site for painters and small home improvement companies.",
        "sub_es": "Una web profesional para pintores y pequeñas empresas de reformas.",
        "sections": [
            {"title": "Interior Painting", "title_es": "Pintura Interior", "text": "Rooms, apartments, villas and commercial spaces.", "text_es": "Habitaciones, apartamentos, villas y locales."},
            {"title": "Exterior Painting", "title_es": "Pintura Exterior", "text": "Walls, gates, facades and outdoor areas.", "text_es": "Paredes, puertas, fachadas y exteriores."},
            {"title": "Estimate Form", "title_es": "Formulario de Presupuesto", "text": "Customers can describe the work and upload photos later.", "text_es": "Los clientes pueden describir el trabajo y luego subir fotos."}
        ],
        "cards": ["Interior painting", "Exterior painting", "Small repairs", "Free estimate"],
        "cards_es": ["Pintura interior", "Pintura exterior", "Pequeñas reparaciones", "Presupuesto gratis"]
    },
    {
        "slug": "mechanic", "icon": "🔧",
        "name": "Auto Mechanic", "name_es": "Taller Mecánico",
        "desc": "Garage demo for diagnostics, service booking and repair enquiries.",
        "desc_es": "Demo de taller para diagnosis, reservas de servicio y consultas de reparación.",
        "img": "https://images.unsplash.com/photo-1632823471565-1ecdf5c668cb?auto=format&fit=crop&w=1600&q=80",
        "hero": "Garage and mechanic booking demo", "hero_es": "Demo para taller y mecánico",
        "sub": "Let customers request diagnostics, tyres, brakes, servicing and repairs online.",
        "sub_es": "Permite solicitar diagnosis, neumáticos, frenos, mantenimiento y reparaciones online.",
        "sections": [
            {"title": "Repair Request", "title_es": "Solicitud de Reparación", "text": "Customer sends car model, issue and preferred date.", "text_es": "El cliente envía modelo, problema y fecha preferida."},
            {"title": "Service Booking", "title_es": "Reserva de Servicio", "text": "Oil, filters, brakes, tyres and inspection requests.", "text_es": "Aceite, filtros, frenos, neumáticos e inspecciones."},
            {"title": "Trust Elements", "title_es": "Elementos de Confianza", "text": "Reviews, gallery and clear contact details.", "text_es": "Reseñas, galería y datos de contacto claros."}
        ],
        "cards": ["Diagnostics", "Tyres & brakes", "Oil service", "Repair enquiry"],
        "cards_es": ["Diagnosis", "Neumáticos y frenos", "Cambio de aceite", "Consulta reparación"]
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
