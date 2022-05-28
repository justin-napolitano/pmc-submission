#import pyfiglet
#from pyfiglet import Figlet
#from lolpython import lol_py
import subprocess
from time import sleep
from random import randrange
from datetime import datetime

class config:

    def __init__(self):
        self.cname = self.cname_init()


    def cname_init(self):
        cname = "ch4.jnapolitano.io"
        return cname



class dependency_pipeline:

    def __init__(self):
        self.dependencies_log = self.install_dependencies()

    def install_dependencies(self):
        ##print("Dependency Check")
        utility_functions.seperator()
        #subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'my_package'])
        result = subprocess.run(['pip', 'install', '-r', 'requirements.txt'], capture_output=True, text=True)
        print(result.stdout)

        print(result.stderr)

        ##print("DependenCies INstalled")
        utility_functions.seperator()

        return(result)

class build_pipeline:

    def __init__(self):

        self.clean_log=self.make_clean()
        self.make_log=self.make_html()
        self.add_log=self.add()
        self.commit_log=self.commit()
        self.push_log=self.push()

    def make_clean(self):

        ##print("Now i'm cleaning the old build")


        #subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'my_package'])
        result = subprocess.run(['jupyter-book', 'clean', 'jupyter-book'], capture_output=True, text=True)
        print(result.stdout)
        print(result.stderr)

        ##print("ClEAN")

        return result


    def make_html(self):
        ##print("Making dE HTML BUIld")
        #subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'my_package'])
        result = subprocess.run(['jupyter-book', 'build', 'jupyter-book'], capture_output=True, text=True)
        print(result.stdout)
        print(result.stderr)
        ##print("i make it")

        return result

    def commit(self):
        time_stamp=utility_functions.timestamp()
        ##print("commiting !!!")


        #subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'my_package'])
        result = subprocess.run(['git', 'commit', '-m', 'autocommit on' + time_stamp], capture_output=True, text=True)
        ##print("Output")

        print(result.stdout)
        ##print("Errors")

        print(result.stderr)


        ##print("committed")
        return result


    def push(self):
        time_stamp=utility_functions.timestamp()
        ##print("PUshing")
        #subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'my_package'])
        result = subprocess.run(['git', 'push'], capture_output=True, text=True)
        ##print("Output")

        print(result.stdout)
        ##print("Errors")

        print(result.stderr)


        ##print("pushed it")

        return result


    def add(self):

        ##print("Adding CHanges!!!")


        #subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'my_package'])
        result = subprocess.run(['git', 'add', '.'], capture_output=True, text=True)
        ##print("Output")

        print(result.stdout)
        ##print("Errors")

        print(result.stderr)


        ##print("changes added")

        return result


class deploy_pipeline:

    def __init__(self,cname):
        self.deploy_log = self.deploy(cname)

    def deploy(self,cname):

        ##print("DEPLOYING!!!")


        #subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'my_package'])
        result = subprocess.run(['ghp-import', '-n', '-p', '-f', '-c', cname, '_build/html' ], capture_output=True, text=True)
        ##print("Output")

        print(result.stdout)
        ##print("Errors")

        print(result.stderr)


        ##print("i deployz it")
        print('your site is live at ' + cname)

        return result



def introduction():
    print("INstalling Depenedencies")
    print("B4 we begin")
    print("you Should read the requirments.txt file")
    print("If you don't trust me press ctr-c now to stop this program.   Then, read the file. I'm giving you 15 seconds to think this through")
    sleep(2)

def command():
    result = subprocess.run(['ls', '-l'], capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)



class utility_functions:

    def thinking():
        think = '-------------'
        i=0
        j=0
        end=randrange(3,9)
        think = think
        #sleep(10)
        ##print(think)


    def timestamp():
        dt = datetime.now()
        ts = datetime.timestamp(dt)
        ts = str(ts)
        return ts

    def seperator():
        seperator = '-------------'
        sep = seperator
        #sleep(10)
        ##print(sep)




def main():
    conf = config()
    introduction()
    #install_dependencies()
    #dependency_log = dependency_pipeline()
    build_log = build_pipeline()
    deploy_log = deploy_pipeline(conf.cname)


if __name__ == "__main__":
    main()
