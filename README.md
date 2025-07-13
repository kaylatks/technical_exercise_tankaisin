# Technical Exercise
This repo is used to store the exercise script.

## 📂 Folder Structure

```bash
.
technical_exercise_tankaisin/
├── README.md
├── SectionA/
│   ├── SectionA.sql

├── SectionB/
│   ├── docker_output 
│   │   ├── carsome.csv
│   ├── Dockerfile
│   └── main.py
│   └── requirements.txt

```
---

## Section A: SQL
This is only the result by using postgresql.

---
## Section B: Carsome scraper
- to build and scrap the data from carsome webpage by using docker image
- in order to have the get the scrap result, please follow the instruction below.


### Features ✨
- Scrapes car data from Carsome
- Saves output to CSV (`carsome_data.csv`)
- Dockerized for easy use 🐳

### How to Use 🛠️
Step 1: Clone the repository
```bash
git clone https://github.com/kaylatks/technical_exercise_tankaisin.git
```
Step 2: Open docker🐳 and make sure docker deskstop is running.

Step 3: To build the docker image
```bash
cd SectionB
```
```bash
docker build -t carsome_scraper .
```
Step 4: Get the scrape result.

📂 To create the folder in your local under SectionB same directory with docker file
```bash
mkdir -p ./docker_output
```

📥To scrap the data by using docker image. 
*📌Note: the output folder name need to same as what you create previous step.*
```bash
docker run --rm -v "$PWD/docker_output:/app/docker_output" carsome_scraper
```





