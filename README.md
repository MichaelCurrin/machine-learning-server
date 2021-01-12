# Machine Learning Server
>Classify images using a trained machine learning model and Python web server API. 

_Author: Michael Currin_

![Deep Learning Workshops logo](mlserver/static/img/Deep_Learning_Workshops_logo.png)

The purpose of this application is to provide a predictions service (whether through the command-line or browser) which can receive an image and then return either:
- probable color labels and confidence scores at a co-ordinate point, classifying with labels such as those in [colors.txt](mlserver/models/builtinColorClassifier/colors.txt).
- provide digit labels and confidence scores for an image of a handwritten digit, using labels like these: [digits.txt](mlserver/models/builtinDigitClassifier/digits.txt). The MNIST dataset was used for training.


## Note

This project is not actively maintained. There are more elegant and modern ways to achieve what is done here and also more interesting that this. I am only going to update dependencies for security vulnerabilities.


## Background

As part of [Deep Learning Workshops](https://deeplearningworkshops.com) in Cape Town, I give a talk on how to a productionise a machine learning service in a web server. This project contains the code and instructions needed to setup one's own local prediction service and is intended as additional material for anyone attending the workshops or with an interest in this topic.  

Some of the concepts and approaches I discuss in my talk are for scaling a service deployed to production. However, this project only is a simplified version of such a predictions service, with some infrastructure removed. Since this is only expected to be run locally and so that the main logic is clearer to follow.


## Documentation

- [Installation instructions](docs/installation.md)
- [Usage instructions](docs/usage.md) for starting the web app and uploading the project's [sample images](sampleImages/) to the server
- [Custom Models](docs/customModels.md) for optionally dropping in a user-trained model
- [API endpoints](docs/api.md)

Note that this project was written and tested on a Linux environment using Python 3.6.
