# MongoDB Sharding Project – Airbnb London Listings

![MongoDB](https://img.shields.io/badge/MongoDB-4EA94B?logo=mongodb&logoColor=white&style=for-the-badge)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white&style=for-the-badge)
![Node.js](https://img.shields.io/badge/Node.js-339933?logo=nodedotjs&logoColor=white&style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white&style=for-the-badge)
![pandas](https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=white&style=for-the-badge)
![GitHub](https://img.shields.io/badge/GitHub-181717?logo=github&logoColor=white&style=for-the-badge)

This project demonstrates how to build and query a **MongoDB sharded cluster** using Docker and insert real-world data from the **Airbnb London listings** dataset. It simulates a production grade environment and showcases horisontal scaling using sharding.

## Project Goals

-   Practice advanced MongoDB infrastructure using **sharded architecture**
-   Use **Docker** to orchestrate MongoDB config servers, shards, and mongos router
-   Clean and prepare real data using **Python (pandas)**
-   Insert and query data using **Node.js and the MongoDB driver**

## Tech Stack

-   **MongoDB 6.0** – Sharded cluster with 2 shards and 1 config server
-   **Docker Compose** – Container orchestration for MongoDB setup
-   **Python 3.11.7** – For data preparation and CSV-to-JSON conversion
-   **pandas** – Data cleaning and formatting
-   **Node.js** – Inserting large JSON files into MongoDB via script
-   **Git & GitHub** – Version control and project sharing
-   **Shell / CLI** – Manual setup and replica set initiation

## 📁 Project Structure

```
mongodb_sharding_database/
├── data/ # Contains cleaned CSV and JSON datasets (ignored by Git to avoid slow push on GitHub)
│ └── cleaned_airbnb_listings.csv
│ └── cleaned_airbnb_listings.json
├── src/
│ ├── initiate_cluster.js # Adds shards & enables sharding
│ ├──convert_csv_to_json.py # Cleans and converts CSV file to JSON
│ └── insert_data.js # Inserts data into MongoDB
├── sharding_database/
│ └── docker-compose.yml # Spins up MongoDB sharded cluster
├── .gitignore
├── package-lock.json # Ignored by Git
├── package.json
├── README.md
└── requirements.txt # Python dependencies
```

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/konomissira/sharding_database_mongodb.git
cd sharding_database_mongodb
```

### Data Preprocessing

-   Convert the CSV file to JSON (JSONL) with this command:

```
python src/convert_csv_to_json.py # From the root directory
```

### Spin up MongoDB Cluster with Docker

```
cd sharding_database
docker compose up -d
```

## MongoDB Sharding Configuration & Data Insertion

### Step 1: Initiate the Config Server Replica Set

```
docker exec -it configsvr1 mongosh --port 27019
```

Inside mongosh:

```
rs.initiate({
  _id: "configReplSet",
  configsvr: true,
  members: [{ _id: 0, host: "configsvr1:27019" }]
})
exit #To exit mongosh
```

### Step 2: Initiate Each Shard Replica Set

#### Shard 1

```
docker exec -it shard1 mongosh --port 27018
```

Inside mongosh:

```
   rs.initiate({
  _id: "shardReplSet1",
  members: [{ _id: 0, host: "shard1:27018" }]
})

exit # To exit mongosh
```

#### Shard 2

```
docker exec -it shard2 mongosh --port 27020
```

Inside mongosh:

```
rs.initiate({
  _id: "shardReplSet2",
  members: [{ _id: 0, host: "shard2:27020" }]
})

exit # To exit mongosh
```

### Step 3: Enable Sharding

```
mongosh --host localhost:27017
```

Then run:

```
load("src/initiate_cluster.js")
```

### Step 4: Insert Data into airbnb.listings

Install dependencies (only once):

```
npm init -y
npm install mongodb
```

Then run the insert script:

```
 node src/insert_data.js
```

### Query Examples

#### Count documents

```
   db.listings.countDocuments()
```

#### Listings in Camden

```
   db.listings.find({ neighbourhood: "Camden" }).limit(5).pretty()
```

#### Entire flats under £100

```
   db.listings.find({
    room_type: "Entire home/apt",
    price: { $lte: 100 }
    }).limit(5).pretty()
```

#### Geo-filtered listings

```
   db.listings.find({
    latitude: { $gt: 51.5 },
    longitude: { $lt: -0.1 }
    }).limit(5).pretty()
```

### Sharding Strategy

```
-   Shard key: neighbourhood
-   Rationale: High cardinality, well distributed, commonly queried
-   Shards: shardReplSet1, shardReplSet2
-   Verified using: sh.status()
```

## About Me:

This project was created by a Data Engineer based in the UK currently looking for job opportunities.
It demonstrates cloud-readiness, infrastructure setup, data pipeline thinking, and scalable database architecture using open-source tools.

### License

This project is open-source and available under the MIT License.
