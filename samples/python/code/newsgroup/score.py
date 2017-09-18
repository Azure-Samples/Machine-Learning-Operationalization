# Score.py file
# Must be included when deploying the model using the Azure ML CLIs
# Requires init and run functions to be defined.
# Run this file "python score.py" to generate a schema for the web service

def init():
    from sklearn.externals import joblib
    # load the saved model file
    global model
    model = joblib.load('model.pkl')

def run(doc_text):
    #Load the library 
    from sklearn.datasets import fetch_20newsgroups
    
    #Load the same categories as used in training sample
    categories = ['comp.graphics', 'rec.autos','sci.med', 'misc.forsale']
    #Load the newsgroups from data folder
    twenty_train = fetch_20newsgroups(data_home='./data',subset='train',categories=categories, shuffle=True, random_state=42)
    
    doc_input = [doc_text]
    predicted_category = ''
    
    #Get prediction using the loaded model
    predicted = model.predict(doc_input)
    
    #Get the category
    for doc, category in zip(doc_input, predicted):
        predicted_category = twenty_train.target_names[category]

    # Return the result
    return predicted_category

def main():
    # Load the Azure ML libraries to generate a schema
    from azureml.api.schema.dataTypes import DataTypes
    from azureml.api.schema.sampleDefinition import SampleDefinition
    from azureml.api.realtime.services import generate_schema
    
    # Test the init and run functions using test data
    test_doc_text = "SUVs are very popular"
    init()
    category = run(test_doc_text)
    print(category)

    # Generate the schema file (schema.json)
    inputs = {"doc_text": SampleDefinition(DataTypes.STANDARD, test_doc_text)}
    generate_schema(run_func=run, inputs=inputs, filepath='./outputs/schema.json')

if __name__ == "__main__":
    main()
