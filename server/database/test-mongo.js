const mongoose = require('mongoose');
const Dealerships = require('./dealership');

// Connect to MongoDB
mongoose.connect("mongodb://localhost:27017/", {'dbName':'dealershipsDB'})
  .then(() => console.log('Connected to MongoDB'))
  .catch(err => console.error('Failed to connect to MongoDB:', err));

// Test query
async function testQuery() {
  try {
    const dealers = await Dealerships.find();
    console.log(`Found ${dealers.length} dealers`);
    console.log('First dealer:', dealers[0]);
  } catch (err) {
    console.error('Error querying dealers:', err);
  } finally {
    mongoose.disconnect();
  }
}

testQuery();