#! /bin/bash
#目标机器 10.237.41.100

user=root # 数据库用户
pass=root # 用户密码
socket=/home/work/data/tmp/mysql3308.sock  # 多实例sock文件地址
#IP=$1	  #目标机器IP
#MYDUMP="/home/work/app/mysql/bin/mysqldump -t --default-character-set=utf8  -h${IP} -P3308 -u${user} -p${pass} --databases" # mysqldump连接

MYDUMP="/home/work/app/mysql/bin/mysqldump -t --default-character-set=utf8 -S ${socket} -u${user} -p${pass} --databases" # mysqldump连接

#备份时间
LOCALTM=`date +"%Y%m%d"`

#备份基础路径
BASEDIR=/home/work/backup

#初始化基础表

declare -A map=()

map["wms3"]="xm_wms3 --tables xm_admin_user xm_admin_user_mihome xm_mihome xm_wms3_auth_assignment xm_wms3_auth_item xm_wms3_auth_item_child xm_wms3_auth_rule "  
map["xm_wps"]="xm_wps --tables xm_admin_user xm_admin_user_mihome xm_auth_assignment xm_auth_item xm_auth_item_child xm_auth_rule xm_authassignment xm_authitem xm_authitemchild "
map["xm_notify"]="xm_notify --tables  authassignment  authitem  authitemchild  sequence  testlenght  xm_admin_user  xm_biz  xm_biz_enable  xm_biz_recive  xm_biz_type  xm_count_msg_num  xm_errdecode_msg  xm_msg_count  xm_recive"
map["xm_buy_n"]="xm_buy_n  --tables authassignment authitem authitemchild xm_auth_assignment xm_auth_assignment_category xm_auth_item xm_auth_item_child xm_customer_account xm_customer_account_apply xm_department_level xm_department xm_department_usage xm_user xm_user_auth xm_user_group"
map["xm_pss_dev"]="xm_pss_dev --tables xm_admin_department xm_admin_user xm_authassignment xm_authitem xm_authitemchild"
map["xm_cs"]="xm_cs --tables xm_admin_department xm_admin_group xm_admin_user xm_auth_assignment xm_auth_item xm_auth_item_child"
map["xm_wp"]="xm_wp --tables  xm_admin_department xm_admin_user xm_authassignment xm_authitem xm_authitemchild"





#定义MySQL本地备份路径
BAKDIR=${BASEDIR}/${LOCALTM}/   # 保存的文件地址
if [ ! -d $BAKDIR ];then
	mkdir -p $BAKDIR
fi


#备份数据库数据
for key in ${!map[@]}  
do  
	echo ${key}  
	${MYDUMP} ${map[$key]} >  "${BAKDIR}${key}".sql
done  

	
##压缩当天备份sql文件
cd ${BASEDIR}
echo pwd
tar cvf  ${LOCALTM}_data.tar  ./${LOCALTM}





