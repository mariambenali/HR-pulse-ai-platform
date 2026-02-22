import os
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.impute import SimpleImputer



BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../")
)

file_path = os.path.join(
    BASE_DIR,
    "data",
    "cleaned_data",
    "cleaned_data.csv"
)

def pipeline_predict_salary():

    #load data
    df = pd.read_csv(file_path)

    #split data
    X = df.drop(columns=["mean_salary"])
    y = df["mean_salary"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size= 0.2,
        random_state= 42
    )

    num_features = ['company_age']
    cat_features = ['Industry', 'Sector', 'size_category']
    text_features = ['Job Title', 'Job Description', 'Company Name']

    #transformer
    # Numérique : imputer + scaler
    num_transformer = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    # Catégoriel : imputer + OHE
    cat_transformer = Pipeline([
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('ohe', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])

    title_transformer = TfidfVectorizer(max_features=50, ngram_range=(1,2)) 
    desc_transformer = TfidfVectorizer(max_features=100, stop_words='english') 
    preprocessor = ColumnTransformer(transformers=[ 
        ('num', num_transformer, num_features), 
        ('cat', cat_transformer, cat_features), 
        ('title', title_transformer, 'Job Title'), 
        ('desc', desc_transformer, 'Job Description'), ],
        remainder='drop')
    
    #pipeline predict
    model = Pipeline([ 
        ('preprocessor', preprocessor), 
        ('regressor', RandomForestRegressor(
            n_estimators=100,

            random_state=42)) ]) 
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    #evaluation
    y_pred = model.predict(X_test)
    print("MAE :", mean_absolute_error(y_test, y_pred))
    print("R²  :", r2_score(y_test, y_pred))

    return y_pred

print(pipeline_predict_salary())