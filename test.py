# coding=utf-8
# method River
import re #正则
import xlwt #excel生成
import os 
import math
from decimal import getcontext, Decimal

def foo(fileName):
    #fileName = 'new'
    file = open("./" + fileName+'.txt', 'r')
    arr = []
    for line in file.readlines()[7:]:
        line = line.strip()
        # fields=re.split(r'\s+',line)
        temp = re.split(r'\s+', line)
        arr.append(list(temp))
        #print("读取的数据为: %s" % (line))
    file.close()
    new_arr=[]
    i=0
    for i in range(len(arr)):
    	temp=[]
    	temp.append(arr[i][5])
    	temp.append(arr[i][6])
    	temp.append(arr[i][9])
    	new_arr.append(temp)
    return new_arr


def  electric_processing(data):
	num=0
	result=[]
	temp=0
	for i in range(len(data)):
		res=[]
		if(num<3):
			temp=temp+float(data[i][2])
			num=num+1
			if(num==3):
				if(float(data[i][2])<=0):
					break
				temp=math.log10(temp)
				temp = Decimal(temp).quantize(Decimal('0.00'))
				res.append(data[i-2][0])
				res.append(4)
				res.append(float(temp))
				result.append(res)
				num=0
				temp=0
	temp_start=result[0].copy()
	temp_stop=result[len(result)-1].copy()
	for i in [1,7]:
		temp_start[1]=i
		result.append(temp_start.copy())
		temp_stop[1]=i
		result.append(temp_stop.copy())
	return result






fileName = input('请输入文件名:')
data = foo(fileName)
#结果result
result=electric_processing(data)

#生成.dat文件
res_file=open(''+fileName+'.dat','w')
for i in range(len(result)):
	res_file.write(str(result[i][0])+','+str(result[i][1])+','+str(result[i][2])+'\r\n')

print('已生成'+fileName+'.dat文件!')
print('')
print('')
print('')
input('按任意键退出....')