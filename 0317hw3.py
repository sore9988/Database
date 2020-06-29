import pymysql
import os
import prettytable

link=pymysql.connect(
	host="localhost",
	user="root",
	passwd="",
	db="2020-03-13",
	charset="utf8",
	port=3306
	)
c=link.cursor()
def getdata():
	c.execute("SELECT `A`.`編號`,`A`.`姓名`,`A`.`生日`,`A`.`地址`,`B`.`tel` \
		FROM `members` AS `A` LEFT JOIN `phone` AS `B` ON `A`.`編號`=`B`.`member_id` order by `A`.`編號` asc")
	x = c.fetchall()
	# print(x[0][0])
	for i in range(c.rowcount):
		if x[i][0]==x[i-1][0] and i>1:
			p.add_row(["", "", "","",x[i][4]])
		else:
			p.add_row(x[i])
	print(p)
os.system("cls")
o = -1	
while o != "0":
	p = prettytable.PrettyTable([" 編號 ", " 姓名 ", " 生日 ", " 地址 ", "電話"], encoding = "utf-8")
	if o == "0":
		os.system("cls")
	elif o == "1":
		getdata()
	elif o == "2":
		name = input("請輸入姓名:")
		birth = input("請輸入生日:")
		address = input("請輸入地址:")
		c.execute("INSERT INTO `members` (`姓名`,`生日`,`地址`) VALUES(%s,%s,%s)", (name, birth, address))
		link.commit()
		os.system("cls")
	elif o == "3":
		getdata()
		n = input("請輸入編號:")
		name = input("請輸入姓名:")
		birth = input("請輸入生日:")
		address = input("請輸入地址:")
		c.execute("UPDATE `members` SET `姓名`=%s, `生日`=%s, `地址`=%s WHERE `編號`=%s", (name, birth, address, n))
		link.commit()
		os.system("cls")
	elif o == "4":
		getdata()
		n = input("請輸入刪除編號:")
		c.execute("DELETE FROM `members` WHERE `編號`=%s", n)
		link.commit()
		os.system("cls")
	elif o == "5":
		getdata()
		n = input("請輸入要添加電話的編號:")
		number = input("請輸入電話號碼:")
		c.execute("INSERT INTO `phone`(`member_id`, `tel`) VALUES (%s,%s)", (n, number))
		link.commit()
		os.system("cls")
	elif o == "6":
		getdata()
		n = input("請輸入刪除編號:")
		c2=link.cursor()
		c2.execute("SELECT `id`,`tel` FROM `phone` WHERE `member_id`=%s", n )
		x = c2.fetchall()
		p2 = prettytable.PrettyTable([" 編號 ", "電話"], encoding = "utf-8")
		for i in range(c2.rowcount):
			p2.add_row(x[i])
		print(p2)
		num = input("請輸入刪除電話編號:")
		c2.execute("DELETE FROM `phone` WHERE `id`=%s", num)
		link.commit()
		os.system("cls")
	print("(0) 離開程式\n(1) 顯示會員資料\n(2) 新增會員資料\n(3) 更新會員資料\n(4) 刪除會員資料\n(5) 新增會員電話\n(6) 刪除會員電話")
	o = input("請選擇指令:")
	os.system("cls")
link.close()

