from flask import Flask, request, render_template
from flask import jsonify
import vobject
import json
from pymongo import MongoClient
import pymongo
import certifi
from bson import json_util
from bson import ObjectId
from bson import json_util



print("hei")
# print(json_text)







#mongodb+srv://vegardstamadsen:zvNcYlvVwuE1ScJv@cluster0.bomsogj.mongodb.net/test
try:
    # Connect to MongoDB
    client = pymongo.MongoClient("mongodb+srv://vegardstamadsen:zvNcYlvVwuE1ScJv@cluster0.bomsogj.mongodb.net/test", tlsCAFile=certifi.where())
    print("Connected to MongoDB")

    # Select database
    mydb = client["CloudContacts"]

    # Select collection
    mycol = mydb["Contacts"]

    # Define document to be inserted
   # mydoc = {"name": "Johnnybot", "address": "Highway 39"}

    # Insert document into collection
   # x = mycol.insert_one(mydoc)

    # Print the ObjectID of the inserted document
   # print(x.inserted_id)
  

except Exception as e:
    print(f"Could not connect to MongoDB: {e}")










'''
mongodb+srv://vegardstamadsen:zvNcYlvVwuE1ScJv@cluster0.bomsogj.mongodb.net/?retryWrites=true&w=majority
'''


app = Flask("Api")


# Simulated database
CONTACTS =[]
contactsMy = []


contacts = []

# Load the JSON data from file



@app.route('/')
def hello():
    
    return 'Velkommen til vår API'
    
    


'''
@app.route('/contacts')
def get_contacts():
    
    for contact in mycol.find():
        # convert the MongoDB document to a JSON-serializable format
        contact = json.loads(json_util.dumps(contact))
        contacts.append(contact)
    return jsonify(contacts)
'''   

# Settings
MyData = []

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    

    
   
    if request.method == 'POST':
        file = request.files['file']
        file_content = file.read().decode('utf-8')
        text = vobject.readComponents(file_content)


        
        for dataContact in text:
            
            phone = "--No Information--"
            try:
                phone = str(dataContact.tel.value)
            except AttributeError:
                pass
            
            address = "--No Information--"
            try:
                address = str(dataContact.adr.value)
            except AttributeError:
                pass

            company = "--No Information--"
            try:
                company = str(dataContact.org.value[0])
            except AttributeError:
                pass


            MyContact = {
                'email': dataContact.email.value,
                'name': str(dataContact.n.value),
                'fullname': dataContact.fn.value,
                'address': address,
                'company': company,
                'phone': phone,
 
            }

            
            result = mycol.insert_one(MyContact)
            MyData.append(str(result.inserted_id))

        return jsonify({'message': MyData}) 
        
    else:
        # show the upload form
        return render_template('upload.html')
        
    
@app.route('/contacts')
def get_contacts():
    # clear the contacts list
    contacts = []

    # retrieve all contacts from the MongoDB collection
    for contact in mycol.find():
        # convert the MongoDB document to a JSON-serializable format
        contact = json.loads(json_util.dumps(contact))
        contacts.append(contact)

    # return the contacts as a JSON response
    return jsonify(contacts)

@app.route('/contacts/email/<email>')
def get_contact_by_email(email):
    # retrieve the contact from the MongoDB collection using the email address
    contact = mycol.find_one({'email': email})

    if contact is not None:
        # convert the MongoDB document to a JSON-serializable format
        contact = json.loads(json_util.dumps(contact))
        return jsonify(contact)
    else:
        return f"Contact with email {email} does not exist"


@app.route('/contacts/id/<string:id>')
def get_contact_by_id(id):
    # retrieve the contact from the MongoDB collection using the id
    contact = mycol.find_one({'_id': ObjectId(id)})

    if contact is not None:
        # convert the MongoDB document to a JSON-serializable format
        contact = json.loads(json_util.dumps(contact))
        return jsonify(contact)
    else:
        return f"Contact with id {id} does not exist"





'''
@app.route('/data')
def get_data():
    for d in contactsDATA:
        
        json_data = json_util.dumps(d)
        mycol.insert_one(json.loads(json_data))
        
    return contactsDATA
'''    


@app.route('/contacts', methods=['POST'])
def create_contact():
    # get the contact data from the request body
    name = request.json['name']
    address = request.json['address']

    # create a new contact object
    contact = {'name': name, 'address': address}

    # insert the contact object into the MongoDB collection
    result = mycol.insert_one(contact)

    # return the ID of the newly inserted contact
    return {'id': str(result.inserted_id)}


@app.route('/contacts/<id>', methods=['DELETE'])
def delete_contact(id):
    del CONTACTS[int(id)]
    return  {'id': id}


# This starts the application (if you run the script instead of launging flask
# from the command line).
if __name__ == '__main__':
    '''The variable __name__ is set to the name/title of the script. If this is
    equal to '__main__', then that means this program is run directly (from the
    start button or the command line). If not, it probably means that the script
    was imported as a module and not as a script. I.e. the code in this if does
    not run if the file is imported as a module.'''

    app.run()
