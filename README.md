# member-info-aggregator
Aggregates member data from various APIs

This API aggregates the values from N other external sources, given they all are online and return the same data structure.

In case of any errors from a specific source will cause that source to be disconsidered. If all are disconsidered/unavailable than it returns a 400 error.

You can alter the aggregation strategy using env vars (see docker-compose.xml for the options). You can always inform the desired strategy on the URL (considering it is a valid option).

# Python
Version 3.10  (for libraries version see `requirements.txt`)

# Setup
1. Clone this repo (`git clone`, IDE)
2. Create a virtual environment (`pyenv`, IDE)
3. Install requirements (`pip install -r requirements.txt`)

# Running
You can:
1. Run the tests: `pytest`

The tests use the requests-mock to mock the external APIs requests and simulte different scenarions. They may take a couple extra seconds to run because one of them simulates the situation where all external APIs are down.

2. Run the server with docker-compose `docker-compose up`

Note: Running the server will not do much since the external APIs point nowhere. You will receive a 400 with "All sources are unavailable".

Note: The endpoint is `http://localhost:8000/members/1/` and you can use append `?aggregation_strategy=` to choose the strategy. Valid options are AVG, MIN, MAX.
