import streamlit as st
import google.generativeai as genai
from PIL import Image
import json
import os
from datetime import datetime, date, timedelta

# 1. الإعدادات البصرية والموسيقى (CSS Injection)
st.set_page_config(page_title="DRY_DIVISION IMPERIAL 2026", page_icon="⚔️", layout="wide")

# رابط خلفية التنانين الأسطورية الفخمة
bg_img = "https://images.alphacoders.com/133/1332463.png"

st.markdown(f"""
<style>
    /* الخلفية العامة */
    .stApp {{
        background-image: url("{bg_img}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    /* تصميم القوائم الزجاجية */
    [data-testid="stSidebar"] {{
        background-color: rgba(0, 0, 0, 0.85) !important;
        backdrop-filter: blur(15px);
        border-right: 2px solid #d4af37;
    }}
    /* النصوص الذهبية */
    h1, h2, h3, .stSubheader {{
        color: #d4af37 !important;
        font-family: 'Cinzel', serif;
        text-shadow: 3px 3px 6px #000;
        text-align: center;
    }}
    /* الأزرار الملكية */
    .stButton>button {{
        background: linear-gradient(45deg, #d4af37, #b59410) !important;
        color: black !important;
        font-weight: bold !important;
        border-radius: 25px !important;
        border: none !important;
        transition: 0.4s;
        width: 100%;
    }}
    .stButton>button:hover {{
        transform: scale(1.05);
        box-shadow: 0px 0px 15px #d4af37;
        background: #fff !important;
    }}
    /* صناديق المعلومات */
    .stAlert, .stMarkdown, [data-testid="stExpander"] {{
        background-color: rgba(20, 20, 20, 0.7) !important;
        border: 1px solid #d4af37 !important;
        border-radius: 15px !important;
        color: white !important;
    }}
</style>

<iframe src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-16.mp3" allow="autoplay" style="display:none" id="iframeAudio"></iframe>
<audio autoplay loop><source src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-16.mp3" type="audio/mp3"></audio>
""", unsafe_allow_html=True)

# 2. نظام قاعدة البيانات
DB_FILE = "dry_division_master_db.json"

def load_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding='utf-8') as f: return json.load(f)
        except: return {}
    return {}

def save_db(data):
    with open(DB_FILE, "w", encoding='utf-8') as f: json.dump(data, f, indent=4, ensure_ascii=False)

if 'user_db' not in st.session_state:
    st.session_state['user_db'] = load_db()

# 3. إعداد الذكاء الاصطناعي (المحرك المزدوج)
API_KEY = "AIzaSyBBeoQqdGZbG8j66oLBJ6kEc89uucAnUY8"
genai.configure(api_key=API_KEY)

def smart_ai_analysis(image, mode):
    models = ['gemini-1.5-flash', 'gemini-1.5-pro']
    prompts = {
        "ماسح الوجبات AI 🍎": "أنت خبير تغذية ملكي. حلل الوجبة: السعرات، البروتين، الكارب، الدهون، وقدم نصيحة احترافية.",
        "التحليل البدني 💪": "أنت مدرب كمال أجسام أسطوري. حلل صورة الجسم أو الـ InBody وقدر نسبة الدهون والكتلة العضلية."
    }
    for m in models:
        try:
            model = genai.GenerativeModel(m)
            res = model.generate_content([prompts.get(mode, "تحليل"), image])
            return res.text
        except: continue
    return "⚠️ عذراً يا قائد، هناك ضغط على السيرفرات العالمية. حاول مجدداً بعد ثوانٍ."

# 4. نظام تسجيل الدخول والحظر والموافقة
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.markdown("<h1>⚔️ DRY_DIVISION IMPERIAL SYSTEM ⚔️</h1>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["🔑 دخول المحاربين", "🛡️ إنشاء حساب جديد"])
    
    with t1:
        u = st.text_input("اسم المستخدم").strip()
        p = st.text_input("كلمة المرور", type='password').strip()
        if st.button("دخول إلى مركز القيادة"):
            user_data = st.session_state['user_db'].get(u)
            if u == "admin_mohamed" and p == "mohamed_dev_2026":
                st.session_state.update({'logged_in':True, 'current_user':u, 'is_admin':True})
                st.rerun()
            elif user_data and user_data['password'] == p:
                ban_date = user_data.get('ban_until')
                if ban_date and datetime.strptime(ban_date, '%Y-%m-%d').date() > date.today():
                    st.error(f"🚫 حسابك محظور حتى {ban_date} لمخالفة القوانين الملكية.")
                else:
                    st.session_state.update({'logged_in':True, 'current_user':u, 'is_admin':False})
                    st.rerun()
            else: st.error("❌ بيانات خاطئة!")

    with t2:
        st.subheader("🛡️ الميثاق الملكي (التسجيل)")
        nu = st.text_input("اسم مستخدم جديد")
        np = st.text_input("باسورد جديد", type='password')
        
        with st.expander("📜 شروط وقوانين الإمبراطورية"):
            st.write("1. يمنع مشاركة الحساب مع الآخرين.\n2. يمنع رفع صور خادشة للحياء (حظر فوري).\n3. فترة التجربة 6 أيام فقط.")
        
        agree = st.checkbox("أقر أنا المحارب بأنني قرأت الشروط وأوافق على الالتزام بها.")
        if st.button("تفعيل الحساب والبدء 🚀", disabled=not agree):
            if nu and np and nu not in st.session_state['user_db']:
                st.session_state['user_db'][nu] = {
                    'password': np, 'is_pro': False, 'pro_expire': None,
                    'reg_date': str(date.today()), 'ban_until': None
                }
                save_db(st.session_state['user_db'])
                st.success("✅ تم التسجيل بنجاح! سجل دخولك الآن.")
            else: st.warning("البيانات ناقصة أو الاسم مأخوذ.")
    st.stop()

# --- بعد تسجيل الدخول ---
user_id = st.session_state['current_user']
is_admin = st.session_state['is_admin']
u_data = st.session_state['user_db'].get(user_id, {})

# حساب الصلاحية
expire_str = u_data.get('pro_expire')
is_pro = False
if expire_str and datetime.strptime(expire_str, '%Y-%m-%d').date() >= date.today():
    is_pro = True

reg_date = datetime.strptime(u_data.get('reg_date', str(date.today())), '%Y-%m-%d').date()
trial_left = max(0, 6 - (date.today() - reg_date).days)
has_access = is_admin or is_pro or trial_left > 0

# 5. القائمة الجانبية (إدارة القائد)
with st.sidebar:
    st.markdown(f"<h2>DRY_DIVISION</h2>", unsafe_allow_html=True)
    status = "👑 ADMIN" if is_admin else ("💎 PRO" if is_pro else f"⏳ TRIAL ({trial_left} D)")
    st.write(f"المحارب: **{user_id}** | الحالة: `{status}`")
    
    choice = st.selectbox("القائمة الإمبراطورية", ["الملف الشخصي 👤", "ماسح الوجبات AI 🍎", "التحليل البدني 💪", "خطط الاشتراك 💳", "الدعم الفني 📞"])
    
    if is_admin:
        st.divider()
        st.subheader("🛠️ لوحة تحكم القائد")
        target = st.selectbox("اختر مستخدم", [u for u in st.session_state['user_db'] if u != "admin_mohamed"])
        
        # تفعيل المدة
        dur = st.radio("مدة التفعيل", ["شهر", "3 أشهر", "سنة"])
        if st.button("✅ تفعيل PRO"):
            days = 30 if dur == "شهر" else (90 if dur == "3 أشهر" else 365)
            st.session_state['user_db'][target]['pro_expire'] = str(date.today() + timedelta(days=days))
            save_db(st.session_state['user_db'])
            st.success(f"تم تفعيل {target}")

        # الحظر
        b_days = st.number_input("أيام الحظر", 1, 365, 7)
        if st.button("🚫 حظر"):
            st.session_state['user_db'][target]['ban_until'] = str(date.today() + timedelta(days=b_days))
            save_db(st.session_state['user_db'])
            st.error("تم الحظر")
        if st.button("🔓 فك الحظر"):
            st.session_state['user_db'][target]['ban_until'] = None
            save_db(st.session_state['user_db'])
            st.success("تم الفك")

    if st.button("خروج آمن 🚪"):
        st.session_state['logged_in'] = False
        st.rerun()

# 6. محتوى الصفحات
if choice == "خطط الاشتراك 💳":
    st.header("💎 باقات النخبة الملكية")
    c1, c2, c3 = st.columns(3)
    wa = "201141930176"
    plans = [("باقة المحارب", "5$", "اشتراك_شهري"), ("باقة الوحش", "12$", "اشتراك_3أشهر"), ("الباقة الملكية", "59$", "اشتراك_سنوي")]
    for col, (n, p, m) in zip([c1, c2, c3], plans):
        with col:
            st.info(f"### {n}\n**{p}**")
            st.markdown(f'<a href="https://wa.me/{wa}?text={m}_{user_id}" target="_blank"><button style="width:100%; background:#25D366; color:white; border:none; padding:12px; border-radius:10px; cursor:pointer; font-weight:bold;">واتساب / فودافون كاش 📱</button></a>', unsafe_allow_html=True)
            st.markdown(f'<br><a href="https://instapay.me/mohamed" target="_blank"><button style="width:100%; background:#6c5ce7; color:white; border:none; padding:12px; border-radius:10px; cursor:pointer; font-weight:bold;">إنستا باي ⚡</button></a>', unsafe_allow_html=True)

elif choice == "الدعم الفني 📞":
    st.header("📞 تواصل مع القيادة")
    st.write(f"📧 البريد: **mohamedabdoteto22@gmail.com**")
    st.write(f"📸 إنستجرام: **[@mohamed_36do](https://instagram.com/mohamed_36do)**")
    st.write(f"📱 واتساب: **01141930176**")

elif choice in ["ماسح الوجبات AI 🍎", "التحليل البدني 💪"]:
    st.header(choice)
    if not has_access:
        st.error("🔒 انتهت فترة القوة المجانية. اشترك لتفعيل طاقتك مجدداً!")
    else:
        file = st.file_uploader("ارفع الصورة للتحليل الإمبراطوري", type=['jpg','png','jpeg'])
        if file and st.button("بدء التحليل ✨"):
            with st.spinner("جاري استدعاء الذكاء الاصطناعي الأسطوري..."):
                img = Image.open(file).convert("RGB")
                st.info(smart_ai_analysis(img, choice))

elif choice == "الملف الشخصي 👤":
    st.header("بيانات المحارب")
    st.write(f"اسم المستخدم: **{user_id}**")
    st.write(f"تاريخ الانضمام: **{reg_date}**")
    st.write(f"الحالة: **{status}**")
