import requests
from bs4 import BeautifulSoup
import json

def get_almsand_sa_services():
    """
    استخراج خدمات موقع almsand.sa
    """
    services = {}
    
    # خدمات منصة ايجار
    services['خدمات منصة ايجار'] = [
        "انشاء حسابات سكنية وتجارية.",
        "انشاء عقود تجارية وسكنية.",
        "توثيق العقود الإلكترونية.",
        "تنظيم القطاع الايجار للعقاري.",
        "ادارة الاملاك."
    ]
    
    # خدمات حساب المواطن
    services['خدمات حساب المواطن'] = [
        "نقدم خدمات متكاملة لحساب المواطن لمساعدتك في التسجيل، تحديث البيانات، وضمان استمرارية الدعم بكل سهولة.",
        "نساعد في مراجعة الأهلية، تقديم الاعتراضات، وإدارة الحساب لضمان حصولك على الاستحقاق المالي المستحق.",
        "نقوم بمتابعة حالة الطلبات وتقديم الحلول لأي مشكلات تواجهك في المنصة الرسمية لحساب المواطن.",
        "هدفنا هو تسهيل الإجراءات وضمان استفادتك من الدعم الحكومي بكل دقة وسرعة."
    ]
    
    return services

def get_almsand_net_services():
    """
    استخراج خدمات موقع almsand.net
    """
    services = {}
    
    # تصميم تجربة المستخدم
    services['تصميم تجربة المستخدم'] = [
        "تصميم واجهات المستخدم (UI)",
        "تصميم تجربة المستخدم (UX)",
        "هوية بصرية متكاملة",
        "تصميم الشعارات والعلامات"
    ]
    
    # تطوير المواقع والتطبيقات
    services['تطوير المواقع والتطبيقات'] = [
        "تطوير مواقع الويب",
        "تطبيقات الجوال",
        "حلول التجارة الإلكترونية",
        "أنظمة إدارة المحتوى"
    ]
    
    # التسويق الرقمي
    services['التسويق الرقمي'] = [
        "تحسين محركات البحث (SEO)",
        "إعلانات وسائل التواصل",
        "إدارة المحتوى الرقمي",
        "تحليل البيانات والأداء"
    ]
    
    # الاستضافة والسحابة
    services['الاستضافة والسحابة'] = [
        "استضافة مشتركة ومخصصة",
        "حلول السحابة الإلكترونية",
        "إدارة الخوادم والسيرفرات",
        "حماية وأمان متكامل"
    ]
    
    # بناء الهوية والعلامة
    services['بناء الهوية والعلامة'] = [
        "استراتيجية العلامة التجارية",
        "تصميم الشعار والهوية",
        "أدلة العلامة التجارية",
        "مواد تسويقية متكاملة"
    ]
    
    # الاستشارات الرقمية
    services['الاستشارات الرقمية'] = [
        "استراتيجيات التحول الرقمي",
        "تحليل وتقييم الوضع الحالي",
        "خطط تنفيذية مفصلة",
        "متابعة وتقييم الأداء"
    ]
    
    return services

def get_live_website_content(url):
    """
    استخراج المحتوى المباشر من الموقع
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # استخراج النصوص الرئيسية
        content = {
            'title': soup.title.string if soup.title else '',
            'headings': [h.get_text().strip() for h in soup.find_all(['h1', 'h2', 'h3', 'h4'])],
            'paragraphs': [p.get_text().strip() for p in soup.find_all('p') if p.get_text().strip()],
            'lists': [li.get_text().strip() for li in soup.find_all('li') if li.get_text().strip()]
        }
        
        return content
    except Exception as e:
        print(f"خطأ في استخراج المحتوى من {url}: {e}")
        return None

if __name__ == "__main__":
    print("استخراج خدمات almsand.sa...")
    almsand_sa_services = get_almsand_sa_services()
    for service_name, details in almsand_sa_services.items():
        print(f"\nخدمة: {service_name}")
        for detail in details:
            print(f"- {detail}")

    print("\n" + "="*50)
    print("استخراج خدمات almsand.net...")
    almsand_net_services = get_almsand_net_services()
    for service_name, details in almsand_net_services.items():
        print(f"\nخدمة: {service_name}")
        for detail in details:
            print(f"- {detail}")

