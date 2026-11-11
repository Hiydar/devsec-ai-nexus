document.getElementById('scan-btn').addEventListener('click', async () => {
    var code = document.getElementById('code-input').value;
    var resultsBox = document.getElementById('results-box');

    if (!code.trim()) {
        resultsBox.innerHTML = '<p style="color: #f85149;">الرجاء إدخال كود برمجي أولاً!</p>';
        return;
    }

    resultsBox.innerHTML = '<p style="color: #d29922;">جاري تحليل وفحص الكود...</p>';

    try {
        var response = await fetch('/api/scan', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code: code, language: 'python' })
        });
        
        var data = await response.json();
        
        if (data.issues.length === 0) {
            resultsBox.innerHTML = '<p style="color: #3fb950; font-weight: bold;">✓ لم يتم اكتشاف ثغرات أمنية، الكود آمن!</p>';
        } else {
            var htmlContent = '<p style="color: #f85149; font-weight: bold;">⚠️ تم اكتشاف (' + data.total_issues + ') مشكلة أمنية:</p>';
            
            data.issues.forEach(function(issue) {
                htmlContent += '<div class="issue-item" style="margin-top: 10px; padding: 10px; border-left: 3px solid #f85149; background: #161b22;">' +
                               '<strong>سطر ' + issue.line + ':</strong> ' + issue.issue + '<br>' +
                               '<small style="color: #8b949e;"><code>' + issue.code_snippet + '</code></small>' +
                               '</div>';
            });
            resultsBox.innerHTML = htmlContent;
        }
    } catch (error) {
        console.error(error); 
        resultsBox.innerHTML = '<p style="color: #f85149;">حدث خطأ أثناء الاتصال بالخادم.</p>';
    }
});