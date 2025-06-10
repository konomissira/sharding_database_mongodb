sh.addShard("shardReplSet1/shard1:27018");
sh.addShard("shardReplSet2/shard2:27020");

// Enable sharding for the DB
sh.enableSharding("airbnb");

// Shard the collection by 'neighbourhood'
sh.shardCollection("airbnb.listings", { neighbourhood: 1 });

print("Sharding setup complete.");
