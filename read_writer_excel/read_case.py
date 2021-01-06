import os

class Read_case:

    def __init__(self):
        path =os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.case_path = os.path.join(path,'case')
        #print(self.case_path)
    def all_file(self):
        fileList = os.listdir(self.case_path)
        num = []
        dic={}
        # print(fileList)
        for file_m in fileList:
            path_nu=file_m.split('_')
            num.append(path_nu[-1])
            # print(file_m)
        x=0
        for i in num:
            dic[i]=fileList[x]
            x+=1
        num.sort()
        case_list = []
        for i in num:
            path_name = os.path.join(self.case_path,dic[i])
            case_list.append(path_name)
        # print(case_list)
        return case_list




if __name__ == "__main__":
    a = Read_case()
    a.all_file()