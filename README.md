## End-to-end setup for a capture data in API MARVEL to mySQL <h1>

![image](https://user-images.githubusercontent.com/119074041/204691806-3c3043eb-066b-4ff6-9264-3361d3cf99ca.png)

### Important <h3>
#### it's necessary to create an .env file in the root (marvel_project/) of the project with the following keys: <h4>
* DB_PASSWORD=yourpassword
* DB_USER=root
* APIKEY=yourkeyapi
* HASH=yourhash
* MD5HASH=yourmd5hash
* DB_HOST=mysql
  
  
### Requirements <h3>
+ Linux/MacOS
+ Docker
+ Python 3
+ MYSQL

### Folder Structure <h3>
 * marvel_project/ - contains docker-compose, dockerfile(img python) and requierements. (important file .env above mentioned)
 * marvel_project/db/ - contains dockerfile (img mysql) and database_dbmrv.sql (queries run on starting)
 * marvel_project/src/ - API server code
  
  
  
### Development Dependencies <h3>
#### The file requierements in the repo contains: <h4>
+ SQLAlchemy
+ mysql
+ mysql-connector-python
+ mysqlclient
+ pandas
+ requests
#### requirements are contained and running in docker<h4>
  
### future developments <h3>
* apply concept SOLID
* apply design patterns

