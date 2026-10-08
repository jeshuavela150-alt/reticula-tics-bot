import os
import telebot
import google.generativeai as genai
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import json

# =======================================================
# TUS CLAVES SECRETAS (Leídas desde la nube)
# =======================================================
TOKEN_TELEGRAM = os.environ.get("TOKEN_TELEGRAM")
TOKEN_GEMINI = os.environ.get("TOKEN_GEMINI")

bot = telebot.TeleBot(TOKEN_TELEGRAM)
genai.configure(api_key=TOKEN_GEMINI)

# =======================================================
# 1. BASE DE DATOS
# =======================================================
base_de_datos_reticula = {
    # SEMESTRE 1 
    "ACF-2301": {"nombre": "Cálculo Diferencial", "semestre": 1, "horas_teoricas": 3, "horas_practicas": 2, "creditos": 5, "prerrequisitos": [], "es_especialidad": False, "solo_apartir_4to_sem": False}, 
    "AEF-1032": {"nombre": "Fundamentos de Programación", "semestre": 1, "horas_teoricas": 3, "horas_practicas": 2, "creditos": 5, "prerrequisitos": [], "es_especialidad": False, "solo_apartir_4to_sem": False}, 
    "TIF-1019": {"nombre": "Matemáticas Discretas I", "semestre": 1, "horas_teoricas": 3, "horas_practicas": 2, "creditos": 5, "prerrequisitos": [], "es_especialidad": False, "solo_apartir_4to_sem": False}, 
    "TIP-1017": {"nombre": "Introducción a las TIC's", "semestre": 1, "horas_teoricas": 3, "horas_practicas": 0, "creditos": 3, "prerrequisitos": [], "es_especialidad": False, "solo_apartir_4to_sem": False}, 
    "ACH-2307": {"nombre": "Taller de Ética", "semestre": 1, "horas_teoricas": 0, "horas_practicas": 4, "creditos": 4, "prerrequisitos": [], "es_especialidad": False, "solo_apartir_4to_sem": False}, 
    "ACC-0906": {"nombre": "Fundamentos de Investigación", "semestre": 1, "horas_teoricas": 2, "horas_practicas": 2, "creditos": 4, "prerrequisitos": [], "es_especialidad": False, "solo_apartir_4to_sem": False}, 

    # SEMESTRE 2 
    "ACF-0902": {"nombre": "Cálculo Integral", "semestre": 2, "horas_teoricas": 3, "horas_practicas": 2, "creditos": 5, "prerrequisitos": ["ACF-2301"], "es_especialidad": False, "solo_apartir_4to_sem": False}, 
    "AEB-1054": {"nombre": "Programación Orientada a Objetos", "semestre": 2, "horas_teoricas": 1, "horas_practicas": 4, "creditos": 5, "prerrequisitos": ["AEF-1032"], "es_especialidad": False, "solo_apartir_4to_sem": False}, 
    "TIF-1020": {"nombre": "Matemáticas Discretas II", "semestre": 2, "horas_teoricas": 3, "horas_practicas": 2, "creditos": 5, "prerrequisitos": ["TIF-1019"], "es_especialidad": False, "solo_apartir_4to_sem": False}, 
    "ACF-0903": {"nombre": "Álgebra Lineal", "semestre": 2, "horas_teoricas": 3, "horas_practicas": 2, "creditos": 5, "prerrequisitos": [], "es_especialidad": False, "solo_apartir_4to_sem": False}, 
    "TIF-1009": {"nombre": "Contabilidad y Costos", "semestre": 2, "horas_teoricas": 3, "horas_practicas": 2, "creditos": 5, "prerrequisitos": [], "es_especialidad": False, "solo_apartir_4to_sem": False}, 
    "AEF-1052": {"nombre": "Probabilidad y Estadística", "semestre": 2, "horas_teoricas": 3, "horas_practicas": 2, "creditos": 5, "prerrequisitos": [], "es_especialidad": False, "solo_apartir_4to_sem": False}, 

    # SEMESTRE 3 
    "TIE-1018": {"nombre": "Matemáticas Aplicadas a Comunicaciones", "semestre": 3, "horas_teoricas": 3, "horas_practicas": 1, "creditos": 4, "prerrequisitos": ["ACF-0902"], "es_especialidad": False, "solo_apartir_4to_sem": False}, 
    "TID-1012": {"nombre": "Estructuras y Organización de Datos", "semestre": 3, "horas_teoricas": 2, "horas_practicas": 3, "creditos": 5, "prerrequisitos": ["AEB-1054"], "es_especialidad": False, "solo_apartir_4to_sem": False}, 
    "TIF-1021": {"nombre": "Matemáticas para la Toma de Decisiones", "semestre": 3, "horas_teoricas": 3, "horas_practicas": 2, "creditos": 5, "prerrequisitos": [], "es_especialidad": False, "solo_apartir_4to_sem": False}, 
    "ACD-0908": {"nombre": "Desarrollo Sustentable", "semestre": 3, "horas_teoricas": 2, "horas_practicas": 3, "creditos": 5, "prerrequisitos": [], "es_especialidad": False, "solo_apartir_4to_sem": False}, 
    "TIC-1011": {"nombre": "Electricidad y Magnetismo", "semestre": 3, "horas_teoricas": 2, "horas_practicas": 2, "creditos": 4, "prerrequisitos": [], "es_especialidad": False, "solo_apartir_4to_sem": False}, 
    "TIF-1013": {"nombre": "Fundamentos de Redes", "semestre": 3, "horas_teoricas": 3, "horas_practicas": 2, "creditos": 5, "prerrequisitos": [], "es_especialidad": False, "solo_apartir_4to_sem": False}, 

    # SEMESTRE 4 
    "TID-1004": {"nombre": "Análisis de Señales y Sistemas de Comunicación", "semestre": 4, "horas_teoricas": 2, "horas_practicas": 3, "creditos": 5, "prerrequisitos": ["TIE-1018"], "es_especialidad": False, "solo_apartir_4to_sem": True}, 
    "AEF-1031": {"nombre": "Fundamentos de Base de Datos", "semestre": 4, "horas_teoricas": 3, "horas_practicas": 2, "creditos": 5, "prerrequisitos": ["TID-1012"], "es_especialidad": False, "solo_apartir_4to_sem": False}, 
    "AEC-1061": {"nombre": "Sistemas Operativos I", "semestre": 4, "horas_teoricas": 2, "horas_practicas": 2, "creditos": 4, "prerrequisitos": [], "es_especialidad": False, "solo_apartir_4to_sem": True}, 
    "TID-1010": {"nombre": "Desarrollo de Emprendedores", "semestre": 4, "horas_teoricas": 2, "horas_practicas": 3, "creditos": 5, "prerrequisitos": [], "es_especialidad": False, "solo_apartir_4to_sem": False}, 
    "TID-1008": {"nombre": "Circuitos Eléctricos y Electrónicos", "semestre": 4, "horas_teoricas": 2, "horas_practicas": 3, "creditos": 5, "prerrequisitos": ["TIC-1011"], "es_especialidad": False, "solo_apartir_4to_sem": False}, 
    "TIF-1025": {"nombre": "Redes de Computadoras", "semestre": 4, "horas_teoricas": 3, "horas_practicas": 2, "creditos": 5, "prerrequisitos": ["TIF-1013"], "es_especialidad": False, "solo_apartir_4to_sem": False}, 

    # SEMESTRE 5 
    "TIF-1029": {"nombre": "Telecomunicaciones", "semestre": 5, "horas_teoricas": 3, "horas_practicas": 2, "creditos": 5, "prerrequisitos": ["TID-1004"], "es_especialidad": False, "solo_apartir_4to_sem": False}, 
    "AEH-1063": {"nombre": "Taller de Base de Datos", "semestre": 5, "horas_teoricas": 1, "horas_practicas": 3, "creditos": 4, "prerrequisitos": ["AEF-1031"], "es_especialidad": False, "solo_apartir_4to_sem": False}, 
    "TIB-1024": {"nombre": "Programación II", "semestre": 5, "horas_teoricas": 1, "horas_practicas": 4, "creditos": 5, "prerrequisitos": ["AEB-1054"], "es_especialidad": False, "solo_apartir_4to_sem": False}, 
    "AED-1062": {"nombre": "Sistemas Operativos II", "semestre": 5, "horas_teoricas": 2, "horas_practicas": 3, "creditos": 5, "prerrequisitos": ["AEC-1061"], "es_especialidad": False, "solo_apartir_4to_sem": False}, 
    "TIC-1005": {"nombre": "Arquitectura de Computadoras", "semestre": 5, "horas_teoricas": 2, "horas_practicas": 2, "creditos": 4, "prerrequisitos": ["TID-1008"], "es_especialidad": False, "solo_apartir_4to_sem": False}, 
    "TIF-1026": {"nombre": "Redes Emergentes", "semestre": 5, "horas_teoricas": 3, "horas_practicas": 2, "creditos": 5, "prerrequisitos": ["TIF-1025"], "es_especialidad": False, "solo_apartir_4to_sem": False}, 

    # SEMESTRE 6 
    "TIC-1028": {"nombre": "Tecnologías Inalámbricas", "semestre": 6, "horas_teoricas": 2, "horas_practicas": 2, "creditos": 4, "prerrequisitos": ["TIF-1029"], "es_especialidad": False, "solo_apartir_4to_sem": False}, 
    "TIF-1007": {"nombre": "Base de Datos Distribuidas", "semestre": 6, "horas_teoricas": 3, "horas_practicas": 2, "creditos": 5, "prerrequisitos": ["AEH-1063"], "es_especialidad": False, "solo_apartir_4to_sem": False}, 
    "AEB-1055": {"nombre": "Programación Web", "semestre": 6, "horas_teoricas": 1, "horas_practicas": 4, "creditos": 5, "prerrequisitos": ["TIB-1024"], "es_especialidad": False, "solo_apartir_4to_sem": False}, 
    "TIC-1014": {"nombre": "Ingeniería de Software", "semestre": 6, "horas_teoricas": 2, "horas_practicas": 2, "creditos": 4, "prerrequisitos": [], "es_especialidad": False, "solo_apartir_4to_sem": False}, 
    "TIH-1016": {"nombre": "Interacción Humano Computadora", "semestre": 6, "horas_teoricas": 1, "horas_practicas": 3, "creditos": 4, "prerrequisitos": [], "es_especialidad": False, "solo_apartir_4to_sem": False}, 
    "TIF-1003": {"nombre": "Administración y Seguridad de Redes", "semestre": 6, "horas_teoricas": 3, "horas_practicas": 2, "creditos": 5, "prerrequisitos": ["TIF-1026"], "es_especialidad": False, "solo_apartir_4to_sem": False}, 

    # SEMESTRE 7 
    "ACA-0909": {"nombre": "Taller de Investigación I", "semestre": 7, "horas_teoricas": 0, "horas_practicas": 4, "creditos": 4, "prerrequisitos": [], "es_especialidad": False, "solo_apartir_4to_sem": False}, 
    "TIC-1022": {"nombre": "Negocios Electrónicos I", "semestre": 7, "horas_teoricas": 2, "horas_practicas": 2, "creditos": 4, "prerrequisitos": [], "es_especialidad": False, "solo_apartir_4to_sem": False}, 
    "AEB-1011": {"nombre": "Desarrollo de Aplicaciones para Dispositivos Móviles", "semestre": 7, "horas_teoricas": 1, "horas_practicas": 4, "creditos": 5, "prerrequisitos": ["AEB-1055"], "es_especialidad": False, "solo_apartir_4to_sem": False}, 
    "TIC-1027": {"nombre": "Taller de Ingeniería de Software", "semestre": 7, "horas_teoricas": 2, "horas_practicas": 2, "creditos": 4, "prerrequisitos": ["TIC-1014"], "es_especialidad": False, "solo_apartir_4to_sem": False}, 
    "TIC-1002": {"nombre": "Administración Gerencial", "semestre": 7, "horas_teoricas": 2, "horas_practicas": 2, "creditos": 4, "prerrequisitos": [], "es_especialidad": False, "solo_apartir_4to_sem": False}, 

    # SEMESTRE 8 
    "ACA-0910": {"nombre": "Taller de Investigación II", "semestre": 8, "horas_teoricas": 0, "horas_practicas": 4, "creditos": 4, "prerrequisitos": ["ACA-0909"], "es_especialidad": False, "solo_apartir_4to_sem": False}, 
    "TIC-1023": {"nombre": "Negocios Electrónicos II", "semestre": 8, "horas_teoricas": 2, "horas_practicas": 2, "creditos": 4, "prerrequisitos": [], "es_especialidad": False, "solo_apartir_4to_sem": False}, 
    "TIC-1006": {"nombre": "Auditoría en Tecnologías de la Información", "semestre": 8, "horas_teoricas": 2, "horas_practicas": 2, "creditos": 4, "prerrequisitos": [], "es_especialidad": False, "solo_apartir_4to_sem": False}, 
    "TIC-1015": {"nombre": "Ingeniería del Conocimiento", "semestre": 8, "horas_teoricas": 2, "horas_practicas": 2, "creditos": 4, "prerrequisitos": [], "es_especialidad": False, "solo_apartir_4to_sem": False}, 
    "TIF-1001": {"nombre": "Administración de Proyectos", "semestre": 8, "horas_teoricas": 3, "horas_practicas": 2, "creditos": 5, "prerrequisitos": [], "es_especialidad": False, "solo_apartir_4to_sem": False}, 

    # MÓDULO DE ESPECIALIDAD (INTERNET DE LAS COSAS)
    "ICV-2201": {"nombre": "Sistemas Web con Servlets y Oracle", "semestre": "Especialidad", "horas_teoricas": 0, "horas_practicas": 5, "creditos": 5, "prerrequisitos": [], "es_especialidad": True, "solo_apartir_4to_sem": False}, 
    "ICV-2202": {"nombre": "Cubos OLAP para inteligencia empresarial", "semestre": "Especialidad", "horas_teoricas": 0, "horas_practicas": 5, "creditos": 5, "prerrequisitos": [], "es_especialidad": True, "solo_apartir_4to_sem": False}, 
    "ICB-2203": {"nombre": "Fundamentos de Internet de las cosas", "semestre": "Especialidad", "horas_teoricas": 0, "horas_practicas": 5, "creditos": 5, "prerrequisitos": [], "es_especialidad": True, "solo_apartir_4to_sem": False}, 
    "ICB-2204": {"nombre": "Ciberseguridad", "semestre": "Especialidad", "horas_teoricas": 1, "horas_practicas": 4, "creditos": 5, "prerrequisitos": [], "es_especialidad": True, "solo_apartir_4to_sem": False}, 
    "ICV-2205": {"nombre": "Programación de Aplicaciones para Ambientes distribuidos", "semestre": "Especialidad", "horas_teoricas": 0, "horas_practicas": 5, "creditos": 5, "prerrequisitos": [], "es_especialidad": True, "solo_apartir_4to_sem": False}, 
    "ICB-2206": {"nombre": "Internet de las Cosas Avanzado", "semestre": "Especialidad", "horas_teoricas": 1, "horas_practicas": 4, "creditos": 5, "prerrequisitos": [], "es_especialidad": True, "solo_apartir_4to_sem": False}, 

    # TRÁMITES FINALES Y LIBERACIONES
    "RES0001": {"nombre": "Residencia Profesional", "semestre": 9, "horas_teoricas": 0, "horas_practicas": 0, "creditos": 10, "prerrequisitos": [], "es_especialidad": False, "solo_apartir_4to_sem": False},
    "SS-0001": {"nombre": "Servicio Social", "semestre": "Trámite", "horas_teoricas": 0, "horas_practicas": 0, "creditos": 10, "prerrequisitos": [], "es_especialidad": False, "solo_apartir_4to_sem": False}, 
    "ACT-COMP": {"nombre": "Actividades Complementarias", "semestre": "Trámite", "horas_teoricas": 0, "horas_practicas": 0, "creditos": 5, "prerrequisitos": [], "es_especialidad": False, "solo_apartir_4to_sem": False} 
}

# =======================================================
# 1.5 CONFIGURAR EL "CEREBRO" DE GEMINI
# =======================================================
# Convertimos el diccionario a texto para que Gemini lo pueda leer
datos_texto = json.dumps(base_de_datos_reticula, ensure_ascii=False)

instrucciones_ia = f"""
Eres el asistente escolar oficial de la carrera de Ingeniería en TICs.
Tu objetivo es responder de forma amable, clara y útil a los estudiantes.
Basa todas tus respuestas ÚNICAMENTE en la siguiente información de la retícula:
{datos_texto}

Reglas importantes:
- Si te preguntan por créditos totales de la carrera, responde que son 260.
- El servicio social pide el 60% de créditos aprobados.
- La residencia pide el 70% de créditos aprobados.
- Si no sabes algo o no está en la retícula, dile al estudiante que consulte con su coordinador.
- Usa formato amigable con emojis si aplica.
"""

modelo_ia = genai.GenerativeModel('gemini-3.8-flash', system_instruction=instrucciones_ia)


# =======================================================
# 2. MENÚ PRINCIPAL (/start)
# =======================================================
@bot.message_handler(commands=['start', 'menu'])
def menu_principal(message):
    teclado = InlineKeyboardMarkup()
    btn_guia = InlineKeyboardButton("📖 Guía de Lectura", callback_data="btn_guia")
    btn_ruta = InlineKeyboardButton("🔗 Seriación y Rutas", callback_data="btn_ruta")
    btn_tramites = InlineKeyboardButton("🎓 Trámites y Liberaciones", callback_data="btn_tramites")
    btn_especialidad = InlineKeyboardButton("💻 Especialidad IoT", callback_data="btn_especialidad")
    
    teclado.add(btn_guia)
    teclado.add(btn_ruta)
    teclado.add(btn_tramites)
    teclado.add(btn_especialidad)
    
    mensaje_bienvenida = (
        "¡Hola! 🤖 Soy tu asistente virtual con Inteligencia Artificial para la retícula de TICs.\n\n"
        "Puedes usar los botones de abajo, o simplemente **escribirme tu duda de forma natural**, por ejemplo:\n"
        "_'¿Qué materias me piden para tomar Base de Datos?'_"
    )
    bot.send_message(message.chat.id, mensaje_bienvenida, parse_mode="Markdown", reply_markup=teclado)

# =======================================================
# 3. BUSCADOR RÁPIDO DE MATERIAS (/materia)
# =======================================================
@bot.message_handler(commands=['materia'])
def consultar_materia(message):
    try:
        clave = message.text.split()[1].upper()
        if clave in base_de_datos_reticula:
            materia = base_de_datos_reticula[clave]
            respuesta = f"📚 *{materia['nombre']}*\nCréditos: {materia['creditos']}\n"
            if materia['prerrequisitos']:
                nombres_pre = [base_de_datos_reticula[p]["nombre"] for p in materia['prerrequisitos'] if p in base_de_datos_reticula]
                respuesta += f"⚠️ Prerrequisitos: {', '.join(nombres_pre)}"
            else:
                respuesta += "✅ Prerrequisitos: Ninguno."
            bot.reply_to(message, respuesta, parse_mode="Markdown")
        else:
            bot.reply_to(message, "❌ No encontré esa clave.")
    except IndexError:
        bot.reply_to(message, "⚠️ Escríbelo así: /materia CLAVE")

# =======================================================
# 4. RESPUESTA A LOS BOTONES
# =======================================================
@bot.callback_query_handler(func=lambda call: True)
def respuesta_botones(call):
    if call.data == "btn_guia":
        bot.send_message(call.message.chat.id, "Los números debajo de las materias (ej. 3-2-5) significan: \nHoras Teóricas - Horas Prácticas - Créditos Totales.")
    elif call.data == "btn_ruta":
        bot.send_message(call.message.chat.id, "Para consultar prerrequisitos rápido, escribe /materia seguido de la clave. Ejemplo: /materia TIC-1014")
    elif call.data == "btn_tramites":
        bot.send_message(call.message.chat.id, "El Servicio Social requiere el 60% de créditos y la Residencia el 70%.")
    elif call.data == "btn_especialidad":
        bot.send_message(call.message.chat.id, "El Módulo es 'Internet de las Cosas, Ciberseguridad y Base de Datos' (25 créditos).")

# =======================================================
# 5. EL NUEVO ATRAPA-TODO CON GEMINI (MAGIA IA)
# =======================================================
@bot.message_handler(func=lambda message: True)
def charlar_con_gemini(message):
    bot.send_chat_action(message.chat.id, 'typing') 
    
    try:
        respuesta_ia = modelo_ia.generate_content(message.text)
        bot.reply_to(message, respuesta_ia.text)
        
    except Exception as e:
        print(f"\n🔴 ERROR DE GEMINI: {e}\n") # <--- Esta es la línea clave
        bot.reply_to(message, "¡Ups! 😅 Mi cerebro de inteligencia artificial está procesando demasiada información. Intenta preguntarme de nuevo en un momento.")
# =======================================================
# 6. ENCENDIDO DEL BOT
# =======================================================
print("¡Bot con Inteligencia Artificial encendido!")
bot.infinity_polling()