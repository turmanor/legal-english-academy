import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from datetime import datetime, timezone, timedelta


def build_html(now_bj: datetime) -> str:
    rows = [
        ("中国财经", "人民币汇率与跨境资本流动", "今日市场关注稳增长与流动性节奏，短端利率预期平稳。", "若后续政策进一步明朗，风险偏好可能提升。", "https://www.reuters.com/world/china/"),
        ("中国科技", "国产AI与算力基础设施", "头部企业继续加大模型与算力投入，产业链协同增强。", "关注算力成本、商业化落地与监管边界。", "https://www.scmp.com/topics/artificial-intelligence"),
        ("中国国际时政", "区域经贸合作议题", "多边合作仍围绕供应链韧性与贸易便利化推进。", "外需与出口结构变化将影响相关板块估值。", "https://www.fmprc.gov.cn/"),
        ("英美财经", "美联储路径与美元资产", "市场继续交易通胀与就业数据对利率路径的影响。", "美债收益率波动会传导至全球风险资产定价。", "https://www.ft.com/us-economy"),
        ("英美科技", "AI监管与平台竞争", "英美监管机构持续关注生成式AI合规与数据治理。", "合规成本上升，但也可能提升行业进入门槛。", "https://www.theverge.com/ai-artificial-intelligence"),
        ("英美国际时政", "地缘政治与能源价格", "地缘事件扰动下，能源与航运价格敏感性上升。", "输入型通胀与供应链风险值得持续跟踪。", "https://www.bbc.com/news/world"),
    ]

    items = []
    for i, (cat, title, what, impact, link) in enumerate(rows, 1):
        items.append(f"""
        <h3>{i}. [{cat}] {title}</h3>
        <ul>
          <li><b>发生了什么：</b>{what}</li>
          <li><b>为什么重要：</b>{impact}</li>
          <li><b>原文链接：</b><a href='{link}'>{link}</a></li>
          <li><b>配图位：</b>（正式版将自动插入网页截图）</li>
        </ul>
        """)

    return f"""
    <html><body>
    <h2>全球财经科技时政简报（模板预览）</h2>
    <p>北京时间：{now_bj.strftime('%Y-%m-%d %H:%M')}</p>
    <p>本邮件为自动化模板验证版：每次6-8条、1:1覆盖中国与英美、分析型结构。</p>
    <h3>今日三条主线（示例）</h3>
    <ol>
      <li>货币政策与风险资产定价联动增强。</li>
      <li>AI商业化进入“算力+合规”双约束阶段。</li>
      <li>地缘事件通过能源与供应链传导至通胀预期。</li>
    </ol>
    {''.join(items)}
    <hr />
    <h3>小红书可发文案（示例）</h3>
    <p>今天重点看三件事：政策预期、AI商业化、地缘能源扰动。短线波动加大，但中线仍看基本面与现金流质量。收藏这份中英新闻对照，明早复盘直接用。</p>
    </body></html>
    """


def build_pdf_placeholder(path: str, now_bj: datetime) -> None:
    # Tiny valid PDF placeholder for attachment check
    content = f"%PDF-1.1\n1 0 obj<<>>endobj\n2 0 obj<< /Length 44 >>stream\nTemplate Report {now_bj.strftime('%Y-%m-%d %H:%M')}\nendstream\nendobj\n3 0 obj<< /Type /Catalog /Pages 4 0 R >>endobj\n4 0 obj<< /Type /Pages /Kids [5 0 R] /Count 1 >>endobj\n5 0 obj<< /Type /Page /Parent 4 0 R /MediaBox [0 0 300 200] /Contents 2 0 R >>endobj\nxref\n0 6\n0000000000 65535 f \n0000000009 00000 n \n0000000028 00000 n \n0000000105 00000 n \n0000000154 00000 n \n0000000213 00000 n \ntrailer<< /Root 3 0 R /Size 6 >>\nstartxref\n302\n%%EOF"
    with open(path, 'wb') as f:
        f.write(content.encode('latin-1', 'ignore'))


def send_mail():
    smtp_host = os.getenv('SMTP_HOST', 'smtp.qq.com')
    smtp_port = int(os.getenv('SMTP_PORT', '465'))
    smtp_user = os.environ['SMTP_USER']
    smtp_pass = os.environ['SMTP_PASS']
    to_addr = os.environ['TO_EMAIL']

    now_bj = datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=8)))
    subject = f"【模板验收】全球财经科技时政简报 | {now_bj.strftime('%Y-%m-%d')}"

    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = to_addr
    msg['Subject'] = subject

    html = build_html(now_bj)
    msg.attach(MIMEText(html, 'html', 'utf-8'))

    pdf_path = 'daily_report_template.pdf'
    build_pdf_placeholder(pdf_path, now_bj)
    with open(pdf_path, 'rb') as f:
        part = MIMEApplication(f.read(), _subtype='pdf')
        part.add_header('Content-Disposition', 'attachment', filename='news-brief-template.pdf')
        msg.attach(part)

    with smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=30) as server:
        server.login(smtp_user, smtp_pass)
        server.sendmail(smtp_user, [to_addr], msg.as_string())


if __name__ == '__main__':
    send_mail()
    print('Mail sent.')
