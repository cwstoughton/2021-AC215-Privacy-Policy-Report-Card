AC215-Privacy Policy Report Card
==============================

AC215 Fall 2021

Project Description
------------

The goal of this project is to build an application that will allow users to enter
the URL of a privacy policy, and receive a "report card" explaining which categories
of user data the application collects and shares.


Design Overview
------------

When a user submits a privacy policy to be graded, the app needs to take a number of steps to evaluate it
1. The front end accepts the user's input
    - The React front end takes the url as input, and passes it to an API running as a separate microservice
2. The API receives the URL request and passes it to the backend inference engine
3. The inference engine incorporates elements of the training data pipeline to fetch and parse the text of the privacy policy
4. The inference engine passes the encoded privacy policy to the model for inference
   - Our model is designed to detect the presence of language that indicates the collection of certain user data.
     It does this for each paragraph of the policy. Because a given paragraph may contain any combination of trackers,
     we have created a custom ensemble model to detect each tracker type as a binary response variable. 
4. The model completes its inferences and passes the result as a dictionary back to the API
5. The API returns model inferences as a JSON to the frontend.
6. The front end renders the model's output for the user to review


Project Organization and Key Components
------------

- Data : Stores raw training data

- Pipeline: Stores files for processing raw data into training sets                                             
    - Create_Unlabeled_Dataset.py -> scrapes the web for fine-tuning data                
    - Labeled_Data_Pipeline.py -> parses raw training data from APP350 into dataframe    
    - Training_Data_Pipeline.py -> encodes text data for training                        
- models: contains files for training and generating models  

- Demo: Contains files for the prototype and demo backend                                            
    - demo_app.py -> API to serve model inferences                                          
    - demo_model_builder.py -> functions for inference model building                       
    - demo_inference_backend.py -> builds ensemble model using Demo_Model_Weights           
                                                                                                   
- Demo_frontend:Contains files for the prototype and demo react frontend
    - Todos.jsx -> functions for handling API calls                        
    - App.js -> structure of the app


      .
      ├── LICENSE
      ├── Makefile
      ├── README.md
      ├── models
      ├── notebooks
      │   ├── Fine Tuning Experiments
      ├── Pipeline
      │   ├── Labeled_Data_Pipeline.py #Creates training data from APP350 Dataset
      │   ├── Create_Unlabeled_Dataset.py #Creates fine-tuning data via web-scraping
      │   ├── Training_Data_Piepline.py #Encodes text data for training
      ├── Demo # conains files for the backend prototype and demo
      │   ├── 
      ├── Demo_Frontend #conains files for the frontend prototype and demo
      │   ├── Fine Tuning Experiments
      ├── notebooks
      │   ├── Fine Tuning Experiments
      ├── references
      ├── requirements.txt
      ├── setup.py
      ├── src
      │   ├── __init__.py
      │   └── build_features.py
      ├── submissions
      │   ├── milestone1_groupname
      │   ├── milestone2_groupname
      └── test_project.py
--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>

