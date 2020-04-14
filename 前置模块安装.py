import os
print("检测前置中")

def import_park(name):
    try:
        exec("import "+name)
        print(name+'成功导入')
    except:
        print("缺少前置{}，正在下载补全".format(name))
        os.system("pip install "+name)

pack_list=['json','lxml','requests','urllib','easygui']
for i in pack_list:
    import_park(i)
print("前置检测完成")
