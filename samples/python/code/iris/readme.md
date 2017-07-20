# Iris sample
The following sample will train and save a model using the Iris dataset. We will then use the saved the model to deploy it as a web service.

Steps:
1. Set up your environment
2. Create web service
3. Run web service

Call the setup command from the command line to create your environment if not already done.

- az ml env setup 

Create the web service

- az ml service create realtime -f iris_score.py --model-file model.pkl --model-name irismodel1 -n irisservice1 -r scikit-py

Run the service

- az ml service run realtime -n irisservice1 -d "\\"3.4,4.2,5.1,3.1\\""

See troubleshooting see the troubleshooting guide.
