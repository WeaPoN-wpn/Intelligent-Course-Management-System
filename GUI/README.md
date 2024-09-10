## To Use This GUI

### 1. create the database 
```sql
mysql -u root -p  
-- input ur password  
create databse sample_data;  
source user_password.sql;  
INSERT INTO user (id, username, password) VALUES (1,'vfzzz', '123456');  
```
### 2. use main_page.py
change your mysql server username, password in line 6  

```python
myconn = mysql.connector.connect(host="localhost", user="xxx", passwd="xxxxx", database="sample_data")
