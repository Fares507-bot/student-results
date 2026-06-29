from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)


# دالة الترجمة للرموز
def get_symbol(value):
    mapping = {
        'ممتاز': 'م',
        'جيد جداً': 'جج',
        'جيد': 'ج',
        'مقبول': 'ق',
        'ضعيف': 'ض',
        'راسب': 'ض'
    }
    return mapping.get(str(value).strip(), value)


def get_student_result(seat_no):
    excel_file = 'results.xlsx'
    if not os.path.exists(excel_file):
        return None, "ملف البيانات غير موجود."

    try:
        df = pd.read_excel(excel_file)
        df.columns = df.columns.str.strip()

        seat_col = next((c for c in df.columns if 'جلوس' in c or 'seat' in c.lower()), df.columns[0])
        df[seat_col] = df[seat_col].astype(str).str.strip()
        student_data = df[df[seat_col] == str(seat_no).strip()]

        if student_data.empty:
            return None, "رقم الجلوس غير موجود."

        row = student_data.iloc[0]
        result = {}
        for col in df.columns:
            # هنا بنستخدم دالة الترجمة عشان نحول الكلمة لرمز
            result[col] = get_symbol(row[col])

        return result, None
    except Exception as e:
        return None, f"خطأ: {str(e)}"


@app.route('/', methods=['GET', 'POST'])
def index():
    searched = False
    result = None
    error_msg = None
    if request.method == 'POST':
        searched = True
        seat_no = request.form.get('seat_no')
        if seat_no:
            result, error_msg = get_student_result(seat_no)
    return render_template('index.html', searched=searched, result=result, error_msg=error_msg)


if __name__ == '__main__':
    app.run(debug=True)