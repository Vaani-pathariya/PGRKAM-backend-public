from flask import Flask,jsonify,request
from flask_cors import CORS
import assemblyai as aai
from datetime import datetime
import os
import pyrebase
app = Flask(__name__)
CORS(app)
config = {
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()
db = firebase.database()
#The below function is used to get data 
@app.route('/user-data')
def get_all_data():
    try:
        data = db.child('Users').get().val()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)})
#The below function is used to send data to mongodb 
@app.route('/submit-data', methods=['POST'])
def submit_data():
    try:
        data = request.json
        db.child('Users').push(data)
        return jsonify({"message": "Data sent to Firebase successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})
#Update query :
@app.route('/update-data/<user_id>', methods=['PUT'])
def update_data(user_id):
    try:
        data_to_update = request.json
        db.child('Users').child(user_id).update(data_to_update)
        return jsonify({"message": f"Data for user {user_id} updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})
#Deletion query : 
@app.route('/delete-data/<user_id>', methods=['DELETE'])
def delete_data(user_id):
    try:
        db.child('Users').child(user_id).remove()
        return jsonify({"message": f"Data for user {user_id} deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})
#Function to increment any value by 1 in mongodb : 
@app.route('/increment-count/<user_id>', methods=['PUT'])
def increment_count(user_id):
    try:
        data = db.child('Users').child(user_id).child('Age').get().val()
        db.child('Users').child(user_id).child('Age').set(data+1)
        return jsonify({"message": f"Count for user {user_id} incremented successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})
    
#PDF upload route : 
@app.route('/upload-pdf', methods=['POST'])
def upload_pdf():
    try:
        # Get the uploaded file from the request
        file = request.files['file']

        # Upload the file to Firebase Storage
        filename = os.path.basename(file.filename)
        storage.child(filename).put(file)

        # Get the download URL of the uploaded file
        download_url = storage.child(filename).get_url(None)

        return jsonify({'success': True, 'download_url': download_url})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
#Update image route : 
@app.route('/update_pdf', methods=['POST'])
def update_pdf():
    try:
        # Get the updated file from the request
        updated_file = request.files['file']

        # Assuming you have a specific PDF file you want to update
        pdf_file_name = "city.png"

        # Update the existing PDF file in Firebase Storage
        storage.child(f'pdfs/{pdf_file_name}').put(updated_file)

        # Get the updated download URL of the PDF file
        updated_download_url = storage.child(f'pdfs/{pdf_file_name}').get_url(None)

        return jsonify({'success': True, 'updated_download_url': updated_download_url})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
#Send message Api 
@app.route('/send-message', methods=['POST'])
def send_message():
    try:
        data = request.json
        sender = data.get('sender')
        receiver = data.get('receiver')
        message_text = data.get('message_text')
        db.child('Messages').push({
            'sender': sender,
            'receiver': receiver,
            'message_text': message_text,
            'timestamp': datetime.utcnow().isoformat()
        })
        return jsonify({"message": "Message sent successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})
# Get messages from Firebase
@app.route('/get-messages/<user_id>', methods=['GET'])
def get_messages(user_id):
    try:
        messages = db.child('Messages').order_by_child('sender').equal_to(user_id).get()
        return jsonify(messages)
    except Exception as e:
        return jsonify({"error": str(e)})
@app.route('/get-jobs')
def get_jobs():
    try:
        data = db.child('JobsPosted').get().val()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)})
@app.route('/get-success')
def get_success():
    try:
        data = db.child('Success').get().val()
        
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)})
@app.route('/gender-data')
def get_all_gender():
    try:
        data = db.child('Gender').get().val()
        
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)})
@app.route('/location-data')
def get_all_location():
    try:
        data = db.child('Location').get().val()
        
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)})
@app.route('/traffic-data')
def get_all_traffic():
    try:
        data = db.child('Platform').get().val()
        
        
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)})
@app.route('/get-average-salary')
def get_all_average_salary():
    try:
        data = db.child('AverageSalary').get().val()
        
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)})
@app.route('/get-device')
def get_all_device ():
    try:
        data = db.child('Device').get().val()
        
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)})
@app.route('/get-options')
def get_all_options ():
    try:
        data = db.child('Options').get().val()
        
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)})
@app.route('/get-retention')
def get_all_retention ():
    try:
        data = db.child('Retention').get().val()
       
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)})
@app.route('/Job-data/Featured/<user_id>')
def get_featured(user_id):
    try:
        data = db.child('JobsPosted').child('Featured').child(user_id).get().val()
       
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)})
@app.route('/increment-failure', methods=['PUT'])
def increment_failure():
    try:
        data = db.child('Success').child('Failure').get().val()
        db.child('Success').child('Failure').set(data+1)
        return jsonify({"message": " incremented successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})
@app.route('/decrement-failure', methods=['PUT'])
def decrement_failure():
    try:
        data = db.child('Success').child('Failure').child(11).get().val()
        db.child('Success').child('Failure').set(data-1)
        change=db.child('Success').child('Success_data').get().val()
        db.child('Success').child('Failure').set(change+1)
        return jsonify({"message": " done successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)



# # Retrieve pdf document:
# @app.route('/get-pdf/<document_id>', methods=['GET'])
# def get_pdf(document_id):
#     try:
#         collection = mongo.db.Resume
#         document = collection.find_one({'_id': ObjectId(document_id)})

#         if document:
#             pdf_data = base64.b64decode(document['pdf_data'])
#             return pdf_data, 200, {'Content-Type': 'application/pdf'}
#         else:
#             return jsonify({"message": "No document found with the specified ID"}), 404
#     except Exception as e:
#         return jsonify({"error": str(e)})