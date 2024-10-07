import React, { useState } from 'react';

const ImageCarousel = ({ images }) => {
  const [currentIndex, setCurrentIndex] = useState(0);  // Track the current image index

  // Handlers for next and previous buttons
  const handleNext = () => {
    setCurrentIndex((prevIndex) => (prevIndex + 1) % images.length);
  };

  const handlePrev = () => {
    setCurrentIndex((prevIndex) => (prevIndex - 1 + images.length) % images.length);
  };

  return (
    <div>
      <div>
        <img
          src={`data:image/jpeg;base64,${images[currentIndex]}`}
          alt={`Location ${currentIndex}`}
          style={{ width: '500px', height: '500px' }}
        />
      </div>
      <button onClick={handlePrev}>Previous</button>
      <button onClick={handleNext}>Next</button>
    </div>
  );
};

export default ImageCarousel;
