const express = require('express');
const mongoose = require('mongoose');
const fs = require('fs');
const  cors = require('cors')
const app = express()
const port = 3030;

app.use(cors())
app.use(express.json());
app.use(require('body-parser').urlencoded({ extended: false }));

const reviews_data = JSON.parse(fs.readFileSync("reviews.json", 'utf8'));
const dealerships_data = JSON.parse(fs.readFileSync("dealerships.json", 'utf8'));

mongoose.connect("mongodb://mongo_db:27017/",{'dbName':'dealershipsDB'})
  .then(() => console.log('Connected to MongoDB'))
  .catch(err => console.error('Failed to connect to MongoDB:', err));


const Reviews = require('./review');

const Dealerships = require('./dealership');

// Initialize database with data
Reviews.deleteMany({}).then(()=>{
  Reviews.insertMany(reviews_data['reviews'])
    .then(() => console.log('Reviews data loaded successfully'))
    .catch(err => console.error('Error loading reviews data:', err));
});

Dealerships.deleteMany({}).then(()=>{
  Dealerships.insertMany(dealerships_data['dealerships'])
    .then(() => console.log('Dealerships data loaded successfully'))
    .catch(err => console.error('Error loading dealerships data:', err));
});


// Express route to home
app.get('/', async (req, res) => {
    res.send("Welcome to the Mongoose API")
});

// Express route to fetch all reviews
app.get('/fetchReviews', async (req, res) => {
  try {
    const documents = await Reviews.find();
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to fetch reviews by a particular dealer
app.get('/fetchReviews/dealer/:id', async (req, res) => {
  try {
    const documents = await Reviews.find({dealership: req.params.id});
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to fetch all dealerships
app.get('/fetchDealers', async (req, res) => {
  try {
    const documents = await Dealerships.find();
    console.log('Fetched dealerships:', documents.length);
    res.json(documents);
  } catch (error) {
    console.error('Error fetching dealerships:', error);
    res.status(500).json({ error: 'Error fetching dealerships' });
  }
});

// Express route to fetch Dealers by a particular state
app.get('/fetchDealers/:state', async (req, res) => {
  try {
    const state = req.params.state;
    console.log('Fetching dealers in state:', state);
    
    // Use a case-insensitive regex to match the state name
    const stateRegex = new RegExp('^' + state + '$', 'i');
    console.log('Using regex pattern for state search');
    
    // Also try to match by state abbreviation (st field)
    const documents = await Dealerships.find({
      $or: [
        { state: stateRegex },
        { st: state.toUpperCase() }
      ]
    });
    
    console.log('Found dealers in state:', documents.length);
    res.json(documents);
  } catch (error) {
    console.error('Error fetching dealerships by state:', error);
    res.status(500).json({ error: 'Error fetching dealerships by state' });
  }
});

// Express route to fetch dealer by a particular id
app.get('/fetchDealer/:id', async (req, res) => {
  try {
    const dealerId = parseInt(req.params.id);
    console.log('Fetching dealer with ID:', dealerId);
    const document = await Dealerships.findOne({ id: dealerId });
    if (!document) {
      console.log('Dealer not found with ID:', dealerId);
      return res.status(404).json({ error: 'Dealer not found' });
    }
    console.log('Found dealer:', document);
    res.json(document);
  } catch (error) {
    console.error('Error fetching dealer:', error);
    res.status(500).json({ error: 'Error fetching dealer' });
  }
});

//Express route to insert review
app.post('/insert_review', express.raw({ type: '*/*' }), async (req, res) => {
  data = JSON.parse(req.body);
  const documents = await Reviews.find().sort( { id: -1 } )
  let new_id = documents[0]['id']+1

  const review = new Reviews({
		"id": new_id,
		"name": data['name'],
		"dealership": data['dealership'],
		"review": data['review'],
		"purchase": data['purchase'],
		"purchase_date": data['purchase_date'],
		"car_make": data['car_make'],
		"car_model": data['car_model'],
		"car_year": data['car_year'],
	});

  try {
    const savedReview = await review.save();
    res.json(savedReview);
  } catch (error) {
		console.log(error);
    res.status(500).json({ error: 'Error inserting review' });
  }
});

// Start the Express server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
