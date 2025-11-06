import os
import pandas as pd
import numpy as np
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_functions import read_yaml,load_data
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE

logger = get_logger(__name__)

class DataProcessor:
    def __init__(self,train_path,test_path,processed_dir,config_path):
        self.train_path = train_path
        self.test_path= test_path
        self.processed_dir = processed_dir

        self.config = read_yaml(config_path)

        if not os.path.exists(self.processed_dir):
            os.makedirs(self.processed_dir)
        
    def preprocess_data(self,df):
        try:
            logger.info("Starting our data processing step")

            logger.info("Dropping the columns")
            df.drop(columns = ['Booking_ID'],inplace = True)
            df.drop_duplicates(inplace=True)

            cat_cols = self.config['data_processing']['categorical_columns']
            num_cols = self.config['data_processing']['numerical_columns']

            logger.info("Applying Label Encoding")

            label_encoder = LabelEncoder()
            mappings= {}

            mappings= {}

            for col in cat_cols:
                df[col] = label_encoder.fit_transform(df[col])

                mappings[col] = {label:code for label,code in zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_))}
                        
            logger.info("Label Mappings are:")
            for col,mapping in mappings.items():
                logger.info(f"{col}: {mapping}")
            
            logger.info("Doing Skewness Handling")
            skewness_threshold = self.config['data_processing']['skewness_threshold']
            skewness = df[num_cols].apply(lambda x:x.skew())

            for column in skewness[skewness > skewness_threshold].index:
                df[column] = np.log1p(df[column])
            
            return df


        except Exception as e:
            logger.error(f"Error during preprocess step {e}")
            raise CustomException("Error during preprocess step", e)

    def balance_data(self,df) : 
        try:
            logger.info("Handling Imbalanced Data")
            X= df.drop(columns = "booking_status")
            y= df["booking_status"]

            smote = SMOTE(random_state=42)

            X_resampled, y_resampled = smote.fit_resample(X,y)

            balanced_df = pd.DataFrame(X_resampled, columns= X.columns)
            balanced_df['booking_status'] = y_resampled

            logger.info("Data balanced sucesfully")
            return balanced_df


        except Exception as e:
            logger.error(f"Error duing balancing data step {e}")
            raise CustomException("Error while balancing data",e)

    def select_important_features(self, df):
        """
        Select top N important features using RandomForest feature importance
        """
        try:
            number_of_top_features = self.config["data_processing"]["number_of_top_features"]
            logger.info("Starting feature importance selection")
            X = df.drop(columns="booking_status")
            y = df["booking_status"]

            model = RandomForestClassifier(random_state=42)
            model.fit(X, y)

            feature_importances = pd.Series(model.feature_importances_, index=X.columns)
            top_features = feature_importances.nlargest(number_of_top_features).index.tolist()

            logger.info(f"Top {number_of_top_features} important features: {top_features}")

            selected_df = df[top_features + ["booking_status"]]

            logger.info("Feature selection completed successfully")
            return selected_df

        except Exception as e:
            logger.error(f"Error during feature selection step {e}")
            raise CustomException("Error while selecting important features", e)

    def save_data(self,df,file_path):
        try:
            logger.info("Saving our data in processed folder")
            df.to_csv(file_path, index=False)
            logger.info(f"Data saved sucesfully to {file_path}")
        except Exception as e:
            logger.error(f"Error during saving data step {e}")
            raise CustomException("Error while saving data", e)
        
    def process(self):
        try:
            logger.info("Loading data from RAW directory")

            train_df = load_data(self.train_path)
            test_df = load_data(self.test_path)

            train_df= self.preprocess_data(train_df)
            test_df= self.preprocess_data(test_df)

            train_df= self.balance_data(train_df)
            

            train_df= self.select_important_features(train_df)
            test_df= test_df[train_df.columns]

            self.save_data(train_df,PROCESSED_TRAIN_DATA_PATH)
            self.save_data(test_df,PROCESSED_TEST_DATA_PATH)

            logger.info("Data processing comleted sucesfully")


    
        except Exception as e:
            logger.error(f"Error during lData processing pipeline {e}")
            raise CustomException("Error during Data processing pipeline", e)
        
if __name__=='__main__':
    processor = DataProcessor(TRAIN_FILE_PATH,TEST_FILE_PATH,PROCESSED_DIR,CONFIG_PATH)
    processor.process()
