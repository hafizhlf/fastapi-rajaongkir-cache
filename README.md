
# FastAPI RajaOngkir Cache

## Description

FastAPI RajaOngkir Cache is a project that provides a caching layer for accessing the RajaOngkir API, allowing users to efficiently retrieve shipping costs, provinces, cities, and subdistricts while minimizing API requests.

## Features

-   Calculate shipping costs between locations using various courier services.
-   Retrieve a list of provinces, cities, and subdistricts in Indonesia.
-   Caching mechanism to reduce the number of API requests and improve performance.

## Installation

1.  Clone the repository: `git clone https://github.com/hafizhlf/fastapi-rajaongkir-cache.git`
2.  Navigate to the project directory: `cd fastapi-rajaongkir-cache`
3.  Install dependencies: `pip install -r requirements.txt`
4.  Create a .env file in the root directory of the project.
5.  Add your RajaOngkir API key to the .env file:

`RAJAONGKIR_API_KEY=your_api_key`

Replace `"your_api_key"` with your actual RajaOngkir API key.

## Usage

1.  Run the FastAPI server: `uvicorn main:app --reload`
2.  Access the API endpoints using a web browser or API client.

## API Endpoints

### /shipping-cost/
- **Description**: Calculate shipping cost between two locations.
- **Method**: GET
- **Parameters**:
  - `origin`: Origin location
  - `destination`: Destination location
  - `weight`: Weight of the shipment
  - `courier`: Courier service provider
- **Example**: `/shipping-cost/?origin=Jakarta&destination=Surabaya&weight=1&courier=jne`

### /provinces/
- **Description**: Retrieve a list of provinces in Indonesia.
- **Method**: GET

### /cities/{province_id}
- **Description**: Retrieve a list of cities in a specific province.
- **Method**: GET
- **Parameters**:
  - `province_id`: ID of the province
- **Example**: `/cities/12` (Retrieve cities in province with ID 12)

### /cities/
- **Description**: Retrieve a list of all cities in Indonesia.
- **Method**: GET

### /subdistricts/{city_id}
- **Description**: Retrieve a list of subdistricts in a specific city.
- **Method**: GET
- **Parameters**:
  - `city_id`: ID of the city
- **Example**: `/subdistricts/123` (Retrieve subdistricts in city with ID 123)

### /couriers/
- **Description**: Retrieve a list of available courier services.
- **Method**: GET

## Authentication

The project does not currently require authentication. Ensure that your RajaOngkir API key is kept secure.

## Dependencies

-   FastAPI
-   HTTPX

## Contributing

Contributions are welcome! Please fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Credits

-   Created by Hafizh Ibnu Syam

## Contact

For questions or feedback, feel free to reach out to hafizhlf@outlook.com.
