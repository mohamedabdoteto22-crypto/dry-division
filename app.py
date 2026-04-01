import streamlit as st
import google.generativeai as genai
from PIL import Image
from datetime import date, timedelta
import pandas as pd

# 1. إعدادات الصفحة والتصميم
st.set_page_config(page_title="DRY_DIVISION PRO", page_icon="⚔️", layout="wide")

# 2. الموسيقى التحفيزية
def add_bg_music(url):
    st.markdown(
        f"""
        <iframe src="{url}" allow="autoplay" style="display:none"></iframe>
        <audio autoplay loop><source src="{url}" type="audio/mp3"></audio>
        """, 
        unsafe_allow_html=True
    )

add_bg_music("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")

# 3. إعداد الذكاء الاصطناعي (Gemini) - تم تحديث طريقة الاستدعاء لتجنب الخطأ
API_KEY = "AIzaSyBBeoQqdGZbG8j66oLBJ6kEc89uucAnUY8"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# 4. إدارة الحسابات
if 'user_db' not in st.session_state:
    st.session_state['user_db'] = {} 
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# واجهة تسجيل الدخول
if not st.session_state['logged_in']:
    st.title("⚔️ DRY_DIVISION ⚡ مركز العمليات")
    tab1, tab2 = st.tabs(["تسجيل الدخول 🔑", "إنشاء حساب محارب 🛡️"])
    
    with tab1:
        u = st.text_input("اسم المستخدم")
        p = st.text_input("كلمة المرور", type='password')
        if st.button("دخول"):
            if u in st.session_state['user_db'] and st.session_state['user_db'][u]['password'] == p:
                st.session_state['logged_in'] = True
                st.session_state['current_user'] = u
                st.rerun()
            else:
                st.error("بيانات الدخول خاطئة")
                
    with tab2:
        nu = st.text_input("اسم مستخدم جديد")
        np = st.text_input("كلمة مرور جديدة", type='password')
        if st.button("تفعيل الحساب الجديد"):
            if nu and np:
                st.session_state['user_db'][nu] = {
                    'password': np,
                    'start_date': date.today(),
                    'is_pro': False,
                    'weight_history': {},
                    'user_info': {} 
                }
                st.success("تم إنشاء الحساب! سجل دخولك الآن.")
    st.stop()

# بيانات المستخدم الحالي
current_user = st.session_state['current_user']
user_profile = st.session_state['user_db'][current_user]
days_active = (date.today() - user_profile['start_date']).days
is_trial_active = days_active < 6

# 5. القائمة الجانبية
with st.sidebar:
    st.title("DRY_DIVISION PRO")
    st.write(f"المحارب: **{current_user}**")
    if user_profile['is_pro']:
        st.success("الاشتراك: PRO فعال ✅")
    elif is_trial_active:
        st.warning(f"متبقي {6 - days_active} أيام تجريبية")
    else:
        st.error("انتهت الفترة التجريبية ⚠️")
    
    menu = ["الملف الشخصي 👤", "بروفايل التطور 📊", "ماسح الوجبات AI 🍎", "التحليل البدني 💪", "خطة التغذية AI 🥗", "خطط الاشتراك 💳", "الدعم الفني 📞"]
    choice = st.selectbox("القائمة", menu)
    if st.button("تسجيل الخروج"):
        st.session_state['logged_in'] = False
        st.rerun()

# --- التنفيذ ---

if choice == "الملف الشخصي 👤":
    st.header("👤 إعدادات البيانات الشخصية")
    col1, col2 = st.columns(2)
    with col1:
        u_age = st.number_input("السن", 10, 100, 25)
        u_height = st.number_input("الطول (سم)", 100, 250, 170)
    with col2:
        u_weight = st.number_input("الوزن (كجم)", 30.0, 250.0, 75.0)
        u_goal = st.selectbox("الهدف البدني", ["تنشيف عالي", "ضخامة صافية", "تحسين لياقة", "خسارة وزن"])
    if st.button("حفظ البيانات"):
        user_profile['user_info'] = {"age": u_age, "height": u_height, "weight": u_weight, "goal": u_goal}
        st.success("تم الحفظ!")

elif choice == "بروفايل التطور 📊":
    st.header("📊 تتبع الوزن")
    w = st.number_input("سجل وزنك اليوم", 30.0, 250.0)
    if st.button("حفظ"):
        user_profile['weight_history'][str(date.today())] = w
        st.success("تم التحديث")
    if user_profile['weight_history']:
        st.line_chart(pd.DataFrame.from_dict(user_profile['weight_history'], orient='index', columns=['Weight']))

elif choice == "الدعم الفني 📞":
    st.header("📞 التواصل مع الإدارة")
    st.markdown(f"- **واتساب:** [01141930176](https://wa.me/201141930176)\n- **إنستا:** [@Mohamed_36do](https://instagram.com/Mohamed_36do)\n- **إيميل:** mohmaedabsoteto22@gmail.com")

elif choice == "خطط الاشتراك 💳":
    st.header("💎 خطط العضوية")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("شهري", "5$")
    c2.metric("3 أشهر", "12$")
    c3.metric("6 أشهر", "28.99$")
    c4.metric("سنوي", "59.99$")
    st.markdown(f"**فودافون كاش:** `01002884985` | **إنستا باي:** `01141930176`")
    st.file_uploader("ارفع إيصال التحويل", type=["jpg", "png"])

# حماية ومعالجة الـ AI (تم إصلاح منطق إرسال الصور هنا)
else:
    if not user_profile['is_pro'] and not is_trial_active:
        st.error("❌ انتهت الفترة المجانية. يرجى الاشتراك.")
    else:
        u_info = str(user_profile.get('user_info', 'بيانات عامة'))
        img_input = st.file_uploader("ارفع الصورة للتحليل", type=["jpg", "png", "jpeg"])
        
        if img_input and st.button("بدء التحليل الذكي ✨"):
            with st.spinner("جاري التواصل مع الذكاء الاصطناعي..."):
                try:
                    # تحويل الصورة لتنسيق متوافق مع الموديل لتجنب NotFound
                    image_parts = Image.open(img_input)
                    
                    if choice == "ماسح الوجبات AI 🍎":
                        prompt = f"حلل السعرات والماكروز لهذه الوجبة بناءً على بيانات المستخدم: {u_info}"
                    elif choice == "التحليل البدني 💪":
                        prompt = f"حلل المستوى البدني ونقاط الضعف بناءً على: {u_info}"
                    else:
                        prompt = f"صمم نظام غذائي كامل بناءً على الـ InBody المرفق وبيانات: {u_info}"
                    
                    # إرسال الطلب بشكل سليم
                    response = model.generate_content([prompt, image_parts])
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"حدث خطأ: {e}")
                    st.info("حاول رفع الصورة مرة أخرى أو تأكد من جودة الاتصال.")
