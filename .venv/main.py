#abdallah kokash---1220116
import os
import json
import csv
import logging
import argparse


class commandExecuter:
    def __init__(self, threshold):
        self.threshold = int(threshold.replace('KB', '')) * 1024

    def Mv_last(self, src_directory, des_directory):
        if not os.path.exists(src_directory):
            return -5
        if  not os.path.isdir(src_directory) or not os.path.isdir(des_directory):
            return -5
        list = os.listdir(src_directory)
        list_of_files = [f for f in list if os.path.isfile(os.path.join(src_directory, f))]
        if not list_of_files:
            return -5
        full_path = [os.path.join(src_directory, i) for i in list_of_files]
        latest_file = max(full_path, key=os.path.getctime)
        if not os.path.exists(des_directory):
            os.makedirs(des_directory)
        destination = os.path.join(des_directory, os.path.basename(latest_file))
        os.replace(latest_file, destination)
        return -1

    def Categorize(self, directory):
        if not os.path.exists(directory):
            return -5
        if not os.path.isdir(directory):
            return -5
        try:
            os.makedirs(os.path.join(directory, 'SmallerThanThreshold'))
            os.makedirs(os.path.join(directory, 'LargerThanThreshold'))
        except:
            pass
        list = os.listdir(directory)
        list_of_files = [f for f in list if os.path.isfile(os.path.join(directory, f))]
        full_path = [os.path.join(directory, i) for i in list_of_files]
        for i in full_path:
            if os.stat(i).st_size >= self.threshold:
                os.replace(i, os.path.join(directory, 'LargerThanThreshold', os.path.basename(i)))
            else:
                os.replace(i, os.path.join(directory, 'SmallerThanThreshold', os.path.basename(i)))
        return -1

    def Count(self, directory):
        if not os.path.exists(directory):
            return -5
        if not os.path.isdir(directory):
            return -5
        list = os.listdir(directory)
        lsit_of_files = [f for f in list if os.path.isfile(os.path.join(directory, f))]
        return len(lsit_of_files)

    def Delete(self, file, directory):
        if not os.path.exists(os.path.join(directory, file)):
            return -5
        if not os.path.isdir(directory) or not os.path.isfile(os.path.join(directory, file)):
            return -5
        os.remove(os.path.join(directory, file))
        return -1

    def Rename(self, old_name, new_name, directory):
        if not os.path.exists(os.path.join(directory, old_name)):
            return -5
        if not os.path.isdir(directory) or not os.path.isfile(os.path.join(directory,old_name)):
            return -5
        os.rename(os.path.join(directory, old_name), os.path.join(directory, new_name))
        return -1

    def List(self, directory):
        if not os.path.exists(directory):
            return -5
        if not os.path.isdir(directory):
            return -5
        return os.listdir(directory)

    def Sort(self, directory, criteria):
        if not os.path.exists(directory):
            return -5
        if not os.path.isdir(directory):
            return -5
        list = os.listdir(directory)
        list_of_files = [f for f in list if os.path.isfile(os.path.join(directory, f))]
        if criteria == 'name':
            list_of_files.sort()
        elif criteria == 'size':
            list_of_files.sort(key=lambda x: os.path.getsize(os.path.join(directory, x)))
        elif criteria == 'date':
            list_of_files.sort(key=lambda x: os.path.getctime(os.path.join(directory, x)))
        else:
            return -5
        return list_of_files


class scriptExecuter:
    commandNumber=1
    def __init__(self, configuration):
        self.configuration = configuration
        self.commandExecuter = commandExecuter(self.configuration['Threshold_size'])
        self.results=[]
        logging.basicConfig(filename='commandDebugger.log',level=logging.DEBUG,format='%(asctime)s - %(levelname)s - %(message)s')

    def readFile(self, file_path):
        file = open(file_path, 'r')
        count = 0
        command = []
        for line in file:
            if count >= self.configuration['Max_commands']:
                break
            command.append(line)
            count += 1
        file.close()
        return command

    def execute(self, command):
        parts = command.strip().split(' ')
        function = parts[0]
        args = parts[1:]
        if function == 'Mv_last':
            result = self.commandExecuter.Mv_last(args[0][1:-1], args[1][1:-1])
            self.results.append(result)
        elif function == 'Categorize':
            result = self.commandExecuter.Categorize(args[0][1:-1])
            self.results.append(result)
        elif function == 'Count':
            result = self.commandExecuter.Count(args[0][1:-1])
            self. results.append(result)
        elif function == 'Delete':
            result = self.commandExecuter.Delete(args[0][1:-1], args[1][1:-1])
            self.results.append(result)
        elif function == 'Rename':
            result = self.commandExecuter.Rename(args[0][1:-1], args[1][1:-1], args[2][1:-1])
            self.results.append(result)
        elif function == 'List':
            result = self.commandExecuter.List(args[0][1:-1])
            self.results.append(result)
        elif function == 'Sort':
            result = self.commandExecuter.Sort(args[0][1:-1], args[1][1:-1])
            self.results.append(result)
        else:
            result =-10
            self.results.append(0)
        logging.info("-------------------------------------------------------------")
        logging.info('this is command number # %d '%(scriptExecuter.commandNumber))
        logging.info('this is a %s command'%(function))
        if result == -5:
            logging.debug("path was not found")
            logging.info('%s function Faild'%(function))
        elif result == -10:
            logging.debug('%s function does not exist'%(function))
            logging.info('%s function faild'%(function))
        else:
            logging.debug("path was found")
            logging.info('%s function was successful'% (function))
        scriptExecuter.commandNumber += 1
        return result

    def writeOutputHelper(self, store_file):
        if not os.path.exists(store_file):
            os.makedirs(os.path.join(store_file, 'passed'))
            os.makedirs(os.path.join(store_file, 'Failed'))
        outputFile = 'C:\\Users\\OC\\Desktop\\pythonProject\\.venv\\%s' % (store_file)
        if self.configuration['Same_dir'] != True:
            for i in self.results:
                if i == -10 or i == -5:
                    outputFile = 'C:\\Users\\OC\\Desktop\\pythonProject\\.venv\\%s\\Failed' % (store_file)
                    break
                else:
                    outputFile = 'C:\\Users\\OC\\Desktop\\pythonProject\\.venv\\%s\\passed' % (store_file)
        list = os.listdir(outputFile)
        list_of_files = [f for f in list if os.path.isfile(os.path.join(outputFile, f))]
        full_path = [os.path.join(outputFile, i) for i in list_of_files]
        if len(list_of_files) > self.configuration['Max_log_files'] - 1:
            oldest_file = min(full_path, key=os.path.getctime)
            os.remove(oldest_file)
        return outputFile

    def writeOutput(self, outputFile):
        if self.configuration['Output'] == 'csv':
            num = 0
            with open("csv.txt", 'r') as csvNum:
                num = csvNum.read()
            csv_file = open(os.path.join(outputFile, 'output%s.csv' % (num)), 'w')
            fieldNames = ["line", "status"]
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldNames)
            count = 1
            for i in self.results:
                if i == -10 or i == -5:
                    csv_writer.writerow({"line": 'line-%d' % (count), "status": "faild"})
                elif i == -1:
                    csv_writer.writerow({"line": 'line-%d' % (count), "status": "success"})
                else:
                    csv_writer.writerow({"line": 'line-%d' % (count), "status": "success"})
                    print(i)
                count += 1
            with open("csv.txt", 'w') as csvNum:
                num = int(num, 10)
                num = num + 1
                num = str(num)
                csvNum.write(num)
        else:
            num = 0
            with open("log.txt", 'r') as logNum:
                num = logNum.read()
            log_file = os.path.join(outputFile, 'output%s.log' % (num))
            for handler in logging.root.handlers[:]:
                logging.root.removeHandler(handler)
            logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(levelname)s - %(message)s')
            count = 1
            for i in self.results:
                if i == -5 or i == -10:
                    logging.info('line-%d---faild' % (count))
                elif i == -1:
                    logging.info('line-%d---success' % (count))
                else:
                    logging.info('line-%d---success' % (count))
                    print(i)
                count += 1
            with open("log.txt", 'w') as logNum:
                num = int(num, 10)
                num = num + 1
                num = str(num)
                logNum.write(num)

def main():
    parser = argparse.ArgumentParser(description="Script Executor")
    parser.add_argument('-i', '--input', required=True, help="Input script file")
    parser.add_argument('-o','--output', required=True, help="Output file name")
    args = parser.parse_args()
    with open("configuration.json", 'r') as configFile:
        configuration = json.load(configFile)
    exuter = scriptExecuter(configuration)
    commands=exuter.readFile(args.input)
    for command in commands:
        exuter.execute(command)
    loc=exuter.writeOutputHelper(args.output)
    exuter.writeOutput(loc)
if __name__ == '__main__':
    main()

#yess
