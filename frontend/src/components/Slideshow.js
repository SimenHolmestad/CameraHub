import React from 'react';
import FullscreenImage from './FullscreenImage';


function Slideshow({ imageUrls }) {
  const [currentImageIndex, setCurrentImageIndex] = React.useState(0);
  const [nextImageIndex, setNextImageIndex] = React.useState(1 % imageUrls.length);
  let nextImageRef = React.useRef(1 % imageUrls.length);
  let numberOfImagesRef = React.useRef(imageUrls.length);

  React.useEffect(() => {
    numberOfImagesRef.current = imageUrls.length
  }, [imageUrls]);

  React.useEffect(() => {
    const interval = setInterval(() => {
      const currentValue = nextImageRef.current
      let nextValue = Math.floor(Math.random() * numberOfImagesRef.current)
      if (currentValue === nextValue) {
        nextValue = (nextValue + 1) % numberOfImagesRef.current
      }

      setCurrentImageIndex(currentValue)
      setTimeout(() => {
        nextImageRef.current = nextValue
        setNextImageIndex(nextValue)
      }, 1000)
    }, 8000);
    return () => clearInterval(interval);
  }, []);

  return (
    <>
      <FullscreenImage imageUrl={ imageUrls[nextImageIndex] }/>
      <FullscreenImage imageUrl={ imageUrls[currentImageIndex] } time={ 2000 }/>
    </>
  );
}

export default Slideshow
