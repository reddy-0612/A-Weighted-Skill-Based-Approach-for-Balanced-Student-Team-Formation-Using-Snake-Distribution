
# Overview
This project presents an automated approach for forming balanced student teams using a weighted skill-based scoring model and the Snake Distribution algorithm. Unlike traditional team formation methods that rely only on academic performance or random assignment, this approach considers multiple evaluation factors such as topic-specific skills, CGPA, and general technical skills to create fair and well-balanced project teams. 

## Features
- Topic-aware team formation (VLSI, Coding/ML, Signal Processing)
- Weighted scoring based on multiple student attributes
- Min-Max normalization for fair feature comparison
- Automatic preprocessing and handling of missing values
- Snake Distribution algorithm for balanced team allocation
- Generates team assignments in CSV format

## Methodology
The proposed system follows these steps:

1. Data preprocessing and cleaning
2. Feature selection based on project domain
3. Encoding and normalization of student data
4. Weighted capability score calculation
5. Student ranking based on capability scores
6. Balanced team formation using the Snake Distribution algorithm

The scoring model prioritizes:
- **Topic-specific skills** (highest weight)
- **CGPA**
- **General technical and communication skills**

This ensures that every team contains a balanced mix of high-, medium-, and low-performing students. 

## Technologies Used
- Python
- Pandas
- NumPy
- Scikit-learn (MinMaxScaler)

## Input
The program accepts a CSV dataset containing student information, including:
- Student Name
- CGPA
- Topic-specific skills
- Technical skills
- General skills
- Communication and presentation abilities

## Output
The program generates the teams based on their capability score and prevents clustering of highly skilled students into a single team.


## Advantages
- Fair and balanced student team formation
- Prevents clustering of highly skilled students into a single team
- Adaptable to different project domains
- Easy to implement and computationally efficient
- Suitable for academic project allocation and collaborative learning environments :contentReference[oaicite:2]{index=2}

