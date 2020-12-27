import React from 'react';
import SlideshowPage from './SlideshowPage';
import LastImage from './LastImage';

function QrCodeLastImagePage(props) {
  const albumName = props.match.params.albumName
  return (
    <>
      <SlideshowPage {...props}/>
      <LastImage albumName={albumName} overlay={true} overlayTime={20000}/>
    </>
  );
}

export default QrCodeLastImagePage
