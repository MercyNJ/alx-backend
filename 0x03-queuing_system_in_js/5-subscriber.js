import redis from 'redis';

const subscriber = redis.createClient();
const CHANNEL = 'holberton school channel';

subscriber.on('error', (err) => {
  console.error(`Redis client not connected to the server: ${err}`);
});

subscriber.on('connect', () => {
  console.log('Redis client connected to the server');
  subscriber.subscribe(CHANNEL);
});

subscriber.on('message', (channel, message) => {
  if (channel === CHANNEL) {
    console.log(message);

    if (message === 'KILL_SERVER') {
      subscriber.unsubscribe(CHANNEL);
      subscriber.quit();
    }
  }
});
