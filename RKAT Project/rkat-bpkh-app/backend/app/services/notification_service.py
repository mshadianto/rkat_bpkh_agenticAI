from typing import List, Dict
from app.models.user import User, UserRole
from app.models.rkat import RKAT
import smtplib
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
from app.config import settings

class NotificationService:
    """Service for sending notifications and alerts"""
    
    def __init__(self):
        self.smtp_server = settings.smtp_host
        self.smtp_port = settings.smtp_port
        self.username = settings.email_username
        self.password = settings.email_password
    
    def send_email(self, to_emails: List[str], subject: str, body: str, html_body: str = None):
        """Send email notification"""
        try:
            msg = MimeMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.username
            msg['To'] = ', '.join(to_emails)
            
            # Add text and HTML parts
            text_part = MimeText(body, 'plain')
            msg.attach(text_part)
            
            if html_body:
                html_part = MimeText(html_body, 'html')
                msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
                
            return True
        except Exception as e:
            print(f"Email sending failed: {e}")
            return False
    
    def notify_rkat_submission(self, rkat: RKAT, reviewers: List[User]):
        """Notify reviewers about new RKAT submission"""
        subject = f"RKAT Baru untuk Review: {rkat.title}"
        body = f"""
        RKAT baru telah disubmit untuk review:
        
        Judul: {rkat.title}
        Tahun: {rkat.year}
        Total Anggaran: Rp {rkat.total_budget:,.0f}
        Pembuat: {rkat.creator.full_name}
        Tanggal Submit: {rkat.submitted_at}
        
        Silakan login ke sistem untuk melakukan review.
        """
        
        emails = [user.email for user in reviewers]
        self.send_email(emails, subject, body)
    
    def notify_rkat_status_update(self, rkat: RKAT, action: str, comments: str = None):
        """Notify RKAT creator about status update"""
        status_map = {
            "approve": "disetujui",
            "reject": "ditolak",
            "request_revision": "memerlukan revisi"
        }
        
        subject = f"Update Status RKAT: {rkat.title}"
        body = f"""
        RKAT Anda telah {status_map.get(action, action)}:
        
        Judul: {rkat.title}
        Status Baru: {rkat.status.value}
        """
        
        if comments:
            body += f"\nKomentar: {comments}"
        
        body += "\n\nSilakan login ke sistem untuk informasi lebih lanjut."
        
        self.send_email([rkat.creator.email], subject, body)