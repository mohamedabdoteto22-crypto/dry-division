import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
from datetime import date

# 1. إعدادات الهوية والتصميم
st.set_page_config(page_title="DRY_DIVISION AI", page_icon="⚔️", layout="wide")

# 2. تفعيل الذكاء الاصطناعي (Gemini) بمفتاحك
API_KEY = "AIzaSyBBeoQqdGZbG8j66oLBJ6kEc89uucAnUY8"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. واجهة التطبيق الرئيسية
st.title("DRY_DIVISION ⚡ ULTIMATE AI")
st.markdown("---")

# 4. القائمة الجانبية للتنقل الاحترافي
with st.sidebar:
    st.image("https://img.icons8.com/ios-filled/100/ffffff/skull.png") # أيقونة تعبيرية
    st.title("COMMAND CENTER")
    menu = [
        "الملف الشخصي 👤", 
        "ماسح الوجبات الذكي 🍎", 
        "خطة التغذية المخصصة 🥗",
        "تحليل الجسم والتدريب 💪", 
        "سجل البيانات اليومي 📝"
    ]
    choice = st.selectbox("اختر المهمة", menu)
    st.markdown("---")
    st.write("STATUS: ONLINE")

# --- 1. الملف الشخصي (لجعل النظام يناسب الجميع) ---
if choice == "الملف الشخصي 👤":
    st.header("👤 إعدادات المحارب")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("الاسم الكامل", "محمد عبد القادر")
        age = st.number_input("السن", 15, 70, 24)
        gender = st.selectbox("الجنس", ["ذكر", "أنثى"])
    with col2:
        weight = st.number_input("الوزن الحالي (كجم)", 40.0, 200.0, 95.0)
        height = st.number_input("الطول (سم)", 120, 220, 175)
        goal = st.selectbox("الهدف الاستراتيجي", ["تنشيف ونشافة عضلية (Dryness)", "ضخامة عضلية صافية", "خسارة دهون سريعة"])

    if st.button("حفظ وتحديث النظام"):
        st.session_state['user_data'] = f"الاسم: {name}, السن: {age}, الوزن: {weight}, الطول: {height}, الهدف: {goal}"
        st.success("تم تحديث بروتوكول البيانات الشخصية بنجاح.")

# --- 2. ماسح الوجبات الذكي ---
elif choice == "ماسح الوجبات الذكي 🍎":
    st.header("📷 تحليل الوجبات الفوري")
    st.info("ارفع صورة الوجبة ليقوم الذكاء الاصطناعي بتقدير السعرات")
    img_file = st.file_uploader("Upload Meal Image", type=["jpg", "png", "jpeg"])
    if img_file:
        img = Image.open(img_file)
        st.image(img, width=400, caption="المستشعرات تلتقط البيانات...")
        if st.button("تحليل المكونات"):
            user_info = st.session_state.get('user_data', "بيانات عامة لمستخدم رياضي")
            with st.spinner('جاري المسح...'):
                prompt = f"أنت خبير تغذية. حلل هذه الوجبة لمستخدم ببيانات: ({user_info}). اذكر السعرات، البروتين، الكارب، الدهون، ومدى ملاءمتها لهدفه."
                response = model.generate_content([prompt, img])
                st.markdown(response.text)

# --- 3. خطة التغذية المخصصة ---
elif choice == "خطة التغذية المخصصة 🥗":
    st.header("🥗 نظام غذائي مخصص (InBody Based)")
    st.write("ارفع صورة الـ InBody لتصميم وجبات تناسب طبيعة جسمك")
    inbody_img = st.file_uploader("Upload InBody Report", type=["jpg", "png", "jpeg"])
    if inbody_img:
        img = Image.open(inbody_img)
        st.image(img, width=300)
        if st.button("توليد خطة الوجبات"):
            user_info = st.session_state.get('user_data', "بيانات عامة")
            with st.spinner('جاري تصميم الخطة المخصصة...'):
                prompt = f"بناءً على بيانات المستخدم ({user_info}) وتقرير الـ InBody، صمم برنامج غذائي كامل (فطور، غداء، عشاء، سناك) يركز على تحسين التكوين العضلي والنشافة."
                response = model.generate_content([prompt, img])
                st.success("الخطة الغذائية المقترحة:")
                st.markdown(response.text)

# --- 4. تحليل الجسم والتدريب ---
elif choice == "تحليل الجسم والتدريب 💪":
    st.header("🛡️ تقييم الحالة البدنية والتدريب")
    st.write("ارفع صور الجسم (أمام، خلف، جوانب) أو الـ InBody")
    files = st.file_uploader("ارفع الصور هنا", accept_multiple_files=True, type=["jpg", "png", "jpeg"])
    if files:
        for f in files:
            st.image(Image.open(f), width=200)
        if st.button("إصدار التقرير والجدول التدريبي"):
            user_info = st.session_state.get('user_data', "بيانات عامة")
            with st.spinner('جاري تحليل الكتلة العضلية والنشافة...'):
                prompt = f"أنت مدرب محترف. حلل هذه الصور للمستخدم ({user_info}) وأعط: 1- تقدير نسبة الدهون. 2- نقاط القوة والضعف. 3- جدول تدريب 3 أيام مكثف يناسب حالته."
                img_to_analyze = Image.open(files[0])
                response = model.generate_content([prompt, img_to_analyze])
                st.markdown(response.text)

# --- 5. سجل البيانات اليومي ---
elif choice == "سجل البيانات اليومي 📝":
    st.header("📝 التتبع اليدوي")
    w = st.number_input("تحديث الوزن (kg)", value=95.0)
    c = st.number_input("السعرات اليومية المستهلكة", value=2000)
    if st.button("حفظ السجل"):
        with open("dry_log.csv", "a") as f:
            f.write(f"{date.today()},{w},{c}\n")
        st.success("تم تأمين البيانات في السجل التاريخي.")
