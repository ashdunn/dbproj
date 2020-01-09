# Speech Recognition for Instacart Database Queries

This application allows you to use speech recognition to execute queries on the Instacart MySQL database.

### Application on Startup
![Image description](https://lh5.googleusercontent.com/DqLsVccQpZl3xEwFXwPfEbEK-R9D7mhLmsriDeLFFfrXCrEdvsZ8f7tfMpZMucFyaHJI7oj2EWJb3s46xfzHkqnrL7L-EQft4hp2gMfA0jNthE3K4tpgPrEp8PnYPt0LjEe7Mjr05XQ)

### Simple Query
[![Simple Query](https://drive.google.com/uc?export=view&id=1UIzw9FdSs9Bnwi0j7NNemeuRKMLAvwvU)](https://drive.google.com/file/d/1JJdUxGdmFKOq8bYv_-Hx-wRX4rS9jRUc/view?usp=sharing)

### More Complex Query
[![More Complex Query](https://drive.google.com/uc?export=view&id=11KsfGakZzdyPib2Ry9i2XQSPEA0dIkjG)](https://drive.google.com/file/d/1AGdSJOvvMwBRMo7lDEszzzNRwivpgYdh/view?usp=sharing)

### Error Handling - MySQL Error displayed on application
![Image description](https://lh3.googleusercontent.com/8dMtM-nnXzR1Nh4zHhxeyz_dLxDHJ3VnxnL6f25TAJzv87gy7qGsTgGwT8udZUaxWXGKREZ-Sj8o2g2fOZ3jm_ggrfoFisF3QURjFGNC=s1600)



## Getting Started

clone the project:
```
git@github.com:ashdunn/dbproj
```

```
cd dbproj
```

```
python3 alexa.py
```

### Input
 * Spoken MySQL query
 * Must verbalize symbols: comma, quote, space (within quotes only), open/close parenthesis, percent sign
### Output
 * Results of query as a table in new window
 * Title of window is query and number of rows in result set


### Prerequisites

* python3
* pyaudio
* tkinter
* speech_recognition
* pillow
* Local MySQL Instacart Database

## Authors

* **Ashley Dunn**

* **Rachel George**
