"""
通过 QQ 邮箱 SMTP 发送论文日报
"""

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from typing import List, Dict

from send_notification import build_notification_message

SMTP_HOST = "smtp.qq.com"
SMTP_PORT = 465
SENDER = "710821898@qq.com"


def markdown_to_html(md_text: str) -> str:
    """将 Markdown 简单转换为 HTML"""
    lines = md_text.split('\n')
    html_lines = []
    in_list = False

    for line in lines:
        # 标题
        if line.startswith('### '):
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append(f'<h3>{_inline(line[4:])}</h3>')
        elif line.startswith('## '):
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append(f'<h2>{_inline(line[3:])}</h2>')
        elif line.startswith('# '):
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append(f'<h1>{_inline(line[2:])}</h1>')
        # 分割线
        elif line.strip() == '---':
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append('<hr>')
        # 列表
        elif line.startswith('- ') or (len(line) > 2 and line[0].isdigit() and line[1] == '.'):
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
            content = line[2:].strip() if line.startswith('- ') else line[line.index('.')+1:].strip()
            html_lines.append(f'<li>{_inline(content)}</li>')
        # 空行
        elif line.strip() == '':
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append('<br>')
        # 普通段落
        else:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append(f'<p>{_inline(line)}</p>')

    if in_list:
        html_lines.append('</ul>')

    body = '\n'.join(html_lines)
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
         max-width: 800px; margin: 0 auto; padding: 20px; color: #333; }}
  h1 {{ color: #1a1a2e; border-bottom: 2px solid #4a90d9; padding-bottom: 8px; }}
  h2 {{ color: #2c3e50; }}
  h3 {{ color: #2980b9; margin-top: 24px; }}
  hr {{ border: none; border-top: 1px solid #ddd; margin: 16px 0; }}
  a {{ color: #4a90d9; }}
  p {{ margin: 4px 0; line-height: 1.6; }}
  ul {{ margin: 4px 0; padding-left: 20px; }}
  li {{ line-height: 1.6; }}
  strong {{ color: #2c3e50; }}
  .footer {{ color: #999; font-size: 0.85em; margin-top: 32px; border-top: 1px solid #eee; padding-top: 12px; }}
</style>
</head>
<body>
{body}
</body>
</html>"""


def _inline(text: str) -> str:
    """处理行内 Markdown（粗体、链接）"""
    import re
    # **bold**
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # [text](url)
    text = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', text)
    # *italic*
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    return text


def send_email(papers: List[Dict], password: str, recipients: List[str] = None) -> bool:
    """
    发送论文日报邮件

    Args:
        papers: 论文列表
        password: QQ 邮箱授权码
        recipients: 收件人列表，默认发给自己

    Returns:
        是否发送成功
    """
    print("\n" + "=" * 60)
    print("📧 准备发送邮件")
    print("=" * 60)

    if recipients is None:
        recipients = [SENDER]

    today = datetime.now().strftime('%Y年%m月%d日')
    title, md_content = build_notification_message(papers)
    html_content = markdown_to_html(md_content)

    msg = MIMEMultipart('alternative')
    msg['Subject'] = title
    msg['From'] = SENDER
    msg['To'] = ', '.join(recipients)

    # 纯文本备用版本
    msg.attach(MIMEText(md_content, 'plain', 'utf-8'))
    # HTML 主版本
    msg.attach(MIMEText(html_content, 'html', 'utf-8'))

    try:
        print(f"📤 连接 {SMTP_HOST}:{SMTP_PORT}...")
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
            server.login(SENDER, password)
            server.sendmail(SENDER, recipients, msg.as_string())

        print(f"✅ 邮件发送成功 → {', '.join(recipients)}")
        return True

    except smtplib.SMTPAuthenticationError:
        print("❌ 认证失败，请检查授权码是否正确")
        return False
    except Exception as e:
        print(f"❌ 邮件发送失败: {e}")
        return False
