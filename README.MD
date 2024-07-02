# EPIC movie recommender

## Overview
This project is a Movie Recommendation System that uses RAG (Retrieval augmented generation) to suggest movies to users based on similarity to the sellected movie. The system is designed to provide accurate recommendations to enhance user experience.
Project also includes web scraping scripts for various sites.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Data](#data)
- [Results](#results)
- [Contact](#contact)

## Features
- Movie recommendations
- User-friendly interface
- Scalable and efficient algorithm
- admin management of movies
## Requirements
- git
- docker

## Installation
1. Put your open ai api key to .env file
2. Clone the repository:
    ```bash
    git clone https://github.com/EPIC-Recommender/EPIC-Recommender.git
    ```
3. Change into the project directory:
    ```bash
    cd EPIC-Recommender
    ```
4. Install the required dependencies:
    ```bash
    docker build -t epic_image .
    ```
5. Run the container:
    ```bash
    docker run -d -p 5432:5432 -p 80:80 epic-recommender
    ```
    

## Usage
1. Open http://localhost in your browser to see the website 
    

## Data
Data used for this project is scraped from varius websites

## Contact
If you have any questions or need further assistance, feel free to contact us

## Results
![images](https://preview.redd.it/hk7h4ibnf6ad1.png?width=1920&format=png&auto=webp&s=6bdec1e38d976796065419b2059ae621ea037d10)
![images](![alt text](image.png))
![images](![alt text](image-1.png))
