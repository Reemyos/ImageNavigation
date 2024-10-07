import React, { useState } from 'react';
import { LiaAngleRightSolid, LiaAngleLeftSolid } from "react-icons/lia";
import './App.css'; // We'll style here

function App() {
  const [origin, setOrigin] = useState('');
  const [destination, setDestination] = useState('');
  const [images, setImages] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);

  const fetchImages = async () => {
    const res = await fetch(
        `http://localhost:8000/image_navigation/?origin=${origin}&destination=${destination}`
    );
    const imageArray = await res.json();
    setImages(imageArray);
    setCurrentIndex(0); // Reset to the first image
  };

  const nextImage = () => {
    setCurrentIndex((prevIndex) => (prevIndex + 1) % images.length);
  };

  const prevImage = () => {
    setCurrentIndex((prevIndex) => (prevIndex - 1 + images.length) % images.length);
  };

  return (
    <div className="app-container">
      <h1 className="header">Image Navigation</h1>

      <div className="input-container">
        <input
          type="text"
          placeholder="Origin"
          value={origin}
          onChange={(e) => setOrigin(e.target.value)}
          className="input-field"
        />
        <input
          type="text"
          placeholder="Destination"
          value={destination}
          onChange={(e) => setDestination(e.target.value)}
          className="input-field"
        />
        <button onClick={fetchImages} className="submit-button">Submit</button>
      </div>

      {images.length > 0 && (
        <div className="image-viewer">
          <button onClick={prevImage} className="nav-button">
            <LiaAngleLeftSolid></LiaAngleLeftSolid>
          </button>
          <img
            src={`data:image/jpeg;base64,${images[currentIndex]}`}
            alt="Location"
            className="image"
          />
          <button onClick={nextImage} className="nav-button">
            <LiaAngleRightSolid></LiaAngleRightSolid>
          </button>
        </div>
      )}
    </div>
  );
}

export default App;
