import recommender
import pickle

with open('model.pkl', 'rb') as file:
    # Load the data from the pickle file
    model = pickle.load(file)

with open('dict1.pkl', 'rb') as file:
    # Load the data from the pickle file
    dict1 = pickle.load(file)

with open('dict2.pkl', 'rb') as file:
    # Load the data from the pickle file
    dict2= pickle.load(file)

print(dict1)


print(model.make_recommendation('I believe in miracles',10))