// Insert data into the airbnb.listings collection
const fs = require('fs');
const { MongoClient } = require('mongodb');

const uri = 'mongodb://localhost:27017';
const dbName = 'airbnb';
const collectionName = 'listings';
const filePath = './data/cleaned_airbnb_listings.json';

async function run() {
  const client = new MongoClient(uri);
  try {
    await client.connect();
    const db = client.db(dbName);
    const collection = db.collection(collectionName);

    const lines = fs.readFileSync(filePath, 'utf-8').split('\n').filter(Boolean);
    const docs = lines.map(JSON.parse);

    const chunkSize = 1000;
    for (let i = 0; i < docs.length; i += chunkSize) {
      const chunk = docs.slice(i, i + chunkSize);
      await collection.insertMany(chunk);
      console.log(`Inserted ${i + chunk.length} documents...`);
    }

    console.log('All documents inserted.');
  } finally {
    await client.close();
  }
}

run().catch(console.dir);