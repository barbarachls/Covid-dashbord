# Introduction
This is a COVID-19 dashboard. It displays the different data related to 
coronavirus and a list of 5 articles also related to the coronavirus. The 
news and the data can be updated at a scheduled time by the user.The user 
can delete any news articles they don't want to see again, they can also 
cancel any update.

#Requirement

Use python 3.9 or over

To use the Dashboard you first need to install in the command window:
* pip install uk-covid19
* pip install flask
* pip install requests
 

#How to use it

You first need to run the main.py module. Then open http://127.0.0.1:5000/index
in your browser.

There is a configuration file called config.json. To change the location  of 
the data, it will be needed to change it in the file. by default the nation 
location is England and the city location is Exeter.

You will need your own **API key**, For that go to https://newsapi.org/ and 
generate you own key. You will then need to change the configuration file 
and replace 'your API key' with yours.

#Testing
To test the different module/function of this project, Pytest needs to be 
installed.

* pip install pytest

###Details

**_Project used for demonstration_**

Author - Barbara Charles

index.html file Author - Matt Collison
