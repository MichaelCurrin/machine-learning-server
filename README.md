# Machine Learning Server
>Classify images using a trained machine learning model and Python web server API. 

_Author: Michael Currin_

![Deep Learning Workshops logo](mlserver/static/img/Deep_Learning_Workshops_logo.png)

## About

I give a talk on how to a productionise a machine learning service in a web server, as part of [Deep Learning Workshops](https://deeplearningworkshops.com) in Cape Town. This project contains the code and instructions needed to setup one's own local prediction service and is intended as additional material for anyone attending the workshops or with an interest in this topic.

Some of the concepts and approaches I discuss in my talk are for scaling a service deployed to production. However, this project only is a simplified version of such a predictions service, with some infrastructure removed. Since this is only expected to be run locally and so that the main logic is clearer to follow.

## Documentation

- [Installation instructions](docs/installation.md)
- [Usage instructions](docs/usage.md) for starting the web app and uploading the project's [sample images](/sampleIages) to the server
- [Custom Models](docs/customModels.md) for optionally dropping in a user-trained model
- [API endpoints](docs/api.md)

Note that this project was written and tested on a Linux environment using Python 3.6.
