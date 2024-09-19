# titanic MLOps Project

This repo holds the code for a deployment of a Machine Learning model based on the Titanic competition.

### Data Flow

As a user requires predictions from our model the endpoint returns a JSON with the predicted values for the given entries.
These, along with the processed features are then stored in the Feature Store and Prediction Tables as part of a database.

Initially, we are only writing the predictions in a SQLite database, which is portable as part of a Python deployment.

The API was tested locally using Postman and the JSON files in the local directory. Further test automation for this part should be included.

## Challenges

- The hardest part has been to think about the database interaction. Moving away from my familiarit
- I found it very challenging to try and separate the components of the API along with the database.
- The model selected for deployment made it hard to think about scalability since it is a static problem from which we cannot get mor data for improvement of the model.
- I am also unfamiliar with API deployment and proper testing. I have mostly built multiple batch jobs which are "easier" and do not require as much maintenance
- Understanding the Git Workflow, other than simply creating the branches to add pieces of the application. I need to understand better the whole purpose of having a set workflow and building from it.
- I have no familiarity with SonarCloud so within the timeframe I prioritized having a working endpoint.

## Potential Problems

I am aware this is not the optimal solution for such deployment since there are multiple pitfalls:

- Latency: the API request should wait or depend on the data warehouse transactions to happen or be successful. Further modularization of such components would be ideal
- Not Fault Tolerant: Since these parts are all within the same API call, we do need to better handle the connections to the Feature Store or Data Warehouse, as it makes this API a bad abstraction of a batch job.
- The current deployed model was trained locally, and it is not a service/model that could improve as there will not be new data


## To Do's

- Setup CI/CD.
- Add more tests (unit, integration, system)
- Integrate monitoring



[//]: # (## Cloud Architecture &#40;ToDo&#41;)

[//]: # ()
[//]: # (The suggested cloud architecture to host this and whichever other model could be as follows:)

[//]: # ()
[//]: # (![MLOps Cloud Architecture]&#40;TitanicMLOps.drawio.png&#41;)

[//]: # ()
[//]: # (1. It is a simple API deployment architecture which exploits SageMaker Serverless from AWS to host the model and open the endpoint to make inference. )

[//]: # (2. As a backend Feature Store or Cloud Data Warehouse solution we use Redshift, since we are also relying on underlying ETLs for creating features for later training and inference.)

[//]: # (3. We also include ECS to help us handle the Docker containers. **Note:** As far as I understand this is not really needed if using SageMaker &#40;but not sure&#41;.)

[//]: # (4. To feed the feature store we will load our raw data onto S3 and we'll manage the pipelines using AWS's native Airflow managed service.)
