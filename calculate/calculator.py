#!/usr/bin/env python3 

import sys
import csv

class Args(object):

    def __init__(self):
        self.__args=sys.argv[1:]
    
    def get_configfile_path(self):
        index=self.__args.index('-c')
        configfile=self.__args[index+1]
        return configfile

    def get_salary_file(self):
        index=self.__args.index('-d')
        salary_file=self.__args[index+1]
        return salary_file

    def get_output_file(self):
        index=self.__args.index('-o')
        output_file=self.__args[index+1]
        return output_file


class Config(object):

    def __init__(self,path):
        self.path=path
        self.config=self._read_config()

    def _read_config(self):
        config={}
        try:
            with open(self.path,'r') as f:
                for str in f:
                    [key,value]=str.split('=')
                    key.strip()
                    value.strip()
                    config[key]=float(value)
            return config
        except:
            print("Parameter Error")

class UserData(object):

    def __init__(self,path):
        self.path=path

        self.userdata=self._read_users_data()

    def _read_users_data(self):
        userdata=[]
        try:
            with open(self.path,'r') as f:
                for str in f:
                    [user_id,salary]=str.split(',')
                    user_id.strip()
                    salary.strip()
                    userdata.append((user_id,float(salary)))
            return userdata
        except:
            print("Parameter Error")
        

class IncomeTaxCalculator(object):
    
    def __init__(self,shebao,salary,output_file):
        self.shebao=shebao
        self.salary=salary
        self.output_file=output_file


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



    def calc_for_all_userdata(self):
        output=[]
        persent=0
        for i in self.shebao.keys():
            if i!='JiShuL' and i!='JiShuH':
                persent+=self.shebao[i]
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
            output.append((i,j,shebao_fee,tax,salary_after_tax))
        return output
    
    def export(self,default="csv"):
        result=self.calc_for_all_userdata()
        with open(self.output_file,'w') as f:
            writer=csv.writer(f)
            for i in result:
                str="{},{:.0f},{:.2f},{:.2f},{:.2f}".format(*i)
                str_list=str.split(',')
#                print(str_list)    test 
                writer.writerow(str_list)
            
              
        
if __name__=='__main__':

    args_file_paths=Args()
    configfile=args_file_paths.get_configfile_path()
    salary_file=args_file_paths.get_salary_file()
    output_file=args_file_paths.get_output_file()
#    print(configfile,' ',salary_file,' ',output_file)    test
    config=Config(configfile).config

#    print(config)               test
    userdata=UserData(salary_file).userdata
#    print(userdata)                 test
    
    output=IncomeTaxCalculator(config,userdata,output_file)
    output.export()
