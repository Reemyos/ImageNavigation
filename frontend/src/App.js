import React, { useState } from 'react';
import axios from 'axios';
import ImageCarousel from './ImageCarousel'; // Import the ImageCarousel component

const App = () => {
  const [origin, setOrigin] = useState('');  // Store the origin input
  const [destination, setDestination] = useState('');  // Store the destination input
  const [images, setImages] = useState([]);  // To hold the images fetched
  const [loading, setLoading] = useState(false);  // Loading state
  const [error, setError] = useState('');  // Error state

  // Function to handle form submission and fetch images
  const handleSubmit = async (e) => {
    e.preventDefault();  // Prevent page reload
    setLoading(true);
    setError('');

    try {
      // Make the API request
      const response = await axios.get('http://localhost:8000/image_navigation/', {
        params: {
          origin: origin,
          destination: destination
        }
      });
      setImages(response.data);  // Set the images in state
    } catch (err) {
      setError('Failed to fetch images. Please check your inputs and try again.');
    } finally {
      setLoading(false);  // Reset loading state
    }
  };

  return (
    <div>
      <h1>Image Navigation</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Origin: </label>
          <input
            type="text"
            value={origin}
            onChange={(e) => setOrigin(e.target.value)}
            placeholder="Enter origin"
            required
          />
        </div>
        <div>
          <label>Destination: </label>
          <input
            type="text"
            value={destination}
            onChange={(e) => setDestination(e.target.value)}
            placeholder="Enter destination"
            required
          />
        </div>
        <button type="submit">Get Images</button>
      </form>

      {/* Loading and error handling */}
      {loading && <p>Loading images...</p>}
      {error && <p>{error}</p>}

      {/* Display the ImageCarousel when images are available */}
      {images.length > 0 && !loading && <ImageCarousel images={images} />}
    </div>
  );
};

export default App;
