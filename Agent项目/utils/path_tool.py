

'''
为整个工程提供统一的绝对路径
'''
import os

#获取工程根目录
def get_project_root() ->str:
    current_file=os.path.abspath(__file__)#获取当前文件的绝对路径
    current_dir = os.path.dirname(current_file)#获取文件夹的绝对路径
    project_root = os.path.dirname(current_dir)# 获取工程的根目录
    return project_root

# 传入相对路径，输出绝对路径
def get_abs_path(relative_path:str)->str:
    project_root = get_project_root()
    return os.path.join(project_root,relative_path)

if __name__ == '__main__':
    x=get_abs_path('config/hhh.txt')
    print(x)