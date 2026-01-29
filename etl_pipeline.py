import pandas as pd
import sqlite3
import json
import os

# --- الرادار: تحديد موقع الملف تلقائياً ---
# هذا الأمر يجيب مكان الملف الحالي (الكود) عشان يدور جنبه
current_folder = os.path.dirname(os.path.abspath(__file__))
json_file = os.path.join(current_folder, 'wuzzuf_full_data.json')
db_path = os.path.join(current_folder, 'wuzzuf_jobs.db')

# --- 1. القراءة من الملف الجاهز ---
def load_data():
    print(f"📍 جاري البحث في المجلد: {current_folder}")
    
    if not os.path.exists(json_file):
        print(f"❌ الملف غير موجود هنا: {json_file}")
        print("💡 تأكدي أن ملف wuzzuf_full_data.json موجود بجانب ملف الكود تماماً!")
        return pd.DataFrame()
    
    print(f"📂 لقينا الكنز! جاري القراءة...")
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        df = pd.DataFrame(data)
        print(f"✅ تم تحميل {len(df)} وظيفة بمهاراتها!")
        return df
    except Exception as e:
        print(f"❌ خطأ في القراءة: {e}")
        return pd.DataFrame()

# --- 2. الحفظ في قاعدة البيانات ---
def save_to_db(df):
    if df.empty:
        return

    print("💾 جاري الحفظ في قاعدة البيانات...")
    conn = sqlite3.connect(db_path)
    df.to_sql("jobs", conn, if_exists="replace", index=False)
    conn.close()
    print("🎉 تم! قاعدة بياناتك (wuzzuf_jobs.db) الآن ملياااانة 637 وظيفة!")

# --- تشغيل ---
if __name__ == "__main__":
    df = load_data()
    save_to_db(df)