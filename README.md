# News-Map (Python, FastAPI, MongoDB, NLP, Geocoding, Spacy)
Backend for an application that crawls news articles from the web and stores locations from places mentioned in those articles in a MongoDB database.

Currently only a crawler for CNN is written. Take a look at the cnn crawler and write one for another news source. In the future it would be cool to extend the service such that you are able to compare different news sources (from different countries) and see where what places are mentioned the most.

For the geocoding part, first the places are being extracted using the spacy package (NLP). A lot of different geocoding services then return the coordinates for the location strings and the coordinates are stored in the database.

## Develop / Run
- copy `.env.example` to `.env` and fill out the values
- download the [docker vscode extension](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker) and build the image and run the container through vscode
- to build the image and run the container without vscode do the following: `docker build -t myimage .`, `docker run --env-file .env --name mycontainer -p 80:80 myimage`
- to stop and remove do the following: `docker stop mycontainer`, `docker rm mycontainer` 