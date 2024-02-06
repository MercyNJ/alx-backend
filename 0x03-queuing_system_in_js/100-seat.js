const express = require('express');
const redis = require('redis');
const { promisify } = require('util');
const kue = require('kue');

const app = express();
const port = 1245;

const client = redis.createClient();
const getAsync = promisify(client.get).bind(client);

reserveSeat(50);

let reservationEnabled = true;

async function reserveSeat(number) {
  await client.set('available_seats', number);
}

async function getCurrentAvailableSeats() {
  const seats = await getAsync('available_seats');
  return seats ? parseInt(seats) : 0;
}

const queue = kue.createQueue();

app.get('/available_seats', async (req, res) => {
  const numberOfAvailableSeats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats });
});

app.get('/reserve_seat', async (req, res) => {
  if (!reservationEnabled) {
    res.json({ status: 'Reservation are blocked' });
    return;
  }

  const job = queue.create('reserve_seat').save((err) => {
    if (err) {
      res.json({ status: 'Reservation failed' });
    } else {
      res.json({ status: 'Reservation in process' });
    }
  });

  job.on('complete', (result) => {
    console.log(`Seat reservation job ${job.id} completed`);
  });

  job.on('failed', (errorMessage) => {
    console.log(`Seat reservation job ${job.id} failed: ${errorMessage}`);
  });
});

app.get('/process', async (req, res) => {
  res.json({ status: 'Queue processing' });

  const availableSeats = await getCurrentAvailableSeats();
  if (availableSeats === 0) {
    reservationEnabled = false;
  }

  if (availableSeats >= 0) {
    queue.process('reserve_seat', async (job, done) => {
      try {
        await reserveSeat(availableSeats - 1);
        done();
      } catch (error) {
        done(new Error('Not enough seats available'));
      }
    });
  }
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
