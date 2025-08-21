
import json
import random
import re
import os
import joblib
from web_scraper import get_almsand_sa_services, get_almsand_net_services

# Get the directory of the current script
script_dir = os.path.dirname(__file__)

# Construct the absolute paths to the JSON files and model
prepared_data_path = os.path.join(script_dir, "prepared_data.json")
appointments_path = os.path.join(script_dir, "appointments.json")
model_path = os.path.join(script_dir, "ai_model.joblib")

# Load the trained model
model = joblib.load(model_path)

# Define a simple entity extraction function (rule-based for now)
def extract_entities(text):
    entities = {}
    # Service names - expanded to include variations and specific phrases
    service_names_map = {
        "منصة ايجار": "خدمات منصة ايجار",
        "ايجار": "خدمات منصة ايجار",
        "حساب المواطن": "خدمات حساب المواطن",
        "تصميم تجربة المستخدم": "تصميم تجربة المستخدم",
        "تطوير المواقع والتطبيقات": "تطوير المواقع والتطبيقات",
        "التسويق الرقمي": "التسويق الرقمي",
        "الاستضافة والسحابة": "الاستضافة والسحابة",
        "بناء الهوية والعلامة": "بناء الهوية والعلامة",
        "الاستشارات الرقمية": "الاستشارات الرقمية",
        "الرخص التجارية": "الرخص التجارية",
        "العقار": "العقار",
        "البرمجة": "البرمجة",
        "التصميم": "التصميم",
        "الأمور الطلابية": "الأمور الطلابية",
        "المدارس": "المدارس",
        "الإقامات": "الإقامات",
        "المرور": "المرور",
        "الجوازات": "الجوازات",
        "الشهادات الصحية": "الشهادات الصحية",
        "خدمات الوافدين": "خدمات الوافدين",
        "إدارة وإنجاز المعاملات": "إدارة وإنجاز المعاملات",
        "الخدمات الحكومية": "الخدمات الحكومية",
        "الخدمات الطلابية": "الخدمات الطلابية",
        "خدمات التصميم والديزاين": "خدمات التصميم والديزاين",
        "الخدمات البنكية": "الخدمات البنكية",
        "تجديد إقامة": "تجديد إقامة",
        "تأشيرات": "تأشيرات",
        "تأمين": "تأمين"
    }
    
    # Sort keys by length in descending order to match longer phrases first
    sorted_service_names = sorted(service_names_map.keys(), key=len, reverse=True)

    for service_key in sorted_service_names:
        if service_key in text:
            entities["service_name"] = service_names_map[service_key]
            break
    
    # Branch names
    branch_names = ["الدائري", "العيون", "فرع الدائري", "فرع العيون", "مكتب الدائري", "مكتب العيون"]
    for branch in branch_names:
        if branch in text:
            entities["branch_name"] = branch
            break

    # Extract name (simple regex for common Arabic names, needs refinement)
    name_match = re.search(r'(اسمي|أنا|اسمي هو|أدعى)\s+(.*?)(?=\s|$)', text)
    if name_match:
        entities["name"] = name_match.group(2).strip()

    # Extract phone number (simple regex for Saudi numbers)
    phone_match = re.search(r'(\+966|00966|966)?(5\d{8})', text)
    if phone_match:
        entities["phone"] = phone_match.group(2) # Extract only the 8 digits after 5

    # Extract date (simple regex for YYYY-MM-DD or DD-MM-YYYY)
    date_match = re.search(r'\d{4}-\d{2}-\d{2}|\d{2}-\d{2}-\d{4}', text)
    if date_match:
        entities["date"] = date_match.group(0)

    # Extract time (simple regex for HH:MM)
    time_match = re.search(r'\d{1,2}:\d{2}', text)
    if time_match:
        entities["time"] = time_match.group(0)

    return entities

# Function to save appointments
def save_appointment(appointment_details):
    try:
        with open(appointments_path, "r", encoding="utf-8") as f:
            appointments = json.load(f)
    except FileNotFoundError:
        appointments = []
    
    appointments.append(appointment_details)
    
    with open(appointments_path, "w", encoding="utf-8") as f:
        json.dump(appointments, f, ensure_ascii=False, indent=4)

def get_response(text):
    predicted_intent = model.predict([text])[0]
    entities = extract_entities(text)

    # Contact information to be included in general responses
    contact_info = "يمكنك التواصل معنا عبر الأرقام: مكتب الدائري: +966546206165، مكتب العيون: +966546448083 أو زيارة مواقعنا almsand.sa و almsand.net."

    # Rule-based response generation based on intent and extracted entities
    if predicted_intent == "greet":
        return random.choice([
            "أهلاً بك! كيف يمكنني مساعدتك؟",
            "مرحباً! أنا هنا لمساعدتك في أي استفسار.",
            "أهلاً وسهلاً! كيف يمكنني خدمتك؟",
            "مرحباً بك! كيف يمكنني أن أخدمك اليوم؟",
            "أهلاً! تفضل، كيف أستطيع مساعدتك؟",
            "مرحباً! ما الذي تبحث عنه اليوم?"
        ])
    elif predicted_intent == "goodbye":
        return random.choice([
            "مع السلامة! نتمنى لك يوماً سعيداً.",
            "إلى اللقاء! يسعدنا خدمتك.",
            "شكراً لتواصلك! نتمنى لك يوماً موفقاً.",
            "في أمان الله! نأمل أن نراك قريباً.",
            "وداعاً! لا تتردد في التواصل معنا مرة أخرى.",
            "إلى اللقاء! يسعدنا دائماً مساعدتك."
        ])
    elif predicted_intent == "ask_service_general":
        return random.choice([
            f"نقدم مجموعة واسعة من الخدمات. هل تبحث عن خدمة معينة؟ {contact_info}",
            f"لدينا العديد من الخدمات المتنوعة. يرجى تحديد نوع الخدمة التي تهتم بها أو زيارة موقعنا لمعرفة المزيد. {contact_info}",
            f"تفضل بزيارة مواقعنا almsand.sa و almsand.net للاطلاع على قائمة خدماتنا الشاملة. {contact_info}",
            f"خدماتنا تشمل الرخص التجارية، العقار، البرمجة، التصميم، الأمور الطلابية، المدارس، الإقامات، المرور، والجوازات. ما الذي يهمك تحديداً؟ {contact_info}"
        ])
    elif predicted_intent == "ask_contact_info":
        return random.choice([
            "يمكنك التواصل معنا عبر الأرقام التالية: مكتب الدائري: +966546206165، مكتب العيون: +966546448083. أو زيارة مواقعنا almsand.sa و almsand.net.",
            "أرقام التواصل هي: مكتب الدائري: +966546206165، مكتب العيون: +966546448083. كما يمكنك زيارة مواقعنا.",
            "للتواصل، يرجى الاتصال بأحد الأرقام المذكورة أو زيارة موقعنا الإلكتروني.",
            "يمكنك الاتصال بنا على +966546206165 لفرع الدائري، أو +966546448083 لفرع العيون."
        ])
    elif predicted_intent == "ask_branch_location":
        branch = entities.get("branch_name")
        if branch and ("الدائري" in branch or "مكتب الدائري" in branch or "فرع الدائري" in branch):
            return f"مكتب الدائري مختص في الرخص التجارية والعقار والبرمجة والتصميم والأمور الطلابية والمدارس. يمكنك زيارة almsand.net للمزيد من التفاصيل. {contact_info}"
        elif branch and ("العيون" in branch or "مكتب العيون" in branch or "فرع العيون" in branch):
            return f"مكتب العيون مختص في ما يتعلق بالدوائر الحكومية من إقامات ومرور وجوازات. يمكنك زيارة almsand.sa للمزيد من التفاصيل. {contact_info}"
        else:
            return random.choice([
                f"لدينا فرعان، أحدهما على الدائري والآخر على طريق العيون. أي فرع تبحث عنه؟ {contact_info}",
                f"يمكنك زيارة أحد فروعنا: فرع الدائري أو فرع العيون. ما هو الفرع الأقرب إليك؟ {contact_info}",
                f"فرع الدائري يقع على الدائري، وفرع العيون يقع على طريق العيون. {contact_info}"
            ])
    elif predicted_intent == "ask_service_specific":
        service = entities.get("service_name")
        if service:
            # RAG implementation
            if service in ["خدمات منصة ايجار", "خدمات حساب المواطن"]:
                scraped_services = get_almsand_sa_services()
                if service in scraped_services:
                    details = "\n- " + "\n- ".join(scraped_services[service])
                    return f"بالتأكيد، إليك تفاصيل خدمة {service} من موقعنا:\n{details}\n{contact_info}"
            elif service in ["تصميم تجربة المستخدم", "تطوير المواقع والتطبيقات", "التسويق الرقمي", "الاستضافة والسحابة", "بناء الهوية والعلامة", "الاستشارات الرقمية"]:
                scraped_services = get_almsand_net_services()
                if service in scraped_services:
                    details = "\n- " + "\n- ".join(scraped_services[service])
                    return f"بالتأكيد، إليك تفاصيل خدمة {service} من موقعنا:\n{details}\n{contact_info}"
            else:
                return random.choice([
                    f"بالتأكيد، يمكنني تزويدك بمعلومات عن خدمة {service}. ما هو سؤالك تحديداً؟ {contact_info}",
                    f"للحصول على تفاصيل حول خدمة {service}، يرجى تحديد استفسارك بشكل أدق. {contact_info}",
                    f"خدمة {service} متوفرة لدينا. ما الذي تود معرفته عنها؟ {contact_info}",
                    f"لتقديم معلومات دقيقة حول {service}، يرجى توضيح استفسارك. {contact_info}"
                ])
        else:
            return random.choice([
                f"ما هي الخدمة التي تستفسر عنها تحديداً؟ {contact_info}",
                f"يرجى تحديد الخدمة التي تود الاستفسار عنها. {contact_info}"
            ])
    elif predicted_intent == "book_appointment":
        name = entities.get("name")
        phone = entities.get("phone")
        service = entities.get("service_name")
        branch = entities.get("branch_name")
        date = entities.get("date")
        time = entities.get("time")

        if name and phone and service and branch and date and time:
            appointment_details = {
                "name": name,
                "phone": phone,
                "service": service,
                "branch": branch,
                "date": date,
                "time": time
            }
            save_appointment(appointment_details)
            return random.choice([
                f"تم حجز موعدك بنجاح يا {name} لخدمة {service} في فرع {branch} بتاريخ {date} الساعة {time}. سيتم التواصل معك قريباً لتأكيد الموعد. {contact_info}",
                f"مرحباً {name}، تم تأكيد موعدك لـ {service} في {branch} يوم {date} الساعة {time}. شكراً لك. {contact_info}",
                f"تم تسجيل موعدك يا {name} لخدمة {service} في فرع {branch} بتاريخ {date} الساعة {time}. ترقب رسالة تأكيد. {contact_info}"
            ])
        else:
            missing_info = []
            if not name: missing_info.append("الاسم")
            if not phone: missing_info.append("رقم الهاتف")
            if not service: missing_info.append("الخدمة المطلوبة")
            if not branch: missing_info.append("الفرع المفضل")
            if not date: missing_info.append("التاريخ المقترح")
            if not time: missing_info.append("الوقت المقترح")
            
            return random.choice([
                f"لحجز موعد، أحتاج إلى بعض المعلومات الإضافية: {', '.join(missing_info)}. يرجى تزويدي بها. {contact_info}",
                f"يرجى تزويدي بـ {', '.join(missing_info)}. لإتمام حجز الموعد. {contact_info}",
                f"لإتمام حجز موعدك، نحتاج إلى: {', '.join(missing_info)}. هل يمكنك تزويدنا بها؟ {contact_info}"
            ])
    elif predicted_intent == "cancel_appointment":
        return random.choice([
            f"لإلغاء موعدك، يرجى تزويدي برقم الموعد أو اسمك ورقم هاتفك لتحديد الموعد المراد إلغاؤه. {contact_info}",
            f"يمكنك إلغاء موعدك بتزويدنا بتفاصيل الحجز. {contact_info}",
            f"يرجى تزويدي بمعلومات الموعد الذي تود إلغاءه. {contact_info}",
            f"لإلغاء الحجز، أحتاج إلى رقم الموعد أو اسمك ورقم هاتفك. {contact_info}"
        ])
    elif predicted_intent == "modify_appointment":
        return random.choice([
            f"لتعديل موعدك، يرجى تزويدي برقم الموعد أو اسمك ورقم هاتفك، بالإضافة إلى التاريخ والوقت الجديد المقترح. {contact_info}",
            f"يمكنك تعديل موعدك بتزويدنا بتفاصيل الحجز والتاريخ والوقت الجديد. {contact_info}",
            f"للتعديل على موعدك، أحتاج إلى رقم الموعد والتاريخ والوقت الجديد. {contact_info}",
            f"يرجى تزويدي بتفاصيل موعدك الحالي والتاريخ والوقت الجديد الذي تفضله. {contact_info}"
        ])
    elif predicted_intent == "new_customer_inquiry":
        return random.choice([
            f"أهلاً بك عميلنا الجديد! يسعدنا مساعدتك. ما هو استفسارك الأول؟ {contact_info}",
            f"مرحباً بك في المساند! كيف يمكنني مساعدتك اليوم؟ {contact_info}",
            f"يسعدنا انضمامك إلينا. ما الذي تود معرفته؟ {contact_info}",
            f"أهلاً بك! ما هو السؤال الذي يدور في ذهنك كعميل جديد؟ {contact_info}"
        ])
    elif predicted_intent == "ask_price":
        service = entities.get("service_name")
        if service:
            return random.choice([
                f"تختلف تكلفة خدمة {service} حسب التفاصيل. يرجى التواصل معنا على الأرقام المذكورة أو زيارة أحد فروعنا للحصول على عرض سعر دقيق. {contact_info}",
                f"للحصول على سعر دقيق لخدمة {service}, يرجى الاتصال بنا أو زيارة أحد فروعنا. {contact_info}",
                f"تعتمد تكلفة {service} على المتطلبات. يرجى التواصل للحصول على عرض سعر. {contact_info}",
                f"يرجى الاتصال بنا أو زيارة أحد فروعنا للحصول على تفاصيل الأسعار لخدمة {service}. {contact_info}"
            ])
        else:
            return random.choice([
                f"ما هي الخدمة التي تود الاستفسار عن تكلفتها؟ {contact_info}",
                f"يرجى تحديد الخدمة لمعرفة تكلفتها. {contact_info}"
            ])
    elif predicted_intent == "ask_requirements":
        service = entities.get("service_name")
        if service:
            return random.choice([
                f"متطلبات خدمة {service} تختلف. يرجى تزويدي بمزيد من التفاصيل أو التواصل معنا مباشرة. {contact_info}",
                f"للحصول على قائمة المتطلبات لخدمة {service}, يرجى التواصل مع الفرع المختص أو زيارة موقعنا. {contact_info}",
                f"يرجى التواصل معنا لتزويدك بقائمة المتطلبات الدقيقة لخدمة {service}. {contact_info}",
                f"تختلف متطلبات {service} حسب الحالة. يرجى الاتصال بنا للحصول على التفاصيل. {contact_info}"
            ])
        else:
            return random.choice([
                f"ما هي الخدمة التي تود معرفة متطلباتها؟ {contact_info}",
                f"يرجى تحديد الخدمة لمعرفة متطلباتها. {contact_info}"
            ])
    elif predicted_intent == "ask_working_hours":
        return random.choice([
            f"مكاتبنا تعمل من الأحد إلى الخميس من الساعة 9 صباحاً حتى 5 مساءً. {contact_info}",
            f"ساعات العمل من الأحد إلى الخميس، من 9 صباحاً إلى 5 مساءً. {contact_info}",
            f"نعمل من الأحد إلى الخميس، من التاسعة صباحاً حتى الخامسة مساءً. {contact_info}",
            f"أوقات عملنا هي من الأحد إلى الخميس، من 9 صباحاً إلى 5 مساءً. {contact_info}"
        ])
    elif predicted_intent == "confirm_action":
        return random.choice([
            "شكراً لتأكيدك.",
            "حسناً، تم التأكيد.",
            "مفهوم، شكراً لك.",
            "تم التأكيد بنجاح."
        ])
    elif predicted_intent == "deny_action":
        return random.choice([
            "حسناً، لا مشكلة. هل يمكنني مساعدتك في شيء آخر؟",
            "مفهوم. هل هناك أي شيء آخر يمكنني تقديمه لك؟",
            "لا بأس. هل لديك استفسار آخر؟",
            "حسناً. هل يمكنني تقديم مساعدة أخرى؟"
        ])
    else:
        return random.choice([
            f"عذراً، لم أفهم سؤالك. هل يمكنك توضيح ما تبحث عنه؟ {contact_info}",
            f"لم أتمكن من فهم طلبك. يرجى إعادة صياغة السؤال. {contact_info}",
            f"أعتذر، لم أفهم. هل يمكنك طرح السؤال بطريقة أخرى؟ {contact_info}"
        ])


