import pandas as pd
import numpy as np
import dateparser
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model

# Charger le dataset
df = pd.read_csv(r'pwp\prediction_apple\moduleweb\dataset\cours_apple_5.csv')

# Fonction pour nettoyer et convertir les colonnes contenant des valeurs numériques
def clean_and_convert_column(col):
    col = col.str.replace('\u202f', '')  # Supprimer les espaces insécables
    col = col.str.replace(',', '.')      # Remplacer les virgules par des points
    return col.astype(float)             # Convertir en type float

# Nettoyer les colonnes numériques
numeric_cols = ['Ouverture', 'Plus Haut', 'Plus Bas', 'Ferme', 'Clôture Ajustée', 'Volume']
for col in numeric_cols:
    df[col] = clean_and_convert_column(df[col])

# Conversion de la colonne 'Date' en datetime
df['Date'] = df['Date'].apply(lambda x: dateparser.parse(x))
df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)

# Définir la colonne 'Date' comme index
df.set_index('Date', inplace=True)

# Normalisation des données (exemple avec la colonne 'Ferme')
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(df[['Ferme']])

# Paramètres
sequence_length = 120

# Fonction pour créer des séquences
def create_sequences(data, sequence_length):
    X, Y = [], []
    for i in range(sequence_length, len(data)):
        X.append(data[i-sequence_length:i, 0])
        Y.append(data[i, 0])
    return np.array(X), np.array(Y)

# Créer les séquences
X, Y = create_sequences(scaled_data, sequence_length)

# Charger votre modèle sauvegardé (remplacez le chemin avec celui de votre modèle)
model = load_model(r'C:\v_librairie\pwp\prediction_apple\model\prediction.h5')

# Fonction pour prédire les prix futurs (itératif)
def predict_future_prices(n_days):
    # Initialiser la séquence avec les dernières données disponibles
    last_sequence = scaled_data[-sequence_length:].reshape(1, sequence_length, 1)
    
    predictions = []
    
    for _ in range(n_days):
        # Prédire la valeur pour le jour suivant
        predicted_price_scaled = model.predict(last_sequence)
        
        # Revenir à l'échelle originale
        predicted_price = scaler.inverse_transform(predicted_price_scaled.reshape(-1, 1))
        predictions.append(predicted_price[0][0])
        
        # Mettre à jour la séquence en ajoutant la valeur prédite et en supprimant la plus ancienne
        last_sequence = np.append(last_sequence[:, 1:, :], predicted_price_scaled.reshape(1, 1, 1), axis=1)
    
    return predictions
