# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 02:51:49 2021

@author: 0526p
"""
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
from pathlib import Path
import cv2
import numpy as np
import face_recognition
import os
import datetime
import pytz
import csv


root = Tk()


def createSubjectCsvFile(getInput, path_6):
    path = path_6 + '/' + getInput+'.csv'
    with open(path, 'w', newline='') as f:
        theWriter = csv.writer(f)
        theWriter.writerow(['Name', 'Roll No'])


def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

def encoding_section():
    global images, classNames, RollNo
    path_13 = new_path + '/Image Directory/branch'
    path_14 = path_13 + '/' + image_directory_section

    images = []
    classNames = []
    RollNo = []

    myList_1 = os.listdir(path_14)
    for cl in myList_1:
        curImg = cv2.imread(f'{path_14}/{cl}')
        images.append(curImg)
        text = os.path.splitext(cl)[0]
        classNames.append(text.split('.')[0])
        RollNo.append(text.split('.')[1])

def columnCheck(getInput, path_6):
    path = path_6 + '/' + getInput+'.csv'
    with open(path, 'r') as read_obj:
        theReader = csv.reader(read_obj, delimiter=',')
        csvList = []
        for l in theReader:
            csvList.append(l)
    return csvList[0][-1]


def fillStudentNameAndRoll(name, roll, getInput, path_6):
    path = path_6 + '/' + getInput+'.csv'
    with open(path, 'r+') as f:
        myDataList = csv.reader(f)
        rollList = []
        for line in myDataList:
            if line != []:
                rollList.append(line[1])

        if roll not in rollList:
            f.writelines(f"{name},{roll}")
            New_roll = roll
            return New_roll


def fill_blank_column(getInput, path_6):
    path = path_6 + '/' + getInput+'.csv'
    rowList = []
    with open(path, 'r+') as g:
        theReader = csv.reader(g)
        for r in theReader:
            if r != []:
                rowList.append(r)

    len_of_first_index = len(rowList[0])
    dateList = rowList[0][2:len_of_first_index]
    with open(path, 'w') as g:
        theWriter = csv.writer(g)
        for r in rowList:
            if rowList.index(r) == 0:
                pass
            elif len(r) < len_of_first_index:
                i = len(r)-2
                while dateList[i] != dateList[-1]:
                    r.append(0)
                    print(i)
                    i = i+1
            theWriter.writerow(r)


def addNewData(getInput, path_6):
    path = path_6 + '/' + getInput+'.csv'
    rowList = []
    with open(path, 'r') as f:
        thereader = csv.reader(f)
        for row in thereader:
            if row != []:
                rowList.append(row)

    len_of_first_index = len(rowList[0])
    with open(path, 'w') as f:
        fwriter = csv.writer(f)
        for i in rowList:
            if rowList.index(i) == 0:
                pass
            else:
                if len(i) == len_of_first_index:
                    pass
                else:
                    i.append(0)
            fwriter.writerow(i)


def makeNewHeader(getInput, path_6):
    path = path_6 + '/' + getInput+'.csv'
    rowList = []
    with open(path, 'r') as f:
        thereader = csv.reader(f)
        for row in thereader:
            if row != []:
                rowList.append(row)

    with open(path, 'w') as f:
        fwriter = csv.writer(f)
        for i in rowList:
            if rowList.index(i) == 0:
                i.append(now2)
            fwriter.writerow(i)


def markAttendance(getInput, roll, path_6):
    path = path_6 + '/' + getInput+'.csv'
    with open(path, 'r+') as f:
        myDataList = csv.reader(f)
        rowList = []
        rollList = []
        dateList = []
        for line in myDataList:
            if line != []:
                rollList.append(line[1])
                dateList.append(line[-1])
                rowList.append(line)
        indexPosition = rollList.index(roll)
        value = dateList[indexPosition]

    with open(path, 'w') as f:
        fwriter = csv.writer(f)

        if value == '0':
            for i in rowList:
                if rowList.index(i) == indexPosition:
                    i.remove('0')
                    i.append(now1)
                    print(i)
                    cv2.rectangle(img, (40, 20), (390, 60),
                                  (127, 255, 212), cv2.FILLED)
                    cv2.putText(img, 'Attendance Marked', (50, 50),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (230, 20, 60), 2)
                fwriter.writerow(i)
        elif value != '0':
            cv2.rectangle(img, (40, 20), (530, 60),
                          (127, 255, 212), cv2.FILLED)
            cv2.putText(img, 'Attendance Already Marked', (50, 50),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
            for i in rowList:
                fwriter.writerow(i)


def capture(getInput, mylist2, path_6, i, j):
    cap = cv2.VideoCapture(0)

    while True:
        global img
        success, img = cap.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        faceCurFrame = face_recognition.face_locations(imgS)
        encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

        try:
            for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
                matches = face_recognition.compare_faces(
                    encodeListKnown, encodeFace)
                faceDis = face_recognition.face_distance(
                    encodeListKnown, encodeFace)
                matchIndex = np.argmin(faceDis)
        
                if matches[matchIndex]:
                    name = classNames[matchIndex].upper()
                    roll = RollNo[matchIndex]
        
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                    cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 0), 2)
                    cv2.rectangle(img, (x1, y2+4), (x2, y2+110),
                                  (255, 0, 0), cv2.FILLED)
                    cv2.putText(img, name, (x1+10, y2+35),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                    cv2.putText(img, roll, (x1+8, y2+65),
                                cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)
                    cv2.putText(img, now1, (x1+8, y2+95),
                                cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)
        
                    pathFind = f'{getInput}.csv'
                    now2_string = f'{now2}'
                    print(pathFind, mylist2)
                    global checkDate
                    if pathFind in mylist2:
                        checkDate = columnCheck(getInput, path_6)
        
                    if pathFind in mylist2:
                        if checkDate == now2_string:
        
                            return_New_roll = fillStudentNameAndRoll(
                                name, roll, getInput, path_6)
                            if return_New_roll:
                                fill_blank_column(getInput, path_6)
                                addNewData(getInput, path_6)
                                markAttendance(getInput, roll, path_6)
        
                            else:
                                fill_blank_column(getInput, path_6)
                                addNewData(getInput, path_6)
                                markAttendance(getInput, roll, path_6)
        
                        elif checkDate != now2_string:
                            makeNewHeader(getInput, path_6)
                            fill_blank_column(getInput, path_6)
                            fillStudentNameAndRoll(name, roll, getInput, path_6)
                            addNewData(getInput, path_6)
                            markAttendance(getInput, roll, path_6)
        
                    elif pathFind not in mylist2:
                        createSubjectCsvFile(getInput, path_6)
                        makeNewHeader(getInput, path_6)
                        fillStudentNameAndRoll(name, roll, getInput, path_6)
                        addNewData(getInput, path_6)
                        markAttendance(getInput, roll, path_6)
                        mylist2.append(pathFind)
        
                    print()
                    print(faceDis)
                    print(name,
                          '\n',
                          roll,
                          '\n',
                          now1,
                          '\n',
                          now2,
                          '\n')
            
            cv2.imshow('Webcam', img)
            key = cv2.waitKey(10)
            if key == ord('f'):
                subject_window.deiconify()
                cap.release()
                cv2.destroyAllWindows()

        except ValueError:
            split = image_directory_section.split('/')
            cv2.destroyAllWindows()
            cap.release()
            subject_window.deiconify()
            Label(subject_window, text=f'Section {split[2]} Is Empty', bg='lightgoldenrodyellow', fg='red', padx=10).grid(
                    row=i+j+1, column=1)

def open_subject(subjectName, i, j):
    global encodeListKnown
    myList_2 = os.listdir(path_6)
    encodeListKnown = findEncodings(images)
    capture(subjectName, myList_2, path_6, i, j)
    
def new_subject(i, j):

    def show_forward():
        Button(frame_13, text='>>', command=lambda: [subject_directories(
        ), semester_window.withdraw()], bg='white', fg='midnightblue', padx=10).grid(row=0, column=3)
        Button(frame_9, text='>>', command=lambda: [semester_window.deiconify(
        ), section_window.withdraw()], bg='white', fg='midnightblue', padx=10).grid(row=0, column=3)
        Button(frame_5, text='>>', command=lambda: [section_window.deiconify(
        ), batch_window.withdraw()], bg='white', fg='midnightblue', padx=10).grid(row=0, column=3)
        Button(frame_1, text='>>', command=lambda: [batch_window.deiconify(
        ), branch_window.withdraw()], bg='white', fg='midnightblue', padx=10).grid(row=0, column=3)
        Button(root, text='>>', command=lambda: [branch_window.deiconify(
        ), root.withdraw()], bg='white', fg='midnightblue', padx=10).grid(row=0, column=1)

    Button(frame_18, text='<<', command=lambda: [subject_window.destroy(), subject_directories(), semester_window.withdraw(
    ), section_window.withdraw(), batch_window.withdraw(), branch_window.withdraw(), root.withdraw()], bg='white', fg='midnightblue', padx=10).grid(row=0, column=0)
    Button(frame_18, text='Start', command=lambda: [subject_window.destroy(), semester_window.withdraw(), section_window.withdraw(
    ), batch_window.withdraw(), branch_window.withdraw(), show_forward(), root.deiconify()], bg='white', fg='midnightblue', padx=20).grid(row=0, column=1)
    Button(frame_18, text='Home', command=lambda: [subject_window.destroy(), semester_window.withdraw(), section_window.withdraw(
    ), batch_window.withdraw(), branch_window.deiconify(), show_forward()], bg='white', fg='midnightblue', padx=20).grid(row=0, column=2)

    Button(subject_window, text='New',
           state=DISABLED, bg='white', fg='midnightblue', padx=15).grid(row=0, column=3)
    Button(subject_window, text='Remove',
           command=lambda: [subject_window.destroy(), root.withdraw(), branch_window.withdraw(), batch_window.withdraw(
           ), batch_window.withdraw(), section_window.withdraw(), semester_window.withdraw(), remove_subject(i, j)], bg='white', fg='midnightblue').grid(row=0, column=4)

    Label(frame_19, text=str(j)+' '*10, bg='lightgoldenrodyellow',
          fg='black').grid(row=i+j, column=0)

    e = Entry(frame_19, width=25,
              fg='blue', bg='white', borderwidth=10)
    e.grid(row=i+j, column=1)
    e.insert(0, 'Enter Subject Name')

    err = ['Enter', 'Subject', 'Name', 'Enter subject', 'Enter subject', 'Subject name',
           'Subject enter', 'Name subject', 'Name enter', 'Enter subject name']

    def save(i, j, err):
        if e.get().capitalize() in err:
            Label(frame_19, text='Enter Subject Name', bg='lightgoldenrodyellow', fg='red').grid(
                row=i+j+1, column=1)
            new_subject(i, j)
        elif e.get() == '':
            Label(frame_19, text='Enter Subject Name', bg='lightgoldenrodyellow', fg='red').grid(
                row=i+j+1, column=1)
            new_subject(i, j)
        elif (e.get().capitalize()+'.csv') not in os.listdir(path_6):
            getInput = e.get().capitalize()
            createSubjectCsvFile(getInput, path_6)
            makeNewHeader(getInput, path_6)
            subject_window.destroy()
            subject_directories()
        elif e.get().capitalize()+'.csv' in os.listdir(path_6):
            Label(frame_19, text='File Already Exists', bg='lightgoldenrodyellow', fg='red', padx=10).grid(
                row=i+j+1, column=1)
            new_subject(i, j)

    Button(subject_window, text='Save', command=lambda: [save(
        i, j, err)], bg='white', fg='midnightblue', padx=15).grid(row=5, column=2)
    Button(subject_window, text='Cancle', command=lambda: [subject_window.destroy(), subject_directories(), semester_window.withdraw(), section_window.withdraw(
    ), batch_window.withdraw(), branch_window.withdraw(), root.withdraw()], bg='white', fg='midnightblue', padx=10).grid(row=5, column=3)
    Button(subject_window, text='Exit', command=popup_1,
           bg='white', fg='midnightblue', padx=10).grid(row=5, column=4)


def remove_subject(i, j):

    global remove_subject_window, frame_21
    remove_subject_window = Toplevel()
    #remove_subject_window.geometry('400x175')
    remove_subject_window.title(path_6)
    remove_subject_window.iconbitmap(
        'C:/Users/0526p/Pictures/implementation/LLFRAS.ico')
    remove_subject_window.config(bg='lightgoldenrodyellow')

    frame_20 = LabelFrame(remove_subject_window,
                  bg='lightgoldenrodyellow')
    frame_20.grid(row = 0, column = 0)

    def wait_forward():
        Label(subject_window, text=f'Please Wait...', bg='lightgoldenrodyellow', fg='red', padx=10).grid(
                row=i+j+1, column=1)
        Label(subject_window, text=f'WebCam Will Be', bg='lightgoldenrodyellow', fg='red', padx=10).grid(
                row=i+j+2, column=1)
        Label(subject_window, text=f'Open Soon', bg='lightgoldenrodyellow', fg='red', padx=10).grid(
                row=i+j+3, column=1)
    
    def show_forward():
        Button(frame_13, text='>>', command=lambda: [subject_window_directories(
        ), semester_window.withdraw()], bg='white', fg='midnightblue', padx=10).grid(row=0, column=3)
        Button(frame_9, text='>>', command=lambda: [semester_window.deiconify(
        ), section_window.withdraw()], bg='white', fg='midnightblue', padx=10).grid(row=0, column=3)
        Button(frame_5, text='>>', command=lambda: [section_window.deiconify(
        ), batch_window.withdraw()], bg='white', fg='midnightblue', padx=10).grid(row=0, column=3)
        Button(frame_1, text='>>', command=lambda: [batch_window.deiconify(
        ), branch_window.withdraw()], bg='white', fg='midnightblue', padx=10).grid(row=0, column=3)
        Button(root, text='>>', command=lambda: [branch_window.deiconify(
        ), root.withdraw()], bg='white', fg='midnightblue', padx=10).grid(row=0, column=1)

    Button(frame_20, text='<<', command=lambda: [deselect_button(length), remove_subject_window.destroy(), subject_window.destroy(), subject_directories(
    ), semester_window.withdraw(), batch_window.withdraw(), branch_window.withdraw(), root.withdraw()], bg='white', fg='midnightblue', padx=10).grid(row=0, column=0)
    Button(frame_20, text='Start', command=lambda: [deselect_button(length), remove_subject_window.destroy(), subject_window.destroy(), show_forward(
    ), semester_window.withdraw(), section_window.withdraw(), batch_window.withdraw(), root.deiconify()], bg='white', fg='midnightblue', padx=20).grid(row=0, column=1)
    Button(frame_20, text='Home', command=lambda: [deselect_button(length), remove_subject_window.destroy(), subject_window.destroy(), semester_window.withdraw(), section_window.withdraw(
    ), batch_window.withdraw(), branch_window.deiconify(), show_forward()], bg='white', fg='midnightblue', padx=20).grid(row=0, column=2)
    Button(frame_20, text='>>', state=DISABLED, bg='white', fg='midnightblue',
           padx=10).grid(row=0, column=3)
    
    Label(remove_subject_window, text = ' '*30,
          bg='lightgoldenrodyellow').grid(row = 0, column = 1)

    Button(remove_subject_window, text='New',
           command=lambda: [remove_subject_window.destroy(), subject_window.destroy(), subject_directories(), new_subject(i, j), semester_window.withdraw(), section_window.withdraw(), batch_window.withdraw(), branch_window.withdraw(), root.withdraw()], bg='white', fg='midnightblue', padx=15).grid(row=0, column=3)
    Button(remove_subject_window, text='Remove',
           state =  DISABLED, bg='white', fg='midnightblue').grid(row=0, column=4)
    Label(remove_subject_window, text='                                           ', bg='lightgoldenrodyellow').grid(
        row=1)

    frame_21 = LabelFrame(remove_subject_window, text = '                 Subject Name',
                  bg='lightgoldenrodyellow', fg = 'purple')
    frame_21.grid(row = 2, column = 0)
    
    collect_check = []
    def collect(batch):
        collect_check.append(batch)

    def delete(collect_check):
        for b in collect_check:
            path = path_6 + '/' + b
         #   os.rmdir(path)
            os.remove(path)
        remove_subject_window.destroy()
        subject_window.destroy()
        subject_directories()
    
    def selection(collect_check):
        if collect_check == []:
            if os.listdir(path_6) == []:
                remove_subject_window.destroy()
                remove_subject(i, j)
                Label(frame_21, text="No subdirectories",
                      bg='lightgoldenrodyellow', fg='red', padx=10).grid(row=i+j+1, column=1)
            else:
                remove_subject_window.destroy()
                remove_subject(i, j)
                Label(frame_21, text="Select at least one folder",
                      bg='lightgoldenrodyellow', fg='red', padx=10).grid(row=i+j+1, column=1)
        else:
            delete(collect_check)

    def deselect_button(length):
        for k in range(4, length+4):
            check1 = Checkbutton(remove_subject_window,
                                 text=' ', bg='lightgoldenrodyellow')
            check1.grid(row=k, column=0)
            check1.deselect()

    subject_list = os.listdir(path_6)
    i = 3
    j = 1
    length = len(subject_list)
    for subject in subject_list:
        sub = subject.split('.')
        subject_csv_file = sub[0]
        check2 = Checkbutton(frame_21, text=' '*10, command=lambda subject=subject: [
                             collect(subject)], bg='lightgoldenrodyellow')
        check2.grid(row=i+j, column=0)
        check2.deselect()
        Button(frame_21, text=subject_csv_file, command=lambda subject_csv_file=subject_csv_file: [remove_subejct_window.destroy(), open_subject(subject_csv_file, i, j), subject_directories(
        ), subject_window.withdraw(), semester_window.withdraw(), section_window.withdraw(), batch_window.withdraw(), branch_window.withdraw(), root.withdraw()], bg='navy', fg='white', anchor = W, width = 25).grid(row=i+j, column=1, sticky = W+E)
        j = j+1
        i = 3+j

    space = Label(remove_subject_window, text=' ',
                  bg='lightgoldenrodyellow').grid(row=5)

    Button(remove_subject_window, text='Delete', command=lambda: [selection(
            collect_check)], bg='white', fg='midnightblue', padx=15).grid(row=6, column=2)
    Button(remove_subject_window, text='Cancle', command=lambda: [deselect_button(length), remove_subject_window.destroy(), subject_window.destroy(), root.withdraw(
    ), branch_window.withdraw(), batch_window.withdraw(), section_window.withdraw(), semester_window.withdraw(), subject_directories()], bg='white', fg='midnightblue', padx=10).grid(row=6, column=3)
    Button(remove_subject_window, text='Exit', command=popup_1,
           bg='white', fg='midnightblue', padx=10).grid(row=6, column=4)


def subject_directories():

    global subject_window, frame_18, frame_19
    subject_window = Toplevel()
    subject_window.title(path_6)
    subject_window.iconbitmap(
        'C:/Users/0526p/Pictures/implementation/LLFRAS.ico')
    subject_window.config(bg='lightgoldenrodyellow')

    now = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
    global now1, now2
    now1 = now.strftime('%I:%M')
    now2 = now.strftime('%Y-%m-%d')

    
    frame_18 = LabelFrame(subject_window,
                  bg='lightgoldenrodyellow')
    frame_18.grid(row = 0, column = 0)

    def wait_forward():
        Label(subject_window, text=f'Please Wait...', bg='lightgoldenrodyellow', fg='red', padx=10).grid(
                row=i+j+1, column=1)
        Label(subject_window, text=f'WebCam Will Be', bg='lightgoldenrodyellow', fg='red', padx=10).grid(
                row=i+j+2, column=1)
        Label(subject_window, text=f'Open Soon', bg='lightgoldenrodyellow', fg='red', padx=10).grid(
                row=i+j+3, column=1)
    
    def show_forward():
        Button(frame_13, text='>>', command=lambda: [subject_window.deiconify(
        ), semester_window.withdraw()], bg='white', fg='midnightblue', padx=10).grid(row=0, column=3)
        Button(frame_9, text='>>', command=lambda: [semester_window.deiconify(
        ), section_window.withdraw()], bg='white', fg='midnightblue', padx=10).grid(row=0, column=3)
        Button(frame_5, text='>>', command=lambda: [section_window.deiconify(
        ), batch_window.withdraw()], bg='white', fg='midnightblue', padx=10).grid(row=0, column=3)
        Button(frame_1, text='>>', command=lambda: [batch_window.deiconify(
        ), branch_window.withdraw()], bg='white', fg='midnightblue', padx=10).grid(row=0, column=3)
        Button(root, text='>>', command=lambda: [branch_window.deiconify(
        ), root.withdraw()], bg='white', fg='midnightblue', padx=10).grid(row=0, column=1)

    Button(frame_18, text='<<', command=lambda: [subject_window.withdraw(), semester_window.deiconify(
    ), show_forward()], bg='white', fg='midnightblue', padx=10).grid(row=0, column=0)
    Button(frame_18, text='Start', command=lambda: [subject_window.withdraw(), semester_window.withdraw(), section_window.withdraw(
    ), batch_window.withdraw(), root.deiconify(), show_forward()], bg='white', fg='midnightblue', padx=20).grid(row=0, column=1)
    Button(frame_18, text='Home', command=lambda: [subject_window.withdraw(), semester_window.withdraw(), section_window.withdraw(
    ), batch_window.withdraw(), branch_window.deiconify(), show_forward()], bg='white', fg='midnightblue', padx=20).grid(row=0, column=2)
    Button(frame_18, text='>>', state=DISABLED, bg='white', fg='midnightblue',
           padx=10).grid(row=0, column=3)

    Label(subject_window, text = ' '*30,
          bg='lightgoldenrodyellow').grid(row = 0, column = 1)
    
    Button(subject_window, text='New',
           command=lambda: [new_subject(i, j), semester_window.withdraw(), section_window.withdraw(), batch_window.withdraw(), branch_window.withdraw(), root.withdraw()], bg='white', fg='midnightblue', padx=15).grid(row=0, column=3)
    Button(subject_window, text='Remove',
           command=lambda: [root.withdraw(), branch_window.withdraw(), batch_window.withdraw(), batch_window.withdraw(), section_window.withdraw(), semester_window.withdraw(), subject_window.withdraw(), remove_subject(i, j)], bg='white', fg='midnightblue').grid(row=0, column=4)
    Label(subject_window, text='                                           ', bg='lightgoldenrodyellow').grid(
        row=1)
    
    frame_19 = LabelFrame(subject_window, text = 'Sl No       Subject Name',
                  bg='lightgoldenrodyellow', fg = 'purple')
    frame_19.grid(row = 2, column = 0)

    subject_list = os.listdir(path_6)
    i = 3
    j = 1
    k = 0
    for subject in subject_list:
        sub = subject.split('.')
        subject_csv_file = sub[0]
        Label(frame_19, text=str(j)+' '*15, bg='lightgoldenrodyellow',
              fg='black').grid(row=k, column=0)
        Button(frame_19, text=subject_csv_file, command=lambda subject_csv_file=subject_csv_file: [open_subject(subject_csv_file, i, j), subject_window.withdraw(
        ), semester_window.withdraw(), section_window.withdraw(), batch_window.withdraw(), branch_window.withdraw(), root.withdraw()], bg='navy', fg='white', anchor = W, width = 25).grid(row=k, column=1, sticky = W+E)
        j = j+1
        k = k+1
        
    Label(subject_window, text=' ',
          bg='lightgoldenrodyellow').grid(row=3)

    Button(subject_window, text='Exit', command=popup_1,
           bg='white', fg='midnightblue', padx=10).grid(row=5, column=4)
    

def open_semester(semesterName):
    global path_6
    path_6 = path_5 + '/' + semesterName
    subject_directories()


def new_semester(i, j):

    def show_forward():
        Button(frame_9, text='>>', command=lambda: [semester_directories(
        ), section_window.withdraw()], bg='white', fg='midnightblue', padx=10).grid(row=0, column=3)
        Button(frame_5, text='>>', command=lambda: [section_window.deiconify(
        ), batch_window.withdraw()], bg='white', fg='midnightblue', padx=10).grid(row=0, column=3)
        Button(frame_1, text='>>', command=lambda: [batch_window.deiconify(
        ), branch_window.withdraw()], bg='white', fg='midnightblue', padx=10).grid(row=0, column=3)
        Button(root, text='>>', command=lambda: [branch_window.deiconify(
        ), root.withdraw()], bg='white', fg='midnightblue', padx=10).grid(row=0, column=1)

    Button(frame_13, text='<<', command=lambda: [semester_window.destroy(), semester_directories(), section_window.withdraw(
    ), batch_window.withdraw(), branch_window.withdraw(), root.withdraw()], bg='white', fg='midnightblue', padx=10).grid(row=0, column=0)
    Button(frame_13, text='Start', command=lambda: [semester_window.destroy(), section_window.withdraw(), batch_window.withdraw(
    ), branch_window.withdraw(), show_forward(), root.deiconify()], bg='white', fg='midnightblue', padx=20).grid(row=0, column=1)
    Button(frame_13, text='Home', command=lambda: [semester_window.destroy(), section_window.withdraw(), batch_window.withdraw(
    ), branch_window.deiconify(), show_forward()], bg='white', fg='midnightblue', padx=20).grid(row=0, column=2)

    Button(semester_window, text='New', state=DISABLED, bg='white',
           fg='midnightblue', padx=15).grid(row=0, column=3)
    Button(semester_window, text='Remove', command=lambda: [semester_window.destroy(), root.withdraw(), branch_window.withdraw(
    ), batch_window.withdraw(), section_window.withdraw(), remove_semester(i, j)], bg='white', fg='midnightblue').grid(row=0, column=4)

    Label(frame_15, text=str(j) + ' '*15, bg='lightgoldenrodyellow',
          fg='black').grid(row=i+j, column=0)
    Label(frame_15, text='Select Semester', bg='lightgoldenrodyellow', fg='purple').grid(
        row=i+j, column=1)
    
    style= ttk.Style()
    style.theme_use('clam')
    style.configure("TCombobox", foreground = 'blue', fieldbackground= "white", background= 'white')
    
    number_choosen = ttk.Combobox(frame_15, width=20)
    number_choosen['values'] = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
    number_choosen.grid(row=i+j+1, column=1)
    number_choosen.current(0)

    def save(i, j):
        try:
            if number_choosen.get() not in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']:
                Label(frame_15, text="Choose Semester From List", bg='lightgoldenrodyellow', fg='red').grid(
                    row=i+j+2, column=1)
            else:
                os.mkdir(path_5+'/' + number_choosen.get())
                semester_window.destroy()
                semester_directories()
        except FileExistsError:
            if number_choosen.get() == '':
                Label(frame_15, text="You Didn't Select Batch", bg='lightgoldenrodyellow', fg='red').grid(
                    row=i+j+2, column=1)
            elif number_choosen.get() in os.listdir(path_5):
                Label(frame_15, text='File Already Exists', bg='lightgoldenrodyellow', fg='red', padx=10).grid(
                    row=i+j+2, column=1)
                new_semester(i, j)

    Button(semester_window, text='Save', command=lambda: [
           save(i, j)], bg='white', fg='midnightblue', padx=15).grid(row=6, column=2)
    Button(semester_window, text='Cancle', command=lambda: [semester_window.destroy(), semester_directories(), section_window.withdraw(
    ), batch_window.withdraw(), branch_window.withdraw(), root.withdraw()], bg='white', fg='midnightblue', padx=10).grid(row=6, column=3)
    Button(semester_window, text='Exit', command=popup_1,
           bg='white', fg='midnightblue', padx=10).grid(row=6, column=4)


def remove_semester(i, j):
    global remove_semester_window, frame_17
    remove_semester_window = Toplevel()
    # remove_semester_window.geometry('400x175')
    remove_semester_window.title(path_5)
    remove_semester_window.iconbitmap(
        'C:/Users/0526p/Pictures/implementation/LLFRAS.ico')
    remove_semester_window.config(bg='lightgoldenrodyellow')

    frame_16 = LabelFrame(remove_semester_window,
                  bg='lightgoldenrodyellow')
    frame_16.grid(row = 0, column = 0)
    
    def show_forward():
        Button(frame_9, text='>>', command=lambda: [semester_directories(
        ), section_window.withdraw()], bg='white', fg='midnightblue', padx=10).grid(row=0, column=3)
        Button(frame_5, text='>>', command=lambda: [section_window.deiconify(
        ), batch_window.withdraw()], bg='white', fg='midnightblue', padx=10).grid(row=0, column=3)
        Button(frame_1, text='>>', command=lambda: [batch_window.deiconify(
        ), branch_window.withdraw()], bg='white', fg='midnightblue', padx=10).grid(row=0, column=3)
        Button(root, text='>>', command=lambda: [branch_window.deiconify(
        ), root.withdraw()], bg='white', fg='midnightblue', padx=10).grid(row=0, column=1)

    Button(frame_16, text='<<', command=lambda: [deselect_button(length), remove_semester_window.destroy(), semester_window.destroy(), semester_directories(
    ), section_window.withdraw(), batch_window.withdraw(), branch_window.withdraw(), root.withdraw()], bg='white', fg='midnightblue', padx=10).grid(row=0, column=0)
    Button(frame_16, text='Start', command=lambda: [deselect_button(length), remove_semester_window.destroy(), semester_window.destroy(), show_forward(
    ), section_window.withdraw(), batch_window.withdraw(), branch_window.withdraw(), root.deiconify()], bg='white', fg='midnightblue', padx=20).grid(row=0, column=1)
    Button(frame_16, text='Home', command=lambda: [remove_semester_window.destroy(), semester_window.destroy(), section_window.withdraw(
    ), batch_window.withdraw(), branch_window.deiconify(), show_forward()], bg='white', fg='midnightblue', padx=20).grid(row=0, column=2)
    Button(frame_16, text='>>', state=DISABLED,
           bg='white', fg='midnightblue', padx=10).grid(row=0, column=3)
    
    Label(remove_semester_window, text = ' '*30,
          bg='lightgoldenrodyellow').grid(row = 0, column = 1)
    
    Button(remove_semester_window, text='New', command=lambda: [remove_semester_window.destroy(), semester_window.destroy(), semester_directories(), new_semester(
        i, j), section_window.withdraw(), batch_window.withdraw(), branch_window.withdraw(), root.withdraw()], bg='white', fg='midnightblue', padx=15).grid(row=0, column=3)
    Button(remove_semester_window, text='Remove', state=DISABLED,
           bg='white', fg='midnightblue').grid(row=0, column=4)
    Label(remove_semester_window, text='                                          ',
          bg='lightgoldenrodyellow').grid(row=1)

    frame_17 = LabelFrame(remove_semester_window, text = '                 Semester Name',
                  bg='lightgoldenrodyellow', fg = 'purple')
    frame_17.grid(row = 2, column = 0)
    
    collect_check = []

    def collect(batch):
        collect_check.append(batch)

    def delete(collect_check):
        try:
            for b in collect_check:
                path = path_5 + '/' + b
                os.rmdir(path)
            remove_semester_window.destroy()
            semester_window.destroy()
            semester_directories()
        except OSError:
            remove_semester_window.destroy()
            remove_semester(i, j)
            Label(frame_17, text='Delete Permission Denied',
                  bg='lightgoldenrodyellow', fg='red', padx=10).grid(row=i+j+1, column=1)
            Label(frame_17, text="Sub-directories presence",
                  bg='lightgoldenrodyellow', fg='red', padx=10).grid(row=i+j+2, column=1)
            Label(frame_17, text="In selected folder",
                  bg='lightgoldenrodyellow', fg='red', padx=10).grid(row=i+j+3, column=1)

    def selection(collect_check):
        if collect_check == []:
            if os.listdir(path_4) == []:
                remove_semester_window.destroy()
                remove_semester(i, j)
                Label(frame_17, text="No subdirectories",
                      bg='lightgoldenrodyellow', fg='red', padx=10).grid(row=i+j+1, column=1)
            else:
                remove_semester_window.destroy()
                remove_semester(i, j)
                Label(frame_17, text="Select at least one folder",
                      bg='lightgoldenrodyellow', fg='red', padx=10).grid(row=i+j+1, column=1)
        else:
            delete(collect_check)

    def deselect_button(length):
        for k in range(4, length+4):
            check1 = Checkbutton(remove_semester_window,
                                 text=' ', bg='lightgoldenrodyellow')
            check1.grid(row=k, column=0)
            check1.deselect()

    semester_list = os.listdir(path_5)
    i = 3
    j = 1
    length = len(semester_list)
    for semester in semester_list:
        check2 = Checkbutton(frame_17, text=' '*10, command=lambda semester=semester: [
                             collect(semester)], bg='lightgoldenrodyellow')
        check2.grid(row=i+j, column=0)
        check2.deselect()
        Button(frame_17, text=semester, command=lambda semester=semester: [remove_semester_window.destroy(), open_semester(semester), semester_directories(
        ), semester_window.withdraw(), section_window.withdraw(), batch_window.withdraw(), branch_window.withdraw(), root.withdraw()], bg='navy', fg='white', anchor = W, width = 25).grid(row=i+j, column=1, sticky = W+E)
        j = j+1
        i = i+j

    space = Label(remove_semester_window, text=' ',
                  bg='lightgoldenrodyellow').grid(row=5)

    try:
        subject_window.destroy()
        Button(remove_semester_window, text='Delete', command=lambda: [selection(
            collect_check)], bg='white', fg='midnightblue', padx=15).grid(row=6, column=2)
    except TclError:
        Button(remove_semester_window, text='Delete', command=lambda: [selection(
            collect_check)], bg='white', fg='midnightblue', padx=15).grid(row=6, column=2)
    except NameError:
        Button(remove_semester_window, text='Delete', command=lambda: [selection(
            collect_check)], bg='white', fg='midnightblue', padx=15).grid(row=6, column=2)
    Button(remove_semester_window, text='Cancle', command=lambda: [deselect_button(length), remove_semester_window.destroy(), semester_window.destroy(), root.withdraw(
    ), branch_window.withdraw(), batch_window.withdraw(), section_window.withdraw(), semester_directories()], bg='white', fg='midnightblue', padx=10).grid(row=6, column=3)
    Button(remove_semester_window, text='Exit', command=popup_1,
           bg='white', fg='midnightblue', padx=10).grid(row=6, column=4)


def semester_directories():

    global semester_window, frame_13, frame_15
    semester_window = Toplevel()
    semester_window.title(path_5)
    semester_window.iconbitmap(
        'C:/Users/0526p/Pictures/implementation/LLFRAS.ico')
    semester_window.config(bg='lightgoldenrodyellow')

    frame_13 = LabelFrame(semester_window,
                  bg='lightgoldenrodyellow')
    frame_13.grid(row = 0, column = 0)
    
    def show_forward():
        Button(frame_9, text='>>', command=lambda: [semester_window.deiconify(
        ), section_window.withdraw()], bg='white', fg='midnightblue', padx=10).grid(row=0, column=3)
        Button(frame_5, text='>>', command=lambda: [section_window.deiconify(
        ), batch_window.withdraw()], bg='white', fg='midnightblue', padx=10).grid(row=0, column=3)
        Button(frame_1, text='>>', command=lambda: [batch_window.deiconify(
        ), branch_window.withdraw()], bg='white', fg='midnightblue', padx=10).grid(row=0, column=3)
        Button(root, text='>>', command=lambda: [branch_window.deiconify(
        ), root.withdraw()], bg='white', fg='midnightblue', padx=10).grid(row=0, column=1)

    Button(frame_13, text='<<', command=lambda: [semester_window.withdraw(), section_window.deiconify(
    ), show_forward()], bg='white', fg='midnightblue', padx=10).grid(row=0, column=0)
    Button(frame_13, text='Start', command=lambda: [semester_window.withdraw(), section_window.withdraw(
    ), batch_window.withdraw(), root.deiconify(), show_forward()], bg='white', fg='midnightblue', padx=20).grid(row=0, column=1)
    Button(frame_13, text='Home', command=lambda: [semester_window.withdraw(), section_window.withdraw(), batch_window.withdraw(
    ), branch_window.deiconify(), show_forward()], bg='white', fg='midnightblue', padx=20).grid(row=0, column=2)
    Button(frame_13, text='>>', state=DISABLED, bg='white',
           fg='midnightblue', padx=10).grid(row=0, column=3)

    Label(semester_window, text = ' '*30,
          bg='lightgoldenrodyellow').grid(row = 0, column = 1)

    Button(semester_window, text='New', command=lambda: [new_semester(i, j), section_window.withdraw(), batch_window.withdraw(
    ), branch_window.withdraw(), root.withdraw()], bg='white', fg='midnightblue', padx=15).grid(row=0, column=3)
    Button(semester_window, text='Remove', command=lambda: [root.withdraw(), branch_window.withdraw(), batch_window.withdraw(
    ), section_window.withdraw(), semester_window.withdraw(), remove_semester(i, j)], bg='white', fg='midnightblue').grid(row=0, column=4)
    Label(semester_window, text='                                    ',
          bg='lightgoldenrodyellow').grid(row=1)

    try:
        global frame_14
        encoding_section()
        Label(semester_window, text=f'STUDENTS IN SECTION {input_3}',
              bg='lightgoldenrodyellow', fg='purple').grid(row=2, column=0)
        frame_14 = LabelFrame(semester_window,
                  bg='lightgoldenrodyellow', fg = 'purple')
        frame_14.grid(row = 3, column = 0)
        
        h = Scrollbar(frame_14, orient = 'horizontal')
        h.pack(side = BOTTOM, fill = X)
        v = Scrollbar(frame_14)
        v.pack(side = RIGHT, fill = Y)
        
        t1 = Text(frame_14, width = 28, height = 10, wrap = NONE, xscrollcommand = h.set, yscrollcommand = v.set, fg = 'green')
        t1.insert(END, 'Sl    First Name     Last Name     Roll No\n')
        t1.insert(END, ' \n')
        l = 1
        for name, roll in zip(classNames, RollNo):
            spli = name.split(' ')
            first_name = spli[0].capitalize()
            last_name = spli[1].capitalize()
            count_space_1 = 15-len(first_name)
            space_1 = ' '*count_space_1
            count_space_2 = 14-len(last_name)
            space_2 = ' '*count_space_2
            
            t1.insert(END,  str(l)+' '*5+first_name+space_1+last_name+space_2+str(roll))
            t1.insert(END, '\n')
            l = l+1
        
        t1.pack(side = TOP, fill = X)
        h.config(command = t1.xview)
        v.config(command = t1.yview)

    except FileNotFoundError:
        Label(semester_window, text='This Section Is Empty',
              bg='lightgoldenrodyellow', fg = 'purple').grid(row=2, column=0)
        Label(semester_window, text='    ',
              bg='lightgoldenrodyellow').grid(row=3)
        
    k = 4
    Label(semester_window, text='    ', bg='lightgoldenrodyellow').grid(row=k)
    
    frame_15 = LabelFrame(semester_window, text = 'Sl No       Semester Name',
                  bg='lightgoldenrodyellow', fg = 'purple')
    frame_15.grid(row = k+1, column = 0)
    
    semester_list = os.listdir(path_5)
    i = k+2
    j = 1
    z = 0
    for semester in semester_list:
        Label(frame_15, text=str(j)+' '*15, bg='lightgoldenrodyellow',
              fg='black').grid(row=z, column=0)
        Button(frame_15, text=semester, command=lambda semester=semester: [open_semester(semester), semester_window.withdraw(
        ), section_window.withdraw(), batch_window.withdraw(), branch_window.withdraw(), root.withdraw()], bg='navy', fg='white', anchor = W, width = 25).grid(row=z, column=1, sticky = E+W)
        z = z+1
        j = j+1
        i = (k+2)+j

    
    Button(semester_window, text='Exit', command=popup_1,
           bg='white', fg='midnightblue', padx=10).grid(row=6, column=4)


def show_image():
    global show_image_window
    show_image_window = Toplevel()
    show_image_window.title(path_12)
    show_image_window.iconbitmap(
        'C:/Users/0526p/Pictures/implementation/LLFRAS.ico')

    os.chdir(path_12)

    def show_forward():
        Button(section_window, text='>>', command=lambda: [show_image_window.deiconify(
        ), section_window.withdraw()], padx=10).grid(row=0, column=3)
        Button(frame_5, text='>>', command=lambda: [section_window.deiconify(
        ), batch_window.withdraw()], padx=10).grid(row=0, column=3)
        Button(frame_1, text='>>', command=lambda: [batch_window.deiconify(
        ), branch_window.withdraw()], padx=10).grid(row=0, column=3)
        Button(root, text='>>', command=lambda: [
               branch_window.deiconify(), root.withdraw()], padx=10).grid(row=0, column=1)

    Button(show_image_window, text='<<', command=lambda: [show_image_window.withdraw(
    ), section_window.deiconify(), show_forward()], padx=10).grid(row=0, column=0)
    Button(show_image_window, text='Start', command=lambda: [show_image_window.withdraw(), section_window.withdraw(
    ), batch_window.withdraw(), root.deiconify(), show_forward()], padx=20).grid(row=0, column=1)
    Button(show_image_window, text='Home', command=lambda: [show_image_window.withdraw(), section_window.withdraw(
    ), batch_window.withdraw(), branch_window.deiconify(), show_forward()], padx=20).grid(row=0, column=2)
    Label(show_image_window, text='       ').grid(row=1)

    image_list = os.listdir(path_12)
    i = 1
    for image in image_list:
        Label(show_image_window, text=image).grid(row=i+1, column=3)
        i = i+1

    Label(show_image_window, text='  ').grid(row=i+1, column=4)
    Button(show_image_window, text='Exit', command=popup_1,
           padx=10).grid(row=i+1, column=5)


def open_section(sectionName):
    global input_3, image_directory_section
    input_3 = str(sectionName).capitalize()
    image_directory_section = image_directory_batch + '/' + input_3
    if path_11 == None:
        global path_5
        path_5 = path_4 + '/' + input_3
        semester_directories()

    elif path_4 == None:
        global path_12
        path_12 = path_11 + '/' + input_3
        show_image()


def new_section(i, j):

    def show_forward():
        Button(frame_5, text='>>', command=lambda: [section_directories(
        ), batch_window.withdraw()], bg='white', fg='midnightblue', padx=10).grid(row=0, column=3)
        Button(frame_1, text='>>', command=lambda: [batch_window.deiconify(
        ), branch_window.withdraw()], bg='white', fg='midnightblue', padx=10).grid(row=0, column=3)
        Button(root, text='>>', command=lambda: [branch_window.deiconify(
        ), root.withdraw()], bg='white', fg='midnightblue', padx=10).grid(row=0, column=1)

    Button(frame_9, text='<<', command=lambda: [section_window.destroy(), section_directories(), batch_window.withdraw(
    ), branch_window.withdraw(), root.withdraw()], bg='white', fg='midnightblue', padx=10).grid(row=0, column=0)
    Button(frame_9, text='Start', command=lambda: [section_window.destroy(), batch_window.withdraw(
    ), branch_withdraw(), show_forward(), root.deiconify()], bg='white', fg='midnightblue', padx=20).grid(row=0, column=1)
    Button(frame_9, text='Home', command=lambda: [section_window.destroy(), batch_window.withdraw(
    ), branch_window.deiconify(), show_forward()], bg='white', fg='midnightblue', padx=20).grid(row=0, column=2)
    Button(section_window, text='New', state=DISABLED, bg='white',
           fg='midnightblue', padx=15).grid(row=0, column=3)
    Button(section_window, text='Remove', command=lambda: [section_window.destroy(), batch_window.withdraw(
    ), branch_window.withdraw(), root.withdraw(), remove_section(i, j)], bg='white', fg='midnightblue').grid(row=0, column=4)

    Label(frame_10, text=str(j)+' '*15, bg='lightgoldenrodyellow',
          fg='black').grid(row=i+j, column=0)

    e = Entry(frame_10, width=25,
              fg='blue', bg='white', borderwidth=10)
    e.grid(row=i+j, column=1)
    e.insert(0, 'Enter Section Name')

    err = ['Enter', 'Section', 'Name', 'Enter section', 'Enter name', 'Section name',
           'Section enter', 'Name section', 'Name enter', 'Enter section name']

    def save(i, j, err):
        if path_11 == None:
            try:
                if e.get().capitalize() in err:
                    Label(frame_10, text='Enter Section Name', bg='lightgoldenrodyellow', fg='red').grid(
                        row=i+j+1, column=1)
                    new_branch(i, j)
                else:
                    os.mkdir(path_4+'/' + e.get().capitalize())
                    section_window.destroy()
                    section_directories()
            except FileExistsError:
                if e.get() == '':
                    Label(frame_10, text='Enter Section Name', bg='lightgoldenrodyellow', fg='red').grid(
                        row=i+j+1, column=1)
                elif e.get().capitalize() in os.listdir(path_4):
                    Label(frame_10, text='File Already Exists', bg='lightgoldenrodyellow', fg='red', padx=10).grid(
                        row=i+j+1, column=1)
                new_section(i, j)

        elif path_4 == None:
            if e.get() == '':
                Label(new_section_window, text='Enter Section Name', fg='red').grid(
                    row=1, column=1)
                os.mkdir(path_11+'/' + e.get())
            try:
                os.mkdir(path_11+'/' + e.get().capitalize())
                new_section_window.destroy()
                section_window.destroy()
                section_directories()
            except FileExistsError:
                new_section_window.destroy()
                new_section()
                Label(new_section_window, text='File Already Exists', fg='red', padx=10).grid(
                    row=1, column=1)

    Button(section_window, text='Save', command=lambda: [save(
        i, j, err)], bg='white', fg='midnightblue', padx=15).grid(row=5, column=2)
    Button(section_window, text='Cancle', command=lambda: [section_window.destroy(), section_directories(), batch_window.withdraw(
    ), branch_window.withdraw(), root.withdraw()], bg='white', fg='midnightblue', padx=10).grid(row=5, column=3)
    Button(section_window, text='Exit', command=popup_1,
           bg='white', fg='midnightblue', padx=10).grid(row=5, column=4)


def remove_section(i, j):

    global remove_section_window, frame_12
    remove_section_window = Toplevel()
    # remove_section_window.geometry('400x175')
    remove_section_window.title(path_4)
    remove_section_window.iconbitmap(
        'C:/Users/0526p/Pictures/implementation/LLFRAS.ico')
    remove_section_window.config(bg='lightgoldenrodyellow')

    frame_11 = LabelFrame(remove_section_window,
                  bg='lightgoldenrodyellow')
    frame_11.grid(row = 0, column = 0)
    
    def show_forward():
        Button(frame_5, text='>>', command=lambda: [section_directories(
        ), batch_window.withdraw()], bg='white', fg='midnightblue', padx=10).grid(row=0, column=3)
        Button(frame_1, text='>>', command=lambda: [batch_window.deiconify(
        ), branch_window.withdraw()], bg='white', fg='midnightblue', padx=10).grid(row=0, column=3)
        Button(root, text='>>', command=lambda: [branch_window.deiconify(
        ), root.withdraw()], bg='white', fg='midnightblue', padx=10).grid(row=0, column=1)

    Button(frame_11, text='<<', command=lambda: [deselect_button(length), remove_section_window.destroy(), section_window.destroy(
    ), section_directories(), batch_window.withdraw(), branch_window.withdraw(), root.withdraw()], bg='white', fg='midnightblue', padx=10).grid(row=0, column=0)
    Button(frame_11, text='Start', command=lambda: [deselect_button(length), remove_section_window.destroy(), section_window.destroy(
    ), show_forward(), batch_window.withdraw(), branch_window.withdraw(), root.deiconify()], bg='white', fg='midnightblue', padx=20).grid(row=0, column=1)
    Button(frame_11, text='Home', command=lambda: [remove_section_window.destroy(), section_window.destroy(
    ), batch_window.withdraw(), branch_window.deiconify(), show_forward()], bg='white', fg='midnightblue', padx=20).grid(row=0, column=2)
    Button(frame_11, text='>>', state=DISABLED,
           bg='white', fg='midnightblue', padx=10).grid(row=0, column=3)
    
    Label(remove_section_window, text = ' '*30,
          bg='lightgoldenrodyellow').grid(row = 0, column = 1)
    
    Button(remove_section_window, text='New', command=lambda: [remove_section_window.destroy(), section_window.destroy(), section_directories(), new_section(
        i, j), batch_window.withdraw(), branch_window.withdraw(), root.withdraw()], bg='white', fg='midnightblue', padx=15).grid(row=0, column=3)
    Button(remove_section_window, text='Remove', state=DISABLED,
           bg='white', fg='midnightblue').grid(row=0, column=4)
    Label(remove_section_window, text='                                  ',
          bg='lightgoldenrodyellow').grid(row=1)
    
    frame_12 = LabelFrame(remove_section_window, text = '                 Section Name',
                  bg='lightgoldenrodyellow', fg = 'purple')
    frame_12.grid(row = 2, column = 0)
    
    collect_check = []

    def collect(section):
        collect_check.append(section)

    def delete(collect_check):
        try:
            if path_11 == None:
                for b in collect_check:
                    path = path_4 + '/' + b.capitalize()
                    os.rmdir(path)
            elif path_4 == None:
                for b in collect_check:
                    path = path_11 + '/' + b.capitalize()
                    os.rmdir(path)
            remove_section_window.destroy()
            section_window.destroy()
            root.withdraw()
            branch_window.withdraw()
            batch_window.withdraw()
            section_directories()
        except OSError:
            remove_section_window.destroy()
            remove_section(i, j)
            Label(frame_12, text='Delete Permission Denied',
                  bg='lightgoldenrodyellow', fg='red', padx=10).grid(row=i+j+1, column=1)
            Label(frame_12, text="Sub-directories presence",
                  bg='lightgoldenrodyellow', fg='red', padx=10).grid(row=i+j+2, column=1)
            Label(frame_12, text="In selected folder",
                  bg='lightgoldenrodyellow', fg='red', padx=10).grid(row=i+j+3, column=1)

    def selection(collect_check):
        if collect_check == []:
            if os.listdir(path_3) == []:
                remove_section_window.destroy()
                remove_section(i, j)
                Label(frame_12, text="No subdirectories",
                      bg='lightgoldenrodyellow', fg='red', padx=10).grid(row=i+j+1, column=1)
            else:
                remove_section_window.destroy()
                remove_section(i, j)
                Label(frame_12, text="Select at least one folder",
                      bg='lightgoldenrodyellow', fg='red', padx=10).grid(row=i+j+1, column=1)
        else:
            delete(collect_check)

    def deselect_button(length):
        for k in range(4, length+4):
            check1 = Checkbutton(remove_section_window,
                                 text=' ', bg='lightgoldenrodyellow')
            check1.grid(row=k, column=0)
            check1.deselect()

    i = 3
    j = 1
    section_list = os.listdir(path_4)
    length = len(section_list)
    for section in section_list:
        check2 = Checkbutton(frame_12, text=' '*10, command=lambda section=section: [
                             collect(section)], bg='lightgoldenrodyellow')
        check2.grid(row=i+j, column=0)
        check2.deselect()
        Button(frame_12, text=section, command=lambda section=section: [remove_section_window.destroy(), open_section(section), section_directories(
        ), section_window.withdraw(), batch_window.withdraw(), branch_window.withdraw(), root.withdraw()], bg='navy', fg='white', width = 25, anchor = W).grid(row=i+j, column=1, sticky = W+E)
        j = j+1
        i = 3+j
    
    space = Label(remove_section_window, text=' ',
                  bg='lightgoldenrodyellow').grid(row=5)

    try:
        semester_window.destroy()
        Button(remove_section_window, text='Delete', command=lambda: [selection(
            collect_check)], bg='white', fg='midnightblue', padx=15).grid(row=6, column=2)
    except TclError:
        Button(remove_section_window, text='Delete', command=lambda: [selection(
            collect_check)], bg='white', fg='midnightblue', padx=15).grid(row=6, column=2)
    except NameError:
        Button(remove_section_window, text='Delete', command=lambda: [selection(
            collect_check)], bg='white', fg='midnightblue', padx=15).grid(row=6, column=2)
    Button(remove_section_window, text='Cancle', command=lambda: [deselect_button(length), remove_section_window.destroy(), section_window.destroy(
    ), root.withdraw(), branch_window.withdraw(), batch_window.withdraw(), section_directories()], bg='white', fg='midnightblue', padx=10).grid(row=6, column=3)
    Button(remove_section_window, text='Exit', command=popup_1,
           bg='white', fg='midnightblue', padx=10).grid(row=6, column=4)


def section_directories():

    global section_window, frame_9, frame_10
    section_window = Toplevel()
    section_window.config(bg='lightgoldenrodyellow')

    if path_11 == None:
        global section_list
        section_window.title(path_4)
        section_list = os.listdir(path_4)
    elif path_4 == None:
        section_window.title(path_11)
        os.chdir(path_11)
        section_list = os.listdir(path_11)

    section_window.iconbitmap(
        'C:/Users/0526p/Pictures/implementation/LLFRAS.ico')

    frame_9 = LabelFrame(section_window,
                  bg='lightgoldenrodyellow')
    frame_9.grid(row = 0, column = 0)
    
    def show_forward():
        Button(frame_5, text='>>', command=lambda: [section_window.deiconify(
        ), batch_window.withdraw()], bg='white', fg='midnightblue', padx=10).grid(row=0, column=3)
        Button(frame_1, text='>>', command=lambda: [batch_window.deiconify(
        ), branch_window.withdraw()], bg='white', fg='midnightblue', padx=10).grid(row=0, column=3)
        Button(root, text='>>', command=lambda: [branch_window.deiconify(
        ), root.withdraw()], bg='white', fg='midnightblue', padx=10).grid(row=0, column=1)

    Button(frame_9, text='<<', command=lambda: [section_window.withdraw(), batch_window.deiconify(
    ), show_forward()], bg='white', fg='midnightblue', padx=10).grid(row=0, column=0)
    Button(frame_9, text='Start', command=lambda: [section_window.withdraw(), batch_window.withdraw(
    ), root.deiconify(), show_forward()], bg='white', fg='midnightblue', padx=20).grid(row=0, column=1)
    Button(frame_9, text='Home', command=lambda: [section_window.withdraw(), branch_window.deiconify(
    ), show_forward()], bg='white', fg='midnightblue', padx=20).grid(row=0, column=2)
    Button(frame_9, text='>>', state=DISABLED, bg='white',
           fg='midnightblue', padx=10).grid(row=0, column=3)

    Label(section_window, text = ' '*30,
          bg='lightgoldenrodyellow').grid(row = 0, column = 1)

    Button(section_window, text='New', command=lambda: [new_section(i, j), batch_window.withdraw(
    ), branch_window.withdraw(), root.withdraw()], bg='white', fg='midnightblue', padx=15).grid(row=0, column=3)
    Button(section_window, text='Remove', command=lambda: [root.withdraw(), branch_window.withdraw(), batch_window.withdraw(
    ), section_window.withdraw(), remove_section(i, j)], bg='white', fg='midnightblue').grid(row=0, column=4)
    Label(section_window, text='                                  ',
          bg='lightgoldenrodyellow').grid(row=1)

    frame_10 = LabelFrame(section_window, text = 'Sl No       Section Name',
                  bg='lightgoldenrodyellow', fg = 'purple')
    frame_10.grid(row = 2, column = 0)
    
    i = 3
    j = 1
    k = 0
    for section in section_list:
        Label(frame_10, text=str(j)+' '*15, bg='lightgoldenrodyellow',
              fg='black').grid(row=k, column=0)
        Button(frame_10, text=section, command=lambda section=section: [open_section(section), section_window.withdraw(
        ), batch_window.withdraw(), branch_window.withdraw(), root.withdraw()], bg='navy', fg='white', width = 25, anchor = W).grid(row=k, column=1, sticky = W+E)
        j = j+1
        k = k+1

    Label(section_window, text=' ',
          bg='lightgoldenrodyellow').grid(row=3)

    Button(section_window, text='Exit', command=popup_1,
           bg='white', fg='midnightblue', padx=10).grid(row=5, column=4)


def open_batch(batchName):
    global image_directory_batch
    input_2 = str(batchName).capitalize()
    image_directory_batch = image_directory_branch + '/' + input_2
    if path_10 == None:
        global path_4, path_11
        path_11 = None
        path_4 = path_3 + '/' + input_2
        section_directories()

    elif path_3 == None:
        path_4 = None
        path_11 = path_10 + '/' + input_2
        section_directories()


def new_batch(i, j):

    def show_forward():
        Button(frame_1, text='>>', command=lambda: [batch_directories(
        ), branch_window.withdraw()], bg='white', fg='midnightblue', padx=10).grid(row=0, column=3)
        Button(root, text='>>', command=lambda: [branch_window.deiconify(
        ), root.withdraw()], bg='white', fg='midnightblue', padx=10).grid(row=0, column=1)

    Button(frame_5, text='<<', command=lambda: [batch_window.destroy(), batch_directories(
    ), branch_window.withdraw(), root.withdraw()], bg='white', fg='midnightblue', padx=10).grid(row=0, column=0)
    Button(frame_5, text='Start', command=lambda: [batch_window.destroy(), branch_window.withdraw(
    ), show_forward(), root.deiconify()], bg='white', fg='midnightblue', padx=20).grid(row=0, column=1)
    Button(frame_5, text='Home', command=lambda: [batch_window.destroy(), branch_window.deiconify(
    ), show_forward()], bg='white', fg='midnightblue', padx=20).grid(row=0, column=2)
    Button(batch_window, text='New', state=DISABLED, bg='white',
           fg='midnightblue', padx=15).grid(row=0, column=3)
    Button(batch_window, text='Remove', command=lambda: [batch_window.destroy(), branch_window.withdraw(
    ), root.withdraw(), remove_batch(i, j)], bg='white', fg='midnightblue').grid(row=0, column=4)

    Label(frame_6, text=str(j) + ' '*15, bg='lightgoldenrodyellow',
          fg='black').grid(row=i+j, column=0)
    Label(frame_6, text='Select Batch', bg='lightgoldenrodyellow', fg='purple').grid(
        row=i+j, column=1)

    style= ttk.Style()
    style.theme_use('clam')
    style.configure("TCombobox", foreground = 'blue', fieldbackground= "white", background= 'white')

    number_choosen = ttk.Combobox(frame_6, width=20)
    number_choosen['values'] = (2021, 2022, 2023, 2024, 2025, 2026, 2027,  2028, 2029, 2030, 2031, 2032,
                                2033, 2034, 2035, 2036, 2037, 2038, 2039, 2040, 2041, 2042, 2043, 2044, 2045, 2046, 2047, 2048, 2050)
    number_choosen.grid(row=i+j+1, column=1)
    number_choosen.current(0)

    def save(i, j):
        if path_10 == None:
            try:
                os.mkdir(path_3+'/' + number_choosen.get())
                batch_window.destroy()
                batch_directories()
            except FileExistsError:
                if number_choosen.get() == '':
                    Label(frame_6, text="You Didn't Select Batch", bg='lightgoldenrodyellow', fg='red').grid(
                        row=i+j+2, column=1)
                elif number_choosen.get() in os.listdir(path_3):
                    Label(frame_6, text='File Already Exists', bg='lightgoldenrodyellow', fg='red', padx=10).grid(
                        row=i+j+2, column=1)
                    new_batch(i, j)

        elif path_3 == None:
            if e.get() == '':
                Label(new_batch_window, text='Enter Batch Name', bg='lightgoldenrodyellow', fg='red', padx=10).grid(
                    row=i+j, column=1)
                j = j+1
                os.mkdir(path_10+'/' + e.get())
            try:
                os.mkdir(path_10+'/' + e.get().capitalize())
                batch_window.destroy()
                batch_directories()
            except FileExistsError:
                Label(branch_window, text='File Already Exists', bg='lightgoldenrodyellow', fg='red', padx=10).grid(
                    row=i+j, column=1)
                j = j+1
                os.mkdir(path_9 + '/' + e.get())

    Button(batch_window, text='Save', command=lambda: [
           save(i, j)], bg='white', fg='midnightblue', padx=15).grid(row=5, column=2)
    Button(batch_window, text='Cancle', command=lambda: [batch_window.destroy(), batch_directories(
    ), branch_window.withdraw(), root.withdraw()], bg='white', fg='midnightblue', padx=10).grid(row=5, column=3)
    Button(batch_window, text='Exit', command=popup_1, bg='white',
           fg='midnightblue', padx=10).grid(row=5, column=4)


def remove_batch(i, j):

    global remove_batch_window, frame_8
    remove_batch_window = Toplevel()
    remove_batch_window.iconbitmap(
        'C:/Users/0526p/Pictures/implementation/LLFRAS.ico')
    remove_batch_window.config(bg='lightgoldenrodyellow')
    remove_batch_window.title(path_3)

    frame_7 = LabelFrame(remove_batch_window,
                  bg='lightgoldenrodyellow')
    frame_7.grid(row = 0, column = 0)
    
    def show_forward():
        Button(frame_1, text='>>', command=lambda: [batch_directories(
        ), branch_window.withdraw()], bg='white', fg='midnightblue', padx=10).grid(row=0, column=3)
        Button(root, text='>>', command=lambda: [branch_window.deiconify(
        ), root.withdraw()], bg='white', fg='midnightblue', padx=10).grid(row=0, column=1)

    Button(frame_7, text='<<', command=lambda: [deselect_button(length), remove_batch_window.destroy(), batch_window.destroy(
    ), batch_directories(), branch_window.withdraw(), root.withdraw()], bg='white', fg='midnightblue', padx=10).grid(row=0, column=0)
    Button(frame_7, text='Start', command=lambda: [deselect_button(length), remove_batch_window.destroy(), batch_window.destroy(
    ), show_forward(), branch_window.withdraw(), root.deiconify()], bg='white', fg='midnightblue', padx=20).grid(row=0, column=1)
    Button(frame_7, text='Home', command=lambda: [remove_batch_window.destroy(), batch_window.destroy(
    ), branch_window.deiconify(), show_forward()], bg='white', fg='midnightblue', padx=20).grid(row=0, column=2)
    Button(frame_7, text='>>', state=DISABLED, bg='white',
           fg='midnightblue', padx=10).grid(row=0, column=3)
    
    Label(remove_batch_window, text = ' '*30,
          bg='lightgoldenrodyellow').grid(row = 0, column = 1)
    
    Button(remove_batch_window, text='New', command=lambda: [remove_batch_window.destroy(), batch_window.destroy(), batch_directories(
    ), new_batch(i, j), branch_window.withdraw(), root.withdraw()], bg='white', fg='midnightblue', padx=15).grid(row=0, column=3)
    Button(remove_batch_window, text='Remove', state=DISABLED,
           bg='white', fg='midnightblue').grid(row=0, column=4)
    Label(remove_batch_window, text='                                          ',
          bg='lightgoldenrodyellow').grid(row=1)


    frame_8 = LabelFrame(remove_batch_window, text = '                 Batch Name',
                  bg='lightgoldenrodyellow', fg = 'purple')
    frame_8.grid(row = 2, column = 0)
    
    collect_check = []

    def collect(batch):
        collect_check.append(batch)

    def delete(collect_check):
        try:
            if path_10 == None:
                for b in collect_check:
                    path = path_3 + '/' + b.capitalize()
                    os.rmdir(path)
            elif path_3 == None:
                for b in collect_check:
                    path = path_10 + '/' + b.capitalize()
                    os.removedirs(path)

            remove_batch_window.destroy()
            batch_window.destroy()
            root.withdraw()
            branch_window.withdraw()
            batch_directories()
        except OSError:
            remove_batch_window.destroy()
            remove_batch(i, j)
            Label(frame_8, text='Delete Permission Denied',
                  bg='lightgoldenrodyellow', fg='red', padx=10).grid(row=i+j+1, column=1)
            Label(frame_8, text="Sub-directories presence",
                  bg='lightgoldenrodyellow', fg='red', padx=10).grid(row=i+j+2, column=1)
            Label(frame_8, text="In selected folder",
                  bg='lightgoldenrodyellow', fg='red', padx=10).grid(row=i+j+3, column=1)

    def selection(collect_check):
        if collect_check == []:
            if os.listdir(path_3) == []:
                remove_batch_window.destroy()
                remove_batch(i, j)
                Label(frame_8, text="No subdirectories",
                      bg='lightgoldenrodyellow', fg='red', padx=10).grid(row=i+j+1, column=1)
            else:
                remove_batch_window.destroy()
                remove_batch(i, j)
                Label(frame_8, text="Select at least one folder",
                      bg='lightgoldenrodyellow', fg='red', padx=10).grid(row=i+j+1, column=1)
        else:
            delete(collect_check)

    def deselect_button(length):
        for k in range(4, length+4):
            check1 = Checkbutton(remove_batch_window,
                                 text=' ', bg='lightgoldenrodyellow')
            check1.grid(row=k, column=0)
            check1.deselect()
    i = 3
    j = 1
    batch_list = os.listdir(path_3)
    length = len(batch_list)
    for batch in batch_list:
        check2 = Checkbutton(frame_8, text=' '*10, command=lambda batch=batch: [
                             collect(batch)], bg='lightgoldenrodyellow')
        check2.grid(row=i+j, column=0)
        check2.deselect()
        Button(frame_8, text=batch, command=lambda batch=batch: [remove_batch_window.destroy(), open_batch(batch), batch_directories(
        ), batch_window.withdraw(), branch_window.withdraw(), root.withdraw()], bg='navy', fg='white', width = 25, anchor = W).grid(row=i+j, column=1, sticky = W+E)
        j = j + 1
        i = 3 + j

    space = Label(remove_batch_window, text=' ',
                  bg='lightgoldenrodyellow').grid(row=5)

    try:
        section_window.destroy()
        Button(remove_batch_window, text='Delete', command=lambda: [selection(
            collect_check)], bg='white', fg='midnightblue', padx=15).grid(row=6, column=2)
    except TclError:
        Button(remove_batch_window, text='Delete', command=lambda: [selection(
            collect_check)], bg='white', fg='midnightblue', padx=15).grid(row=6, column=2)
    except NameError:
        Button(remove_batch_window, text='Delete', command=lambda: [selection(
            collect_check)], bg='white', fg='midnightblue', padx=15).grid(row=6, column=2)
    Button(remove_batch_window, text='Cancle', command=lambda: [deselect_button(length), remove_batch_window.destroy(), batch_window.destroy(
    ), root.withdraw(), branch_window.withdraw(), batch_directories()], bg='white', fg='midnightblue', padx=10).grid(row=6, column=3)
    Button(remove_batch_window, text='Exit', command=popup_1,
           bg='white', fg='midnightblue', padx=10).grid(row=6, column=4)


def batch_directories():
    global batch_window, frame_5, frame_6
    batch_window = Toplevel()
    batch_window.config(bg='lightgoldenrodyellow')

    if path_10 == None:
        global batch_list
        batch_window.title(path_3)
        # os.chdir(path_3)
        batch_list = os.listdir(path_3)
    elif path_3 == None:
        batch_window.title(path_10)
        os.chdir(path_10)
        batch_list = os.listdir(path_10)

    batch_window.iconbitmap(
        'C:/Users/0526p/Pictures/implementation/LLFRAS.ico')

    frame_5 = LabelFrame(batch_window,
                  bg='lightgoldenrodyellow')
    frame_5.grid(row = 0, column = 0)
    
    def show_forward():
        Button(frame_1, text='>>', command=lambda: [batch_window.deiconify(
        ), branch_window.withdraw()], bg='white', fg='midnightblue', padx=10).grid(row=0, column=3)
        Button(root, text='>>', command=lambda: [branch_window.deiconify(
        ), root.withdraw()], bg='white', fg='midnightblue', padx=10).grid(row=0, column=1)

    Button(frame_5, text='<<', command=lambda: [batch_window.withdraw(), branch_window.deiconify(
    ), show_forward()], bg='white', fg='midnightblue', padx=10).grid(row=0, column=0)
    Button(frame_5, text='Start', command=lambda: [batch_window.withdraw(), root.deiconify(
    ), show_forward()], bg='white', fg='midnightblue', padx=20).grid(row=0, column=1)
    Button(frame_5, text='Home', command=lambda: [batch_window.withdraw(), branch_window.deiconify(
    ), show_forward()], bg='white', fg='midnightblue', padx=20).grid(row=0, column=2)
    Button(frame_5, text='>>', state=DISABLED, bg='white',
           fg='midnightblue', padx=10).grid(row=0, column=3)

    Label(batch_window, text = ' '*30,
          bg='lightgoldenrodyellow').grid(row = 0, column = 1)


    Button(batch_window, text='New', command=lambda: [new_batch(i, j), branch_window.withdraw(
    ), root.withdraw()], bg='white', fg='midnightblue', padx =15).grid(row=0, column=3)
    Button(batch_window, text='Remove', command=lambda: [root.withdraw(), branch_window.withdraw(
    ), batch_window.withdraw(), remove_batch(i, j)], bg='white', fg='midnightblue').grid(row=0, column=4)
    Label(batch_window, text='                                     ',
          bg='lightgoldenrodyellow').grid(row=1)

    frame_6 = LabelFrame(batch_window, text = 'Sl No        Batch Name',
                  bg='lightgoldenrodyellow', fg = 'purple')
    frame_6.grid(row = 2, column = 0)
    
    i = 3
    j = 1
    k = 0
    for batch in batch_list:
        Label(frame_6, text=str(j)+' '*15, bg='lightgoldenrodyellow',
              fg='black').grid(row=k, column=0)
        Button(frame_6, text=batch, command=lambda batch=batch: [open_batch(batch), batch_window.withdraw(
        ), branch_window.withdraw(), root.withdraw()], bg='navy', fg='white', width = 25, anchor = W).grid(row=k, column=1, sticky = W+E)
        j = j+1
        k = k+1

    Label(batch_window, text=' ', bg='lightgoldenrodyellow').grid(row=3)
    
    Button(batch_window, text='Exit', command=popup_1, bg='white',
           fg='midnightblue', padx=10).grid(row=5, column=4)


def open_branch(branchName):
    global image_directory_branch
    input_1 = str(branchName).capitalize()
    image_directory_branch = input_1
    if path_9 == None:
        global path_3, path_10
        path_10 = None
        path_3 = path_2 + '/' + input_1
        batch_directories()

    elif path_2 == None:
        path_3 = None
        path_10 = path_9 + '/' + input_1
        batch_directories()


def new_branch(i, j):

    def show_forward():
        Button(root, text='>>', command=lambda: [branch_directories(), root.withdraw(
        )], bg='white', fg='midnightblue', padx=10).grid(row=0, column=1)

    Button(frame_1, text='<<', command=lambda: [branch_window.destroy(), branch_directories(
    ), root.withdraw()], bg='white', fg='midnightblue', padx=10).grid(row=0, column=0)
    Button(frame_1, text='Start', command=lambda: [branch_window.destroy(), show_forward(
    ), root.deiconify()], bg='white', fg='midnightblue', padx=20).grid(row=0, column=1)
    Button(branch_window, text='New', state=DISABLED, bg='white',
           fg='midnightblue', padx=15).grid(row=0, column=3)
    Button(branch_window, text='Remove', command=lambda: [branch_window.destroy(), root.withdraw(
    ), remove_branch(i, j)], bg='white', fg='midnightblue').grid(row=0, column=4)

    Label(frame_2, text=str(j)+' '*15, bg='lightgoldenrodyellow',
          fg='black').grid(row=i+j, column=0)

    e = Entry(frame_2, width=25,
              fg='blue', bg='white', borderwidth=10)
    e.grid(row=i+j, column=1)
    e.insert(0, 'Enter Branch Name')

    err = ['Enter', 'Branch', 'Name', 'Enter branch', 'Enter name', 'Branch name',
           'Branch enter', 'Name branch', 'Name enter', 'Enter branch name']

    def save(i, j, err):
        if path_9 == None:
            try:
                if e.get().capitalize() in err:
                    Label(frame_2, text='Enter Branch Name', bg='lightgoldenrodyellow', fg='red').grid(
                        row=i+j+1, column=1)
                    new_branch(i, j)
                else:
                    os.mkdir(path_2+'/' + e.get().capitalize())
                    branch_window.destroy()
                    branch_directories()
            except FileExistsError:
                if e.get() == '':
                    Label(frame_2, text='Enter Branch Name', bg='lightgoldenrodyellow', fg='red').grid(
                        row=i+j+1, column=1)
                elif e.get().capitalize() in os.listdir(path_2):
                    Label(frame_2, text='File Already Exists', bg='lightgoldenrodyellow', fg='red', padx=10).grid(
                        row=i+j+1, column=1)
                new_branch(i, j)

        elif path_2 == None:
            if e.get() == '':
                Label(frame_2, text='Enter Branch Name', bg='lightgoldenrodyellow', fg='red').grid(
                    row=i+j, column=1)
                j = j+1
                os.mkdir(path_9 + '/' + e.get())
            try:
                os.mkdir(path_9 + '/' + e.get().capitalize())
                branch_window.destroy()
                branch_directories()
            except FileExistsError:
                Label(frame_2, text='File Already Exists', bg='lightgoldenrodyellow', fg='red', padx=10).grid(
                    row=i+j, column=1)
                j = j+1
                os.mkdir(path_9 + '/' + e.get())

    Button(branch_window, text='Save', command=lambda: [save(
        i, j, err)], bg='white', fg='midnightblue', padx=15).grid(row=5, column=2)
    Button(branch_window, text='Cancle', command=lambda: [branch_window.destroy(), branch_directories(
    ), root.withdraw()], bg='white', fg='midnightblue', padx=10).grid(row=5, column=3)
    Button(branch_window, text='Exit', command=popup_1, bg='white',
           fg='midnightblue', padx=10).grid(row=5, column=4)


def remove_branch(i, j):
    global remove_branch_window, frame_4
    remove_branch_window = Toplevel()
    remove_branch_window.title(path_2)
    remove_branch_window.iconbitmap(
        'C:/Users/0526p/Pictures/implementation/LLFRAS.ico')
    remove_branch_window.config(bg='lightgoldenrodyellow')

    frame_3 = LabelFrame(remove_branch_window,
                  bg='lightgoldenrodyellow')
    frame_3.grid(row = 0, column = 0)
    
    def show_forward():
        Button(root, text='>>', command=lambda: [branch_directories(), root.withdraw(
        )], bg='white', fg='midnightblue', padx=10).grid(row=0, column=1)

    Button(frame_3, text='<<', command=lambda: [deselect_button(length), remove_branch_window.destroy(
    ), branch_window.destroy(), branch_directories(), root.withdraw()], bg='white', fg='midnightblue', padx=10).grid(row=0, column=0)
    Button(frame_3, text='Start', command=lambda: [deselect_button(length), remove_branch_window.destroy(
    ), branch_window.destroy(), show_forward(), root.deiconify()], bg='white', fg='midnightblue', padx=20).grid(row=0, column=1)
    Button(frame_3, text='Home', state=DISABLED,
           bg='white', fg='midnightblue', padx=20).grid(row=0, column=2)
    Button(frame_3, text='>>', state=DISABLED, bg='white',
           fg='midnightblue', padx=10).grid(row=0, column=3)

    Label(remove_branch_window, text = ' '*30,
          bg='lightgoldenrodyellow').grid(row = 0, column = 1)

    Button(remove_branch_window, text='New', command=lambda: [remove_branch_window.destroy(), branch_window.destroy(
    ), branch_directories(), new_branch(i, j), root.withdraw()], bg='white', fg='midnightblue', padx=15).grid(row=0, column=3)
    Button(remove_branch_window, text='Remove', state=DISABLED,
           bg='white', fg='midnightblue').grid(row=0, column=4)
    Label(remove_branch_window, text='                                          ',
          bg='lightgoldenrodyellow').grid(row=1)

    
    collect_check = []

    def collect(branch):
        collect_check.append(branch)

    def delete(collect_check):
        try:
            if path_9 == None:
                for b in collect_check:
                    path = path_2 + '/' + b.capitalize()
                    os.removedirs(path)

            elif path_2 == None:
                for b in collect_check:
                    path = path_9 + '/' + b.capitalize()
                    os.removedirs(path)
            remove_branch_window.destroy()
            branch_window.destroy()
            root.withdraw()
            branch_directories()

        except OSError:
            remove_branch_window.destroy()
            remove_branch(i, j)
            Label(frame_4, text='Delete Permission Denied',
                  bg='lightgoldenrodyellow', fg='red', padx=10).grid(row=i+j+1, column=1)
            Label(frame_4, text="Sub-Directories Presence",
                  bg='lightgoldenrodyellow', fg='red', padx=10).grid(row=i+j+2, column=1)
            Label(frame_4, text="In Selected Folder",
                  bg='lightgoldenrodyellow', fg='red', padx=10).grid(row=i+j+3, column=1)

    def selection(collect_check):
        if collect_check == []:
            remove_branch_window.destroy()
            remove_branch(i, j)
            Label(frame_4, text="Select at least one folder",
                  bg='lightgoldenrodyellow', fg='red', padx=10).grid(row=i+j+1, column=1)
        else:
            delete(collect_check)

    def deselect_button(length):
        for k in range(4, length+4):
            check1 = Checkbutton(remove_branch_window,
                                 text=' ', bg='lightgoldenrodyellow')
            check1.grid(row=k, column=0)
            check1.deselect()
   
    frame_4 = LabelFrame(remove_branch_window, text = '                  Branch Name',
                  bg='lightgoldenrodyellow', fg = 'purple')
    frame_4.grid(row = 2, column = 0)
    
    i = 3
    j = 1
    branch_list = os.listdir(path_2)
    length = len(branch_list)
    for branch in branch_list:
        check2 = Checkbutton(frame_4, text=' '*10, command=lambda branch=branch: [
                             collect(branch)], bg='lightgoldenrodyellow')
        check2.grid(row=i+j, column=0)
        check2.deselect()
        Button(frame_4, text=branch, command=lambda branch=branch: [remove_branch_window.destroy(), open_branch(
            branch), branch_directories(), branch_window.withdraw(), root.withdraw()], bg='navy', fg='white', anchor = W, width = 25).grid(row=i+j, column=1, sticky = W+E)
        j = j + 1
        i = 3 + j

    space = Label(remove_branch_window, text=' ',
                  bg='lightgoldenrodyellow').grid(row=5)

    try:
        batch_window.destroy()
        Button(remove_branch_window, text='Delete', command=lambda: [selection(
            collect_check)], bg='white', fg='midnightblue', padx=15).grid(row=6, column=2)
    except TclError:
        Button(remove_branch_window, text='Delete', command=lambda: [selection(
            collect_check)], bg='white', fg='midnightblue', padx=15).grid(row=6, column=2)
    except NameError:
        Button(remove_branch_window, text='Delete', command=lambda: [selection(
            collect_check)], bg='white', fg='midnightblue', padx=15).grid(row=6, column=2)
    Button(remove_branch_window, text='Cancle', command=lambda: [deselect_button(length), remove_branch_window.destroy(
    ), branch_window.destroy(), root.withdraw(), branch_directories()], bg='white', fg='midnightblue', padx=10).grid(row=6, column=3)
    Button(remove_branch_window, text='Exit', command=popup_1,
           bg='white', fg='midnightblue', padx=10).grid(row=6, column=4)


def branch_directories():
    global branch_window, frame_1, frame_2
    branch_window = Toplevel()
    branch_window.config(bg='lightgoldenrodyellow')

    branch = ['Computer science', 'Electrical',
              'Mechanical', 'Civil', 'Agriculture']
    if path_8 == None:
        global branch_list, path_9
        path_9 = None
        os.chdir(path_1)
        if 'branch' not in os.listdir(path_1):
            global path_2
            path_2 = path_1 + '/' + 'branch'
            os.mkdir(path_2)
            os.chdir(path_2)
            for b in branch:
                os.mkdir(path_2 + '/' + b)
        elif 'branch' in os.listdir(path_1):
            path_2 = path_1 + '/' + 'branch'
            os.chdir(path_2)
            branch_window.title(path_2)
        branch_list = os.listdir(path_2)

    elif path_1 == None:
        path_2 = None
        os.chdir(path_8)
        path_9 = path_8 + '/' + 'branch'
        os.chdir(path_9)
        branch_window.title(path_9)
        branch_list = os.listdir(path_9)
    branch_window.iconbitmap(
        'C:/Users/0526p/Pictures/implementation/LLFRAS.ico')

    frame_1 = LabelFrame(branch_window,
                  bg='lightgoldenrodyellow')
    frame_1.grid(row = 0, column = 0)
    
    def show_forward():
        Button(root, text='>>', command=lambda: [branch_window.deiconify(
        ), root.withdraw()], bg='white', fg='midnightblue', padx=10).grid(row=0, column=1)

    Button(frame_1, text='<<', command=lambda: [branch_window.withdraw(), root.deiconify(
    ), show_forward()], bg='white', fg='midnightblue', padx=10).grid(row=0, column=0)
    Button(frame_1, text='Start', command=lambda: [branch_window.withdraw(), root.deiconify(
    ), show_forward()], bg='white', fg='midnightblue', padx=20).grid(row=0, column=1)
    Button(frame_1, text='Home', state=DISABLED, bg='white',
           fg='midnightblue', padx=20).grid(row=0, column=2)
    Button(frame_1, text='>>', state=DISABLED, bg='white',
           fg='midnightblue', padx=10).grid(row=0, column=3)

    Label(branch_window, text = ' '*30,
          bg='lightgoldenrodyellow').grid(row = 0, column = 1)

    new = Button(branch_window, text='New', command=lambda: [new_branch(
        i, j), root.withdraw()], bg='white', fg='midnightblue', padx=15).grid(row=0, column=3)
    remove = Button(branch_window, text='Remove', command=lambda: [root.withdraw(
    ), branch_window.withdraw(), remove_branch(i, j)], bg='white', fg='midnightblue').grid(row=0, column=4)

    Label(branch_window, text='                                          ',
          bg='lightgoldenrodyellow').grid(row=1)

    
    frame_2 = LabelFrame(branch_window, text = 'Sl No       Branch Name',
                  bg='lightgoldenrodyellow', fg = 'purple')
    frame_2.grid(row = 2, column = 0)

    i = 3
    j = 1
    k = 0
    branch_list = os.listdir(path_2)
    for branch in branch_list:
        Label(frame_2, text=str(j)+' '*15, bg='lightgoldenrodyellow',
              fg='black').grid(row=k, column=0)
        Button(frame_2, text=branch, command=lambda branch=branch: [open_branch(
            branch), branch_window.withdraw(), root.withdraw()], bg='navy', fg='white', anchor=W, width = 25).grid(row=k, column=1, sticky = W+E)
        j = j + 1
        k = k + 1

    space = Label(branch_window, text=' ',
                  bg='lightgoldenrodyellow').grid(row=3)
    
    button_exit = Button(branch_window, text='Exit', command=popup_1,
                    bg='white', fg='midnightblue', padx=10).grid(row=5, column=4)


def get_my_attendance():
    global get_my_attendance_window
    get_my_attendance_window = Toplevel()
    get_my_attendance_window.title(path_17)
    get_my_attendance_window.iconbitmap(
        'C:/Users/0526p/Pictures/implementation/LLFRAS.ico')
    get_my_attendance_window.config(bg='lightgoldenrodyellow')

    frame_24 = LabelFrame(get_my_attendance_window,
                  bg='lightgoldenrodyellow')
    frame_24.grid(row = 0, column = 0)
    
    def show_forward():
        Button(frame_22, text='>>', command=lambda: [get_my_attendance_window.deiconify(
        ), fill_student_data_window.withdraw()], bg='white',
       fg='midnightblue', padx=15).grid(row=0, column=3)
        Button(root, text='>>', command=lambda: [fill_student_data_window.deiconify(
        ), root.withdraw()], bg='white',
       fg='midnightblue', padx=10).grid(row=0, column=1)

    Button(frame_24, text='<<', command=lambda: [get_my_attendance_window.withdraw(
    ), fill_student_data_window.deiconify(), show_forward()], bg='white',
       fg='midnightblue', padx=10).grid(row=0, column=0)
    Button(frame_24, text='Start', command=lambda: [
           get_my_attendance_window.withdraw(), root.deiconify(), show_forward()], bg='white',
       fg='midnightblue', padx=20).grid(row=0, column=1)
    Button(frame_24, text='Home', command=lambda: [get_my_attendance_window.withdraw(
    ), fill_student_data_window.deiconify(), show_forward()], bg='white',
       fg='midnightblue', padx=20).grid(row=0, column=2)
    Button(frame_24, text='>>',
           state=DISABLED, bg='white',
       fg='midnightblue', padx=10).grid(row=0, column=3)
    Label(get_my_attendance_window, text='',
                      bg='lightgoldenrodyellow').grid(row=1)

    Label(get_my_attendance_window, text='Name'+' '*30+'Roll No',
                      bg='lightgoldenrodyellow', fg='purple', anchor = W).grid(row=2, column=0, sticky = W+E)

    with open(path_17, 'r') as f:
        datelist = csv.reader(f)
        x = 0
        for data in datelist:
            if x == 0:
                global list_of_date
                list_of_date = data[2:]

            if stu_roll.get() in data:
                global student_list
                student_list = data


                Label(get_my_attendance_window,
                      text=f"{data[0].capitalize()}{' '*30}{data[1]}",
                      bg='lightgoldenrodyellow', fg='navy', anchor = W).grid(row=3, column=0, sticky = W+E)

            x = x+1
        
        Label(get_my_attendance_window, text='',
                  bg='lightgoldenrodyellow').grid(row=4)
        
        frame_25 = LabelFrame(get_my_attendance_window, text = 'Sl'+' '*10+'Date Status'+' '*27+'Time Status',
                      bg='lightgoldenrodyellow', fg = 'purple')
        frame_25.grid(row = 5, column = 0)
        
        h = Scrollbar(frame_25, orient = 'horizontal')
        h.pack(side = BOTTOM, fill = X)
        v = Scrollbar(frame_25)
        v.pack(side = RIGHT, fill = Y)
        
        t1 = Text(frame_25, width = 28, height = 10, wrap = NONE, xscrollcommand = h.set, yscrollcommand = v.set, fg = 'green')
        
        my_time_list = student_list[2:]
        total_days = len(my_time_list)

        k = 1
        my_total_present = 0
        for i, d in zip(my_time_list, list_of_date):
            if i != '0':
                t1.insert(END,  str(k)+' '*4+str(d)+' '*8+str(i))
                t1.insert(END, '\n')
                my_total_present = my_total_present + 1
                k = k+1

        t1.pack(side = TOP, fill = X)
        h.config(command = t1.xview)
        v.config(command = t1.yview)

        percentage = (my_total_present*100)/total_days

        Label(get_my_attendance_window, text='',
                  bg='lightgoldenrodyellow').grid(row=6)
        
        Label(get_my_attendance_window,
              text=f'Your Presence           :     {my_total_present} day out of {total_days} days',
                      bg='lightgoldenrodyellow', fg='navy', anchor = W).grid(row=7, column=0, sticky = W+E)
        
        Label(get_my_attendance_window, text=f'Attendance Percent :     {percentage:0.2f}%',
                      bg='lightgoldenrodyellow', fg='navy', anchor = W).grid(
            row=8, column=0, sticky = W+E)
        Label(get_my_attendance_window, text='',
                      bg='lightgoldenrodyellow').grid(row=9)

        Button(get_my_attendance_window, text='Exit',
               command=popup_1, bg='white',
       fg='midnightblue', padx = 15).grid(row=10, column=1)


def access_my_attendance():
    global path_17
    path_16 = f'/{stu_branch.get().capitalize()}/{stu_batch.get().capitalize()}/{stu_section.get().capitalize()}/{stu_semester.get().capitalize()}/{stu_subject.get().capitalize()}.csv'
    path_17 = path_15 + path_16

    try:
        get_my_attendance()
    except FileNotFoundError:
        get_my_attendance_window.destroy()
        fill_student_data()
        Label(frame_23,
              text='Entre Valid Data',
                  bg='lightgoldenrodyellow', fg='red', anchor = W).grid(row=6, column=1, sticky = W+E)


def fill_student_data():
    global fill_student_data_window, frame_22, frame_23
    fill_student_data_window = Toplevel()
    fill_student_data_window.title(
        'Live Logging Face Recognition Attendance System')
    fill_student_data_window.iconbitmap(
        'C:/Users/0526p/Pictures/implementation/LLFRAS.ico')
    fill_student_data_window.config(bg='lightgoldenrodyellow')
    
    frame_22 = LabelFrame(fill_student_data_window,
                  bg='lightgoldenrodyellow')
    frame_22.grid(row = 0, column = 0)
    
    def show_forward():
        Button(root, text='>>', command=lambda: [fill_student_data_window.deiconify(
        ), root.withdraw()], bg='white',
       fg='midnightblue', padx=10).grid(row=0, column=1)

    Button(frame_22, text='<<', command=lambda: [fill_student_data_window.withdraw(
    ), root.deiconify(), show_forward()], bg='white',
       fg='midnightblue', padx=15).grid(row=0, column=0)
    Button(frame_22, text='Start', command=lambda: [
           fill_student_data_window.withdraw(), root.deiconify(), show_forward()], bg='white',
       fg='midnightblue', padx=20).grid(row=0, column=1)
    Button(frame_22, text='Home',
           state=DISABLED, bg='white',
       fg='midnightblue', padx=20).grid(row=0, column=2)
    Button(frame_22, text='>>',
           state=DISABLED, bg='white',
       fg='midnightblue', padx=15).grid(row=0, column=3)
    Label(fill_student_data_window, text='',
                      bg='lightgoldenrodyellow').grid(row=1)

    global stu_branch, stu_batch, stu_section, stu_semester, stu_subject, stu_roll
    
    frame_23 = LabelFrame(fill_student_data_window, text = 'Fill Student Details...',
                  bg='lightgoldenrodyellow', fg = 'navy')
    frame_23.grid(row = 2, column = 0)
    
    Label(frame_23, text='Branch'+' '*10,
                      bg='lightgoldenrodyellow', fg='purple', anchor = W).grid(row=0, column=0, sticky = W+E)
    stu_branch = Entry(frame_23,
              fg='blue', bg='white', width=30)
    stu_branch.grid(row=0, column=1)
    stu_branch.insert(0, 'Short form not allow')
    
    Label(frame_23, text='Batch'+' '*10,
                      bg='lightgoldenrodyellow', fg='purple', anchor = W).grid(row=1, column=0, sticky = W+E)
    style= ttk.Style()
    style.theme_use('clam')
    style.configure("TCombobox", foreground = 'blue', fieldbackground= "white", background= 'white')

    stu_batch = ttk.Combobox(frame_23, width=27)
    stu_batch['values'] = (2021, 2022, 2023, 2024, 2025, 2026, 2027,  2028, 2029, 2030, 2031, 2032,
                                2033, 2034, 2035, 2036, 2037, 2038, 2039, 2040, 2041, 2042, 2043, 2044, 2045, 2046, 2047, 2048, 2050)
    stu_batch.grid(row=1, column=1)
    stu_batch.current(0)
    
    Label(frame_23, text='Section'+' '*10,
                      bg='lightgoldenrodyellow', fg='purple', anchor = W).grid(row=2, column=0, sticky = W+E)
    stu_section = Entry(frame_23,
              fg='blue', bg='white', width=30)
    stu_section.grid(row=2, column=1)
    
    Label(frame_23, text='Semester'+' '*10,
                      bg='lightgoldenrodyellow', fg='purple', anchor = W).grid(row=3, column=0, sticky = W+E)
    stu_semester = ttk.Combobox(frame_23, width=27)
    stu_semester['values'] = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
    stu_semester.grid(row=3, column=1)
    stu_semester.current(0)
    
    Label(frame_23, text='Subject'+' '*10,
                      bg='lightgoldenrodyellow', fg='purple', anchor = W).grid(row=4, column=0, sticky = W+E)
    stu_subject = Entry(frame_23,
              fg='blue', bg='white', width=30)
    stu_subject.grid(row=4, column=1)
    
    Label(frame_23, text='Roll No'+' '*10,
                      bg='lightgoldenrodyellow', fg='purple', anchor = W).grid(row=5, column=0, sticky = W+E)
    stu_roll = Entry(frame_23,
              fg='blue', bg='white', width=30)
    stu_roll.grid(row=5, column=1)

    Label(fill_student_data_window, text='', bg='lightgoldenrodyellow').grid(row=3)

    Button(fill_student_data_window, text='Get', command=lambda: [
           fill_student_data_window.withdraw(), access_my_attendance()], bg='white',
       fg='midnightblue', padx = 15).grid(row=5, column=1)
    Button(fill_student_data_window, text='Exit',
           command=popup_1, bg='white',
       fg='midnightblue', padx = 15).grid(row=5, column=2)


root.title('Live Logging Face Recognition Attendance System')
root.iconbitmap('C:/Users/0526p/Pictures/implementation/LLFRAS.ico')
root.config(bg='lightgoldenrodyellow')

Button(root, text='<<', state=DISABLED, bg='white',
       fg='midnightblue', padx=10).grid(row=0, column=0)
Button(root, text='>>', state=DISABLED, bg='white',
       fg='midnightblue', padx=10).grid(row=0, column=1)

Label(root, text=' ', bg='lightgoldenrodyellow').grid(row=1)
Label(root, text='                    Welcome To                     ',
      bg='purple', fg='white').grid(row=2, column=3)
Label(root, text='The Live Logging Facial Recognition',
      bg='purple', fg='white').grid(row=3, column=3)
Label(root, text='             Attendance System                ',
      bg='purple', fg='white').grid(row=4, column=3)

row_value = 3
for i in range(5):
    welcome_3 = Label(root, text='         ',
                      bg='lightgoldenrodyellow').grid(row=row_value)
    row_value = row_value + 1


def image_path():
    global path_1, path_8
    path_1 = None
    path_8 = new_path + '/Image Directory'
    try:
        os.mkdir(path_8)
    except FileExistsError:
        pass


def attendance_path():
    global path_1, path_8
    path_8 = None
    path_1 = new_path + '/Attendance Directory'
    try:
        os.mkdir(path_1)
    except FileExistsError:
        pass


def get_attendance_path():
    global path_15
    path_15 = new_path + '/Attendance Directory/branch'

def popup_1():
    response = messagebox.askquestion('Quit Window!', 'Do you want to quit FARS?')
    if response == 'yes':
        root.destroy()
    else:
        pass
    

global new_path
get_path = str(Path.home())
spli = get_path.split('\\')
new_path = '/'.join(spli)+'/Desktop/Attendance'
try:
    os.mkdir(new_path)
except FileExistsError:
    pass
os.chdir(new_path)

proceed_button = Button(root, text='Attendance Portal', command=lambda: [root.withdraw(
), attendance_path(), branch_directories()], bg='navy', fg='white', padx=10).grid(row=row_value, column=2)
student_button = Button(root, text="Student's Portal", command=lambda: [root.withdraw(
), get_attendance_path(), fill_student_data()], bg='navy', fg='white', padx=10).grid(row=row_value, column=3)
image_button = Button(root, text='Image Portal', command=lambda: [root.withdraw(), image_path(
), branch_directories()], bg='navy', fg='white', padx=10).grid(row=row_value, column=4)
Label(root, text=' ', bg='lightgoldenrodyellow').grid(
    row=row_value + 1, column=5)
button_exit = Button(root, text='Exit', command=popup_1, bg='white',
                     fg='midnightblue', padx=10).grid(row=row_value+2, column=6)

root.mainloop()
