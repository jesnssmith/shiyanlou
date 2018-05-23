#!/usr/bin/env python3 

import sys
import csv
from multiprocessing import Process,Queue
import getopt
import configparser
import datetime

class Args(object):

    def __init__(self):
        self.args=self.get_arg()
        
    def get_arg(self):
        try:
            opts,args=getopt.getopt(sys.argv[1:],"c:d:o:C:")
        except getopt.GetoptError as e:
            print(e)
            
        return dict(opts)
            

class Config(object):
    
    def __init__(self,file):
        self.file=file
        self.config=self.getconfig()
        
    def getconfig(self):
        config=configparser.ConfigParser()
        config.read(self.file)
        return config
        

class UserData(Process):

    def __init__(self,path,q):
        super(UserData,self).__init__()
        self.path=path
        self.q=q



    def run(self):
        userdata=[]
        try:
            with open(self.path,'r') as f:
                for str in f:
                    user_id,salary=str.split(',')
                    user_id.strip()
                    salary.strip()
                    userdata.append((user_id,float(salary)))
            self.q.put(userdata)
        except:
            print("Parameter Error")

     
class IncomeTaxCalculator(Process):
    
    def __init__(self,shebao,q1,q2):
        super(IncomeTaxCalculator,self).__init__()
        self.shebao=shebao
        self.salary=q1.get()
        self.q2=q2


    def calculate_tax(self,owned):
        
        
        if owned <= 0:
            tax=0
        elif owned<=1500:
            tax=owned*0.03
        elif owned<=4500:
            tax=owned*0.1-105
        
        elif owned<=9000:
            tax=owned*0.2-555 
        elif owned<=35000:
            tax=owned*0.25-1005
        elif owned<=55000:
            tax=owned*0.3-2705
        elif owned<=80000:
            tax=owned*0.35-5505
        else:
            tax=owned*0.45-13505
        return tax

    def run(self):
        output=[]
        persent=self.shebao.get('persent')
        l='jishul'
        h='jishuh'
        for i,j in self.salary:
            if j<self.shebao[l] and j>0:
                shebao_fee=self.shebao[l]*persent
            elif j>self.shebao[l] and j<self.shebao[h]:
                shebao_fee= j*persent
            elif j>self.shebao[h]:
                shebao_fee=self.shebao.get(h)*persent
            else:
                print("Invalid salary")
            tax_fee=j-shebao_fee-3500
            tax=self.calculate_tax(tax_fee)
            salary_after_tax=j-shebao_fee-tax
            t=datetime.datetime.now()
            t_str=datetime.datetime.strftime(t,'%Y-%m-%d %H:%M:%S')
            output.append([i,j,format(shebao_fee,'.2f'),format(tax,'.2f'),format(salary_after_tax,'.2f'),t_str])
        self.q2.put(output)

  
def export(output_file,q):
    result=q.get()
    with open(output_file,'w') as f:
        writer=csv.writer(f)
        writer.writerows(result)



   
if __name__ == '__main__':
    a=Args()
    print(a.args.get('-C',False))    
    config_file=a.args.get('-c') 
    city=a.args.get('-C')
    userdata_file=a.args.get('-d')
    output_file=a.args.get('-o')
    if city:
        city=city.upper()
    else:
        city="DEFAULT"
    config=Config(config_file).config
    shebao={'persent':0}
    for key in config[city]:
        value=config[city][key]
        if float(value) > 1:
            shebao[key] = float(value)
        else:
            shebao['persent'] += float(value)
    print(shebao)
    q1 = Queue()
    p1=UserData(userdata_file,q1)
    p1.start()
    p1.join() 
    q2=Queue()     
    p2=IncomeTaxCalculator(shebao,q1,q2)
    p2.start()
    p2.join()
    p3=Process(target=export,args=(output_file,q2)) 
    p3.start()
    