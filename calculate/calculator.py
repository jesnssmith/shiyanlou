#!/usr/bin/env python3 

import sys
import csv
from multiprocessing import Process,Queue

class Args(object):

    def __init__(self):
        self.__args=sys.argv[1:]
        self.c = self.__args[self.__args.index('-c')+1]
        self.d = self.__args[self.__args.index('-d')+1]
        self.o = self.__args[self.__args.index('-o')+1]

#a=Args()
#print(a.c,a.d,a.o)     



class Config(object):

    def __init__(self,path):
        self.path=path
        self.config=self._read_config()

    def _read_config(self):
        config={'shebao':0}
        try:
            with open(self.path,'r') as f:
                for str in f:
                    key,value=str.split('=')[0].strip(),str.split('=')[1].strip()
                    if float(value) > 1:
                        config[key] = float(value)
                    else:
                        config['shebao'] += float(value)
            return config
        except:
            print("Parameter Error")


#b=Config(a.c).config
#print(b)


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
            
#c=UserData(a.d).userdata
#print(c)
        

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
        persent=self.shebao.get('shebao')
        for i,j in self.salary:
            if j<self.shebao['JiShuL'] and j>0:
                shebao_fee=self.shebao['JiShuL']*persent
            elif j>self.shebao['JiShuL'] and j<self.shebao['JiShuH']:
                shebao_fee= j*persent
            elif j>self.shebao['JiShuH']:
                shebao_fee=self.shebao.get('JiShuH')*persent
            else:
                print("Invalid salary")
            tax_fee=j-shebao_fee-3500
            tax=self.calculate_tax(tax_fee)
            salary_after_tax=j-shebao_fee-tax
            output.append([i,j,format(shebao_fee,'.2f'),format(tax,'.2f'),format(salary_after_tax,'.2f')])
        self.q2.put(output)
    
    
    
def export(output_file,q):
    result=q.get()
    with open(output_file,'w') as f:
        writer=csv.writer(f)
        writer.writerows(result)
            
            
if __name__=='__main__':
    a=Args()
    b=Config(a.c).config 
    q1 = Queue()
    p1=UserData(a.d,q1)
    p1.start()
    p1.join() 
    q2=Queue()     
    p2=IncomeTaxCalculator(b,q1,q2)
    p2.start()
    p2.join()
    p3=Process(target=export,args=(a.o,q2)) 
    p3.start()    
