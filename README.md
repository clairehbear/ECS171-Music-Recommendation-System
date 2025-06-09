# ECS171-Music-Recommendation-System
Made by:
Gerard Anderias, Armin Bozorgi, Dylan Choi, Claire Hesley, and Rashmit Shrestha

In order to run the Flask web app, head into the frontend folder by typing "cd ./frontend" into the terminal, and then run the command "python ./app.py"
    This will open a local host server at the address http://127.0.0.1:5000

To use the Flask app:
1. Search a Spotify song or the name of an artist 
2. Click on the star button to add a song to your list of favorites
3. Feel free to delete some favorites or clear all if needed
4. After having one or more favorited song, click on "Get My Song Recommendations" to run our Cosine distance K-means clustering model on the existing favorited songs
5. Finally, feel free to add the recommendations to your favorite, and continue getting recommendations and favorites!

# ECS171 Music Recommendation System

**Authors**: Gerard Anderias, Armin Bozorgi, Dylan Choi, Claire Hesley, and Rashmit Shrestha  
**Formal Report Name**: Music Recommendation through Machine Learning: A Multi-model Analysis of Clustering Techniques

---

## Project Overview

In our project, we compare the effectiveness through 3 cluster models, through training, testing, and evaluation. Then, we craeted a Flask-based web application to use our winning
model to get live-recommendations based on the users' favorite songs. 

Clustering Models we used:
- **Cosine K-Means** *(selected as the final model)*
- **Euclidean K-Means**
- **Fuzzy C-Means**

---

## How to Run the App (Locally)

### 1. Clone the Repository
In your terminal, clone the repository:
```
git clone https://github.com/clairehbear/ECS171-Music-Recommendation-System
```

Then go into the project folder
```
cd ECS171-Music-Recommendation-System
```

### 2. Install packages
Then once inside, navigate to the frontend folder
```
cd frontend
```

Then install the necssary Python packages
```
pip install Flask pandas numpy scikit-learn
```

### 3. Check File Placement
To make sure the demo runs, dataset.csv and cos.pkl should be in the correct places
- dataset.csv should be in ./frontend/data/
- cos.pkl should be in ./backend/models/

### 4. Run the Web App
Finally, in the frontend folder, run the following Python command to start the Flask app
```
python ./app.py
```

The local address will be http://127.0.0.1:5000

## How to Use the App
1. Search a Spotify song or the name of an artist 
2. Click on the star button to add a song to your list of favorites
3. Feel free to delete some favorites or clear all if needed
4. After having one or more favorited song, click on "Get My Song Recommendations" to run our Cosine distance K-means clustering model on the existing favorited songs
5. Finally, feel free to add the recommendations to your favorite, and continue getting recommendations and favorites!