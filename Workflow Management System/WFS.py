import csv
import re

class Project:
    
    def __init__(self):
        self.List_of_Tasks = list()
        self.List_of_Personel = list()
        self.load_task()
        self.load_personel()
        
    def add_task(self):
        self.List_of_Tasks.append(Task(0,0,0,0,0))
        
    def add_personel(self):
        self.List_of_Personel.append(Personel(0,0,0))
        
    def string_to_bool_converter(self, to_convert):#I can't believe Python doesn't have a built in way to convert 'True' and 'False' into True and False, who would ever want to convert 'False' using bool('False') into True. Why Python? Why?
        to_convert = to_convert.upper()
        if to_convert == 'TRUE':
            return True
        elif to_convert == 'FALSE':
            return False
        else:
            return 'Error: string_to_bool_converter encountered unknown input.'
        
    def load_task(self):#loads tasks from the csv file if it exists
        try:
            with open('Tasks.csv', mode='r') as table_file:
                csv_reader = csv.DictReader(table_file)
    
                for row in csv_reader:
                    self.List_of_Tasks.append(Task(row['Name'], row['Qualifications'].split('|'), self.string_to_bool_converter(row['Completed']), row['Time_Left'], int(row['Task_ID'])))
        
                table_file.close()
            print('Tasks CSV File read')
        except Exception as e:
            print(e)
            print('In load_task')
    
        
        
    def load_personel(self):#loads personel from the csv file if it exists
        try:
            with open('Personel.csv', mode='r') as table_file:
                csv_reader = csv.DictReader(table_file)
    
                for row in csv_reader:
                    self.List_of_Personel.append(Personel(row['Name'], row['Qualifications'].split('|'), int(row['Task_Assigned'])))
        
                table_file.close()
            print('Personel CSV File read')
        except Exception as e:
            print(e)
            print('In load_personel')
            
    def purify_list(self, to_purify): #This function cleanses a list to prepare it to be stored into a single cell in a csv file.
        to_purify = re.sub(', ','|',to_purify)
        to_purify = re.sub('\[','',to_purify)
        to_purify = re.sub('\]','',to_purify)
        to_purify = re.sub('\'','',to_purify)
        to_purify = re.sub(',','ERROR_UNEXPECTED_COMMA_LOCATED_HERE',to_purify) #This shouldn't match anything unless the user accidentally added a comma in the qualifications somewhere.
        return to_purify
        
    def save_project(self):
        print('Saving...')
    
        #Saves the list of personel to a CSV file.
        with open('Personel.csv', mode='w') as table_file:
            line = 'Name,Qualifications,Task_Assigned'
            table_file.write(line)
            table_file.write('\n')
            for i in range(0, len(self.List_of_Personel)):
                line = str(self.List_of_Personel[i].Name)+','+str(self.purify_list(str(self.List_of_Personel[i].Qualifications)))+','+str(self.List_of_Personel[i].Task_Assigned)
                table_file.write(line)
                table_file.write('\n')       
            table_file.close()
            
        #Saves the list of tasks to a CSV file.
        with open('Tasks.csv', mode='w') as table_file:
            line = 'Name,Qualifications,Completed,Time_Left,Task_ID'
            table_file.write(line)
            table_file.write('\n')
            for i in range(0, len(self.List_of_Tasks)):
                line = str(self.List_of_Tasks[i].Name)+','+str(self.purify_list(str(self.List_of_Tasks[i].Qualifications)))+','+str(self.List_of_Tasks[i].Completed)+','+str(self.List_of_Tasks[i].Time_Left)+','+str(self.List_of_Tasks[i].Task_ID)
                table_file.write(line)
                table_file.write('\n')       
            table_file.close()
            
        print('Save Successful.')
            
        
    def view_assigned_tasks(self):
        assigned_tasks = list()
        for person in self.List_of_Personel:
            assigned_tasks.append(person.Task_Assigned)
            
        for task in self.List_of_Tasks:
            if task.Task_ID in assigned_tasks:
                print('-----------------')
                print('Task Name: '+str(task.Name))
                print('Task ID: '+str(task.Task_ID))
                print('Task Completion: '+str(task.Completed))
                print('Time Left on Task: '+str(task.Time_Left))
                print('Task Qualifications: ')
                i = 0
                while i < len(task.Qualifications):
            
                    if len(task.Qualifications) == 1:
                        break
            
                    print(str(task.Qualifications[i]) + ' ' + str(task.Qualifications[i+1]))
                    i += 2
        
    def view_unassigned_tasks(self):
        assigned_tasks = list()
        for person in self.List_of_Personel:
            assigned_tasks.append(person.Task_Assigned)
            
        for task in self.List_of_Tasks:
            if task.Task_ID not in assigned_tasks: #The 'not' here allows us to view the tasks not assigned.
                print('-----------------')
                print('Task Name: '+str(task.Name))
                print('Task ID: '+str(task.Task_ID))
                print('Task Completion: '+str(task.Completed))
                print('Time Left on Task: '+str(task.Time_Left))
                print('Task Qualifications: ')
                i = 0
                while i < len(task.Qualifications):
            
                    if len(task.Qualifications) == 1:
                        break
            
                    print(str(task.Qualifications[i]) + ' ' + str(task.Qualifications[i+1]))
                    i += 2
        
    def assignments(self): #essentially, unavailable personel
        for person in self.List_of_Personel:
        
            if person.Task_Assigned == 0:
                continue
        
            print('-----------------')
            print('Name: ' + str(person.Name))
            print('Task Assigned: ' + str(person.Task_Assigned))
            print('Qualifications: ')
            i = 0
            while i < len(person.Qualifications):
            
                if len(person.Qualifications) == 1:
                    break
            
                print(str(person.Qualifications[i]) + ' ' + str(person.Qualifications[i+1]))
                i += 2
                
            print('-----------------')
        
    def available_personel(self):
        for person in self.List_of_Personel:
        
            if person.Task_Assigned != 0:
                continue
        
            print('-----------------')
            print('Name: ' + str(person.Name))
            print('Task Assigned: ' + str(person.Task_Assigned))
            print('Qualifications: ')
            i = 0
            while i < len(person.Qualifications):
            
                if len(person.Qualifications) == 1:
                    break
            
                print(str(person.Qualifications[i]) + ' ' + str(person.Qualifications[i+1]))
                i += 2
                
            print('-----------------')
        
    def list_all_personel(self):
        for person in self.List_of_Personel:
            print('-----------------')
            print('Name: ' + str(person.Name))
            print('Task Assigned: ' + str(person.Task_Assigned))
            print('Qualifications: ')
            i = 0
            while i < len(person.Qualifications):
            
                if len(person.Qualifications) == 1:
                    break
            
                print(str(person.Qualifications[i]) + ' ' + str(person.Qualifications[i+1]))
                i += 2
                
            print('-----------------')
            
            
    def add_task_to_personel(self):
        search = input('Enter Personel Name: ')
        located_person = 0
        
        for person in self.List_of_Personel:
            if person.Name == search:
                located_person = person
                break
                
        if located_person == 0:
            print('Person not found')
        else:
            tasks = list()
            for task in self.List_of_Tasks:
                tasks.append(task.Task_ID)
        
            task_id = int(input('Enter Task ID to Assign: '))
            if task_id in tasks:
                located_person.Task_Assigned = task_id
            else:
                print('Task does not exist.')
    
    def qualification_search(self):
        qual_search = input('Qualification Name: ')
        qual_min_rating = int(input('Minimum Rating: '))
        found_any = False
    
        for person in self.List_of_Personel:
            found = False
            i = 0
            while i < len(person.Qualifications):
            
                if len(person.Qualifications) == 1:
                    break
                
                if person.Qualifications[i] == qual_search:
                    if int(person.Qualifications[i+1]) >= qual_min_rating:
                        found = True
                        found_any = True
                        break
                i += 2
                
                
            if found:
                print('-----------------')
                print('Name: ' + str(person.Name))
                print('Task Assigned: ' + str(person.Task_Assigned))
                print('Qualifications: ')
                i = 0
                while i < len(person.Qualifications):
            
                    if len(person.Qualifications) == 1:
                        break
            
                    print(str(person.Qualifications[i]) + ' ' + str(person.Qualifications[i+1]))
                    i += 2
                
                print('-----------------')
        if not found_any:
            print('No Match')

    def change_time_remaining_on_task(self):
        search = int(input('Enter Task ID: '))
        located_task = 0
        
        for task in self.List_of_Tasks:
            if task.Task_ID == search:
                located_task = task
                break
                
        if located_task == 0:
            print('Task ID not found')
        else:
            located_task.set_time()


    def set_task_completion(self):
        search = int(input('Enter Task ID: '))
        located_task = 0
        
        for task in self.List_of_Tasks:
            if task.Task_ID == search:
                located_task = task
                break
                
        if located_task == 0:
            print('Task ID not found')
        else:
            while 1:
                choice = str(input('Completion Status (True/False, X to cancel): ')).upper
                if choice == 'TRUE' or choice == 'FALSE':
                    status = self.string_to_bool_converter(choice)
                    located_task.set_task_completion(status)
                    break
                elif choice == 'X':
                    break
                else:
                    print('Incorrect Input: Try Again.')
                
            


class Personel:
    Name = 0
    Qualifications = 0
    Task_Assigned = 0

    def selection(self):
        c = 'c'
        while c != 'N' and c != 'Y':
            c = input('Add Qualifications Y/N: ').upper()
            if c != 'N' and c != 'Y':
                print('Error, try again')
                
        return c
    
    def __init__(self, Name, Qualifications, Task_Assigned):
        #There needs to be a constructor capable of working with user input and capable of accepting input from a csv file. There are other ways to implement this but this seems cleanest.
        if Name == 0 and Qualifications == 0 and Task_Assigned == 0:
            self.Name = input('Enter Person Name: ')
            self.Qualifications = list()
            self.Task_Assigned = 0
            c = self.selection()
            while c != 'N' :
                Qualifications = input('Enter Qualifications Name: ')
                required_rating = int(input('Enter required rating (1-5): '))
                self.Qualifications.append(Qualifications)
                self.Qualifications.append(required_rating)
                c = self.selection()
        else:
            self.Name = Name
            self.Qualifications = Qualifications
            self.Task_Assigned = Task_Assigned

class Task:
    Name = 0
    Qualifications = 0
    Completed = 0
    Time_Left = 0
    Task_ID = 0


    Task_ID_Pool = 100 #this is used similar to a static class member in c parler by using class methods to access it.
    
    def selection(self):
        c = 'c'
        while c != 'N' and c != 'Y':
            c = input('Add Qualifications Y/N: ').upper()
            if c != 'N' and c != 'Y':
                print('Error, try again')
        return c

    def set_time(self):
        self.Time_Left = int(input('Set time left (in days) for task: '))
        
    def task_completion(self, status):
        self.Completed = status
      
    @classmethod
    def give_id(self):
        self.Task_ID_Pool += 1
        return self.Task_ID_Pool
        
    @classmethod
    def set_id(self, ID):
        self.Task_ID_Pool = ID
        
    @classmethod
    def check_id_pool(self):
        return self.Task_ID_Pool
    
    def __init__(self, Name, Qualifications, Completed, Time_Left, Task_ID):
        if Name == 0 and Qualifications == 0 and Completed == 0 and Time_Left == 0 and Task_ID == 0:
            self.Name = input('Enter Task Name: ')
            self.Qualifications = list()
            self.Completed = False
            c = self.selection()
            while c != 'N' :
                Qualifications = input('Enter Qualifications Name: ')
                required_rating = input('Enter required rating (1-5): ')
                self.Qualifications.append(Qualifications)
                self.Qualifications.append(required_rating)
                c = self.selection()
        
            self.Task_ID = Task.give_id()
        else:
            self.Name = Name
            self.Qualifications = Qualifications
            self.Completed = Completed
            self.Time_Left = Time_Left
            self.Task_ID = Task_ID
            
            if Task_ID > Task.check_id_pool():
                Task.set_id(Task_ID)#this allows the saved tasks in the csv file to have whatever IDs they want and the Task_ID_Pool will just assign itself the largest and carry on from there.


def personel_management(p):
    while 1:
        print('-----------------')
        print('Personel Management Menu:')
        print('(1) Add Personel')
        print('(2) View Personel Assignments')
        print('(3) View Available Personel')
        print('(4) Add Task to Personel')
        print('(5) Search Qualification')
        print('(6) View All Personel')
        print('(X) Return to Main Menu')
        
        choice = input('Enter Command: ')
        choice = choice.upper()
        
        if choice == '1' or choice == 'ADD PERSONEL':
            p.add_personel()
        elif choice == '2' or choice == 'VIEW PERSONEL ASSIGNMENTS':
            p.assignments()
            input('Press Enter')
        elif choice == '3' or choice == 'VIEW AVAILABLE PERSONEL':
            p.available_personel()
            input('Press Enter')
        elif choice == '4' or choice == 'ADD TASK TO PERSONEL':
            p.add_task_to_personel()
        elif choice == '5' or choice == 'SEARCH QUALIFICATION':
            p.qualification_search()
        elif choice == '6' or choice == 'VIEW ALL PERSONEL':
            p.list_all_personel()
            input('Press Enter')
        elif choice == 'X':
            break
        else:
            print('Unknown Command. Try Again.')
        
        
def task_management(p):
    while 1:
        print('-----------------')
        print('Task Management Menu')
        print('(1) Add Task')
        print('(2) View Unassigned Tasks')
        print('(3) View Tasks in progress')
        print('(4) Change Time Remaining on Task')
        print('(5) Set Task Completion')
        print('(X) Return to Main Menu')
        
        choice = input('Enter Command: ')
        choice = choice.upper()
        
        if choice == '1' or choice == 'ADD TASK':
            p.add_task()
        elif choice == '2' or choice == 'VIEW UNASSIGNED TASKS':
            p.view_unassigned_tasks()
            input('Press Enter')
        elif choice == '3' or choice == 'VIEW TASKS IN PROGRESS':
            p.view_assigned_tasks()
            input('Press Enter')
        elif choice == '4' or choice == 'CHANGE TIME REMAINING ON TASK':
            p.change_time_remaining_on_task()
        elif choice == '5' or choice == 'SET TASK COMPLETION':
            p.set_task_completion()
        elif choice == 'X':
            break
        else:
            print('Unknown Command. Try Again.')
        

#main
p = Project()

print('\nWFS 1.0 initialized.\n')
   
while 1:
    print('-----------------')
    print('Main Menu: ')
    print('(1) Personel Management')
    print('(2) Task Management')
    print('(X) Exit')
    
    choice = input('Enter Command: ')
    choice = choice.upper()
    
    if choice == '1' or choice == 'PERSONEL MANAGEMENT':
        personel_management(p)
    elif choice == '2' or choice == 'TASK MANAGEMENT':
        task_management(p)
    elif choice == 'X':
        break
    else:
        print('Unknown Command. Try Again.')


p.save_project()
print('System Closing...')












