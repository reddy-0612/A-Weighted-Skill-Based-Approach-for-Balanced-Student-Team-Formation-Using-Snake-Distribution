import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import os

# --- 1. USER INPUTS ---
group_size = 4          # N members per team
project_topic = "VLSI"  # Options: "VLSI", "Coding/ML", "Signal Processing"
# ----------------------

file_path = 'Technical Skill Dataset For Project Grouping_final(Sheet1).csv'

if not os.path.exists(file_path):
    print(f"Error: {file_path} not found.")
else:
    # 1. LOAD & CLEAN HEADERS
    df = pd.read_csv(file_path, encoding='latin1')
    df.columns = df.columns.str.replace(r'[^\x00-\x7F]+', ' ', regex=True).str.replace(r'\s+', ' ', regex=True).str.lower().str.strip()

    # 2. KEYWORD COLUMN MAPPING
    new_cols = {}
    for col in df.columns:
        if 'cgpa' in col: new_cols[col] = 'cgpa'
        elif 'logical' in col: new_cols[col] = 'logical_reasoning'
        elif 'vlsi' in col: new_cols[col] = 'vlsi_exposure'
        elif 'machine learning' in col: new_cols[col] = 'ml_exposure'
        elif 'technical idea' in col: new_cols[col] = 'idea_to_solution'
        elif 'programming' in col: new_cols[col] = 'programming_use'
        elif 'instructions' in col: new_cols[col] = 'tech_docs_understanding'
        elif 'signals' in col: new_cols[col] = 'signals_systems_understanding'
        elif 'circuit' in col: new_cols[col] = 'circuit_analysis'
        elif 'consistency' in col: new_cols[col] = 'task_consistency'
        elif 'presenting' in col: new_cols[col] = 'presentation_confidence'
        elif 'name' in col: new_cols[col] = 'student_name'

    df_clean = df.rename(columns=new_cols)

    # 3. FIX EXCEL DATE CORRUPTION IN CGPA
    # Explicitly mapping Excel's "Date" artifacts back to your categories
    date_fix_map = {
        '08-Sep': '8-9', '8-Sep': '8-9', '8th september': '8-9',
        '07-Aug': '7-8', '7-Aug': '7-8', '7th august': '7-8'
    }
    if 'cgpa' in df_clean.columns:
        df_clean['cgpa'] = df_clean['cgpa'].str.strip().replace(date_fix_map)

    # 4. DEFINE FEATURE WEIGHTS
    # Topic (3.0) > CGPA (2.0) > General (1.0)
    general_feats = ['logical_reasoning', 'tech_docs_understanding', 'task_consistency', 'presentation_confidence']
    
    if project_topic == "VLSI":
        topic_feats = ['vlsi_exposure', 'circuit_analysis', 'idea_to_solution']
    elif project_topic == "Coding/ML":
        topic_feats = ['ml_exposure', 'programming_use', 'logical_reasoning']
    else: # Signal Processing
        topic_feats = ['signals_systems_understanding', 'idea_to_solution']

    active_cols = list(set(['cgpa'] + topic_feats + general_feats))
    df_ml = df_clean[[c for c in active_cols if c in df_clean.columns]].copy()

    # 5. ENCODING & IMPUTATION
    # Precise mapping for the sanitized CGPA values
    cgpa_final_map = {'below 7': 0, '7-8': 1, '8-9': 2, 'above 9': 3}
    
    for col in df_ml.columns:
        if col == 'cgpa':
            df_ml[col] = df_ml[col].map(cgpa_final_map).fillna(0)
        elif df_ml[col].dtype == 'object':
            df_ml[col] = df_ml[col].str.strip().fillna(df_ml[col].mode()[0])
            df_ml[col] = df_ml[col].astype('category').cat.codes
        else:
            df_ml[col] = df_ml[col].fillna(df_ml[col].median())

    # 6. CALCULATE WEIGHTED COMPOSITE SCORE
    scaler = MinMaxScaler()
    df_scores = pd.DataFrame(scaler.fit_transform(df_ml), columns=df_ml.columns)

    df_scores['total_score'] = 0
    for col in df_scores.columns:
        if col in topic_feats: df_scores['total_score'] += df_scores[col] * 3.0
        elif col == 'cgpa': df_scores['total_score'] += df_scores[col] * 2.0
        else: df_scores['total_score'] += df_scores[col] * 1.0

    df_clean['final_capability_score'] = df_scores['total_score']

    # 7. SNAKE-SAMPLING TEAM FORMATION (Zero Variance Logic)
    df_sorted = df_clean.sort_values(by='final_capability_score', ascending=False).reset_index(drop=True)
    num_groups = int(np.ceil(len(df_sorted) / group_size))
    df_sorted['group_id'] = 0

    for i in range(len(df_sorted)):
        round_num = i // num_groups
        if round_num % 2 == 0:
            assigned_group = (i % num_groups) + 1
        else:
            assigned_group = num_groups - (i % num_groups)
        df_sorted.loc[i, 'group_id'] = assigned_group

    # 8. FINAL EXPORT
    final_cols = ['group_id', 'student_name', 'final_capability_score', 'cgpa']
    output = df_sorted[[c for c in final_cols if c in df_sorted.columns]]
    output = output.sort_values(by=['group_id', 'final_capability_score'], ascending=[True, False])
    
    output.to_csv('Ideal_Balanced_Teams.csv', index=False)
    print(f"SUCCESS: Groups formed for {project_topic}.")
