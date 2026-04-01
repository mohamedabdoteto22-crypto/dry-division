import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
import os
from datetime import date

# 1. إعدادات الصفحة والسمة (Theme)
st.set_page_config(page_title="DRY_DIVISION AI", page_icon="⚔️", layout="wide")

# 2. إعداد الذكاء الاصطناعي (Gemini)
API_KEY = "AIzaSyBBeoQqdGZbG8j66oLBJ6kEc89uucAnUY8"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. العنوان الرئيسي
st.title("DRY_DIVISION ⚡ AI SYSTEM")
st.markdown("---")

# 4. القائمة الجانبية (Side Bar)
menu = ["لوحة التحكم 📊", "ماسح الوجبات الذكي 🍎", "التحليل البدني والتدريب 💪", "سجل البيانات اليدوي 📝"]
choice = st.sidebar.selectbox("COMMAND CENTER", menu)

# --- الخيار الأول: لوحة التحكم ---
if choice == "لوحة التحكم 📊":
    st.header("مرحباً بك في نظام DRY_DIVISION")
    col1, col2, col3 = st.columns(3)
    col1.metric("الوزن الحالي", "95 kg")
    col2.metric("الطول", "175 cm")
    col3.metric("الحالة", "Active")
    st.info("هدف النظام: الوصول لأعلى مستويات النشافة العضلية (Maximum Vascularity)")

# --- الخيار الثاني: ماسح الوجبات ---
elif choice == "ماسح الوجبات الذكي 🍎":
    st.header("📷 تحليل الوجبات بالذكاء الاصطناعي")
    img_file = st.file_uploader("ارفع صورة وجبتك", type=["jpg", "png", "jpeg"])
    if img_file:
        img = Image.open(img_file)
        st.image(img, width=400)
        if st.button("بدء تحليل السعرات"):
            with st.spinner('جاري قراءة المكونات...'):
                prompt = "بصفتك خبير تغذية، حلل الصورة بدقة وأعطني: 1- اسم الوجبة 2- السعرات التقريبية 3- جرامات البروتين والكارب والدهون 4- نصيحة سريعة لملاءمتها لنظام التنشيف."
                response = model.generate_content([prompt, img])
                st.markdown(response.text)

# --- الخيار الثالث: التحليل البدني والتدريب ---
elif choice == "التحليل البدني والتدريب 💪":
    st.header("🛡️ التقييم البدني الشامل")
    st.write("ارفع صور الجسم (أربع جهات) أو نتيجة الـ InBody")
    files = st.file_uploader("اختر الصور", accept_multiple_files=True, type=["jpg", "png", "jpeg"])
    
    if files:
        for f in files:
            st.image(Image.open(f), width=250)
            
        if st.button("إصدار التقرير والنظام التدريبي"):
            with st.spinner('جاري تحليل التكوين العضلي...'):
                prompt = "أنت مدرب كمال أجسام متخصص في التجهيز للبطولات. حلل هذه الصور (جسم أو إنبادي) وقدم: 1- تقدير نسبة الدهون 2- تقييم الكتلة العضلية والنشافة (Dryness) 3- نقاط الضعف التي تحتاج تركيز 4- جدول تدريبي 3 أيام مكثف جداً للوصول لهدف التنشيف."
                # نرسل أول صورة كعينة للتحليل
                img_to_analyze = Image.open(files[0])
                response = model.generate_content([prompt, img_to_analyze])
                st.success("التقرير الفني والنظام المقترح:")
                st.markdown(response.text)

# --- الخيار الرابع: السجل اليدوي ---
elif choice == "سجل البيانات اليدوي 📝":
    st.header("تحديث البيانات اليومية")
    w = st.number_input("الوزن (kg)", value=95.0)
    c = st.number_input("السعرات المستهلكة", value=2000)
    if st.button("حفظ في السجل"):
        with open("dry_log.csv", "a") as f:
            f.write(f"{date.today()},{w},{c}\n")
        st.success("تم التحديث بنجاح")
