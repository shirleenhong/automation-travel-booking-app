import os
import smtplib
import fnmatch
import math
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from lxml import etree

def send_mail():
    sender = 'DesktopQA@carlsonwagonlit.com'
    recipients = [  'Maridel.Castro@carlsonwagonlit.com', 
                    'Norlan.Bautista@carlsonwagonlit.com',
                    'RJuarez@Carlsonwagonlit.com',
                    'RMartinez2@Carlsonwagonlit.com',
					'SHIRLEEN.HONG@carlsonwagonlit.com',
					'Vivek.Patel@carlsonwagonlit.com',
					'AJIT.SINGH@carlsonwagonlit.com',
					'Jayson.Panganiban@carlsonwagonlit.com',
                    'TChua@carlsonwagonlit.com'
                ]

    file_dir = os.path.dirname(os.path.realpath(__file__))
    base_dir = os.path.basename(file_dir)
    result_file = max([f for f in os.listdir(file_dir) if f.endswith('.xlsx') and not f.startswith('~')], key=os.path.getctime)
    excel_file = file_dir + '//' + ''.join(result_file)

    msg = MIMEMultipart()
    msg['Subject'] = 'Power Express Efficiency Nightly Test Result on SABRE'
    msg['From'] = sender
    msg['To'] = ", ".join(recipients)

    failed_tc = []
    failed_tc_error = []
    total_tc_fail = 0
    total_tc_pass = 0
    total_tc_executed = 0
    xml_files = get_all_xml_files()
    for each_xml_file in xml_files:
        context = etree.iterparse(each_xml_file, events=('end',))
        for event, elem in context:
            if elem.tag == 'test':
                tc_name_attrib = elem.attrib['name']
                tc_status_path = get_test_status_path(elem, tc_name_attrib)[0]
                if tc_status_path.attrib['status'] == 'FAIL':
                    failed_tc.append(tc_name_attrib)
                    failed_tc_error.append(tc_status_path.text)
                    total_tc_fail += 1
                else:
                    total_tc_pass += 1
                elem.clear()
                while elem.getprevious() is not None:
                    del elem.getparent()[0]
        del context

    total_tc_executed = total_tc_fail + total_tc_pass
    percentage = math.ceil(total_tc_pass*100.0 / total_tc_executed)

    template_failed_tc = []
    for tc, error in zip(failed_tc, failed_tc_error):
        template = """
            <tr>
                <td style="text-align: left">""" + repr(tc) + """</td>
                <td style="text-align: left">""" + repr(error) + """</td>
            </tr>
            """        
        template_failed_tc.append(template)

    html = """
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml">
    <head>
    <title>Robotframework Test Results</title>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0 " />
      <style>
         body {
             background-color:#F2F2F2; 
         }
         body, html, table,span,b {
             font-family: Calibri, Arial, sans-serif;
             font-size: 1em; 
         }
         .pastdue { color: crimson; }
         table {
             border: 1px solid silver;
             padding: 6px;
             margin-left: 30px;
         }
         thead {
             text-align: center;
             font-size: 1.1em;        
             background-color: #B0C4DE;
             font-weight: bold;
             color: #2D2C2C;
         }
         tbody {
            text-align: center;
         }
         th {
            word-wrap:break-word;
         }
         td {
            height: 25px;
         }
      </style>
    </head>
    <body>
    <span></span>
    <span><br>Following are the last run execution status.<b><br><br>Test Result:<b><br><br></span>
      <table style="width: 600px;">
         <thead>
            <th style="width: 20vh;"> Total Test Executed </th>
            <th style="width: 20vh;"> Pass </th>
            <th style="width: 20vh;"> Fail </th>
            <th style="width: 15vh;"> Percentage (%%)</th>
        </thead>
        <tbody>
            <tr>
               <td style="text-align: center;">""" + repr(total_tc_executed) + """</td>
               <td style="text-align: center;">""" + repr(total_tc_pass) + """</td>
               <td style="text-align: center;">""" + repr(total_tc_fail) + """</td>
               <td style="text-align: center;">""" + repr(percentage) + """</td>
            </tr>
        </tbody>
      </table>       
    <span><br><br><b>Failed Tests:<b><br><br></span>
      <table style="width: 100%;">
         <thead>
            <th style="width: 20vh;"> Test Case </th>
            <th style="width: 20vh;"> Error </th>             
        </thead>
        <tbody>
            <tr>
                <td>""" + ''.join(template_failed_tc[1:]) + """</td>
            </tr>
        </tbody>
      </table>
    </html>
    """

    try:
        part1 = MIMEBase('application', "octet-stream")
        part1.set_payload(open(excel_file, "rb").read())
        encoders.encode_base64(part1)
        part1.add_header('Content-Disposition', 'attachment; filename="%s"' % result_file)
        msg.attach(part1)
        msg.attach(MIMEText(html, 'html'))
        server = smtplib.SMTP('webmail.nv.carlsonwagonlit.com')
        server.sendmail(sender, recipients, msg.as_string())        
        print 'successfully sent the mail'  
    except Exception as e:
        print "failed to send mail due to error: {}".format(e)

def get_all_xml_files():
    xml_files = []
    for root, dirnames, filenames in os.walk('.'):
        for filename in fnmatch.filter(filenames, '*.xml'):
            xml_files.append(os.path.join(root, filename))
    return xml_files

def get_test_status_path(elem, tc_name_attrib):
    if "'" in tc_name_attrib:
        tc_name_quoted = '"%s"' % tc_name_attrib
        return elem.xpath("//test[@name=" + tc_name_quoted + "]/status")
    else:
        return elem.xpath("//test[@name='" + tc_name_attrib + "']/status")

if __name__ == '__main__':
    send_mail()