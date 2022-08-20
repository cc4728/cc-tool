import win32com.client as win32
#pip install pypiwin32
def send_mail(title,msg,to,cc,attach=None):
    outlook = win32.Dispatch('Outlook.Application')
    mail_item = outlook.CreateItem (0)  # 0: olMailItem

    mail_item.Recipients.Add(to)
    mail_item.Subject = title

    mail_item.Body = msg
    mail_item.CC = cc

    mail_item.Send()

"""
  #  mail_item.BodyFormat = 2          # 2: Html format
  #  mail_item.HTMLBody  = '''
  #      <H2>Hello, This is a test mail.</H2>
  #      '''

mail.To = 'contact@company.com'
mail.Subject = 'Sample Email'
mail.HTMLBody = '<h3>This is HTML Body</h3>'
mail.Body = "This is the normal body"
mail.Attachments.Add('c:\\sample.xlsx')
mail.Attachments.Add('c:\\sample2.xlsx')
mail.CC = 'somebody@company.com'

"""

if __name__ == '__main__':
    cc = "Jing.Cai@mediatek.com;Weifan.Zhang@mediatek.com"
    send_mail("test mail","hello,jing","Jing.Cai@mediatek.com",cc)