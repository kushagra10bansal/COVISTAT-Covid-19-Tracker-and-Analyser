from matplotlib import pyplot as plt
import numpy as np
import csv
import datetime

def simplegrph(d,title='',x_label='',y_label='',rotation=None,width=1,save=None,grid=None):
    fig,ax=plt.subplots()
    plt.style.use('fivethirtyeight')
    for label,values in d.items():
        ax.plot(values[0],values[1],label=label,linewidth=width)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.legend()
    plt.xticks(rotation=rotation)
    plt.tight_layout()
    ax.grid(zorder=0)
    if save:
        plt.savefig(save)
    plt.show()
    return

def country():#For comparison of different countries
    print('''Available formats:
1: Graph
2: Table
0: Return
''')
    fchoice=int(input("Select format: "))

    if fchoice==0:
        print("Redirecting to Main Menu...")
        return
        
    print('''Available Data:
1: Total cases
2: New Cases per day
3: Total Deaths
4: New Deaths per day
0: Back''')
dchoice=int(input("Enter choice: "))
if dchoice==0:
        print('Redirecting to Main Menu...')
        return

    lc=input("Enter list of countries(seperated by commas):")
    lc.lower()
    countrylist=lc.split(',')
    cdict=dict.fromkeys(countrylist)       #making a dictionary with names of countries as keys

    cfile=open("edited file.csv","r")
    cdata=csv.reader(cfile)

    sdate=input("Enter start date(mm-dd-yyyy): ")
    edate=input("Enter end date(mm-dd-yyyy): ")
    start=datetime.datetime.strptime(sdate,'%m-%d-%Y')
    end=datetime.datetime.strptime(edate,'%m-%d-%Y') #inputting start and end dates and 									      #converting them to date datatype
    
    for i in countrylist:
        tcases=[]
        ncases=[]
        tdeaths=[]
        ndeaths=[]
        dates=[]

        for j in cdata:
            if j[1].lower()==i.lower():
                d=datetime.datetime.strptime(j[0],'%m-%d-%Y')
                if start<=d<=end:
                    try:
                        dates.append(j[0])
                        ncases.append(int(j[2]))
                        ndeaths.append(int(j[3]))
                        tcases.append(int(j[4]))
                        tdeaths.append(int(j[5]))
                    except:
                        pass

        #keys are names of countries, each value is a list with first element
        #as a list of dates and second element as a list of cases corresponding to dates.
        if dchoice==1:
            cdict[i]=[dates,tcases]
        elif dchoice==2:           
            cdict[i]=[dates,ncases]
        elif dchoice==3:
            cdict[i]=[dates,tdeaths]
        elif dchoice==4:
            cdict[i]=[dates,ndeaths]
        else:
            print("Invalid Choice...Redirecting to Main Menu")
            cfile.close()
            return

        cfile.seek(0)

    if fchoice==1:              #displaying graph
        simplegrph(cdict,title='Distribution by Country',x_label='Dates',y_label='Number of Cases',rotation='vertical')

    elif fchoice==2:#displaying table
        #Printing headings of columns
        print('%10s' % 'Date',end='')
        for i in countrylist:
            print('%17s' % i,end='')
        print()
        #printing data of each row
        while start<=end:
            print('%10s' % start.date(),end='')
            for j in cdict.keys():
                for i in range(len(cdict[j][0])):
                    date=datetime.datetime.strptime(cdict[j][0][i],'%m-%d-%Y')
                    if date==start:
                        print('%17s' % cdict[j][1][i],end='')
                    else:
                        pass
            print()
            start=start+datetime.timedelta(1)
    return

def age():
    agegrpdtls=open("AgeGroupDetails.csv","r")
    data=csv.reader(agegrpdtls)
    print('''1: Table
2: Graph
0: Return''')
    achoice=int(input("Enter choice: "))
    if achoice==2:
        row=next(data)
        agegrp=[]
        total_cases=[]
        percentage=[]
        for i in data:
            agegrp.append(i[1])
            total_cases.append(int(i[2]))
            percentage.append(float(i[3][:-2]))
        plt.style.use('fivethirtyeight')
        plt.pie(percentage,labels=agegrp)
        plt.legend()
        plt.show()
    elif achoice==1:
        for i in data:
            print('%13s' % i[1],'%12s' % i[2],'%10s' % i[3])
    elif achoice==0:
        print("Redirecting to Main Menu...")
    else:
        print('Invalid Choice... Returning to Main Menu')
    return

def hospital():#states is a list of states input by the user
    hospital=open("HospitalBedsIndia.csv","r")
    data=csv.reader(hospital)
    print('''1: Graph
2: Table
0: Return''')
    hchoice=int(input("Enter choice: "))

    if hchoice==1:
        st=input('Enter list of states seperated by commas: ')
        states=st.split(',')
        row=next(data)
        fig,ax=plt.subplots()
        plt.style.use('fivethirtyeight')

        rbeds=[]
        pbeds=[]
        ubeds=[]
        s_lower=[]

        for i in states:
            s_lower.append(i.title())
        s_lower.sort()

        for i in data:
            if i[1].title() in s_lower:
                rbeds.append(int(i[9]))
                pbeds.append(int(i[7]))
                ubeds.append(int(i[11]))

        x=np.arange(len(s_lower))
        width=0.2
        ax.grid(zorder=0)
        ax.bar(x-width,rbeds,width=width,label="rural",zorder=3)
        ax.bar(x,pbeds,width=width,label="public",zorder=3)
        ax.bar(x+width,ubeds,width=width,label="urban",zorder=3)
        ax.set_xticks(x)
        ax.set_xticklabels(s_lower,rotation='vertical')
        ax.set_xlabel('States')
        ax.set_ylabel("Number of Beds")
        ax.set_title("BEDS")
        ax.legend()
        plt.tight_layout()
        plt.savefig("HospitalGraph.jpeg")
        plt.show()
    elif hchoice==2:
        st=input('Enter list of states seperated by commas: ')
        states=st.split(',')
        print('%17s' % 'State','%15s' % 'Rural Beds','%15s' % 'Urban Beds','%15s' % 'Public beds')
        if st.lower()!='all':
            for i in data:
                if i[1] in states:
                    print('%17s' % i[1],'%15s' % i[9],'%15s' % i[11],'%15s' % i[7])
                else:
                    pass
        else:
            row=next(data)
            for i in data:
                print('%17s' % i[1],'%15s' % i[9],'%15s' % i[11],'%15s' % i[7])
    else:
        print("Redirecting to Main Menu...")
    hospital.close()
    return
                
def tests():
    
    st=input('Enter list of states seperested by commas: ')
    names=st.split(',')
    start=input("Enter start date(dd-mm-yyyy):")
    end=input("Enter end date(dd-mm-yyyy):")
    sdate=datetime.datetime.strptime(start,'%d-%m-%Y')
    edate=datetime.datetime.strptime(end,'%d-%m-%Y')
    
    data=open('StatewiseTestingDetails.csv','r')
    read=csv.reader(data)

    states=dict.fromkeys(names)

    print('{:^10}'.format('Dates'),end='')
    for j in states.keys():
        print('{:^28}'.format(j),end='')
    print()
    print('{:10}'.format(''),end='')
    for i in range(len(names)):
        print('{:^14}'.format('Total Samples'),'{:^14}'.format('Positive'),end='')
    print()
    for i in states.keys():
        total_samples=[]
        positive=[]
        dates=[]
        for j in read:
            if j[1].lower()==i.lower():
                d=datetime.datetime.strptime(j[0],'%d-%m-%Y')
                if sdate<=d<=edate:
                    try:
                        dates.append(j[0])
                        total_samples.append(int(j[2]))
                        positive.append(int(j[4]))
                    except:
                        pass
        states[i]=[dates,total_samples,positive]
        data.seek(0)
    while sdate<=edate:
        print('%10s' % sdate.date(),end='')
        for j in states.keys():
            for i in range(len(states[j][0])):
                date=datetime.datetime.strptime(states[j][0][i],'%d-%m-%Y')
                if date==sdate:
                    print('{:^14d}'.format(states[j][1][i]),'{:^14d}'.format(states[j][2][i]),end='')
                else:
                    pass
        print()
        sdate=sdate+datetime.timedelta(1)

def states():
    print('''Available Formats:
1: Graph
2: Table
0: Return''')
    fchoice=int(input("Enter choice: "))
    if fchoice==0:
        return
    elif fchoice==1:
        print('''Available data:
1: Active Cases
2: Total Cases
3: Total Number of Patients Cured
4: Total Deaths Reported
5: New Cases Reported Per Day
6: New Deaths Reported Per Day''')
        gchoice=int(input("Enter choice: "))

        st=input('Enter list of states seperested by commas: ')
        names=st.split(',')

        start=input("Enter start date(dd-mm-yyyy):")
        end=input("Enter end date(dd-m-yyyy):")
        sdate=datetime.datetime.strptime(start,'%d-%m-%Y')
        edate=datetime.datetime.strptime(end,'%d-%m-%Y')

        data=open('covid_19_india.csv','r')
        read=csv.reader(data)

        d=dict.fromkeys(names)

        for j in d.keys():
            totalcases=[]
            activecases=[]
            cured=[]
            deaths=[]
            dates=[]
            ncases=[]
            ndeaths=[]
            tcases=tdeaths=0

            for i in read:
                stname=i[3].lower()
                if stname==j.lower():
                    date=datetime.datetime.strptime(i[1],'%d-%m-%Y')#ignore - to convert string to date
                    if sdate<=date<=edate:
                        actv=int(i[8])-int(i[7])-int(i[6])
                        dates.append(i[1])
                        totalcases.append(int(i[8]))
                        activecases.append(actv)
                        deaths.append(int(i[7]))
                        cured.append(int(i[6]))
                        ncases.append(int(i[8])-tcases)
                        ndeaths.append(int(i[7])-tdeaths)
                    try:#to avoid error in reading first row
                        tcases=int(i[8])
                        tdeaths=int(i[7])
                    except ValueError:
                        print('k')

            if gchoice==1:
                y='Number of Active cases'
                d[j]=[dates,activecases]
            if gchoice==2:
                y='Number of Total cases'
                d[j]=[dates,totalcases]
            if gchoice==3:
                y='Number of patients cured'
                d[j]=[dates,cured]
            if gchoice==4:
                y='Number of Deaths'
                d[j]=[dates,deaths]
            if gchoice==5:
                y='Number of cases reported per day'
                d[j]=[dates,ncases]
            if gchoice==6:
                y='Number of deaths reported per day'
                d[j]=[dates,ndeaths]
            data.seek(0)

        simplegrph(d,title='RegionWise Distribution',x_label='Dates',y_label='Number of Cases',rotation='vertical',width=0.75,save='states.png')
        return
    elif fchoice==2:
        f=open('statewise.csv',"r")
        data=csv.reader(f)
        print('''
1.Available data
2.Total deaths cases
3.Total cured cases
4.Total active cases''')
        n=int(input('ENTER YOUR CHOICE 1-4:'))
        if n==1:
           for i in data:
               print('%30s'%i[0],'%20s'%i[1],'%20s'%i[2],'%20s'%i[3])
        elif n==2:
           for i in data:
               print('%30s'%i[0],'%20s'%i[1])
        elif n==3:
           for i in data:
               print('%30s'%i[0],'%20s'%i[2])
        elif n==4:
           for i in data:
               print('%30s'%i[0],'%20s'%i[3])
        else:
            print("Invalid Choice...")
        return

    
#Main Function
while True:
    print("""MAIN MENU:
    1: Comparison of Different Countries
    2: Distribution by Age
    3: Data of Hospital Beds(State-Wise)
    4: Testing Data by State
    5: Distribution by State
    0: Exit""")
    mchoice=int(input("Enter choice: "))
    if mchoice==0:
        break
    elif mchoice==1:
        country()
    elif mchoice==2:
        age()
    elif mchoice==3:
        hospital()
    elif mchoice==4:
        tests()
    elif mchoice==5:
        states()


