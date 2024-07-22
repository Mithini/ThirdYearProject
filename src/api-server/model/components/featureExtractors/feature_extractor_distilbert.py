from transformers import DistilBertTokenizer, TFDistilBertModel
import pandas as pd
import numpy as np
import tensorflow as tf


class FeatureExtractor:
    def __init__(self, model_name="distilbert-base-uncased"):
        self.tokenizer = DistilBertTokenizer.from_pretrained(model_name)
        self.model = TFDistilBertModel.from_pretrained(model_name)

    def extract_features(self, books_df_processed):
        document_embeddings = []
        for author, title, desc, genres in zip(books_df_processed['author'], books_df_processed['title'],
                                               books_df_processed['description'], books_df_processed['genres']):
            # Concatenate author, title, and description
            input_text = author + ' ' + title + ' ' + desc
            genre_text = ' '.join(genres)
            input_text = input_text + ' ' + genre_text

            # Tokenize input text
            inputs = self.tokenizer(input_text, padding=True, truncation=True, return_tensors="tf")

            # Forward pass through BERT model
            outputs = self.model(inputs)

            # Extract embeddings
            last_hidden_states = outputs.last_hidden_state
            # You can choose to use the embedding of the [CLS] token or pool the embeddings to get a single vector
            pooled_embedding = tf.reduce_mean(last_hidden_states, axis=1)
            document_embeddings.append(pooled_embedding.numpy())

        # Combine document embeddings with other features
        ##language_features = pd.get_dummies(books_df_processed['language_code']).values
        composite_feature_vector = np.vstack([document_embeddings])

        return composite_feature_vector