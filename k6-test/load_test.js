import http from 'k6/http';
import { sleep } from 'k6';

export const options = {
  scenarios: {
    constant_load: {
      executor: 'per-vu-iterations',  // Ensures each VU runs a fixed number of iterations
      vus: 500,                     // Max 1,000 concurrent users at a time
      iterations: 20,                 // Each VU sends 10 requests (1000 * 10 = 10,000)
    },
  },
};

export default function () {
  http.get('https://ociit27b9c.execute-api.us-east-1.amazonaws.com/prod/');  // Replace with your URL
  sleep(5);  // Simulating avg 1000ms (1s) response time
}
