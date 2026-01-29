import sqlite3
import pandas as pd
from collections import Counter
import os

# --- الرادار: تحديد موقع الملف تلقائياً ---
current_folder = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_folder, 'wuzzuf_jobs.db')

# --- 1. سحب البيانات ---
print(f"📊 جاري الاتصال بقاعدة البيانات في: {db_path}")

if not os.path.exists(db_path):
    print("❌ خطأ: ملف قاعدة البيانات غير موجود في هذا المجلد!")
else:
    try:
        conn = sqlite3.connect(db_path)
        df = pd.read_sql("SELECT * FROM jobs", conn)
        conn.close()

        # --- 2. تحليل المهارات ---
        all_skills = []
        for skills_text in df['Skills'].dropna():
            skills_list = [s.strip() for s in skills_text.split(',')]
            all_skills.extend(skills_list)

        skill_counts = Counter(all_skills)
        top_skills = skill_counts.most_common(10)

        # --- 3. الرسم البياني النصي ---
        print("\n🔥 أكثر 10 مهارات طلباً في سوق العمل (تقرير فوري):")
        print("-" * 50)
        for skill, count in top_skills:
            bar_length = int(count / 10) 
            bar = "█" * bar_length 
            print(f"{skill.ljust(20)} | {bar} ({count})")
        print("-" * 50)
        print("✅ تمت العملية بنجاح!")
        
    except Exception as e:
        print(f"❌ حدث خطأ أثناء فتح الملف: {e}")
        print("💡 نصيحة: تأكدي أن القرص C فيه مساحة فاضية ولو قليلة!")