from langchain_cohere import ChatCohere
from langchain.prompts import PromptTemplate
from src.prompt import prompt_template
from store_index import retreiver
from langchain.chains import RetrievalQA
from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
from bson.objectid import ObjectId  
import secrets


app = Flask(__name__)

secret_key=secrets.token_hex(16)
app.config['SECRET_KEY']=secret_key

bcrypt = Bcrypt(app)

llm = ChatCohere(cohere_api_key="" , temperature=0.4)
prompt = PromptTemplate(
    template=prompt_template,
    input_variables=['context','question']
)

chain_type_kwargs = {"prompt": prompt}

chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever = retreiver,
    input_key="query",
    return_source_documents=True,
    chain_type_kwargs=chain_type_kwargs)

try:
    client = MongoClient('mongodb+srv://testuser:fs8fkJWEzZle2dQS@cluster0.p44e4.mongodb.net/')  # Local MongoDB connection
    db = client['Sarthi']
    users_collection = db['User']
    print("MongoDB connected successfully!")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")


@app.route("/")
def index():
    return render_template('Home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        print(username)
        user_exists = users_collection.find_one({"email": email})
        if user_exists:
            flash('User already exists with this email!', 'error')
            print('Error')
            return redirect(url_for('signup'))
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        users_collection.insert_one({
            "username": username,
            "email": email,
            "password": hashed_password
        })
        flash('Signup successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('Signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' or request.method=='GET':
        username = request.form.get('username')
        password = request.form.get('password')
        user = users_collection.find_one({"username": username})
        if user and bcrypt.check_password_hash(user['password'], password):
            flash('Login successful!', 'success')
            return redirect(url_for('predict'))  
        else:
            flash('Invalid email or password.', 'error')
            return render_template('Login.html')

    return render_template('Login.html')

@app.route("/predict")
def predict():
    return render_template('predict.html')

@app.route("/result.html")
def result():
    return render_template('result.html')

@app.route("/chat.html")
def index1():
    return render_template('chat.html')

@app.route("/aboutus.html")
def aboutus():
    return render_template('aboutus.html')

@app.route("/bot.html")
def darkmode():
    return render_template('bot.html')

@app.route("/get",methods=["GET","POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    print(input)
    result = chain({"query":input})
    print("Response : ",result["result"])
    return str(result["result"])

if __name__ == '__main__':
    app.run(debug=True)