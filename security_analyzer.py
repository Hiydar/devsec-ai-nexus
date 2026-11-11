import re

class CodeAnalyzer:
    # تم إصلاح الخطأ هنا بإضافة الشرطتين السفليتين
    def __init__(self):
        self.patterns = {
            # قمنا بتقليل الطول إلى 4 لكي يكتشف 123456
            "Hardcoded Password / Secret": r"""(?i)(api_key|secret|password|token)\s*=\s*['"][A-Za-z0-9_\-]{4,}['"]""",
            "Insecure Exec/Eval Usage": r'\b(eval|exec)\s*\(',
            "Potential SQL Injection": r'(?i)SELECT\s+.*\s+FROM\s+.*\s*\+\s*',
            # أضفنا قاعدة جديدة لاكتشاف أوامر النظام الخطيرة
            "Dangerous OS Command": r"\b(os\.system|subprocess\.call|subprocess\.run)\s*\(",
        }

    def analyze_code(self, code_content: str):
        findings = []
        lines = code_content.splitlines()

        for line_num, line in enumerate(lines, start=1):
            for issue_type, pattern in self.patterns.items():
                if re.search(pattern, line):
                    findings.append({
                        "line": line_num,
                        "issue": issue_type,
                        "code_snippet": line.strip()
                    })
        return findings