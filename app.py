import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
from datetime import date

# 1. إعدادات الصفحة
st.set_page_config(page_title="DRY_DIVISION PRO 2026", page_icon="⚔️", layout="wide")

# 2. الموسيقى التحفيزية
st.markdown(
    f"""
    <iframe src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" allow="autoplay" style="display:none"></iframe>
    <audio autoplay loop><source src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" type="audio/mp3"></audio>
    """, 
    unsafe_allow_html=True
)

# 3. إعداد الذكاء الاصطناعي - تعديل جوهري لحل خطأ 404
API_KEY = "AIzaSyBBeoQqdGZbG8j66oLBJ6kEc89uucAnUY8"
genai.configure(api_key=API_KEY)

# وظيفة ذكية لاختيار أفضل موديل متاح في السيرفر
def get_best_model():
    try:
        # نحاول أولاً استخدام النسخة الأحدث لعام 2026
        return genai.GenerativeModel('gemini-2.0-flash')
    except:
        try:
            # إذا لم تكن متاحة، نستخدم النسخة المستقرة الأكثر شهرة
            return genai.GenerativeModel('gemini-1.5-flash-latest')
        except:
            # الحل الأخير لضمان عدم توقف البرنامج
            return genai.GenerativeModel('gemini-1.5-flash')

model = get_best_model()

# 4. بيانات المطور (Admin)
ADMIN_USER = "admin_mohamed"
ADMIN_PASS = "mohamed_dev_2026"

# 5. إدارة الحسابات والجلسة
if 'user_db' not in st.session_state:
    st.session_state['user_db'] = {} 
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# --- واجهة تسجيل الدخول ---
if not st.session_state['logged_in']:
    st.title("⚔️ DRY_DIVISION ⚡ COMMAND CENTER")
    t1, t2 = st.tabs(["تسجيل الدخول 🔑", "إنشاء حساب محارب 🛡️"])
    
    with t1:
        u = st.text_input("اسم المستخدم").strip()
        p = st.text_input("كلمة المرور", type='password').strip()
        if st.button("دخول"):
            if u == ADMIN_USER and p == ADMIN_PASS:
                st.session_state['logged_in'] = True
                st.session_state['current_user'] = u
                st.session_state['is_admin'] = True
                st.rerun()
            elif u in st.session_state['user_db'] and st.session_state['user_db'][u]['password'] == p:
                st.session_state['logged_in'] = True
                st.session_state['current_user'] = u
                st.session_state['is_admin'] = False
                st.rerun()
            else:
                st.error("بيانات الدخول غير صحيحة")
                
    with t2:
        nu = st.text_input("اسم مستخدم جديد").strip()
        np = st.text_input("كلمة مرور جديدة", type='password').strip()
        if st.button("تفعيل الحساب"):
            if nu and np:
                st.session_state['user_db'][nu] = {
                    'password': np, 'start_date': date.today(),
                    'is_pro': False, 'weight_history': {}, 'user_info': {}
                }
                st.success("تم إنشاء الحساب!")
    st.stop()

# --- بعد تسجيل الدخول ---
current_user = st.session_state['current_user']
is_admin = st.session_state.get('is_admin', False)

if is_admin:
    is_pro, days_active, is_trial_active = True, 0, True
else:
    user_profile = st.session_state['user_db'][current_user]
    days_active = (date.today() - user_profile['start_date']).days
    is_trial_active = days_active < 6
    is_pro = user_profile['is_pro']

# 6. القائمة الجانبية
with st.sidebar:
    st.title("DRY_DIVISION PRO")
    if is_admin: st.info("وضع المطور نشط 🛠️")
    st.write(f"المحارب: **{current_user}**")
    status = "PREMIUM ✅" if (is_pro or is_admin) else (f"تجربة: {6-days_active} يوم" if is_trial_active else "منتهي ⚠️")
    st.markdown(f"الحالة: **{status}**")
    
    menu = ["الملف الشخصي 👤", "بروفايل التطور 📊", "ماسح الوجبات AI 🍎", "التحليل البدني 💪", "خطة التغذية AI 🥗", "خطط الاشتراك 💳", "الدعم الفني 📞"]
    choice = st.selectbox("القائمة", menu)
    if st.button("تسجيل الخروج"):
        st.session_state['logged_in'] = False
        st.rerun()

# --- الأقسام الوظيفية ---
if choice == "الملف الشخصي 👤":
    st.header("👤 إعدادات البيانات الشخصية")
    age = st.number_input("السن", 10, 100, 25)
    height = st.number_input("الطول (سم)", 100, 250, 170)
    weight = st.number_input("الوزن (كجم)", 30.0, 250.0, 70.0)
    goal = st.selectbox("الهدف", ["تنشيف عالي", "ضخامة صافية", "خسارة وزن"])
    if st.button("حفظ البيانات"):
        if not is_admin: user_profile['user_info'] = {"age": age, "height": height, "weight": weight, "goal": goal}
        st.success("تم الحفظ!")

elif choice == "خطط الاشتراك 💳":
    st.header("💎 خطط العضوية PRO")
    st.success("📱 فودافون كاش: 01002884985")
    st.info("⚡ إنستا باي: 01141930176")

elif choice == "الدعم الفني 📞":
    st.markdown("- **واتساب:** [01141930176](https://wa.me/201141930176)")

# --- معالجة الـ AI المستقرة ---
else:
    if not is_admin and not is_pro and not is_trial_active:
        st.error("❌ انتهت الفترة المجانية.")
    else:
        u_ctx = "مستخدم رياضي محترف" if is_admin else str(user_profile.get('user_info', 'بيانات عامة'))
        img_file = st.file_uploader("ارفع الصورة للتحليل", type=["jpg", "png", "jpeg"])
        
        if img_file and st.button("بدء التحليل ✨"):
            with st.spinner("جاري التواصل مع الذكاء الاصطناعي..."):
                try:
                    img_data = Image.open(img_file).convert("RGB")
                    
                    prompts = {
                        "ماسح الوجبات AI 🍎": f"حلل السعرات والماكروز لهذه الوجبة للمستخدم: {u_ctx}",
                        "التحليل البدني 💪": f"حلل المستوى البدني ونسبة الدهون من الصورة بناءً على: {u_ctx}",
                        "خطة التغذية AI 🥗": f"صمم نظام غذائي كامل بناءً على الـ InBody المرفق وبيانات: {u_ctx}"
                    }
                    
                    # استدعاء الموديل المختار
                    response = model.generate_content([prompts[choice], img_data])
                    st.markdown("### 🤖 تقرير DRY_DIVISION:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"خطأ تقني: {e}")
