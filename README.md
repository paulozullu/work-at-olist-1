# Work at Olist

## Description
This API returns monthly bills for a telephone number. These bills has a list of calls, and each call has a start call and an end call object. 

## Installation
To install this project, plese follow steps below:

1. Install virtualenv
    ```
    sudo pip install virtualenv
    ```
    
2. Clone this project
    ```
    git clone https://github.com/paulozullu/work-at-olist-1.git
    ```
    
3. Inside the created folder (**work-at-olist-1**), run the command above to create the virtual environment
    ```
    virtualenv -p python3 envname
    ```
    
4. Activate the new virtual environment
    ```
    virtualenv envname/bin/activate
    ```
    
5. Install dependencies
   ```
   pip install -r requirements.txt
   ```
   
 6. Create database
    ```
    python manage.py migrate
    ```
##Testing
Access the project folder and run
```
python manage.py test
```

##Work Environment

### PC Specs (Asus K46CA):
- Processor: Intel Core I7-3517U 
- RAM: 8Gb
- SSD: 24Gb
- HD: 1Tb

### SO:
- KDE Neon 5.13 (16.04 LTS)
- Plasma 5.13.3

### Development IDE:
- PyCharm 2018.2 (Community Edition)
Build #PC-182.3684.100, built on July 24, 2018

##API Documentation
To access the API Documentation, follow [this link](https://olist-calls.herokuapp.com/docs/)