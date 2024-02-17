# Kanban_Board
# MAD-2 PROJECT--- KANBAN APP

------------------------------------------


## About Kanban app

  - This app is very similar to kanban board, just like how we can
	have various tasks on kanban board, similarly a user can have 
	different lists of tasks in this app.

  - Users can create their accounts on the app, can create various
	lists of tasks.

  - Users can also set deadline for various tasks.

  - Users can perform CRUD(create, read, update, delete) operations
    on the lists and their tasks.

------------------------------------------

## Technologies required

  - FOR BACK END : Python, Flask, Flask-sqlalchemy, flask_restful, flask-security-too,
                    bcrypt, flask-cors, Flask-caching, Redis, Celery, Mailhog, pdfkit
  
  - FOR FRONT END : Vue , Javascript, Vue-Bootstrap, Vue-chart js.  

------------------------------------------


## How to run the app
  
   - First of all to install all the dependencies, go the main app folder in
    the terminal and run the command--
         ```
         pip3 install -r requirements.txt
         ```

   - There are multiple servers that are needed to be setup before running the app

  1. **Setting up the flask server :**

        - Just go to the main app folder in your terminal and run the command--

           ```
           Python3 main.py
          ```

  2. **Setting up the redis server :**

        - go to the main app folder in your terminal and run the command--

          ```
           redis-server         
          ``` 

  3. **Running the celery workers and celery beat :**

        - go to the main app folder in your terminal and run the following command--
          for celery workers
          
          ```
           celery -A main.celery worker -l info        
          ```        
        - for celery beat run the command--

          ```
            celery -A main.celery beat --max-interval 1 -l info        
          ```

  4. **Running the vue app on server :**
  
        - finally to run the main vue app go the folder frontend/index.html inside
          root folder run the index.html file on a http server. 
