from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from security_analyzer import CodeAnalyzer

# 1. تعريف التطبيق (يجب أن يكون قبل استخدام app)
app = FastAPI(title="DevSec-AI Nexus Engine")

# 2. إعدادات CORS (ضرورية جداً لكي يتواصل ملف app.js مع الخادم)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. ربط الملفات الثابتة (CSS, JS) والقوالب (HTML)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# 4. تعريف المحلل (تأكد من وجود ملف security_analyzer.py في نفس المجلد)
analyzer = CodeAnalyzer()

# 5. نموذج البيانات القادمة من الواجهة
class CodeSubmission(BaseModel):
    code: str
    language: str = "python"

# 6. مسار عرض الصفحة الرئيسية
@app.get("/")
def read_root(request: Request):
    # الصيغة الحديثة والصحيحة لـ FastAPI
    return templates.TemplateResponse(request=request, name="index.html")

# 7. مسار استقبال الكود وفحصه
@app.post("/api/scan")
def scan_code(submission: CodeSubmission):
    try:
        # استدعاء دالة الفحص من ملف security_analyzer.py
        issues = analyzer.analyze_code(submission.code)
        
        return {
            "status": "success",
            "total_issues": len(issues),
            "issues": issues
        }
    except Exception as e:
        # في حال حدوث خطأ داخلي في أداة الفحص
        return {
            "status": "error",
            "message": str(e),
            "total_issues": 0,
            "issues": []
        }