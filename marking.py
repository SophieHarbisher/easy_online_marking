#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 11:13:23 2020

@author: sophie
"""
import os, pickle


class part:
    
    def __init__(self, part_ref, part_marks = 0, part_str = ''):
        self.ref = int(part_ref) # integer reference for the part of question e.g. 0,1,2,...
        self.statement = part_str # option to add in the question string
        self.max_mark = part_marks # can optionally add in the marks available
        self.comments = [] # stores the options for the comments
        
    def add_q_statement(self, part_str): # option to add question string later
        self.statement = part_str
        
    def change_ref(self, new_ref): # option to change the reference later
        self.ref = new_ref
        
    def add_comment(self, new_comment): # option to add more comments
        self.comments.append(new_comment)

class question:
    
    def __init__(self, qu_ref, qu_str = ''):
        self.ref = int(qu_ref)  # qu_ref is a integer reference for a question
        self.statement = qu_str # optional addition of question as string
        self.parts = [] # stores the parts of a question
        self.max_marks = 0. # stores the mark for each part of the question
    
    def add_part(self, part_ref):
        part_str = '' #input('Enter the question/press return... \n')
        part_marks = input('Enter maximum marks for part... \n')
        if(bool(part_marks)==False):
            part_marks = 0
        else:
            part_marks = float(part_marks)
        self.max_marks += part_marks
        new_part = part(part_ref, part_marks, part_str)
        print('Add some comments for student feedback... \n')
        add_more_comments = True
        while add_more_comments == True:
            new_comment = input('Enter comment...\n')
            new_part.add_comment(new_comment)
            add_more = input('Add another comment [Y/n]... \n')
            if bool(add_more) == True and (add_more=='n' or add_more=='N'):
                add_more_comments = False
        self.parts.append(new_part)
    
    def construct_question(self):
        curr_num_parts = 0
        print('Adding first part to the question...')
        add_more_parts = True
        while add_more_parts == True:
            self.add_part(curr_num_parts)
            curr_num_parts += 1
            add_more = input('Add another part [Y/n]... \n')
            if bool(add_more) == True and (add_more=='n' or add_more=='N'):
                add_more_parts = False
        

class marking_scheme:
    
    def __init__(self):
        self.questions = [] 
        self.total_marks = 0.
    
    def add_question(self, qu_ref):
        qu_str = '' #input('Enter the question/press return... \n')
        new_qu = question(qu_ref, qu_str)
        new_qu.construct_question()
        self.questions.append(new_qu)
        self. total_marks += new_qu.max_marks
    
    def construct(self):
        curr_num_q = 0
        print('Adding first question...')
        add_more_qs = True
        while add_more_qs == True:
            self.add_question(curr_num_q)
            curr_num_q += 1
            add_more = input('Add another question [Y/n]... \n')
            if bool(add_more) == True and (add_more=='n' or add_more=='N'):
                add_more_qs = False
    
    def save(self, fn = ''):
        print('Saving marking scheme... \n')
        if os.path.exists('./saved_mark_schemes') == False:
            os.mkdir('./saved_mark_schemes')
        if fn == '':
            fn = input('Enter file name... \n')
        if os.path.exists('./saved_mark_schemes/'+fn):
            overwrite = input('Overwrite file? [Y/n]... \n')
            if bool(overwrite) == True and (overwrite=='n' or overwrite=='N'):
                return
        with open('./saved_mark_schemes/'+fn, 'wb') as file:  # Overwrites any existing file.
            pickle.dump(self, file)

class marks:
    
    def __init__(self):
        self.marks = []
        self.comments = []
    
    def load(self):
        self.fn = input('Enter name of saved mark scheme... \n')
        if os.path.exists('./saved_mark_schemes/'+self.fn)==False:
            print('File does not exist.')
            return
        print('Loading marking scheme...')
        with open('./saved_mark_schemes/'+self.fn, 'rb') as file:
            self.m = pickle.load(file)
        print('Loaded. \n')
    
    def get_mark_scheme(self):
        use_existing = input('Use existing mark scheme? [Y/n]...')
        if bool(use_existing) == True and (use_existing=='n' or use_existing=='N'):
            m = marking_scheme()
            m.construct()
            m.save()
            self.m = m
        else:
            self.load()
    
    def print_comments(self, qu_ref, part_ref):
        c = self.m.questions[qu_ref].parts[part_ref].comments
        [print('['+str(i)+'] '+c[int(i)]+' \n') for i in range(len(c))]
        print('[-1] Add a new comment \n')
    
    def mark_part(self, qu_ref, part_ref):
        print('Available comments: ')
        self.print_comments(qu_ref, part_ref)
        choice = int(input('Choose an option...'))
        if choice != -1:
            part_comment = self.m.questions[qu_ref].parts[part_ref].comments[choice]
        else:
            new_comment = input('Enter alternative comment... \n')
            self.m.questions[qu_ref].parts[part_ref].add_comment(new_comment)
            self.m.save(self.fn) #save new comments
            return self.mark_part(qu_ref, part_ref)
        
        part_mark = float(input('Enter a mark out of '+str(self.m.questions[qu_ref].parts[part_ref].max_mark)+' for Q'+str(qu_ref)+' part '+str(part_ref)+'...'))
        while part_mark>self.m.questions[qu_ref].parts[part_ref].max_mark or part_mark<0:
            print('Value entered not valid.')
            part_mark = float(input('Enter a mark out of '+str(self.m.questions[qu_ref].parts[part_ref].max_mark)+' for Q'+str(qu_ref)+' part '+str(part_ref)+'...'))
    
        return [part_mark, part_comment]
    
    def mark_question(self, qu_ref):
        question_marking = []
        for part in range(len(self.m.questions[qu_ref].parts)):
            part_marking = self.mark_part(qu_ref, int(part))
            question_marking.append(part_marking)
        return question_marking
        
    def mark(self):
        marking = []
        for q in range(len(self.m.questions)):
            marking.append(self.mark_question(q))
        self.marks = marking

    def get_feedback(self):
        feedback = ''
        total_mark = 0.
        for q in range(len(self.m.questions)):
            feedback += 'Question '+str(q+1)+ '\n'
            for p in range(len(self.m.questions[q].parts)):
                part_mark = self.marks[q][p][0]
                total_mark += part_mark
                feedback += 'Part '+str(p+1)+' ['+str(part_mark)+' marks] \n'
                feedback += 'Comment: '+str(self.marks[q][p][1])+'\n'
            feedback += '\n'
        feedback += '\nTOTAL MARKS: '+str(total_mark)
        self.feedback = feedback
        
    def save_feedback(self):
        self.get_feedback()
        if os.path.exists('./saved_marks') == False:
            os.mkdir('./saved_marks')
        fn = input('Enter file name to store feedback... \n')
        if os.path.exists('./saved_marks/'+fn):
            overwrite = input('Overwrite file? [Y/n]... \n')
            if bool(overwrite) == True and (overwrite=='n' or overwrite=='N'):
                return
        with open('./saved_marks/'+fn, 'w') as file:  # Overwrites any existing file.
            file.write(self.feedback)
            file.close()
        
    def flush(self):
        self.marks = []
        self.comments = []
        self.feedback = ''

self = marks()
self.get_mark_scheme()
mark_another = True
while mark_another == True:
    self.mark()
    self.get_feedback()
    self.save_feedback()
    print(self.feedback)
    self.flush()
    ma = input('Mark another script? [Y/n]...')
    if bool(ma) == True and (ma=='n' or ma=='N'):
        mark_another = False