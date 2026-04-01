import streamlit as st
import google.generativeai as genai
from PIL import Image
import json
import os
from datetime import date
import random

# 1. إعدادات الصفحة (التصميم العالمي)
st.set_page_config(page_title="DRY_DIVISION PRO 2026", page_icon="⚔️", layout="wide")

# 2. نظام قاعدة البيانات الدائمة (JSON)
DB_FILE = "dry_division_db.json"

def load_database():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_database(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

if 'user_db' not in st.session_state:
    st.session_state['user_db'] = load_database()

# 3. إعداد الذكاء الاصطناعي (المحرك المقاوم للأعطال)
API_KEY = "AIzaSyBBeoQqdGZbG8j66oLBJ6kEc89uucAnUY8"
genai.configure(api_key=API_KEY)

def smart_ai_analysis(image, mode):
    # محاولة التبديل بين الموديلات لتجنب الـ 429 والـ 404
    available_models = ['gemini-1.5-flash', 'gemini-1.5-pro']
    
    prompts = {
        "ماسح الوجبات AI 🍎": "أنت خبير تغذية عالمي. حلل مكونات الوجبة، السعرات، والماكروز (بروتين، كارب، دهون) بدقة عالية.",
        "التحليل البدني 💪": "أنت خبير كمال أجسام. حلل صورة الجسم أو الـ InBody المرفقة، وقدر نسبة الدهون والكتلة العضلية.",
    }
    
    for model_name in available_models:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content([prompts.get(mode, "تحليل رياضي"), image])
            return response.text
        except:
            continue # جرب الموديل التالي إذا فشل الحالي
            
    return "❌ عذراً يا قائد، السيرفرات مضغوطة حالياً. يرجى المحاولة مرة أخرى بعد 30 ثانية."

# 4. واجهة تسجيل الدخول والتحقق
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.title("⚔️ DRY_DIVISION ⚡ COMMAND CENTER 2026")
    tab1, tab2 = st.tabs(["دخول المحاربين 🔑", "إنشاء حساب جديد 🛡️"])
    
    with tab1:
        u = st.text_input("اسم المستخدم").strip()
        p = st.text_input("كلمة المرور", type='password').strip()
        if st.button("دخول"):
            if u == "admin_mohamed" and p == "mohamed_dev_2026":
                st.session_state['logged_in'], st.session_state['current_user'], st.session_state['is_admin'] = True, u, True
                st.rerun()
            elif u in st.session_state['user_db'] and st.session_state['user_db'][u]['password'] == p:
                st.session_state['logged_in'], st.session_state['current_user'], st.session_state['is_admin'] = True, u, False
                st.rerun()
            else:
                st.error("بيانات الدخول غير صحيحة")
    
    with tab2:
        nu = st.text_input("اختر اسم مستخدم").strip()
        np = st.text_input("اختر كلمة مرور", type='password').strip()
        if st.button("تفعيل الحساب"):
            if nu and np:
                st.session_state['user_db'][nu] = {'password': np, 'is_pro': False, 'reg_date': str(date.today())}
                save_database(st.session_state['user_db'])
                st.success("تم إنشاء الحساب! سجل دخولك الآن.")
    st.stop()

# --- بعد تسجيل الدخول ---
user = st.session_state['current_user']
is_admin = st.session_state['is_admin']
is_pro = st.session_state['user_db'].get(user, {}).get('is_pro', False)

# 5. القائمة الجانبية (Sidebar)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1042/1042310.png", width=100)
    st.title("DRY_DIVISION")
    status = "👑 PREMIUM" if (is_admin or is_pro) else "🆓 TRIAL"
    st.markdown(f"المحارب: **{user}** | الحالة: `{status}`")
    
    menu = ["الملف الشخصي 👤", "ماسح الوجبات AI 🍎", "التحليل البدني 💪", "خطط الاشتراك 💳", "الدعم الفني 📞"]
    choice = st.selectbox("انتقل إلى", menu)
    
    st.markdown("---")
    st.subheader("🎵 راديو الحماس")
    st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
    
    if st.button("تسجيل الخروج"):
        st.session_state['logged_in'] = False
        st.rerun()

# --- الأقسام الوظيفية ---

if choice == "خطط الاشتراك 💳":
    st.header("💎 باقات النخبة المتاحة")
    c1, c2, c3 = st.columns(3)
    wa_link = "https://wa.me/201141930176?text=أريد_الاشتراك_في_"
    
    with c1:
        st.info("### 🥉 باقة المحارب\n**5$ / شهرياً**")
        st.write("- تحليل وجبات يومي\n- دعم فني واتساب")
        st.markdown(f'<a href="{wa_link}باقة_المحارب" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:10px; border-radius:5px; cursor:pointer;">اشترك فودافون كاش</button></a>', unsafe_allow_html=True)
    
    with c2:
        st.success("### 🥈 باقة الوحش\n**12$ / 3 أشهر**")
        st.write("- مميزات المحارب\n- خطط تغذية مخصصة")
        st.markdown(f'<a href="{wa_link}باقة_الوحش" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:10px; border-radius:5px; cursor:pointer;">اشترك فودافون كاش</button></a>', unsafe_allow_html=True)
        
    with c3:
        st.warning("### 🥇 الباقة الملكية\n**59$ / سنوياً**")
        st.write("- وصول كامل غير محدود\n- استشارات مباشرة")
        st.markdown(f'<a href="{wa_link}الباقة_الملكية" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:10px; border-radius:5px; cursor:pointer;">اشترك فودافون كاش</button></a>', unsafe_allow_html=True)

elif choice == "الدعم الفني 📞":
    st.header("📞 مركز دعم المحاربين")
    st.write("إذا واجهت أي مشكلة تقنية أو تريد تفعيل اشتراكك، تواصل معنا فوراً:")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(f"""
        ### 📧 البريد الإلكتروني
        **[mohamedabdoteto22@gmail.com](mailto:mohamedabdoteto22@gmail.com)**
        """)
        st.button("إرسال إيميل مباشر", on_click=lambda: st.write("جاري فتح تطبيق الإيميل..."))
        
    with col_b:
        st.markdown(f"""
        ### 📸 إنستجرام
        **[@mohamed_36do](https://instagram.com/mohamed_36do)**
        """)
        st.markdown(f'<a href="https://instagram.com/mohamed_36do" target="_blank"><button style="width:100%; background-color:#E1306C; color:white; border:none; padding:10px; border-radius:5px;">زيارة البروفايل</button></a>', unsafe_allow_html=True)

    st.markdown("---")
    st.success("📱 رقم الواتساب المباشر: **01141930176**")

elif choice in ["ماسح الوجبات AI 🍎", "التحليل البدني 💪"]:
    st.header(choice)
    if not is_admin and not is_pro:
        st.warning("🔒 هذا القسم مخصص لمشتركي PRO. يرجى التوجه لقسم الاشتراكات لتفعيل حسابك.")
    else:
        uploaded_file = st.file_uploader("ارفع الصورة هنا للتحليل الذكي", type=['jpg', 'jpeg', 'png'])
        if uploaded_file and st.button("بدء التحليل الاحترافي ✨"):
            with st.spinner("جاري التواصل مع الذكاء الاصطناعي..."):
                img = Image.open(uploaded_file).convert("RGB")
                result = smart_ai_analysis(img, choice)
                st.markdown("### 🤖 تقرير DRY_DIVISION AI:")
                st.info(result)

elif choice == "الملف الشخصي 👤":
    st.header("إعدادات محارب DRY_DIVISION")
    # محاكاة البيانات البدنية
    age = st.number_input("السن", 10, 100, 24)
    weight = st.number_input("الوزن الحالي (كجم)", 30, 200, 95)
    height = st.number_input("الطول (سم)", 100, 250, 175)
    if st.button("حفظ البيانات البدنية"):
        st.success("تم الحفظ بنجاح! سيتم استخدام هذه البيانات في التحليلات القادمة.")
