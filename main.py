from selenium import webdriver
from telegram.ext import *
from selenium.common.exceptions import NoSuchElementException
import time
import os
import warnings
import re
warnings.filterwarnings("ignore", category=DeprecationWarning)
op = webdriver.ChromeOptions()
op.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
op.add_argument("--headless")
op.add_argument("--no-sandbox")
op.add_argument("--disable-dev-sh-usage")
vtu_num=""
def start_command(update, context):
    update.message.reply_text("Enter valid VTU Number\n vtuxxxxx")
def handle_message(update, context):
    numbe = str(update.message.text).lower()
    print(numbe)
    res = func(numbe,update,context)
    update.message.reply_text(res)
def func(vtu_num,update,context):
    d=webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=op)
    d.get("http://exams.veltech.edu.in/Studentlogin/StuLogin.aspx")
    ubox=d.find_element_by_xpath('//*[@id="txtUserName"]')
    ubox.send_keys(vtu_num)
    pbox=d.find_element_by_xpath('//*[@id="txtPassword"]')
    pbox.send_keys(vtu_num)
    ld=d.find_element_by_xpath('//*[@id="LoginButton"]')
    ld.click()
    names = d.find_element_by_xpath('//*[@id="ContentPlaceHolder1_lblStudentName"]').text
    sems_comp=d.find_element_by_xpath('//*[@id="ContentPlaceHolder1_lblSemester"]').text
    ti=(int(sems_comp)*8)-8
    update.message.reply_text("Estimated Waiting Time : "+str(ti)+" secs")
    d.get("http://exams.veltech.edu.in/Studentlogin/UserPages/StudentCreditsPoint.aspx")
    ctable = d.find_elements_by_xpath('//*[@id="ContentPlaceHolder1_gvCredits"]/tbody/tr')
    clen = len(ctable)
    credit_code, credit_credit = [], []
    ra,ne,ab=[],[],[]
    for i in range(3, clen + 1):
        stri = d.find_element_by_xpath('//*[ @ id = "ContentPlaceHolder1_gvCredits"]/tbody/tr[' + str(i) + ']/td[1]').text
        l = re.compile("^\d{4}[A-za-z]{2}\d{3}$")
        if (l.match(stri)):
            credit_code.append(stri)
            credit_credit.append(d.find_element_by_xpath('//*[ @ id = "ContentPlaceHolder1_gvCredits"]/tbody/tr[' + str(i) + ']/td[3]').text)
    d.get("http://exams.veltech.edu.in/Studentlogin/UserPages/StudentUniversityResultsBySem.aspx")
    reg_no=d.find_element_by_xpath('//*[@id="ContentPlaceHolder1_lblRegNoTxt"]').text
    branch=d.find_element_by_xpath('//*[@id="ContentPlaceHolder1_lblBranchTxt"]').text
    sem_wise = names+"\n"+reg_no+"\n"+branch+"\n"
    sgpa,ccode,cname,cgrade,ccredit,cgpoints=[],[],[],[],[],[]
    sem_det=""
    for semm in range(1,int(sems_comp)):
        scode = []
        sname = []
        sgrade = []
        d.find_element_by_xpath('//select[@id="ContentPlaceHolder1_ddlSemester"]/option['+str(semm)+']').click()
        time.sleep(3)
        table=d.find_elements_by_xpath('//*[@id="ContentPlaceHolder1_gvExamResult2013"]/tbody/tr')
        sub_count=len(table)
        for i in range(2,sub_count+1):
            p=d.find_element_by_xpath('//*[@id="ContentPlaceHolder1_gvExamResult2013"]/tbody/tr['+str(i)+']/td[3]').text
            scode.append(p)
            p = d.find_element_by_xpath('//*[@id="ContentPlaceHolder1_gvExamResult2013"]/tbody/tr[' + str(i) + ']/td[4]').text
            sname.append(p)
            p = d.find_element_by_xpath('//*[@id="ContentPlaceHolder1_gvExamResult2013"]/tbody/tr[' + str(i) + ']/td[5]').text
            sgrade.append(p)
        scredit=[0]*(sub_count-1)
        for c in scode:
            for coder in credit_code:
                if(coder==c):
                    idex=scode.index(c)
                    j=credit_code.index(coder)
                    scredit[idex]=credit_credit[j]
        for i in range(len(scredit)):
            scredit[i]=int(scredit[i])
        sgpoints=[0]*len(scredit)
        for i in range(len(sgrade)):
            if(sgrade[i]=="A"):
                sgpoints[i]=9*scredit[i]
            elif(sgrade[i]=="S"):
                sgpoints[i]=10*scredit[i]
            elif (sgrade[i] == "B"):
                sgpoints[i] = 8 * scredit[i]
            elif (sgrade[i] == "C"):
                sgpoints[i] = 7 * scredit[i]
            elif (sgrade[i] == "D"):
                sgpoints[i] = 6 * scredit[i]
            elif (sgrade[i] == "RA"):
                ra.append(sname[i])
                sgpoints[i] = 0 * scredit[i]
            elif (sgrade[i] == "NE"):
                ne.append(sname[i])
                sgpoints[i] = 0 * scredit[i]
            elif (sgrade[i] == "AB"):
                ab.append(sname[i])
                sgpoints[i] = 0 * scredit[i]
            else:
                sgpoints[i] = 0 * scredit[i]
        for pp in range(len(scredit)):
            sem_det=scode[pp]+"\t\t"+sname[pp]+"\t\t"+str(scredit[pp])+"\t\t"+sgrade[pp]
        gpa=sum(sgpoints)/(sum(scredit)*10)
        sem_wise=sem_wise+"semester - "+str(semm)+" Gpa : "+str(gpa*10)[0:4]+"\n"
        ccode.extend(scode)
        ccredit.extend(scredit)
        cname.extend(sname)
        cgpoints.extend(sgpoints)
        cgrade.extend(sgrade)
        sgpa.append(gpa)
        gpa3 = sum(cgpoints)/(sum(ccredit)*10)
        sem_wise=sem_wise+"CGPA After Semester - "+str(semm)+" is "+str(gpa3*10)[0:4]+"\n"
        Math.ceil
    cgpa=sum(sgpa)/len(sgpa)
    cgpa2=sum(cgpoints)/(sum(ccredit)*10)
    sem_wise=sem_wise+"\nTotal Cgpa : "+str(cgpa2*10)[0:4]
    if(len(ra)!=0):
        sem_wise=sem_wise+"\n\nRe-Appeared Exam List\n"
        for i in range(len(ra)):
            sem_wise=sem_wise+str(i+1)+" . "+ra[i]
    if (len(ne) != 0):
        sem_wise = sem_wise + "\n\nNot Eligible Exam List\n"
        for i in range(len(ne)):
            sem_wise = sem_wise + str(i + 1) + " . " + ne[i]
    if (len(ab) != 0):
        sem_wise = sem_wise + "\n\nAbsent Exam List\n"
        for i in range(len(ab)):
            sem_wise = sem_wise + str(i + 1) + " . " + ab[i]
    return sem_wise
updater = Updater("5193860219:AAEVRNHmwKbpV4_gqbvBSw0juTL9CEmVGCw", use_context=True)
dp = updater.dispatcher
dp.add_handler(CommandHandler("start", start_command))
dp.add_handler(MessageHandler(Filters.text, handle_message))
updater.start_polling()
updater.idle()












