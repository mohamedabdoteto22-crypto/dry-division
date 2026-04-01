import streamlit as st
import google.generativeai as genai
from PIL import Image
from datetime import date, timedelta
import pandas as pd

# 1. إعدادات الصفحة والتصميم الملكي
st.set_page_config(page_title="DRY_DIVISION PRO", page_icon="⚔️", layout="wide")

# 2. وظيفة تشغيل الموسيقى التحفيزية (تأكد من وجود إنترنت لعمل الرابط)
def add_bg_music(url):
    st.markdown(
        f"""
        <iframe src="{url}" allow="autoplay" style="display:none"></iframe>
        <audio autoplay loop><source src="{url}" type="audio/mp3"></audio>
        """, 
        unsafe_allow_html=True
    )

add_bg_music("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")

# 3. إعداد الذكاء الاصطناعي (Gemini) - إصدار 1.5 فلاش المستقر
API_KEY = "AIzaSyBBeoQqdGZbG8j66oLBJ6kEc89uucAnUY8"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# 4. بيانات المطور (Admin) - الدخول من أي جهاز
ADMIN_USER = "admin_mohamed"
ADMIN_PASS = "mohamed_dev_2026"

# 5. إدارة الجلسة والحسابات
if 'user_db' not in st.session_state:
    st.session_state['user_db'] = {} 
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# --- واجهة تسجيل الدخول ---
if not st.session_state['logged_in']:
    st.title("⚔️ DRY_DIVISION ⚡ COMMAND CENTER")
    tab1, tab2 = st.tabs(["تسجيل الدخول 🔑", "إنشاء حساب محارب 🛡️"])
    
    with tab1:
        u_input = st.text_input("اسم المستخدم").strip()
        p_input = st.text_input("كلمة المرور", type='password').strip()
        
        if st.button("دخول"):
            # التحقق من الأدمن (الأولوية القصوى)
            if u_input == ADMIN_USER and p_input == ADMIN_PASS:
                st.session_state['logged_in'] = True
                st.session_state['current_user'] = u_input
                st.session_state['is_admin'] = True
                st.success("أهلاً بك يا قائد محمد! تم الدخول بصلاحيات المطور.")
                st.rerun()
            
            # التحقق من المستخدمين العاديين
            elif u_input in st.session_state['user_db']:
                if st.session_state['user_db'][u_input]['password'] == p_input:
                    st.session_state['logged_in'] = True
                    st.session_state['current_user'] = u_input
                    st.session_state['is_admin'] = False
                    st.rerun()
                else:
                    st.error("كلمة المرور خاطئة!")
            else:
                st.error("هذا الحساب غير موجود.. يرجى إنشاء حساب جديد.")
                
    with tab2:
        nu = st.text_input("اسم مستخدم جديد").strip()
        np = st.text_input("كلمة مرور جديدة", type='password').strip()
        if st.button("تفعيل الحساب"):
            if nu and np:
                st.session_state['user_db'][nu] = {
                    'password': np,
                    'start_date': date.today(),
                    'is_pro': False,
                    'weight_history': {},
                    'user_info': {} 
                }
                st.success("تم إنشاء الحساب بنجاح! يمكنك الدخول الآن.")
    st.stop()

# --- بعد تسجيل الدخول بنجاح ---
current_user = st.session_state['current_user']
is_admin = st.session_state.get('is_admin', False)

# تحديد حالة الحساب
if is_admin:
    is_pro = True
    days_active = 0
    is_trial_active = True
else:
    user_profile = st.session_state['user_db'][current_user]
    days_active = (date.today() - user_profile['start_date']).days
    is_trial_active = days_active < 6
    is_pro = user_profile['is_pro']

# 6. القائمة الجانبية (Sidebar)
with st.sidebar:
    st.title("DRY_DIVISION PRO")
    if is_admin: st.info("وضع المطور: نشط 🛠️")
    st.write(f"المحارب: **{current_user}**")
    
    if is_pro or is_admin:
        st.success("الحساب: PREMIUM ✅")
    elif is_trial_active:
        st.warning(f"تجربة: متبقي {6 - days_active} أيام")
    else:
        st.error("انتهت الفترة التجريبية ⚠️")
    
    menu = ["الملف الشخصي 👤", "بروفايل التطور 📊", "ماسح الوجبات AI 🍎", "التحليل البدني 💪", "خطة التغذية AI 🥗", "خطط الاشتراك 💳", "الدعم الفني 📞"]
    choice = st.selectbox("اختر المهمة", menu)
    if st.button("تسجيل الخروج"):
        st.session_state['logged_in'] = False
        st.rerun()

# --- الأقسام الوظيفية ---

if choice == "الملف الشخصي 👤":
    st.header("👤 بياناتك البدنية")
    u_age = st.number_input("السن", 10, 100, 25)
    u_height = st.number_input("الطول (سم)", 100, 250, 170)
    u_weight = st.number_input("الوزن (كجم)", 30.0, 250.0, 75.0)
    u_goal = st.selectbox("هدفك الحالي", ["تنشيف عالي", "ضخامة صافية", "خسارة دهون", "تحسين لياقة"])
    if st.button("حفظ البيانات"):
        if not is_admin:
            user_profile['user_info'] = {"age": u_age, "height": u_height, "weight": u_weight, "goal": u_goal}
        st.success("تم الحفظ بنجاح!")

elif choice == "بروفايل التطور 📊":
    st.header("📊 تتبع الوزن")
    w = st.number_input("سجل وزن اليوم", 30.0, 250.0)
    if st.button("تحديث السجل"):
        if not is_admin:
            user_profile['weight_history'][str(date.today())] = w
        st.success("تم التحديث")
    if not is_admin and user_profile['weight_history']:
        df = pd.DataFrame.from_dict(user_profile['weight_history'], orient='index', columns=['Weight'])
        st.line_chart(df)

elif choice == "الدعم الفني 📞":
    st.header("📞 تواصل مع القائد محمد")
    st.markdown(f"""
    - **واتساب:** [01141930176](https://wa.me/201141930176)
    - **إنستجرام:** [@Mohamed_36do](https://instagram.com/Mohamed_36do)
    - **إيميل:** mohmaedabsoteto22@gmail.com
    """)

elif choice == "خطط الاشتراك 💳":
    st.header("💎 تطوير العضوية")
    st.write("الأسعار الحالية:")
    st.write("1. شهري: **5$** | 2. ثلاث أشهر: **12$**")
    st.write("3. ستة أشهر: **28.99$** | 4. سنوي: **59.99$**")
    st.markdown("---")
    st.subheader("💳 الدفع داخل مصر")
    st.success("📱 فودافون كاش: `01002884985`")
    st.info("⚡ إنستا باي: `01141930176`")
    st.file_uploader("ارفع صورة التحويل لتفعيل الـ PRO", type=["jpg", "png"])

# --- معالجة الـ AI (ماسح الوجبات، التحليل البدني، التغذية) ---
else:
    if not is_admin and not is_pro and not is_trial_active:
        st.error("❌ انتهت الـ 6 أيام التجريبية. يرجى الاشتراك لفتح خدمات الـ AI.")
    else:
        # استرجاع سياق بيانات المستخدم لتقديم تحليل دقيق
        u_context = "مستخدم رياضي" if is_admin else str(user_profile.get('user_info', 'بيانات عامة'))
        
        img_input = st.file_uploader("ارفع الصورة للتحليل بواسطة AI", type=["jpg", "png", "jpeg"])
        
        if img_input and st.button("بدء التحليل ✨"):
            with st.spinner("جاري التواصل مع الأقمار الصناعية للذكاء الاصطناعي..."):
                try:
                    # إصلاح خطأ NotFound بتحويل الصورة بشكل سليم
                    image_data = Image.open(img_input)
                    
                    if choice == "ماسح الوجبات AI 🍎":
                        prompt = f"بناءً على بيانات المستخدم ({u_context})، حلل السعرات الحرارية والماكروز في هذه الوجبة وقدم نصيحة."
                    elif choice == "التحليل البدني 💪":
                        prompt = f"حلل المستوى البدني، ونسبة الدهون التقريبية، ونقاط الضعف العضلية بناءً على الصورة وبيانات: {u_context}."
                    else: # خطة التغذية
                        prompt = f"بناءً على صورة الـ InBody المرفقة وبيانات {u_context}، صمم نظاماً غذائياً كاملاً ليوم واحد."
                    
                    # إرسال الطلب للموديل
                    response = model.generate_content([prompt, image_data])
                    st.markdown("### 🤖 تقرير الذكاء الاصطناعي:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"عذراً، حدث خطأ تقني: {e}")
                    st.info("تأكد من أن الصورة واضحة أو حاول مرة أخرى.")
