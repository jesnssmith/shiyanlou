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
        with open(self.path,'r') as f:
            for i in f:
                str=f.readline()
                print(str)
                [key,value]=str.split('=')
                key.strip()
                value.strip()
                config[key]=float(value)
        return config

if __name__=='__main__':

    args_file_paths=Args()
    configfile=args_file_paths.get_configfile_path()
    salary_file=args_file_paths.get_salary_file()
    output_file=args_file_paths.get_output_file()
    print(configfile,' ',salary_file,' ',output_file)
    config=Config(configfile).config

    print(config)
