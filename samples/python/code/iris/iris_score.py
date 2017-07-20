# Init function is called when the container is initialized
def init():
    import pickle
    # Load the model from disk
    f = open('model.pkl', 'rb')
    global model
    model = pickle.load(f)


# This function is invoked when the web service is called with a prediction request
def run(input_data):
    import numpy
    import json
    # Decode the json input
    json_string = json.loads(input_data)
    # Convert string input to float
    input1 = numpy.fromstring(json_string, dtype=float, sep=',').reshape((1, 4))
    # Predict
    score = model.predict(input1)
    # Return json response
    return json.dumps(int(score[0]))
