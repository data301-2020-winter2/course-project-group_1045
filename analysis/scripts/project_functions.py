import pandas as pd

def load_and_process(url_or_path_to_csv_file):

    # Method Chain 1 (Load data and deal with missing data)

    df1 = (
          pd.read_csv(url_or_path_to_csv_file)
          .rename(columns={'age': 'Age', 'sex': 'Sex', 'bmi': 'BMI',
                           'children': 'Children', 'smoker': 'Smoker', 'region': 'Region',
                           'charges': 'Charges'})
          .dropna()
          .sort_values(by='Charges', ascending=False)
          .reset_index()
          .drop(columns='index')
      )

    # Method Chain 2 (Create new columns, drop others, and do processing)

    df2 = (
          df1
          .assign(Body_Shape=get_body_shapes(df1))
          .assign(Charges=df1['Charges'].astype(int), BMI=df1['BMI'].round(1), Region=df1['Region'].str.title(), Sex=df1['Sex'].str.title())
          .rename(columns={'Body_Shape': 'Body Shape'})
      )

    # Make sure to return the latest dataframe

    return df2

def get_body_shapes(df):
    body_shapes = []
    
    for bmi in df['BMI']:
        if bmi < 18:
            body_shapes.append('Under Weight')
            
        elif 18 <= bmi < 23:
            body_shapes.append('Normal Weight')
            
        elif 23 <= bmi < 27:
            body_shapes.append('Over Weight')
            
        elif 27 <= bmi < 32:
            body_shapes.append('Class 1 Obesity')
            
        elif 32 <= bmi < 37:
            body_shapes.append('Class 2 Obesity')
            
        elif 37 <= bmi:
            body_shapes.append('Class 3 Obesity')

    return body_shapes

def compare_smokers_to_bmi(df):
    data = df[['Smoker', 'Body_Shape']]
    
    new_data = pd.DataFrame([[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
                        index=['Under Weight', 'Normal Weight', 'Over Weight', 'Class 1 Obesity', 'Class 2 Obesity', 'Class 3 Obesity'],
                        columns=['Population', 'Non-Smokers', 'Smokers'])


    for i in range(len(data)):
        new_data['Population'][data.loc[i]['Body_Shape']] += 1
        
        if data.loc[i]['Smoker'] == 'no':
            new_data['Non-Smokers'][data.loc[i]['Body_Shape']] += 1
    
        else:
            new_data['Smokers'][data.loc[i]['Body_Shape']] += 1

    return new_data
